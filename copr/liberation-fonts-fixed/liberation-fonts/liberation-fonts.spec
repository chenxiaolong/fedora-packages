%global priority 59
%global fontname liberation
%global fontconf %{priority}-%{fontname}
%global archivename %{name}-%{version}
%global common_desc \
The Liberation Fonts are intended to be replacements for the three most \
commonly used fonts on Microsoft systems: Times New Roman, Arial, and Courier \
New. \
\
This package contains a fixed version of the font that renders correctly in \
Chromium-based applications.

%define catalogue %{_sysconfdir}/X11/fontpath.d

Name:             %{fontname}-fonts
Summary:          Fonts to replace commonly used Microsoft Windows fonts
Version:          1.07.4
Release:          8.1%{?dist}
Epoch:            1
# The license of the Liberation Fonts is a EULA that contains GPLv2 and two
# exceptions:
# The first exception is the standard FSF font exception.
# The second exception is an anti-lockdown clause somewhat like the one in
# GPLv3. This license is Free, but GPLv2 and GPLv3 incompatible.
License:          Liberation
URL:              https://pagure.io/liberation-fonts
Source0:          https://releases.pagure.org/liberation-fonts/%{archivename}.tar.gz
Source2:          %{name}-mono.conf
Source3:          %{name}-sans.conf
Source4:          %{name}-serif.conf
Source5:          %{name}-narrow.conf
Source6:          %{fontname}.metainfo.xml
Source7:          %{fontname}-mono.metainfo.xml
Source8:          %{fontname}-sans.metainfo.xml
Source9:          %{fontname}-serif.metainfo.xml
Source10:         %{fontname}-narrow.metainfo.xml
BuildArch:        noarch

BuildRequires:    fontpackages-devel >= 1.13, xorg-x11-font-utils
BuildRequires:    fontforge-liberation

Requires:         %{fontname}-mono-fonts = %{epoch}:%{version}-%{release}
Requires:         %{fontname}-narrow-fonts = %{epoch}:%{version}-%{release}
Requires:         %{fontname}-sans-fonts = %{epoch}:%{version}-%{release}
Requires:         %{fontname}-serif-fonts = %{epoch}:%{version}-%{release}

%description
%common_desc

Meta-package of Liberation fonts which installs Sans, Serif, and Monospace,
Narrow families.

%package -n %{fontname}-fonts-common
Summary:          Shared common files of Liberation font families
Requires:         fontpackages-filesystem >= 1.13

%description -n %{fontname}-fonts-common
%common_desc

Shared common files of Liberation font families.

%files -n %{fontname}-fonts-common
%doc AUTHORS ChangeLog COPYING License.txt README TODO
%dir %{_fontdir}
%verify(not md5 size mtime) %{_fontdir}/fonts.dir
%verify(not md5 size mtime) %{_fontdir}/fonts.scale
%{catalogue}/%{name}
%{_datadir}/appdata/%{fontname}.metainfo.xml

%package -n %{fontname}-sans-fonts
Summary:      Sans-serif fonts to replace commonly used Microsoft Arial
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-sans-fonts
%common_desc

This is Sans-serif TrueType fonts that replaced commonly used Microsoft Arial.

%_font_pkg -n sans -f *-%{fontname}-sans*.conf LiberationSans-*.ttf
%{_datadir}/appdata/%{fontname}-sans.metainfo.xml

%package -n %{fontname}-serif-fonts
Summary:      Serif fonts to replace commonly used Microsoft Times New Roman
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-serif-fonts
%common_desc

This is Serif TrueType fonts that replaced commonly used Microsoft Times New \
Roman.

%_font_pkg -n serif -f *-%{fontname}-serif*.conf LiberationSerif*.ttf
%{_datadir}/appdata/%{fontname}-serif.metainfo.xml

%package -n %{fontname}-mono-fonts
Summary:      Monospace fonts to replace commonly used Microsoft Courier New
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-mono-fonts
%common_desc

This is Monospace TrueType fonts that replaced commonly used Microsoft Courier \
New.

%_font_pkg -n mono -f *-%{fontname}-mono*.conf LiberationMono*.ttf
%{_datadir}/appdata/%{fontname}-mono.metainfo.xml

%package -n %{fontname}-narrow-fonts
Summary:      Sans-serif Narrow fonts to replace commonly used Microsoft Arial Narrow
Requires:     %{fontname}-fonts-common = %{epoch}:%{version}-%{release}

%description -n %{fontname}-narrow-fonts
%common_desc

This is Sans-Serif Narrow TrueType fonts that replaced commonly used Microsoft \
Arial Narrow.

%_font_pkg -n narrow -f *-%{fontname}-narrow*.conf LiberationSansNarrow*.ttf
%{_datadir}/appdata/%{fontname}-narrow.metainfo.xml

%prep
%autosetup -n %{archivename}

%build
%make_build \
    FONTFORGE=fontforge-liberation \
    FONTLINT=fontlint-liberation
mv liberation-fonts-ttf-%{version}/* .


%install
# fonts .ttf
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}
# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
ln -s %{_fontdir} %{buildroot}%{catalogue}/%{name}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

# Repeat for every font family
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf
install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf
install -m 0644 -p %{SOURCE5} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-narrow.conf

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE6} \
        %{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml
install -Dm 0644 -p %{SOURCE7} \
        %{buildroot}%{_datadir}/appdata/%{fontname}-mono.metainfo.xml
install -Dm 0644 -p %{SOURCE8} \
        %{buildroot}%{_datadir}/appdata/%{fontname}-sans.metainfo.xml
install -Dm 0644 -p %{SOURCE9} \
        %{buildroot}%{_datadir}/appdata/%{fontname}-serif.metainfo.xml
install -Dm 0644 -p %{SOURCE10} \
        %{buildroot}%{_datadir}/appdata/%{fontname}-narrow.metainfo.xml

for fconf in %{fontconf}-mono.conf \
             %{fontconf}-sans.conf \
             %{fontconf}-serif.conf \
             %{fontconf}-narrow.conf; do
  ln -s %{_fontconfig_templatedir}/$fconf \
        %{buildroot}%{_fontconfig_confdir}/$fconf
done

# fonts.{dir,scale}
mkfontscale %{buildroot}%{_fontdir}
mkfontdir %{buildroot}%{_fontdir}

%files

%changelog
* Mon Mar 20 2017 Andrew Gunnerson <andrewgunnerson@gmail.com> - 1:1.07.4-8.1
- Based on Fedora rawhide package
- Fixed URL and source link
- Removed group
- Built with fontforge-liberation to avoid rendering issues in Chromium
