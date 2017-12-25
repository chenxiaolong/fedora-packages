#!/usr/bin/env python3

# Copyright (C) 2017  Andrew Gunnerson <andrewgunnerson@gmail.com>
#
# kmod-signer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kmod-signer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kmod-signer.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import bz2
import enum
import glob
import gzip
import lzma
import os
import struct
import subprocess
import sys

import yaml

# Constants

KMOD_MAGIC = b'~Module signature appended~\n'
KMOD_MAGIC_SIZE = len(KMOD_MAGIC)

# struct module_signature:
#   uint8_t algo;        # Public-key crypto algorithm
#   uint8_t hash;        # Digest algorithm
#   uint8_t id_type;     # Key identifier type
#   uint8_t signer_len;  # Length of signer's name
#   uint8_t key_id_len;  # Length of key identifier
#   uint8_t __pad[3];
#   uint32_t sig_len;    # Length of signature data
KMOD_STRUCT = '>BBBBBxxxI'
KMOD_STRUCT_SIZE = struct.calcsize(KMOD_STRUCT)

# Global variables

signing_cert_path = None
signing_key_path = None


class SigningMode(enum.Enum):
    SKIP_SIGNED = 1
    RESIGN = 2


def info(*args, **kwargs):
    print('--', *args, **kwargs)


def warning(*args, **kwargs):
    print('**', *args, **{**kwargs, 'file': sys.stderr})


def copy_stream(f_in, f_out, buf_size=16 * 1024, size=None):
    while True:
        n = buf_size if size is None else min(buf_size, size)
        buf = f_in.read(n)
        if not buf:
            if size is not None and size > 0:
                raise IOError('Unexpected EOF')
            break
        f_out.write(buf)

        if size is not None:
            size -= len(buf)


def unlink_if_exists(path):
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


def open_by_file_ext(*args, **kwargs):
    path = args[0]
    if path.endswith('.bz2'):
        open_func = bz2.open
    elif path.endswith('.gz'):
        open_func = gzip.open
    elif path.endswith('.xz'):
        open_func = lzma.open
    else:
        open_func = open
    return open_func(*args, **kwargs)


def copy_compressed(input_path, output_path):
    with open_by_file_ext(input_path, 'rb') as f_in:
        with open_by_file_ext(output_path, 'wb') as f_out:
            copy_stream(f_in, f_out)


def get_kmod_kernel_version(path):
    p = subprocess.Popen(
        ['modinfo', '-F', 'vermagic', path],
        stdout=subprocess.PIPE,
    )
    output = p.communicate()
    version = output[0].decode('ascii').split(' ')[0]
    return version


def sign_kmod(input_path, output_path, sign_tool, signing_mode, hash_algo):
    sign_target = output_path + '.signing-tmp'

    try:
        # Decompress or copy input file
        copy_compressed(input_path, sign_target)

        with open_by_file_ext(input_path, 'rb') as f_in:
            seek_pos = -KMOD_MAGIC_SIZE
            f_in.seek(seek_pos, os.SEEK_END)

            magic = f_in.read(KMOD_MAGIC_SIZE)
            if magic == KMOD_MAGIC:
                if signing_mode == SigningMode.SKIP_SIGNED:
                    info('Skipping \'%s\': Already signed' % input_path)
                    return

                # Read module_signature block
                seek_pos -= KMOD_STRUCT_SIZE
                data_size = f_in.seek(seek_pos, os.SEEK_END)
                sig_info = f_in.read(KMOD_STRUCT_SIZE)

                # Get signature length
                _, _, _, _, _, sig_len = \
                    struct.unpack(KMOD_STRUCT, sig_info)
                data_size -= sig_len

                # Copy module without signature
                f_in.seek(0)
                with open(sign_target, 'wb') as f_out:
                    copy_stream(f_in, f_out, size=data_size)

        info('Signing \'%s\'' % input_path)

        subprocess.run([
            sign_tool,
            hash_algo,
            signing_key_path,
            signing_cert_path,
            sign_target,
            sign_target,
        ], check=True)

        # Compress or copy output file
        copy_compressed(sign_target, output_path)
    finally:
        unlink_if_exists(sign_target)


def sign_kernel_modules(globs, signing_mode, hash_algo):
    for g in globs:
        files = glob.glob(g, recursive=True)
        if not files:
            warning('No files matched glob \'%s\'' % g)
            continue

        for f in files:
            # The sign-tool version needs to match the kernel version since the
            # module signing format has changed several times.
            kernel_version = get_kmod_kernel_version(f)
            sign_tool = '/usr/src/kernels/%s/scripts/sign-file' \
                % kernel_version
            if not os.path.isfile(sign_tool):
                raise Exception('sign-tool for kernel %s not found'
                                % kernel_version)

            sign_kmod(f, f, sign_tool, signing_mode, hash_algo)


def parse_signing_mode(mode):
    if mode == 'skip_signed':
        return SigningMode.SKIP_SIGNED
    elif mode == 'resign':
        return SigningMode.RESIGN
    else:
        raise ValueError('Unknown signing mode: \'%s\'' % mode)


def main():
    global signing_cert_path, signing_key_path

    parser = argparse.ArgumentParser()
    parser.add_argument('-c',  '--config',
                        default='/etc/sysconfig/kmod-signer',
                        help='Path to config file')

    args = parser.parse_args()

    # Load config file
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    global_config = config['global']
    signing_cert_path = global_config['cert_path']
    signing_key_path = global_config['key_path']

    if not os.path.isfile(signing_cert_path):
        raise IOError('Signing certificate does not exist \'%s\''
                      % signing_cert_path)
    elif not os.path.isfile(signing_key_path):
        raise IOError('Signing key does not e xist \'%s\''
                      % signing_key_path)

    # Sign kernel modules
    kmod_config = config['kmod_signing']
    if kmod_config['enabled']:
        sign_kernel_modules(
            kmod_config['file_patterns'],
            parse_signing_mode(kmod_config['signing_mode']),
            kmod_config['hash_algorithm'],
        )
    else:
        info('Kernel module signing is disabled')

    info('Completed successfully')

if __name__ == '__main__':
    main()
