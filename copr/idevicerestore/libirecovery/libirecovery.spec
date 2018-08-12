%global commit 27b13f782720199420f7dc07993deed1958a0dbf
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           libirecovery
Version:        0.1
Release:        1.git%{shortcommit}%{?dist}
Summary:        Library and utility to talk to iBoot/iBSS via USB

License:        LGPLv2+
URL:            https://github.com/libimobiledevice/libirecovery
Source0:        https://github.com/libimobiledevice/libirecovery/archive/%{commit}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  systemd

BuildRequires:  libusb-devel
BuildRequires:  readline-devel

%description
libirecovery is a cross-platform library which implements communication to
iBoot/iBSS found on Apple's iOS devices via USB. A command-line utility is also
provided.


%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.


%package utils
Summary:        Utilites for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description utils
Utilites for use with %{name}.


%prep
%autosetup -n %{name}-%{commit}

autoreconf -fi


%build
%configure --disable-static
%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete


%files
%license COPYING
%doc README
%{_libdir}/%{name}.so.*
%{_udevrulesdir}/39-libirecovery.rules


%files devel
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so
%{_includedir}/%{name}.h


%files utils
%{_bindir}/irecovery


%changelog
* Sun Aug 12 2018 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.1-1.git27b13f7
- Initial release
