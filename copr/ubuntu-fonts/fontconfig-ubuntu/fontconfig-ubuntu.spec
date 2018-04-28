%global ubuntu_rel 0ubuntu2

Name:           fontconfig-ubuntu
Version:        2.12.6
Release:        2%{?dist}
Summary:        Default fontconfig configuration from Ubuntu

License:        MIT and Public Domain and UCD
URL:            https://launchpad.net/ubuntu/+source/fontconfig
Source0:        https://launchpad.net/ubuntu/+archive/primary/+files/fontconfig_%{version}-%{ubuntu_rel}.debian.tar.xz
Patch0:         0001-Fix-compatibility-with-2.13.0.patch

BuildArch:      noarch

BuildRequires:  fontpackages-devel
BuildRequires:  patchutils

Requires:       fontconfig >= %{version}

%description
This package contains some of the default Ubuntu fontconfig
configuration. In particular, any changes that don't require patching
the normal fontconfig package's files are included.

The following patches are currently excluded:
* 02_indic_names.patch
* 03_prefer_dejavu.patch
* 04_mgopen_fonts.patch


%prep
%autosetup -n debian -p1

filterdiff -x '*/conf.d/Makefile.am' \
    patches/04_ubuntu_monospace_lcd_filter_conf.patch \
    | patch -p1
filterdiff -x '*/conf.d/Makefile.am' \
    patches/05_ubuntu_add_antialiasing_confs.patch \
    | patch -p1


%build


%install
# Install configs
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir}/
install -m 0644 \
    conf.d/10-antialias.conf \
    %{buildroot}%{_fontconfig_templatedir}/
install -m 0644 \
    conf.d/53-monospace-lcd-filter.conf \
    %{buildroot}%{_fontconfig_templatedir}/

# Enable configs
install -m 0755 -d %{buildroot}%{_fontconfig_confdir}/
ln -s %{_fontconfig_templatedir}/10-antialias.conf \
    %{buildroot}%{_fontconfig_confdir}/
ln -s %{_fontconfig_templatedir}/11-lcdfilter-default.conf \
    %{buildroot}%{_fontconfig_confdir}/
ln -s %{_fontconfig_templatedir}/70-no-bitmaps.conf \
    %{buildroot}%{_fontconfig_confdir}/


%files
%doc README.Debian
%license copyright
%config(noreplace) %{_fontconfig_confdir}/*.conf
%{_fontconfig_templatedir}/*.conf


%changelog
* Sat Apr 28 2018 Andrew Gunnerson <andrewgunnerson@gmail.com> - 2.12.6-2
- Fix compatibility with fontconfig 2.13.0

* Sun Dec 3 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 2.12.6-1
- Initial release
