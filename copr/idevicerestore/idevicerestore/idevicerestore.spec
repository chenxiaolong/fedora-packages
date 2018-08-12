%global commit 707856d9005a48ee006dfcc7e5424473cf9e7652
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           idevicerestore
Version:        0.0
Release:        1.git%{shortcommit}%{?dist}
Summary:        Tool to restore firmware files to iOS devices

License:        LGPLv3
URL:            https://github.com/libimobiledevice/idevicerestore
Source0:        https://github.com/libimobiledevice/idevicerestore/archive/%{commit}.tar.gz
# From: https://aur.archlinux.org/cgit/aur.git/tree/0001-configure.ac-check-for-pthreads.patch?h=idevicerestore-git
Patch0:         0001-configure.ac-check-for-pthreads.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  libcurl-devel
BuildRequires:  libimobiledevice-devel
BuildRequires:  libirecovery-devel
BuildRequires:  libplist-devel
BuildRequires:  libusbmuxd-devel
BuildRequires:  libzip-devel
BuildRequires:  openssl-devel

%description
The idevicerestore tool allows to restore firmware files to iOS devices.

It is a full reimplementation of all granular steps which are performed during
restore of a firmware to a device.

In general, upgrades and downgrades are possible, however subject to
availability of SHSH blobs from Apple for signing the firmware files.


%prep
%autosetup -n %{name}-%{commit}

autoreconf -fi


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc AUTHORS README TODO
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Aug 12 2018 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.0-1.git707856d
- Initial release
