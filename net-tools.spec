Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	2.10
Release:	4
License:	GPLv2
Group:		System/Configuration/Networking
Url:		https://github.com/ecki/net-tools
Source0:	https://github.com/ecki/net-tools/archive/%{name}-%{version}.tar.gz
Source1:	net-tools-config.h
Source2:	net-tools-config.make

# (tpg) patches from openSuse
Patch1:		0001-Add-ether-wake-binary.patch
Patch2:		0002-Do-not-warn-about-interface-socket-not-binded.patch
Patch4:		0004-By-default-do-not-fopen-anything-in-netrom_gr.patch
Patch6:		0006-Allow-interface-stacking.patch

BuildRequires:	gettext
BuildRequires:	pkgconfig(bluez)
BuildRequires:	kernel-release-headers
BuildRequires:	pkgconfig(libselinux)
BuildRequires:	help2man
Requires:	hostname
Recommends:	traceroute

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%autosetup -p1

cp %{SOURCE1} ./config.h
cp %{SOURCE2} ./config.make

%build
%set_build_flags
%make_build CC=%{__cc}

%install
%make_install BINDIR=%{_bindir} SBINDIR=%{_bindir}

# Fix manpage locations
mv %{buildroot}%{_mandir}/de_DE %{buildroot}%{_mandir}/de
mv %{buildroot}%{_mandir}/fr_FR %{buildroot}%{_mandir}/fr
# Generate missing manpages
for tool in iptunnel ipmaddr; do
    t="%{buildroot}/%{_mandir}/man8/${tool}.8"
    help2man -s8 "%{buildroot}%{_sbindir}/${tool}" --no-discard-stderr >"${t}"
done

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc COPYING
%{_bindir}/*
%doc %{_mandir}/man[58]/*
%doc %{_mandir}/*/man[58]/*
