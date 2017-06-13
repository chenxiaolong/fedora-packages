%{?mingw_package_header}

Summary:        Google C++ testing framework
Name:           mingw-gtest
Version:        1.8.0
Release:        1.1%{?dist}
License:        BSD
URL:            http://code.google.com/p/googletest/
Source0:        https://github.com/google/googletest/archive/release-%{version}.tar.gz

# https://github.com/google/googletest/issues/845
Patch1:         gtest-null-pointer.patch

# https://github.com/google/googletest/pull/721
Patch2:         0001-Fix-compilation-on-MinGW-with-native-threads.patch
Patch3:         0002-Don-t-use-pthread-when-on-MinGW-even-if-available.patch

# https://github.com/google/googletest/pull/856
Patch4:         0001-Fix-build-with-MinGW-w64.patch

Patch5:         0001-Install-pkgconfig-files.patch
Patch6:         0002-Install-DLLs-to-correct-directory.patch

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw64-gcc-c++

BuildRequires:  cmake
#BuildRequires:  python-devel

%description
Framework for writing C++ tests on a variety of platforms (GNU/Linux,
Mac OS X, Windows, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.


# Mingw32
%package -n mingw32-gtest
Summary:        Google C++ testing framework

%description -n mingw32-gtest
Framework for writing C++ tests on a variety of platforms (GNU/Linux,
Mac OS X, Windows, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.


%package -n mingw32-gmock
Summary:        Google C++ Mocking Framework
Requires:       mingw32-gtest = %{version}-%{release}

%description -n mingw32-gmock
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++'s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:

 o lets you create mock classes trivially using simple macros,
 o supports a rich set of matchers and actions,
 o handles unordered, partially ordered, or completely ordered
   expectations,
 o is extensible by users, and
 o works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
   Symbian.


# Mingw64
%package -n mingw64-gtest
Summary:        Google C++ testing framework

%description -n mingw64-gtest
Framework for writing C++ tests on a variety of platforms (GNU/Linux,
Mac OS X, Windows, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of
assertions, user-defined assertions, death tests, fatal and non-fatal
failures, various options for running the tests, and XML test report
generation.


%package -n mingw64-gmock
Summary:        Google C++ Mocking Framework
Requires:       mingw64-gtest = %{version}-%{release}

%description -n mingw64-gmock
Inspired by jMock, EasyMock, and Hamcrest, and designed with C++'s
specifics in mind, Google C++ Mocking Framework (or Google Mock for
short) is a library for writing and using C++ mock classes.

Google Mock:

 o lets you create mock classes trivially using simple macros,
 o supports a rich set of matchers and actions,
 o handles unordered, partially ordered, or completely ordered
   expectations,
 o is extensible by users, and
 o works on Linux, Mac OS X, Windows, Windows Mobile, minGW, and
   Symbian.


%{?mingw_debug_package}


%prep
%autosetup -n googletest-release-%{version} -N
%patch1 -p1 -b .0-null-pointer
%patch2 -p1 -b .fix-native-threads
%patch3 -p1 -b .disable-pthreads
%patch4 -p1 -b .fix-mingw-w64
%patch5 -p1 -b .pkgconfig
%patch6 -p1 -b .dll-bin-dir

# Delete backup files that get installed
find -name '*.fix-native-threads' -delete
find -name '*.fix-mingw-w64' -delete


%build
pushd googletest
%mingw_cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_SKIP_BUILD_RPATH=TRUE \
    -DVERSION=%{version} \
    #-DPYTHON_EXECUTABLE=%{__python2} \
    #-Dgtest_build_tests=ON
%mingw_make %{?_smp_mflags}
popd

pushd googlemock
%mingw_cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_SKIP_BUILD_RPATH=TRUE \
    -DVERSION=%{version} \
    #-Dgmock_build_tests=ON
%mingw_make %{?_smp_mflags}
popd


%install
pushd googletest
%mingw_make_install DESTDIR=%{buildroot}
popd

pushd googlemock
%mingw_make_install DESTDIR=%{buildroot}
popd


# Win32
%files -n mingw32-gtest
%license googletest/LICENSE
%doc googletest/CHANGES googletest/CONTRIBUTORS googletest/README.md
%{mingw32_bindir}/libgtest.dll
%{mingw32_bindir}/libgtest_main.dll
%{mingw32_includedir}/gtest/
%{mingw32_libdir}/libgtest.dll.a
%{mingw32_libdir}/libgtest_main.dll.a
%{mingw32_libdir}/pkgconfig/gtest.pc

%files -n mingw32-gmock
%license googlemock/LICENSE
%doc googlemock/CHANGES googlemock/CONTRIBUTORS googlemock/README.md
%{mingw32_bindir}/libgmock.dll
%{mingw32_bindir}/libgmock_main.dll
%{mingw32_includedir}/gmock/
%{mingw32_libdir}/libgmock.dll.a
%{mingw32_libdir}/libgmock_main.dll.a
%{mingw32_libdir}/pkgconfig/gmock.pc


# Win64
%files -n mingw64-gtest
%license googletest/LICENSE
%doc googletest/CHANGES googletest/CONTRIBUTORS googletest/README.md
%{mingw64_bindir}/libgtest.dll
%{mingw64_bindir}/libgtest_main.dll
%{mingw64_includedir}/gtest/
%{mingw64_libdir}/libgtest.dll.a
%{mingw64_libdir}/libgtest_main.dll.a
%{mingw64_libdir}/pkgconfig/gtest.pc

%files -n mingw64-gmock
%license googlemock/LICENSE
%doc googlemock/CHANGES googlemock/CONTRIBUTORS googlemock/README.md
%{mingw64_bindir}/libgmock.dll
%{mingw64_bindir}/libgmock_main.dll
%{mingw64_includedir}/gmock/
%{mingw64_libdir}/libgmock.dll.a
%{mingw64_libdir}/libgmock_main.dll.a
%{mingw64_libdir}/pkgconfig/gmock.pc


%changelog
* Sun Jun 11 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 1.8.0-1.1
- Convert to mingw package
- Update to 1.8.0
- Add gmock

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 15 2017 Terje Rosten <terje.rosten@ntnu.no> - 1.7.0-8
- Use patch from Jonathan Wakely to fix opt issue (rhbz#1408291)

* Wed Dec 21 2016 Merlin Mathesius <mmathesi@redhat.com> - 1.7.0-7
- Disable C++ compiler optimization to fix FTBFS (BZ#1406937).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 Dominik Mierzejewski <rpm@greysector.net> - 1.7.0-4
- rebuilt for gcc-5.0.0-0.22.fc23

* Mon Feb 23 2015 Terje Rosten <terje.rosten@ntnu.no> - 1.7.0-3
- Rebuild for gcc5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Terje Rosten <terje.rosten@ntnu.no> - 1.7.0-1
- 1.7.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Rex Dieter <rdieter@fedoraproject.org> 1.6.0-3
- use %%cmake macro, fix %%check, use RPM_BULID_ROOT consistently

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 28 2012 Akira TAGOH <tagoh@redhat.com> - 1.6.0-1
- New upstream release.
- Using autotools isn't supported in upstream anymore. switching to cmake.
- undefined reference issues seems gone now. (#813825)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 15 2011 Akira TAGOH <tagoh@redhat.com> j- 1.5.0-5
- Fix FTBFS issue; update libtool files instead of disabling rpath things.

* Sun Mar 20 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.5.0-4
- add patch from Dan Horák to let 'make check' work 

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.5.0-2
- add python to buildreq 

* Wed Jan 12 2011 Terje Rosten <terje.rosten@ntnu.no> - 1.5.0-1
- 1.5.0
- some cleanup

* Thu Aug 26 2010 Dan Horák <dan[at]danny.cz> - 1.4.0-2
- added workaround for linking the tests on Fedora >= 13 (#564953, #599865)

* Sat Nov 14 2009 Debarshi Ray <rishi@fedoraproject.org> - 1.4.0-1
- Version bump to 1.4.0.
  * New feature: the event listener API.
  * New feature: test shuffling.
  * New feature: the XML report format is closer to junitreport and can
    be parsed by Hudson now.
  * New feature: elapsed time for the tests is printed by default.
  * New feature: comes with a TR1 tuple implementation such that Boost
    is no longer needed for Combine().
  * New feature: EXPECT_DEATH_IF_SUPPORTED macro and friends.
  * New feature: the Xcode project can now produce static gtest libraries in
    addition to a framework.
  * Compatibility fixes for gcc and minGW.
  * Bug fixes and implementation clean-ups.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 1.3.0-2.20090601svn257
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 01 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3.0-1
- Version bump to 1.3.0.
  * New feature: ability to use Google Test assertions in other testing
    frameworks.
  * New feature: ability to run disabled test via
    --gtest_also_run_disabled_tests.
  * New feature: the --help flag for printing the usage.
  * New feature: access to Google Test flag values in user code.
  * New feature: a script that packs Google Test into one .h and one .cc file
    for easy deployment.
  * New feature: support for distributing test functions to multiple machines
    (requires support from the test runner).
  * Bug fixes and implementation clean-ups.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jul 05 2008 Debarshi Ray <rishi@fedoraproject.org> - 1.0.0-1
- Initial build.
