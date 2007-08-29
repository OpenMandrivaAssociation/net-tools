Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	1.60
Release:	%mkrel 20
License:	GPL
Group:		System/Configuration/Networking
URL:		http://www.tazenda.demon.co.uk/phil/net-tools/
Source0:	http://www.tazenda.demon.co.uk/phil/net-tools/net-tools-%{version}.tar.bz2
Source2:	net-tools-%{version}-config.h
Source3:	net-tools-%{version}-config.make
Source4:	ether-wake.c
Source5:	ether-wake.8
Source6:	mii-diag.c
Source7:	mii-diag.8
Source8:	%{name}.bash-completion
Patch1:		net-tools-1.57-bug22040.patch
Patch2:		net-tools-1.60-miiioctl.patch
Patch3:		net-tools-1.60-manydevs.patch
Patch4:		net-tools-1.60-virtualname.patch
Patch5:		net-tools-1.60-cycle.patch
Patch6:		net-tools-1.60-nameif.patch
Patch7:		net-tools-1.60-ipx.patch
Patch8:		net-tools-1.60-inet6-lookup.patch
Patch9:		net-tools-1.60-man.patch
Patch10:	net-tools-1.60-gcc33.patch
Patch11:	net-tools-1.60-trailingblank.patch
Patch12:	net-tools-1.60-interface.patch
Patch13:	net-tools-1.60-x25.patch
Patch14:	net-tools-1.60-gcc34.patch
Patch15:	net-tools-1.60-overflow.patch
Patch19:	net-tools-1.60-siunits.patch
Patch20:	net-tools-1.60-trunc.patch
Patch21:	net-tools-1.60-return.patch
Patch22:	net-tools-1.60-parse.patch
Patch23:	net-tools-1.60-netmask.patch
Patch24:	net-tools-1.60-ulong.patch
Patch25:	net-tools-1.60-bcast.patch
Patch26:	net-tools-1.60-mii-tool-obsolete.patch
Patch27:	net-tools-1.60-netstat_ulong.patch
Patch28:	net-tools-1.60-note.patch
Patch29:	net-tools-1.60-num-ports.patch
Patch30:	net-tools-1.60-duplicate-tcp.patch
Patch31:	net-tools-1.60-statalias.patch
Patch32:	net-tools-1.60-isofix.patch
Patch34:	net-tools-1.60-ifconfig_ib.patch
Patch35:	net-tools-1.60-de.patch
Patch37:	net-tools-1.60-pie.patch
Patch38:	net-tools-1.60-ifaceopt.patch
Patch39:	net-tools-1.60-trim_iface.patch
Patch40:	net-tools-1.60-stdo.patch
Patch41:	net-tools-1.60-statistics.patch
Patch42:	net-tools-1.60-netdevice.patch
BuildRequires:	gettext
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep

%setup -q
%patch1 -p1 -b .bug22040
%patch2 -p1 -b .miiioctl
%patch3 -p0 -b .manydevs
%patch4 -p1 -b .virtualname
%patch5 -p1 -b .cycle
%patch6 -p1 -b .nameif
%patch7 -p1 -b .ipx
%patch8 -p1 -b .inet6-lookup
%patch9 -p1 -b .man
%patch10 -p1 -b .gcc33
%patch11 -p1 -b .trailingblank
%patch12 -p1 -b .interface
%patch13 -p1 -b .x25
%patch14 -p1 -b .gcc34
%patch15 -p1 -b .overflow
%patch19 -p1 -b .siunits
%patch20 -p1 -b .trunc
%patch21 -p1 -b .return
%patch22 -p1 -b .parse
%patch23 -p1 -b .netmask
%patch24 -p1 -b .ulong
%patch25 -p1 -b .bcast
%patch26 -p1 -b .obsolete
%patch27 -p1 -b .netstat_ulong
%patch28 -p1 -b .note
%patch29 -p1 -b .num-ports
%patch30 -p1 -b .dup-tcp
%patch31 -p1 -b .statalias
%patch32 -p1 -b .isofix
%patch34 -p1 -b .ifconfig_ib
%patch35 -p1 
%patch37 -p1 -b .pie
%patch38 -p1 -b .ifaceopt
%patch39 -p1 -b .trim-iface
%patch40 -p1 -b .stdo
%patch41 -p1 -b .statistics
%patch42 -p1 -b .netdevice

cp %{SOURCE2} config.h
cp %{SOURCE3} config.make
cp %{SOURCE4} ether-wake.c
cp %{SOURCE5} man/en_US/ether-wake.8
cp %{SOURCE6} mii-diag.c
cp %{SOURCE7} man/en_US/mii-diag.8

%ifarch alpha
perl -pi -e "s|-O2||" Makefile
%endif

%build
export CFLAGS="%{optflags} $CFLAGS"

make
gcc %{optflags} -o ether-wake ether-wake.c
gcc %{optflags} -o mii-diag mii-diag.c

#man pages conversion
#french 
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/fr_FR/arp.8 && mv arp.tmp man/fr_FR/arp.8
iconv -f iso-8859-1 -t utf-8 -o ethers.tmp man/fr_FR/ethers.5 && mv ethers.tmp man/fr_FR/ethers.5
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/fr_FR/hostname.1 && mv hostname.tmp man/fr_FR/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/fr_FR/ifconfig.8 && mv ifconfig.tmp man/fr_FR/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/fr_FR/netstat.8 && mv netstat.tmp man/fr_FR/netstat.8
iconv -f iso-8859-1 -t utf-8 -o plipconfig.tmp man/fr_FR/plipconfig.8 && mv plipconfig.tmp man/fr_FR/plipconfig.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/fr_FR/route.8 && mv route.tmp man/fr_FR/route.8
iconv -f iso-8859-1 -t utf-8 -o slattach.tmp man/fr_FR/slattach.8 && mv slattach.tmp man/fr_FR/slattach.8
#portugal
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/pt_BR/arp.8 && mv arp.tmp man/pt_BR/arp.8
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/pt_BR/hostname.1 && mv hostname.tmp man/pt_BR/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/pt_BR/ifconfig.8 && mv ifconfig.tmp man/pt_BR/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/pt_BR/netstat.8 && mv netstat.tmp man/pt_BR/netstat.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/pt_BR/route.8 && mv route.tmp man/pt_BR/route.8
#german
iconv -f iso-8859-1 -t utf-8 -o arp.tmp man/de_DE/arp.8 && mv arp.tmp man/de_DE/arp.8
iconv -f iso-8859-1 -t utf-8 -o ethers.tmp man/de_DE/ethers.5 && mv ethers.tmp man/de_DE/ethers.5
iconv -f iso-8859-1 -t utf-8 -o hostname.tmp man/de_DE/hostname.1 && mv hostname.tmp man/de_DE/hostname.1
iconv -f iso-8859-1 -t utf-8 -o ifconfig.tmp man/de_DE/ifconfig.8 && mv ifconfig.tmp man/de_DE/ifconfig.8
iconv -f iso-8859-1 -t utf-8 -o netstat.tmp man/de_DE/netstat.8 && mv netstat.tmp man/de_DE/netstat.8
iconv -f iso-8859-1 -t utf-8 -o plipconfig.tmp man/de_DE/plipconfig.8 && mv plipconfig.tmp man/de_DE/plipconfig.8
iconv -f iso-8859-1 -t utf-8 -o route.tmp man/de_DE/route.8 && mv route.tmp man/de_DE/route.8
iconv -f iso-8859-1 -t utf-8 -o slattach.tmp man/de_DE/slattach.8 && mv slattach.tmp man/de_DE/slattach.8

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt

make BASEDIR=%{buildroot} mandir=%{_mandir} install

install -m 755 ether-wake %{buildroot}/sbin
install -m 755 mii-diag %{buildroot}/sbin

rm %{buildroot}/sbin/rarp
rm %{buildroot}%{_mandir}/man8/rarp.8*
rm %{buildroot}%{_mandir}/*/man8/rarp.8*

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%find_lang %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README README.ipv6 TODO INSTALLING ABOUT-NLS
%{_sysconfdir}/bash_completion.d/%{name}
/bin/*
/sbin/*
%{_mandir}/man[158]/*
%lang(de) %{_mandir}/de/man[158]/*
%lang(fr) %{_mandir}/fr/man[158]/*
%lang(pt) %{_mandir}/pt/man[158]/*
