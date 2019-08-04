# For SELinux
%global modulename bumblebee-extra

Name:           bumblebee
Version:        3.2.1
Release:        4%{?dist}
Summary:        Daemon to support NVIDIA Optimus via VirtualGL

License:        GPLv3+
URL:            https://bumblebee-project.org/
Source0:        https://bumblebee-project.org/bumblebee-%{version}.tar.gz
Source1:        bumblebee-blacklist.conf
Source2:        %{modulename}.te

# Patches from Arch Linux:
# https://git.archlinux.org/svntogit/community.git/tree/trunk?h=packages/bumblebee
Patch0:         0001-bb_nvidia_modeset-detection_bug699_01.patch
Patch1:         0002-bb_nvidia_modeset-detection_bug699_02.patch
Patch2:         0003-bb_nvidia_umv_detection_bug699.patch
Patch3:         0004-bb_nvidia_drm_detection_bug699_01.patch
Patch4:         0005-bb_nvidia_drm_detection_bug699_02.patch
Patch5:         0006-bb_hexadicimal_bug573.patch
Patch6:         0007-bb_mutebblogger.patch
Patch7:         0008-libglvnd.patch

Patch10:        0001-Execute-usr-libexec-Xorg.wrap-instead-of-Xorg.patch
Patch11:        0002-xorg.conf.nvidia-Treat-ABI-mismatch-as-warning.patch
Patch12:        0003-bumblebee-bugreport-Add-support-for-Fedora.patch
Patch13:        0001-Add-option-to-always-unload-the-driver-on-exit.patch

BuildRequires:  gcc
BuildRequires:  help2man
BuildRequires:  systemd

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(x11)

Requires:       VirtualGL
Requires(pre):  shadow-utils

Requires:       %{name}-selinux = %{version}-%{release}

Recommends:     bbswitch-kmod
Recommends:     primus

%{?systemd_requires}

%description
Bumblebee daemon is a rewrite of the original Bumblebee service,
providing an elegant and stable means of managing Optimus hybrid
graphics chipsets. A primary goal of this project is to not only enable
use of the discrete GPU for rendering, but also to enable smart power
management of the dGPU when it's not in use.


%package selinux
Summary:        SELinux policies for bumblebee

BuildRequires:  selinux-policy-devel

Requires(post): libselinux-utils
Requires(post): policycoreutils
Requires(post): policycoreutils-python-utils
Requires(post): selinux-policy-base >= %{_selinux_policy_version}

BuildArch:      noarch

%description selinux
SELinux policy module for use with bumblebee.


%prep
%autosetup -p1


%build
# Despite what configure.ac says, omitting CONF_DRIVER_MODULE_NVIDIA is not the
# same as setting it to 'nvidia'. It needs to be set in order for the
# proprietary driver to have a higher priority than nouveau. See src/driver.c
# for the driver handling logic.
%configure \
    CONF_PRIMUS_LD_PATH=%{_prefix}/lib64/primus:%{_prefix}/lib/primus \
    CONF_LDPATH_NVIDIA=%{_prefix}/lib64:%{_prefix}/lib \
    CONF_MODPATH_NVIDIA=%{_libdir}/nvidia/xorg,%{_libdir}/xorg/modules \
    CONF_DRIVER_MODULE_NVIDIA=nvidia \
    --with-udev-rules=%{_udevrulesdir} \
    --without-pidfile
%make_build

# Build SELinux module
cp %{SOURCE2} .
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp


%install
%make_install \
    completiondir=%{_datadir}/bash-completion/completions

# Install systemd unit
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 scripts/systemd/bumblebeed.service \
    %{buildroot}%{_unitdir}/

# Install modprobe blacklist
install -d -m 0755 %{buildroot}%{_prefix}/lib/modprobe.d
install -m 0644 %{SOURCE1} \
    %{buildroot}%{_prefix}/lib/modprobe.d/bumblebee.conf

# Fix bash-completion name
mv %{buildroot}%{_datadir}/bash-completion/completions/{bumblebee,optirun}

# Install SELinux module
install -d -p %{buildroot}%{_datadir}/selinux/packages
install -p -m 0644 %{modulename}.pp.bz2 \
    %{buildroot}%{_datadir}/selinux/packages/


%pre
getent group bumblebee >/dev/null || groupadd -r bumblebee


%post
%systemd_post bumblebeed.service


%preun
%systemd_preun bumblebeed.service


%postun
# Don't restart the daemon since the discrete GPU might be in use
%systemd_postun bumblebeed.service


%post selinux
%selinux_modules_install %{_datadir}/selinux/packages/%{modulename}.pp.bz2


%postun selinux
if [ "${1}" -eq 0 ]; then
    %selinux_modules_uninstall %{modulename}
fi


%files
%doc %{_docdir}/%{name}/
%license COPYING
%dir %{_sysconfdir}/bumblebee/
%dir %{_sysconfdir}/bumblebee/xorg.conf.d/
%config(noreplace) %{_sysconfdir}/bumblebee/bumblebee.conf
%config(noreplace) %{_sysconfdir}/bumblebee/xorg.conf.d/10-dummy.conf
%config(noreplace) %{_sysconfdir}/bumblebee/xorg.conf.nouveau
%config(noreplace) %{_sysconfdir}/bumblebee/xorg.conf.nvidia
%{_bindir}/bumblebee-bugreport
%{_bindir}/optirun
%{_sbindir}/bumblebeed
%{_prefix}/lib/modprobe.d/bumblebee.conf
%{_unitdir}/bumblebeed.service
%{_udevrulesdir}/99-bumblebee-nvidia-dev.rules
%{_datadir}/bash-completion/completions/optirun
%{_mandir}/man1/bumblebeed.1*
%{_mandir}/man1/optirun.1*


%files selinux
%{_datadir}/selinux/packages/%{modulename}.pp.bz2


%changelog
* Sun Aug 04 2019 Andrew Gunnerson <andrewgunnerson@gmail.com> - 3.2.1-4
- Add gcc to build dependencies

* Sat Aug 03 2019 Elia Geretto <elia.f.geretto@gmail.com> - 3.2.1-3
- Add support for AlwaysUnloadKernelDriver

* Mon Dec 25 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 3.2.1-2
- Add -selinux subpackage that allows bumblebeed to write to /proc/acpi/bbswitch

* Mon Dec 25 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 3.2.1-1
- Initial release
- Based on Arch Linux package
