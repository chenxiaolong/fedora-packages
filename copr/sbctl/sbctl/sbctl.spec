# NOTE: This does not follow Fedora's golang packaging guidelines and downloads
#       golang dependencies from the internet during the build.

Name:           sbctl
Version:        0.12
Release:        2%{?dist}
Summary:        Secure Boot key manager

License:        MIT
URL:            https://github.com/Foxboron/sbctl
Source0:        https://github.com/Foxboron/sbctl/releases/download/%{version}/sbctl-%{version}.tar.gz

ExclusiveArch:  %{golang_arches}

Requires:       binutils
Requires:       util-linux

Recommends:     systemd-udev

BuildRequires:  asciidoc
BuildRequires:  git
BuildRequires:  go-rpm-macros

%description
sbctl intends to be a user-friendly secure boot key manager capable of setting
up secure boot, offer key management capabilities, and keep track of files that
needs to be signed in the boot chain.


%prep
%setup -q
sed -i '/go build/d' Makefile


%build
export GOPATH=%{_builddir}/go
%global gomodulesmode GO111MODULE=on
%gobuild -o sbctl ./cmd/sbctl
%make_build


%install
%make_install PREFIX=%{_prefix}


%transfiletriggerin -P 1 -- /boot /efi /usr/lib /usr/libexec
if grep -q -m 1 -e '\.efi$' -e '/vmlinuz$'; then
    exec </dev/null
    %{_bindir}/sbctl sign-all -g
fi


%files
%license LICENSE
%doc README.md
%{_bindir}/sbctl
%{_prefix}/lib/kernel/install.d/91-sbctl.install
%{_mandir}/man8/sbctl.8*
%{_datadir}/bash-completion/completions/sbctl
%{_datadir}/fish/vendor_completions.d/sbctl.fish
%{_datadir}/zsh/site-functions/_sbctl


%changelog
* Sun Nov 12 2023 Andrew Gunnerson <accounts+fedora@chiller3.com> - 0.12-2
- Switch to upstream 91-sbctl.install kernel-install script

* Fri Oct 20 2023 Andrew Gunnerson <accounts+fedora@chiller3.com> - 0.12-1
- Update to version 0.12

* Sat Mar 25 2023 Andrew Gunnerson <accounts+fedora@chiller3.com> - 0.11-1
- Update to version 0.11

* Mon Dec 12 2022 Andrew Gunnerson <accounts+fedora@chiller3.com> - 0.10-1
- Update to version 0.10

* Tue May 3 2022 Andrew Gunnerson <chillermillerlong@hotmail.com> - 0.9-1
- Update to version 0.9

* Thu Jan 27 2022 Andrew Gunnerson <chillermillerlong@hotmail.com> - 0.8-1
- Initial release
