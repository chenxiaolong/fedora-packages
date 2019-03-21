%{?mingw_package_header}

Name:           mingw-libsodium
Version:        1.0.17
Release:        1%{?dist}
Summary:        MinGW package for the Sodium crypto library

License:        ISC
URL:            https://download.libsodium.org/doc/
Source0:        https://download.libsodium.org/libsodium/releases/libsodium-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils


%description
Sodium is a new, easy-to-use software library for encryption, decryption,
signatures, password hashing and more. It is a portable, cross-compilable,
installable, packageable fork of NaCl, with a compatible API, and an extended
API to improve usability even further. Its goal is to provide all of the core
operations needed to build higher-level cryptographic tools. The design
choices emphasize security, and "magic constants" have clear rationales.

The same cannot be said of NIST curves, where the specific origins of certain
constants are not described by the standards. And despite the emphasis on
higher security, primitives are faster across-the-board than most
implementations of the NIST standards.


# Mingw32
%package -n mingw32-libsodium
Summary:        %{summary}

%description -n mingw32-libsodium
%{description}


%package -n mingw32-libsodium-static
Summary:        Static version of the MinGW libsodium library
Requires:       mingw32-libsodium = %{version}-%{release}

%description -n mingw32-libsodium-static
Static version of the MinGW libsodium library.


# Mingw64
%package -n mingw64-libsodium
Summary:        %{summary}

%description -n mingw64-libsodium
%{description}


%package -n mingw64-libsodium-static
Summary:        Static version of the MinGW libsodium library
Requires:       mingw64-libsodium = %{version}-%{release}

%description -n mingw64-libsodium-static
Static version of the MinGW libsodium library.


%?mingw_debug_package


%prep
%setup -q -n libsodium-%{version}


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.def' -delete
find $RPM_BUILD_ROOT -name '*.la' -delete


# Win32
%files -n mingw32-libsodium
%license LICENSE
%doc AUTHORS ChangeLog README.markdown THANKS
%{mingw32_bindir}/libsodium-23.dll
%{mingw32_includedir}/sodium.h
%{mingw32_includedir}/sodium/
%{mingw32_libdir}/libsodium.dll.a
%{mingw32_libdir}/pkgconfig/libsodium.pc

%files -n mingw32-libsodium-static
%{mingw32_libdir}/libsodium.a


# Win64
%files -n mingw64-libsodium
%license LICENSE
%doc AUTHORS ChangeLog README.markdown THANKS
%{mingw64_bindir}/libsodium-23.dll
%{mingw64_includedir}/sodium.h
%{mingw64_includedir}/sodium/
%{mingw64_libdir}/libsodium.dll.a
%{mingw64_libdir}/pkgconfig/libsodium.pc

%files -n mingw64-libsodium-static
%{mingw64_libdir}/libsodium.a


%changelog
* Wed Mar 20 2019 Andrew Gunnerson <andrewgunnerson@gmail.com> - 1.0.17-1
- Initial release
