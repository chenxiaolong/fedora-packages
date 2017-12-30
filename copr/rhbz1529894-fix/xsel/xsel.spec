Name:           xsel
Version:        1.2.0
Release:        20.1%{?dist}
Summary:        Command line clipboard and X selection tool
Group:          Applications/System
License:        MIT
URL:            http://www.vergenet.net/~conrad/software/xsel/
Source0:        http://www.vergenet.net/~conrad/software/xsel/download/xsel-%{version}.tar.gz
# Applied upstream (BZ#690214)
Patch0:         xsel-1.2.0-MAX_NUM_TARGETS.patch
# Upstream: https://github.com/kfish/xsel/commit/ba8656dc7c7e771c802fc957ce3dd128d4b6e3ae
Patch1:         xsel-1.2.0-fix-large-pastes.patch
# Patch for rhbz#1473002, taken from https://github.com/kfish/xsel/pull/6
Patch2:         xsel-1.2.0-fix-java-pasting.patch
# Upstream: https://github.com/kfish/xsel/pull/16
Patch3:         0001-Do-not-prematurely-terminate-string-while-receiving-.patch
Patch4:         0002-Send-correct-SelectionNotify-event-when-starting-INC.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libSM-devel libXt-devel libXext-devel

%description
XSel is a command line or script utility, similar to xclip, that can copy the
primary and secondary X selection, or any highlighted text, to or from a file,
stdin or stdout. It can also append to and delete the clipboard or buffer that
you would paste with the middle mouse button.

%prep
%setup -q
%patch0 -p1 -b .MAX_NUM_TARGETS
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_mandir}/man1/xsel.1x*
%{_bindir}/xsel

%changelog
* Sat Dec 30 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 1.2.0-20.1
- Add patches for https://github.com/kfish/xsel/pull/16

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-19
- Fix pasting into Java programs
- Resolves: rhbz#1473002

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 05 2012 Hans de Goede <hdegoede@redhat.com> - 1.2.0-10
- Fix xsel not working when pasting large amounts of text

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 07 2011 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.0-8
- xsel-1.2.0-MAX_NUM_TARGETS.patch: fix xsel overflow of supported_targets array
  (BZ#690214 - Thanks Hans de Goede)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 08 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.0-4
- retag for F-8, missing spec file

* Sat Jul 26 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.0-3
- file section to catch all man compressions & no compressions

* Sat Apr 19 2008 Henry Kroll <nospam[AT]thenerdshow.com> - 1.2.0-2
- Standardize build section, remove unnecessary CDEBUGFLAGS.
- Break up long lines, general cleanup.

* Sat Apr 12 2008 Henry Kroll <nospam[AT]thenerdshow.com> - 1.2.0-1
- Version upgrade
- Change license to MIT Old Style
- Fix URL, Requires, BuildRequires. 
- Change group to Applications/System re: xclip. Include keywords
 in the description to make it easier to find.

* Thu Mar 20 2008 Henry Kroll <nospam[AT]thenerdshow.com> - 1.1.0-1
- RPM test build
