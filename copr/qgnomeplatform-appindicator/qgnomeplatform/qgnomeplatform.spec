
Name:           qgnomeplatform
Version:        0.3
Release:        5.1%{?dist}
Summary:        Qt Platform Theme aimed to accommodate Gnome settings

License:        LGPLv2+
URL:            https://github.com/MartinBriza/QGnomePlatform
Source0:        https://github.com/MartinBriza/QGnomePlatform/archive/%{version}/QGnomePlatform-%{version}.tar.gz

Patch0:         https://github.com/chenxiaolong/QGnomePlatform/commit/021ee8699aa76ca4f74d206b848ae289487b96a5.patch

# Upstream patches

BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  gtk3-devel
BuildRequires:  libinput-devel
BuildRequires:  libXrender-devel
# please document if/why this is needed, FTBFS against qt-5.7.0 in rawhide obviously -- rex
#BuildRequires:  qt5-qtbase-devel >= 5.6.0 qt5-qtbase-devel <= 5.6.100
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-static

Requires:       adwaita-qt5%{?_isa}

BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%description
QGnomePlatform is a Qt Platform Theme aimed to accommodate as much of
GNOME settings as possibleand utilize them in Qt applications without
modifying them - making them fit into the environment as well as possible.


%prep
%autosetup -p1 -n  QGnomePlatform-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{qmake_qt5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}

%files
%doc README.md
%license LICENSE
%{_qt5_libdir}/qt5/plugins/platformthemes/libqgnomeplatform.so


%changelog
* Sun Oct 22 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.3-5.1
- Add patch for AppIndicator support
- https://github.com/MartinBriza/QGnomePlatform/pull/29

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3-5
- rebuild (qt5)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3-2
- rebuild (qt5)

* Mon May 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.3-1
- Update to 0.3

* Mon May 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.2-17.20170206git
- rebuild (Qt 5.9)

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.2-16.20170206git
- fresh 20170206 snapshot (#1438024)

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.2-15.20161205git
- rebuild (Qt 5.8)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2-14.20161205git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Jan Grulich <jgrulich@redhat.com> - 0.2-13.20161205git
- Fix crash in font dialog (bz#1378003)

* Thu Dec 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-12.20161024git
- rebuild (qt5)

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> 0.2-11.20161024git
- release++

* Thu Nov 17 2016 Rex Dieter <rdieter@fedoraproject.org> 0.2-10.20161024git.2
- branch rebuild (qt5)

* Mon Oct 24 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-10.20161024git
- Fix Gtk3 dialogs on wayland

* Mon Jul 18 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-9.20160718git
- Fix not working dialogs

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> 0.2-8.20160621git
- rebuild (qt5-qtbase)

* Wed Jul 13 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-7.20160621git
- Remove runtime dependency on GDM

* Wed Jun 29 2016 Rex Dieter <rdieter@fedoraproject.org> 0.2-6.20160621git
- rebuild (qt5)

* Tue Jun 21 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-5.20160621git
- Don't fallback to gtk+ style

* Fri Jun 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.2-4.20160531git
- arch'd adwaita-qt5 runtime dep
- use system %%_qt5_version macro, instead of by-hand one here
- BR: qt5-qtbase-private-devel (helps track hard qt5-qtbase runtime dep)

* Fri Jun 10 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-3.20160531git
- rebuild (qt5-qtbase)

* Mon Jun 06 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-2.20160531git
- Add runtime dependency on adwaita-qt5 (bz#1332103)

* Tue May 31 2016 Jan Grulich <jgrulich@redhat.com> - 0.2-1.20160531git
- Update to latest git snapshot

* Wed Apr 20 2016 Jan Grulich <jgrulich@redhat.com> - 0.1-5
- Pull in upstream changes

* Wed Mar 16 2016 Jan Grulich <jgrulich@redhat.com> - 0.1-4
- Improve font size

* Thu Feb 25 2016 Jan Grulich <jgrulich@redhat.com> - 0.1-3
- Revert usage of qgnomeplatform.env in GDM

* Thu Feb 25 2016 Jan Grulich <jgrulich@redhat.com> - 0.1-2
- Install qgnomeplatform.env to gdm to automatically use it after we log in

* Tue Feb 16 2016 Jan Grulich <jgrulich@redhat.com> - 0.1-1
- First version
