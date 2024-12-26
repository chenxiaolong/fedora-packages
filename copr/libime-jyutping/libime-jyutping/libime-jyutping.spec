# This key is used to sign the official git tags in the fcitx5 repo:
# https://github.com/fcitx/fcitx5/releases
%global fingerprint 2cc8a0609ad2a479c65b6d5c8e8b898cbf2412f9

Name:           libime-jyutping
Version:        1.0.12
Release:        1%{?dist}
Summary:        An implementation of jyutping (粵拼) via libime

License:        LGPL-2.1-or-later AND GPL-3.0-or-later
URL:            https://github.com/fcitx/libime-jyutping
Source0:        https://download.fcitx-im.org/fcitx5/%{name}/%{name}-%{version}_dict.tar.zst
Source1:        https://download.fcitx-im.org/fcitx5/%{name}/%{name}-%{version}_dict.tar.zst.sig
Source2:        https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x%{fingerprint}#/%{fingerprint}.gpg

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  fcitx5-chinese-addons-devel
BuildRequires:  fcitx5-devel
BuildRequires:  fmt-devel
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gnupg2
BuildRequires:  libime-devel
BuildRequires:  libzstd-devel
BuildRequires:  ninja-build

Requires:       %{name}-data


%description
This is an implementation of jyutping (粵拼) via libime. The data file is
derived from libpinyin and rime-jyutping.


%package data
Summary:        Data files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}


%description data
This provides the dictionary data file for %{name}.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       boost-devel
Requires:       fcitx5-devel
Requires:       libime-devel
Requires:       libzstd-devel

%description devel
Development files for %{name}.


%package -n fcitx5-jyutping
Summary:        fcitx5 input method based on %{name}
Requires:       %{name}%{?isa} = %{version}-%{release}

%description -n fcitx5-jyutping
fcitx5 input method based on %{name}.


%prep
%{gpgverify} --keyring='%{S:2}' --signature='%{S:1}' --data='%{S:0}'
%autosetup


%build
%cmake -GNinja
%cmake_build


%install
%cmake_install

%find_lang fcitx5-jyutping


%check
%ctest


%files
%license LICENSES/LGPL-2.1-or-later.txt
%doc README.md
%{_bindir}/libime_jyutpingdict
%{_libdir}/libIMEJyutping.so.*
%{_libdir}/libime/zh_HK.lm
%{_libdir}/libime/zh_HK.lm.predict


%files data
%{_datadir}/libime/jyutping.dict


%files devel
%{_includedir}/LibIME/libime/jyutping/
%{_libdir}/cmake/LibIMEJyutping/
%{_libdir}/libIMEJyutping.so


%files -n fcitx5-jyutping -f fcitx5-jyutping.lang
%{_libdir}/fcitx5/libjyutping.so
%{_datadir}/fcitx5/addon/jyutping.conf
%{_datadir}/fcitx5/inputmethod/jyutping.conf
%{_datadir}/metainfo/org.fcitx.Fcitx5.Addon.Jyutping.metainfo.xml


%changelog
* Wed Dec 25 2024 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1.0.12-1
- Initial release
