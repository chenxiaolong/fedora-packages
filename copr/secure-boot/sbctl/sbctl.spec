# NOTE: This does not follow Fedora's golang packaging guidelines and downloads
#       golang dependencies from the internet during the build.

Name:           sbctl
Version:        0.8
Release:        1%{?dist}
Summary:        Secure Boot key manager

License:        MIT
URL:            https://github.com/Foxboron/sbctl
Source0:        https://github.com/Foxboron/sbctl/releases/download/%{version}/sbctl-%{version}.tar.gz
Source1:        91-sbctl.install

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
cp %{SOURCE1} contrib/kernel-install/91-sbctl.install


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
* Thu Jan 27 2022 Andrew Gunnerson <chillermillerlong@hotmail.com> - 0.8-1
- Initial release
