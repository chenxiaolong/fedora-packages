%{?mingw_package_header}

Name:		    mingw-jansson
Version:	    2.10
Release:	    2.1%{?dist}
Summary:	    C library for encoding, decoding and manipulating JSON data

License:	    MIT
URL:		    http://www.digip.org/jansson/
Source0:	    http://www.digip.org/jansson/releases/jansson-%{version}.tar.bz2

# Already merged upstream and will be available in 2.11
# https://github.com/akheron/jansson/commit/28666cead0a4c946b234d42f25b8a9db81f9bbdf
Patch00:	    jansson-2.10-optionalpack.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc

#BuildRequires:	python-sphinx

%description
Small library for parsing and writing JSON documents.


# Mingw32
%package -n mingw32-jansson
Summary:	    C library for encoding, decoding and manipulating JSON data

%description -n mingw32-jansson
Small library for parsing and writing JSON documents.


%package -n mingw32-jansson-static
Summary:        Static library for jansson
Requires:       mingw32-jansson = %{version}-%{release}

%description -n mingw32-jansson-static
Small library for parsing and writing JSON documents. This package contains
static libraries for jansson.


# Mingw64
%package -n mingw64-jansson
Summary:	    C library for encoding, decoding and manipulating JSON data

%description -n mingw64-jansson
Small library for parsing and writing JSON documents.


%package -n mingw64-jansson-static
Summary:        Static library for jansson
Requires:       mingw64-jansson = %{version}-%{release}

%description -n mingw64-jansson-static
Small library for parsing and writing JSON documents. This package contains
static libraries for jansson.


%{?mingw_debug_package}


%prep
%autosetup -n jansson-%{version} -p1


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install INSTALL="install -p" DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete


# Win32
%files -n mingw32-jansson
%license LICENSE
%doc CHANGES
%{mingw32_bindir}/libjansson-*.dll
%{mingw32_includedir}/jansson*.h
%{mingw32_libdir}/libjansson.dll.a
%{mingw32_libdir}/pkgconfig/jansson.pc

%files -n mingw32-jansson-static
%license LICENSE
%{mingw32_libdir}/libjansson.a


# Win64
%files -n mingw64-jansson
%license LICENSE
%doc CHANGES
%{mingw64_bindir}/libjansson-*.dll
%{mingw64_includedir}/jansson*.h
%{mingw64_libdir}/libjansson.dll.a
%{mingw64_libdir}/pkgconfig/jansson.pc

%files -n mingw64-jansson-static
%license LICENSE
%{mingw64_libdir}/libjansson.a


%changelog
* Sun Jun 11 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 2.10-2.1
- Convert to mingw package

* Sat Jun 10 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2.10-2
- Add upstream patch for optional arguments to json_pack()
- Migrate to use autosetup macro

* Thu Mar 02 2017 Nathaniel McCallum <npmccallum@redhat.com> - 2.10-1
- Update to Jansson 2.10

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2.9-1
- Update to Jansson 2.9

* Fri Sep 16 2016 Nathaniel McCallum <npmccallum@redhat.com> - 2.8-1
- Update to Jansson 2.8
- Add json_auto_t patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 05 2015 Jiri Pirko <jpirko@redhat.com> 2.7-1
- Update to Jansson 2.7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 15 2014 Jiri Pirko <jpirko@redhat.com> 2.6-3
- Create devel-doc package

* Tue Mar 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.6-2
- Package cleanups

* Thu Feb 13 2014 Jared Smith <jsmith@fedoraproject.org> - 2.6-1
- Update to Jansson 2.6 for CVE-2013-6401 

* Sat Jan 25 2014 Jiri Pirko <jpirko@redhat.com> 2.5-1
- Update to Jansson 2.5.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 08 2012 Jiri Pirko <jpirko@redhat.com> 2.4-1
- Update to Jansson 2.4.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Jiri Pirko <jpirko@redhat.com> 2.3-1
- Update to Jansson 2.3.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 11 2011 Sean Middleditch <sean@middleditch.us> 2.1-1
- Update to Jansson 2.1.
- Drop Sphinx patch, no longer necessary.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 03 2010 Sean Middleditch <sean@middleditch.us> 1.3-1
- Update to Jansson 1.3.
- Disable warnings-as-errors for Sphinx documentation.

* Thu Jan 21 2010 Sean Middleditch <sean@middleditch.us> 1.2-1
- Update to Jansson 1.2.

* Thu Jan 11 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-4
- Update jansson description per upstream's suggestions.
- Removed README from docs.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-3
- Correct misspelling of jansson in the pkg-config file.

* Thu Jan 09 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-2
- Fix Changelog dates.
- Mix autoheader warning.
- Added make check.
- Build and install HTML documentation in -devel package.

* Thu Jan 07 2010 Sean Middleditch <sean@middleditch.us> 1.1.3-1
- Initial packaging for Fedora.
