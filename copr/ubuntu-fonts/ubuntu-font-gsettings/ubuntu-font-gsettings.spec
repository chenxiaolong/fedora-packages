Name:           ubuntu-font-gsettings
Version:        18.04.5
Release:        1%{?dist}
Summary:        GSettings overrides to set Ubuntu fonts as default

License:        GPLv2+
URL:            https://launchpad.net/ubuntu/+source/ubuntu-settings
Source0:        https://launchpad.net/ubuntu/+archive/primary/+files/ubuntu-settings_%{version}.tar.xz
Patch0:         0001-Remove-non-font-gsettings-overrides.patch

BuildArch:      noarch

Requires:       gnome-settings-daemon
Requires:       gsettings-desktop-schemas
Requires:       ubuntu-family-fonts
Recommends:     fontconfig-ubuntu

%description
This package contains the default font-related GSettings overrides from
Ubuntu.


%prep
%autosetup -n ubuntu-settings-%{version} -p1


%build


%install
install -m 0755 -d %{buildroot}%{_datadir}/glib-2.0/schemas/
install -m 0644 \
    debian/ubuntu-settings.gsettings-override \
    %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override


%files
%license debian/copyright
%{_datadir}/glib-2.0/schemas/10_%{name}.gschema.override


%changelog
* Sat Apr 28 2018 Andrew Gunnerson <andrewgunnerson@gmail.com> - 18.04.5
- Update to 18.04.5

* Sun Dec 3 2017 Andrew Gunnerson <chenxiaolong@cxl.epac.to> - 17.10.18
- Initial release
