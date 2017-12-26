%global commit d1afbf6fce2778c0751eddf19db9882e04f18bfd
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global desc \
Primus is a shared library that provides OpenGL and GLX APIs and implements\
low-overhead local-only client-side OpenGL offloading via GLX forking, similar\
to VirtualGL. It intercepts GLX calls and redirects GL rendering to a secondary\
X display, presumably driven by a faster GPU. On swapping buffers, rendered\
contents are read back using a PBO and copied onto the drawable it was supposed\
to be rendered on in the first place.


Name:           primus-source
Version:        0.2
Release:        1.git%{shortcommit}%{?dist}
Summary:        Faster OpenGL offloading for Bumblebee

License:        ISC
URL:            https://github.com/amonakov/primus
Source0:        https://github.com/amonakov/primus/archive/%{commit}.tar.gz
# From Arch Linux
Patch0:         register_cleanup.patch
# https://github.com/amonakov/primus/pull/195
Patch1:         0001-primus-needs-this-variable-workaround-for-libglvnd-e.patch
# Fix primusrun paths
Patch10:        0001-Use-Fedora-specific-library-paths.patch

BuildRequires:  gcc-c++
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel

%description
%{desc}


# Hack to allow primus to be noarch and primus-libs to be multilib
%package -n primus
Summary:        Faster OpenGL offloading for Bumblebee

Requires:       primus-libs = %{version}-%{release}
Requires:       bumblebee

BuildArch:      noarch

%description -n primus
%{desc}


%package -n primus-libs
Summary:        Shared libraries for primus

%description -n primus-libs
%{desc}


%prep
%autosetup -p1 -n primus-%{commit}


%build
export CXXFLAGS='%{optflags}'
export LIBDIR=%{_lib}
# Use glvnd libGL ($$ because this gets dereferenced by the Makefile)
export PRIMUS_libGLa='/usr/$$LIB/libGL.so.1'
%make_build


%install
# Install launcher
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 primusrun \
    %{buildroot}%{_bindir}/

# Install library
install -d -m 0755 %{buildroot}%{_libdir}/primus
install -m 0755 %{_lib}/libGL.so.1 \
    %{buildroot}%{_libdir}/primus/

# Install bash-completion file
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions/
install -m 0644 primus.bash-completion \
    %{buildroot}%{_datadir}/bash-completion/completions/primusrun

# Install man page
install -d -m 0755 %{buildroot}%{_mandir}/man1/
install -m 0644 primusrun.1 \
    %{buildroot}%{_mandir}/man1/


%post -n primus-libs -p /sbin/ldconfig


%postun -n primus-libs -p /sbin/ldconfig


%files -n primus
%doc README.md technotes.md
%license LICENSE.txt
%{_bindir}/primusrun
%{_datadir}/bash-completion/completions/primusrun
%{_mandir}/man1/primusrun.1*


%files -n primus-libs
%dir %{_libdir}/primus/
%{_libdir}/primus/libGL.so.1


%changelog
* Mon Dec 25 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.2.1.gitd1afbf6
- Initial release
- Based on Arch Linux package
