%define date 20150915

Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	2.0
Release:	1.%{date}.1
License:	GPLv2
Group:		System/Configuration/Networking
Url:		http://net-tools.sourceforge.net
#git archive --format=tar --remote=git://git.code.sf.net/p/net-tools/code master | xz > net-tools-2.0-$(date +%Y%m%d).tar.xz
Source0:	net-tools-%{version}-%{date}.tar.xz
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
Patch1:		net-tools-cycle.patch
# various man page fixes merged into one patch
Patch4:		net-tools-man.patch
# netstat: interface option now works as described in the man page (#61113, #115987)
Patch5:		net-tools-interface.patch
# filter out duplicate tcp entries (#139407)
Patch6:		net-tools-duplicate-tcp.patch
# don't report statistics for virtual devices (#143981)
Patch7:		net-tools-statalias.patch
# clear static buffers in interface.c by Ulrich Drepper (#176714)
Patch8:		net-tools-interface_stack.patch
# ifconfig crash when interface name is too long (#190703)
Patch10:	net-tools-ifconfig-long-iface-crasher.patch
# use all interfaces instead of default (#1003875)
Patch20:	ether-wake-interfaces.patch

BuildRequires:	gettext
BuildRequires:	systemd
BuildRequires:	pkgconfig(bluez)

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -q -c
#apply_patches
%patch1 -p1 -b .cycle
%patch2 -p1 -b .man
%patch3 -p1 -b .interface
%patch4 -p1 -b .dup-tcp
%patch5 -p1 -b .statalias
%patch6 -p1 -b .stack
%patch7 -p1 -b .long_iface

cp %{SOURCE1} ./config.h
cp %{SOURCE2} ./config.make
cp %{SOURCE3} .
cp %{SOURCE4} ./man/en_US
cp %{SOURCE5} .
cp %{SOURCE6} ./man/en_US
cp %{SOURCE7} ./man/en_US
cp %{SOURCE8} ./man/en_US

%patch20 -p1 -b .interfaces

touch ./config.h

%build
%setup_compile_flags
make CC=%{__cc}

%{__cc} %{optflags} %{ldflags} -o ether-wake ether-wake.c
%{__cc} %{optflags} %{ldflags} -o mii-diag mii-diag.c

%install
mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt

make BASEDIR=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} install

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

# remove hostname (has its own package)
rm %{buildroot}%{_bindir}/dnsdomainname
rm %{buildroot}%{_bindir}/domainname
rm %{buildroot}%{_bindir}/hostname
rm %{buildroot}%{_bindir}/nisdomainname
rm %{buildroot}%{_bindir}/ypdomainname
rm -rf %{buildroot}%{_mandir}/de/man1
rm -rf %{buildroot}%{_mandir}/fr/man1
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_mandir}/pt/man1

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE9} %{buildroot}%{_unitdir}

%find_lang %{name} --all-name --with-man

%files -f %{name}.lang
%doc COPYING
%config(noreplace) %{_unitdir}/arp-ethers.service
/bin/*
/sbin/*
%{_mandir}/man[58]/*
