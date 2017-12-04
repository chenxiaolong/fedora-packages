%global fontname ubuntu-family
%global fontconf 81-%{fontname}.conf

Name:           %{fontname}-fonts
Version:        0.83
Release:        1%{?dist}
Summary:        Ubuntu font family

# This is spelled 'Licence' in debian/copyright
License:        Ubuntu Font Licence 1.0
URL:            https://design.ubuntu.com/font/
Source0:        https://launchpad.net/ubuntu/+archive/primary/+files/ubuntu-font-family-sources_%{version}.orig.tar.gz
# Fix for Qt 4 applications:
# https://bugs.launchpad.net/ubuntu-font-family/+bug/744812/comments/81
Source1:        https://bugs.launchpad.net/ubuntu-font-family/+bug/744812/+attachment/3941239/+files/81-ubuntu.conf

BuildArch:      noarch

BuildRequires:  fontpackages-devel

Requires:       fontpackages-filesystem

%description
The Ubuntu typeface has been specially created to complement the Ubuntu
tone of voice. It has a contemporary style and contains characteristics
unique to the Ubuntu brand that convey a precise, reliable and free
attitude.


%prep
%autosetup -n ubuntu-font-family-sources-%{version}


%build


%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p \
    Ubuntu-L*.ttf \
    Ubuntu-R*.ttf \
    Ubuntu-M*.ttf \
    Ubuntu-B*.ttf \
    Ubuntu-C.ttf \
    UbuntuMono-*.ttf \
    %{buildroot}%{_fontdir}

install -m 0755 -d \
    %{buildroot}%{_fontconfig_templatedir} \
    %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
    %{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
    %{buildroot}%{_fontconfig_confdir}/


%_font_pkg -f %{fontconf} *.ttf

%doc CONTRIBUTING.txt FONTLOG.txt README.txt TRADEMARKS.txt
%license copyright.txt LICENCE.txt LICENCE-FAQ.txt


%changelog
* Sun Dec 3 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.83-1
- Initial release
