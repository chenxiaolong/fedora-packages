%define buildforkernels akmod
%define debug_package %{nil}

Name:           bbswitch-kmod
Version:        0.8
Release:        3%{?dist}
Summary:        Kernel module for powering off discrete GPU on Optimus laptops

License:        GPLv2+
URL:            https://github.com/Bumblebee-Project/bbswitch
Source0:        https://github.com/Bumblebee-Project/bbswitch/archive/v%{version}.tar.gz

BuildRequires:  kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
bbswitch is a kernel module for powering off the discrete GPU on NVIDIA
Optimus-enabled laptops.

This package contains the bbswitch kernel module for kernel %{kversion}.


%package common
Summary:        Common files for bbswitch kernel module
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description common
This package contains the common files (license, documentation, etc.) for the
bbswitch kernel module.


%prep
%setup -q -T -c
tar xf %{SOURCE0}

# For common package
cp bbswitch-%{version}/{COPYING,NEWS,README.md} .

%{?kmodtool_check}

kmodtool --target %{_target_cpu} --repo %{repo} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

for kernel_version in %{?kernel_versions}; do
    cp -al bbswitch-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make %{?_smp_mflags} \
        -C "${kernel_version##*___}" \
        M=${PWD}/_kmod_build_${kernel_version%%___*} \
        modules
done


%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 0755 _kmod_build_${kernel_version%%___*}/bbswitch.ko \
        %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/bbswitch.ko
done

%{?akmod_install}


%files common
%doc NEWS README.md
%license COPYING


%changelog
* Tue Jan 07 2020 Andrew Gunnerson <chillermillerlong@hotmail.com> - 0.8-3
- Change deprecated SUBDIRS= to M=
- https://github.com/chenxiaolong/fedora-packages/issues/9

* Mon May 20 2019 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.8-2
- Rebuild against new kmodtool

* Mon Dec 25 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 0.8-1
- Initial release
