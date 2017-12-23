Name:       kmod-signer
Version:    0.1
Release:    1%{?dist}
Summary:    Tool for automatically signing kernel modules

License:    GPLv3+
URL:        https://github.com/chenxiaolong/fedora-packages
Source0:    kmod-signer.py
Source1:    kmod-signer.yaml

BuildArch:  noarch

Requires:   python3
Requires:   python3-PyYAML

%description
Simple tool for automatically signing kernel modules.


%prep


%build


%install
install -dm755 %{buildroot}%{_sbindir}/
install -m755 %{SOURCE0} %{buildroot}%{_sbindir}/%{name}

install -dm755 %{buildroot}%{_sysconfdir}/sysconfig
install -m600 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}


# Post kmod installation:
# * /usr/lib/modules/**/*.ko
# * /lib/modules/**/*.ko
# Post kernel installation (for dkms):
# * /boot/vmlinuz-*
# Post dkms module installation:
# * /usr/src/**/dkms.conf

# Can't be enabled until the fix for the following bug is released:
# https://github.com/rpm-software-management/rpm/issues/370
#%%transfiletriggerin -P 1 -- /usr/lib/modules /lib/modules /boot /usr/src
#if grep -q -m 1 -e '\.ko$' -e '^/boot/vmlinuz-' -e '/dkms.conf$'; then
#    exec </dev/null
#    %%{name}
#fi


%files
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}


%changelog
* Fri Dec 22 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.1-1
- Initial release
