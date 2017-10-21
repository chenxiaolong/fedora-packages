%{?mingw_package_header}

Name:           mingw-libarchive
Version:        3.3.1
Release:        2.1%{?dist}
Summary:        MinGW package for handling streaming archive formats

License:        BSD
URL:            http://www.libarchive.org/
Source0:        http://www.libarchive.org/downloads/libarchive-%{version}.tar.gz
# Fix detection of OpenSSL
Patch1:         libarchive-mingw-openssl.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  mingw32-bzip2
BuildRequires:  mingw64-bzip2
BuildRequires:  mingw32-libxml2
BuildRequires:  mingw64-libxml2
BuildRequires:  mingw32-lz4-libs
BuildRequires:  mingw64-lz4-libs
BuildRequires:  mingw32-openssl
BuildRequires:  mingw64-openssl
BuildRequires:  mingw32-xz-libs
BuildRequires:  mingw64-xz-libs
BuildRequires:  mingw32-zlib
BuildRequires:  mingw64-zlib
BuildRequires:  automake autoconf libtool


%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


# Mingw32
%package -n mingw32-libarchive
Summary:        MinGW package for handling streaming archive formats

%description -n mingw32-libarchive
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%package -n mingw32-libarchive-static
Summary:        Static version of the MinGW libarchive library
Requires:       mingw32-libarchive = %{version}-%{release}


%description -n mingw32-libarchive-static
Static version of the MinGW libarchive library.


%package -n     mingw32-bsdtar
Summary:        MinGW package for bsdtar utility

%description -n mingw32-bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n     mingw32-bsdcat
Summary:        MinGW package for bsdcat utility

%description -n mingw32-bsdcat
The bsdcat package contains standalone bsdcat utility split off regular
libarchive packages.


%package -n     mingw32-bsdcpio
Summary:        MinGW package for bsdcpio utility

%description -n mingw32-bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.



# Mingw64
%package -n mingw64-libarchive
Summary:        MinGW package for handling streaming archive formats


%description -n mingw64-libarchive
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%package -n mingw64-libarchive-static
Summary:        Static version of the MinGW libarchive library
Requires:       mingw64-libarchive = %{version}-%{release}


%description -n mingw64-libarchive-static
Static version of the MinGW libarchive library.


%package -n     mingw64-bsdtar
Summary:        MinGW package for bsdtar utility

%description -n mingw64-bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n     mingw64-bsdcat
Summary:        MinGW package for bsdcat utility

%description -n mingw64-bsdcat
The bsdcat package contains standalone bsdcat utility split off regular
libarchive packages.


%package -n     mingw64-bsdcpio
Summary:        MinGW package for bsdcpio utility

%description -n mingw64-bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.


%?mingw_debug_package


%prep
%setup -q -n libarchive-%{version}
%patch1 -p1 -b.openssl


%build
build/autogen.sh
%mingw_configure
%mingw_make %{?_smp_mflags} V=1


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name cpio.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name mtree.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name tar.5 -exec rm -f {} ';'

# Remove documentation which duplicates that found in the native package.
rm -r $RPM_BUILD_ROOT/%{mingw32_prefix}/share
rm -r $RPM_BUILD_ROOT/%{mingw64_prefix}/share


# Win32
%files -n mingw32-libarchive
%license COPYING
%doc NEWS
%{mingw32_bindir}/libarchive-13.dll
%{mingw32_includedir}/archive.h
%{mingw32_includedir}/archive_entry.h
%{mingw32_libdir}/libarchive.dll.a
%{mingw32_libdir}/pkgconfig/libarchive.pc

%files -n mingw32-libarchive-static
%{mingw32_libdir}/libarchive.a

%files -n mingw32-bsdtar
%{mingw32_bindir}/bsdtar.exe

%files -n mingw32-bsdcat
%{mingw32_bindir}/bsdcat.exe

%files -n mingw32-bsdcpio
%{mingw32_bindir}/bsdcpio.exe


# Win64
%files -n mingw64-libarchive
%license COPYING
%doc NEWS
%{mingw64_bindir}/libarchive-13.dll
%{mingw64_includedir}/archive.h
%{mingw64_includedir}/archive_entry.h
%{mingw64_libdir}/libarchive.dll.a
%{mingw64_libdir}/pkgconfig/libarchive.pc

%files -n mingw64-libarchive-static
%{mingw64_libdir}/libarchive.a

%files -n mingw64-bsdtar
%{mingw64_bindir}/bsdtar.exe

%files -n mingw64-bsdcat
%{mingw64_bindir}/bsdcat.exe

%files -n mingw64-bsdcpio
%{mingw64_bindir}/bsdcpio.exe


%changelog
* Fri Oct 20 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 3.3.1-2.1
- Enable LZ4 support

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Michael Cronenworth <mike@cchtml.com> - 3.3.1-1
- Update to 3.3.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Michael Cronenworth <mike@cchtml.com> - 3.2.2-1
- Update to 3.2.2 (CVE-2016-8687 CVE-2016-8688 CVE-2016-8689)

* Fri Aug 05 2016 Michael Cronenworth <mike@cchtml.com> - 3.2.1-2
- Add patch to fix OpenSSL detection on MinGW

* Fri Aug 05 2016 Michael Cronenworth <mike@cchtml.com> - 3.2.1-1
- Update to 3.2.1 (CVE-2016-6250)

* Wed Jun 01 2016 Michael Cronenworth <mike@cchtml.com> - 3.2.0-1
- Update to 3.2.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 29 2013 Michael Cronenworth <mike@cchtml.com> - 3.1.2-1
- Update to 3.1.2
- Fix CVE-2013-0211: read buffer overflow on 64-bit systems (#927105)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Michael Cronenworth <mike@cchtml.com> - 3.1.1-1
- New upstream release.

* Tue Nov 20 2012 Michael Cronenworth <mike@cchtml.com> - 3.0.4-3
- Package description fixes.

* Mon Nov 19 2012 Michael Cronenworth <mike@cchtml.com> - 3.0.4-2
- Package review fixes.

* Thu Jun 07 2012 Michael Cronenworth <mike@cchtml.com> - 3.0.4-1
- Initial RPM release.

