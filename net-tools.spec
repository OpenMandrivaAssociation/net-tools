%define date 20160912
%ifarch %{ix86}
%define _disable_lto 1
%endif

Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	2.10
Release:	1
License:	GPLv2
Group:		System/Configuration/Networking
Url:		http://net-tools.sourceforge.net
# (tpg) https://github.com/ecki/net-tools
#git archive --format=tar --remote=git://git.code.sf.net/p/net-tools/code master | xz > net-tools-2.0-$(date +%Y%m%d).tar.xz
Source0:	https://github.com/ecki/net-tools/archive/%{name}-%{version}.tar.gz
Source1:	net-tools-config.h
Source2:	net-tools-config.make
Source3:	ether-wake.c
Source4:	ether-wake.8
Source5:	mii-diag.c
Source6:	mii-diag.8
Source7:	iptunnel.8
Source8:	ipmaddr.8
Source9:	arp-ethers.service

# adds <delay> option that allows netstat to cycle printing through statistics every delay seconds.
Patch1: net-tools-cycle.patch
# various man page fixes merged into one patch
Patch2: net-tools-man.patch
# linux-4.8
Patch3: net-tools-linux48.patch
# use all interfaces instead of default (#1003875)
Patch20: ether-wake-interfaces.patch
# use all interfaces instead of default (#1003875)
Patch21: net-tools-ifconfig-EiB.patch
Patch22: net-tools-timer-man.patch
Patch23: net-tools-interface-name-len.patch
Patch24: net-tools-covscan.patch

BuildRequires:	gettext
BuildRequires:	pkgconfig(bluez)
BuildRequires:	kernel-headers
BuildRequires:	pkgconfig(libselinux)

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -q -c %{name}-%{version}-%{date}

cp %{SOURCE1} ./config.h
cp %{SOURCE2} ./config.make
cp %{SOURCE3} .
cp %{SOURCE4} ./man/en_US
cp %{SOURCE5} .
cp %{SOURCE6} ./man/en_US
cp %{SOURCE7} ./man/en_US
cp %{SOURCE8} ./man/en_US

%autopatch -p1

touch ./config.h

%build
%serverbuild_hardened
%set_cbuild_flags
%make_build CC=%{__cc}
%make_build CC=%{__cc} ether-wake
%{__cc} %{optflags} -pie %{ldflags} -fPIE -o mii-diag mii-diag.c

%install
mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt

make BASEDIR=%{buildroot} BINDIR="/bin" SBINDIR="/sbin" install

# ifconfig and route are installed into /bin by default
# mv them back to /sbin for now as I (jpopelka) don't think customers would be happy
mv %{buildroot}/bin/ifconfig %{buildroot}/sbin
mv %{buildroot}/bin/route %{buildroot}/sbin

install -m 755 ether-wake %{buildroot}/sbin
install -m 755 mii-diag %{buildroot}/sbin

rm %{buildroot}/sbin/rarp
rm %{buildroot}%{_mandir}/man8/rarp.8*
rm %{buildroot}%{_mandir}/de/man8/rarp.8*
rm %{buildroot}%{_mandir}/fr/man8/rarp.8*
rm %{buildroot}%{_mandir}/pt/man8/rarp.8*

# otherwise %%find_lang finds them even they're empty
rm -rf %{buildroot}%{_mandir}/de/man1
rm -rf %{buildroot}%{_mandir}/fr/man1
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_mandir}/pt/man1
rm -rf %{buildroot}%{_mandir}/pt/man5

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE9} %{buildroot}%{_unitdir}

%find_lang %{name} --all-name --with-man

%post
%systemd_post arp-ethers.service

%preun
%systemd_preun arp-ethers.service

%postun
%systemd_postun arp-ethers.service

%files -f %{name}.lang
%doc COPYING
%{_unitdir}/arp-ethers.service
/bin/*
/sbin/*
%{_mandir}/man[58]/*
