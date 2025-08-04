%global buildforkernels akmod
%global debug_package %{nil}

%global _name ProCapture
%global _archive_name ProCaptureForLinux

Name:           %{_name}-kmod
Version:        1.3.4420
Release:        2%{?dist}
Summary:        Driver for Magewell Pro Capture Family

License:        Proprietary
URL:            https://www.magewell.com/downloads/pro-capture#/driver/linux-x86
Source0:        https://www.magewell.com/files/drivers/%{_archive_name}_%{version}.tar.gz
Patch0:         0001-Wrap-deprecated-v4l2-callbacks-instead-of-removing-t.patch
Patch1:         0002-Use-timer_container_of-on-6.16.patch

BuildRequires:  kmodtool
BuildRequires:  systemd-rpm-macros

%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{_name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
%{summary}

This package contains the kernel module for kernel %{kversion}.


%package common
Summary:        Common utilities for the ProCapture driver
ExclusiveArch:  i686 x86_64

%description common
This package contains the supporting utilities for the ProCapture kernel module.


%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{_name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c

%patch -P0 -p1 -d %{_archive_name}_%{version}
%patch -P1 -p1 -d %{_archive_name}_%{version}

for kernel_version in %{?kernel_versions}; do
  cp -a %{_archive_name}_%{version}/src _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make V=1 %{?_smp_mflags} \
        -C ${kernel_version##*___} \
        M=${PWD}/_kmod_build_${kernel_version%%___*} \
        modules
done


%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/%{_name}.ko \
        %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{_name}.ko
done

pushd %{_archive_name}_%{version}

%ifarch x86_64
bits=64
%else
bits=32
%endif

install -Dm755 bin/mwcap-control_${bits} %{buildroot}%{_bindir}/mwcap-control
install -Dm755 bin/mwcap-info_${bits} %{buildroot}%{_bindir}/mwcap-info

install -Dm644 src/res/* \
    -t %{buildroot}%{_datadir}/%{_name}/res/

install -dm755 %{buildroot}%{_modprobedir}
sed 's,/usr/local/,/usr/,g' \
    < scripts/%{_name}.conf \
    > %{buildroot}%{_modprobedir}/%{_name}.conf

# Fix the typo.
install -Dm644 scripts/10-procatpure-event-dev.rules \
    %{buildroot}%{_udevrulesdir}/10-procapture-event-dev.rules

popd

%{?akmod_install}


%files common
%doc %{_archive_name}_%{version}/quick_start.txt
%doc %{_archive_name}_%{version}/docs/
%{_bindir}/mwcap-control
%{_bindir}/mwcap-info
%{_datadir}/%{_name}/res/*.png
%{_modprobedir}/%{_name}.conf
%{_udevrulesdir}/10-procapture-event-dev.rules


%changelog
* Mon Aug 04 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1.3.4420-2
- Add support for kernel 6.16

* Tue Jul 01 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1.3.4420-1
- Update to 1.3.4420
- Reintroduce removed v4l2 callbacks via wrappers

* Mon Jun 30 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1.3.4418-2
- Add support for kernel 6.15

* Mon Mar 24 2025 Andrew Gunnerson <accounts+fedora@chiller3.com> - 1.3.4418-1
- Initial release
