Name:           wooting-udev-rules
Version:        1
Release:        1%{?dist}
Summary:        udev rules for Wooting keyboards

License:        CC0-1.0
URL:            https://wootility.io/
Source0:        70-wooting.rules

BuildArch:      noarch

BuildRequires:  systemd-rpm-macros


%description
%{summary}


%prep


%build


%install
install -D -m 644 %{SOURCE0} -t %{buildroot}%{_udevrulesdir}/


%files
%{_udevrulesdir}/70-wooting.rules


%changelog
* Sat Apr 12 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1-1
- Initial release
