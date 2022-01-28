Name:           dracut-config-efistub
Version:        1
Release:        1%{?dist}
Summary:        Config to enable dracut's efistub generation by default

License:        GPLv2+
URL:            https://github.com/chenxiaolong/fedora-packages
Source0:        50-efistub.conf
Source1:        50-dracut-uefi.install

BuildArch:      noarch

Requires:       dracut
Requires:       systemd-udev

%description
This package provides a configuration to enable dracut's built-in support for
efistub generation. This package has no effect on systems booted without EFI.


%prep


%build


%install
install -d -m 0755 %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/
install -m 0644 %{SOURCE0} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/
install -d -m 0755 %{buildroot}%{_prefix}/lib/kernel/install.d/
install -m 0755 %{SOURCE1} %{buildroot}%{_prefix}/lib/kernel/install.d/


%files
%{_prefix}/lib/dracut/dracut.conf.d/50-efistub.conf
%{_prefix}/lib/kernel/install.d/50-dracut-uefi.install


%changelog
* Fri Jan 28 2022 Andrew Gunnerson <chillermillerlong@hotmail.com> - 1-1
- Initial release
