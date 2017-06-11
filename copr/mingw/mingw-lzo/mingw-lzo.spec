%{?mingw_package_header}

Name:           mingw-lzo
Version:        2.08
Release:        9.1%{?dist}
Summary:        Data compression library with very fast (de)compression
License:        GPLv2+
URL:            http://www.oberhumer.com/opensource/lzo/
Source0:        http://www.oberhumer.com/opensource/lzo/download/lzo-%{version}.tar.gz
Patch0:         lzo-2.08-configure.patch
Patch1:         lzo-2.08-rhbz1309225.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-zlib
BuildRequires:  mingw64-zlib

%description
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


# Mingw32
%package -n mingw32-lzo
Summary:        Data compression library with very fast (de)compression

%description -n mingw32-lzo
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package -n mingw32-lzo-minilzo
Summary:        Mini version of lzo for apps which don't need the full version

%description -n mingw32-lzo-minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%package -n mingw32-lzo-static
Summary:        Static library for lzo
Requires:       mingw32-lzo = %{version}-%{release}

%description -n mingw32-lzo-static
LZO is a portable lossless data compression library written in ANSI C.
This package contains static libraries for lzo.


%package -n mingw32-lzo-minilzo-static
Summary:        Static library for minilzo
Requires:       mingw32-lzo-minilzo = %{version}-%{release}

%description -n mingw32-lzo-minilzo-static
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support. This package contains static libraries for
minilzo.


# Mingw64
%package -n mingw64-lzo
Summary:        Data compression library with very fast (de)compression

%description -n mingw64-lzo
LZO is a portable lossless data compression library written in ANSI C.
It offers pretty fast compression and very fast decompression.
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio
while still decompressing at this very high speed.


%package -n mingw64-lzo-minilzo
Summary:        Mini version of lzo for apps which don't need the full version

%description -n mingw64-lzo-minilzo
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support.


%package -n mingw64-lzo-static
Summary:        Static library for lzo
Requires:       mingw64-lzo = %{version}-%{release}

%description -n mingw64-lzo-static
LZO is a portable lossless data compression library written in ANSI C.
This package contains static libraries for lzo.


%package -n mingw64-lzo-minilzo-static
Summary:        Static library for minilzo
Requires:       mingw64-lzo-minilzo = %{version}-%{release}

%description -n mingw64-lzo-minilzo-static
A small (mini) version of lzo for embedding into applications which don't need
full blown lzo compression support. This package contains static libraries for
minilzo.


%{?mingw_debug_package}


%prep
%setup -q -n lzo-%{version}
%patch0 -p1 -z .configure
%patch1 -p1 -z .rhbz1309225
# mark asm files as NOT needing execstack
for i in asm/i386/src_gas/*.S; do
  echo '.section .note.GNU-stack,"",@progbits' >> $i
done


%build
%mingw_configure --disable-dependency-tracking --enable-static --enable-shared
%mingw_make %{?_smp_mflags}
# build minilzo too (bz 439979)
# Win32
%{mingw32_target}-gcc \
    %{mingw32_cflags} \
    -fpic \
    -Iinclude/lzo \
    -o build_win32$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o \
    -c minilzo/minilzo.c
%{mingw32_target}-ar \
    rcs \
    build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo.a \
    build_win32$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o
%{mingw32_target}-gcc \
    -g -shared \
    -o build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo-0.dll \
    -Wl,--out-implib,build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo.dll.a \
    build_win32$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o
# Win64
%{mingw64_target}-gcc \
    %{mingw64_cflags} \
    -fpic \
    -Iinclude/lzo \
    -o build_win64$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o \
    -c minilzo/minilzo.c
%{mingw64_target}-ar \
    rcs \
    build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo.a \
    build_win64$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o
%{mingw64_target}-gcc \
    -g -shared \
    -o build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo-0.dll \
    -Wl,--out-implib,build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo.dll.a \
    build_win64$MINGW_BUILDDIR_SUFFIX/minilzo/minilzo.o


%install
%mingw_make_install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete
# Win32
install -m 755 build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo-0.dll %{buildroot}%{mingw32_bindir}
install -m 644 build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo.dll.a %{buildroot}%{mingw32_libdir}
install -m 644 build_win32$MINGW_BUILDDIR_SUFFIX/libminilzo.a %{buildroot}%{mingw32_libdir}
install -p -m 644 minilzo/minilzo.h %{buildroot}%{mingw32_includedir}/lzo
# Win64
install -m 755 build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo-0.dll %{buildroot}%{mingw64_bindir}
install -m 644 build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo.dll.a %{buildroot}%{mingw64_libdir}
install -m 644 build_win64$MINGW_BUILDDIR_SUFFIX/libminilzo.a %{buildroot}%{mingw64_libdir}
install -p -m 644 minilzo/minilzo.h %{buildroot}%{mingw64_includedir}/lzo

# Remove doc
rm -rf %{buildroot}%{mingw32_datadir}/doc/lzo
rm -rf %{buildroot}%{mingw64_datadir}/doc/lzo


# Win32
%files -n mingw32-lzo
%license COPYING
%doc AUTHORS THANKS NEWS
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{mingw32_bindir}/liblzo2-*.dll
%{mingw32_includedir}/lzo
%{mingw32_libdir}/liblzo2.dll.a

%files -n mingw32-lzo-minilzo
%license COPYING
%doc minilzo/README.LZO
%{mingw32_bindir}/libminilzo-*.dll
%{mingw32_libdir}/libminilzo.dll.a

%files -n mingw32-lzo-static
%license COPYING
%{mingw32_libdir}/liblzo2.a

%files -n mingw32-lzo-minilzo-static
%license COPYING
%{mingw32_libdir}/libminilzo.a


# Win64
%files -n mingw64-lzo
%license COPYING
%doc AUTHORS THANKS NEWS
%doc doc/LZOAPI.TXT doc/LZO.FAQ doc/LZO.TXT
%{mingw64_bindir}/liblzo2-*.dll
%{mingw64_includedir}/lzo
%{mingw64_libdir}/liblzo2.dll.a

%files -n mingw64-lzo-minilzo
%license COPYING
%doc minilzo/README.LZO
%{mingw64_bindir}/libminilzo-*.dll
%{mingw64_libdir}/libminilzo.dll.a

%files -n mingw64-lzo-static
%license COPYING
%{mingw64_libdir}/liblzo2.a

%files -n mingw64-lzo-minilzo-static
%license COPYING
%{mingw64_libdir}/libminilzo.a


%changelog
* Sun Jun 11 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 2.08-9.1
- Convert to mingw package
- Remove Group and BuildRoot options

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Karsten Hopp <karsten@redhat.com> - 2.08-8
- remove -O1 workaround, add patch by Jakub Jelinek instead (bug #1309225)

* Wed Feb 17 2016 Karsten Hopp <karsten@redhat.com> - 2.08-7
- use -O1 compiler optimizations on ppc64le (bug #1309225)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 2.08-5
- Link libminilzo with -z now

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.08-2
- fix license handling

* Mon Jun 30 2014 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.08-1
- New upstream
- Fix CVE-2014-4607

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 14 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 2.06-1
- Upgrade to latest upstream
- Apply patch from Nicolas Chauvet

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May  1 2008 Lubomir Rintel <lkundrak@v3.sk> 2.03-1
- New upstream release
- Changed the license to GPLv2+

* Wed Apr  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-5
- Fix configure failure with -Werror-implicit-function-declaration in CFLAGS
- Add a minilzo subpackage which contains a shared version of minilzo, to be
  used by all applications which ship with their own copy of it (bz 439979)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.02-4
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-3
- Update License tag for new Licensing Guidelines compliance

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-2
- FE6 Rebuild

* Wed Jul 26 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.02-1
- New upstream release 2.02, soname change!

* Mon Jul 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.08-7
- Taking over as maintainer since Anvil has other priorities
- Add a patch to fix asm detection on i386 (bug 145882, 145893). Thanks to
  Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe> for the initial patch.
- Removed unused build dependency on nasm
- Remove static lib
- Cleanup %%doc a bit

* Thu Mar 16 2006 Dams <anvil[AT]livna.org> - 1.08-6.fc5
- Rebuild for new gcc

* Tue Jan 17 2006 Dams <anvil[AT]livna.org> - 1.08-5.fc5
- Bumped release for gcc 4.1 rebuild

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.08-4
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:1.08-0.fdr.2
- Typo un devel description
- Added post and postun scriptlets
- Added URL in Source0

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.
