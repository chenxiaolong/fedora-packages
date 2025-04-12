Name:           android-udev-rules
Version:        20250314
Release:        1%{?dist}
Summary:        Comprehensive udev rules for Android devices

License:        GPL-3.0-or-later
URL:            https://github.com/M0Rf30/android-udev-rules
Source0:        https://github.com/M0Rf30/android-udev-rules/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros


%description
%{summary}


%prep
%autosetup -n android-udev-rules-%{version}


%build


%install
install -D -m 644 51-android.rules -t %{buildroot}%{_udevrulesdir}/
install -D -m 644 android-udev.conf -t %{buildroot}%{_sysusersdir}/


%files
%doc README.md
%license LICENSE
%{_udevrulesdir}/51-android.rules
%{_sysusersdir}/android-udev.conf


%changelog
* Sat Apr 12 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 20250314-1
- Initial release
