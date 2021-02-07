Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	2.10
Release:	1
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
%serverbuild_hardened
%set_build_flags
%make_build CC=%{__cc}

%install
%make_install BINDIR=%{_bindir} SBINDIR=%{_sbindir}

# Fix manpage locations
mv %{buildroot}%{_mandir}/de_DE %{buildroot}%{_mandir}/de
mv %{buildroot}%{_mandir}/fr_FR %{buildroot}%{_mandir}/fr
# Generate missing manpages
for tool in iptunnel ipmaddr; do
    t="%{buildroot}/%{_mandir}/man8/${tool}.8"
    help2man -s8 "%{buildroot}%{_sbindir}/${tool}" --no-discard-stderr >"${t}"
done

# (tpg) provide compat symlinks
mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}/bin
for i in ether-wake nameif plipconfig slattach arp ipmaddr iptunnel; do
    ln -sf %{_sbindir}/$i %{buildroot}/sbin/$i
done
for i in netstat ifconfig route; do
    ln -sf %{_bindir}/$i %{buildroot}/bin/$i
done

%find_lang %{name} --all-name

%files -f %{name}.lang
%doc COPYING
/bin/*
/sbin/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man[58]/*
%{_mandir}/*/man[58]/*
