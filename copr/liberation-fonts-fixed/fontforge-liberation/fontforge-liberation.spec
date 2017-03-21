%global gnulib_githead 2bf7326
%global gittag0 20161012

Name:           fontforge-liberation
Version:        %{gittag0}
Release:        6.1%{?dist}
Summary:        Outline and bitmap font editor

License:        GPLv3+
URL:            http://fontforge.github.io/
Source0:        https://github.com/fontforge/fontforge/archive/%{gittag0}.tar.gz#/fontforge-%{version}.tar.gz
# https://github.com/fontforge/fontforge/issues/1725
Source1:        http://git.savannah.gnu.org/gitweb/?p=gnulib.git;a=snapshot;h=%{gnulib_githead};sf=tgz;name=gnulib-%{gnulib_githead}.tar.gz
# https://github.com/fontforge/fontforge/pull/1723
Patch0:         fontforge-20140813-use-system-uthash.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1433628
Patch1:         0001-Revert-Fix-read-write-of-bits-USE_TYPO_METRICS-and-W.patch
Patch2:         0002-Rename-binaries-and-libraries-to-not-conflict-with-o.patch

Requires:       xdg-utils
Requires:       autotrace
Requires:       hicolor-icon-theme

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  libungif-devel
BuildRequires:  libxml2-devel
BuildRequires:  freetype-devel
BuildRequires:  libuninameslist-devel
BuildRequires:  pango-devel
BuildRequires:  cairo-devel
BuildRequires:  libspiro-devel
BuildRequires:  gnulib-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  readline-devel
BuildRequires:  uthash-devel

Provides: bundled(gnulib)

%description
FontForge (former PfaEdit) is a font editor for outline and bitmap
fonts. It supports a range of font formats, including PostScript
(ASCII and binary Type 1, some Type 3 and Type 0), TrueType, OpenType
(Type2) and CID-keyed fonts.

This is a patched version of the package meant for building
liberation-fonts only.


%prep
%autosetup -p1 -n fontforge-%{version}
tar xzf %{SOURCE1}


%build
./bootstrap --skip-git --gnulib-srcdir=gnulib-%{gnulib_githead}
export CFLAGS="%{optflags} -fno-strict-aliasing"

%configure \
    --disable-python-scripting \
    --disable-python-extension \
    --without-x
%make_build


%install
%make_install

rename -- .1 -liberation.1 %{buildroot}%{_mandir}/man1/*.1

# Remove unneeded files
rm -r \
    %{buildroot}%{_datadir}/doc/fontforge \
    %{buildroot}%{_datadir}/fontforge \
    %{buildroot}%{_datadir}/locale \
    %{buildroot}%{_includedir} \
    %{buildroot}%{_libdir}/pkgconfig

find %{buildroot} \( -name '*.a' -o -name '*.la' -o -name '*.so' \) -delete


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS
%license LICENSE
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_mandir}/man1/*.1*


%changelog
* Sun Mar 19 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 20161012-6.1
- Based on Fedora rawhide package
- Rename package and strip away anything that's not needed for building liberation-fonts
