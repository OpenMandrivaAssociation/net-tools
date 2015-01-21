%define git 20120702git

Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	1.60
# Don't increase 37 here
Release:	38.%{git}.4
License:	GPLv2
Group:		System/Configuration/Networking
Url:		http://net-tools.sourceforge.net
# git archive --format=tar --remote=git://net-tools.git.sourceforge.net/gitroot/net-tools/net-tools master | xz > net-tools-%%{version}.%%{checkout}.tar.xz
Source0:	net-tools-%{version}.%{git}.tar.xz
Source2:	net-tools-%{version}-config.h
Source3:	net-tools-%{version}-config.make
Source4:	ether-wake.c
Source5:	ether-wake.8
Source6:	mii-diag.c
Source7:	mii-diag.8
Source8:	iptunnel.8
Source9:	ipmaddr.8
Source10:	arp-ethers.service
# adds <delay> option that allows netstat to cycle printing through statistics every delay seconds.
Patch1:		net-tools-1.60-cycle.patch
# Fixed incorrect address display for ipx (#46434)
Patch2:		net-tools-1.60-ipx.patch
# hostname lookup problems with route --inet6 (#84108)
Patch3:		net-tools-1.60-inet6-lookup.patch
# various man page fixes merged into one patch
Patch4:		net-tools-1.60-man.patch
# netstat: interface option now works as described in the man page (#61113, #115987)
Patch5:		net-tools-1.60-interface.patch
# filter out duplicate tcp entries (#139407)
Patch6:		net-tools-1.60-duplicate-tcp.patch
# don't report statistics for virtual devices (#143981)
Patch7:		net-tools-1.60-statalias.patch
# clear static buffers in interface.c by Ulrich Drepper (#176714)
Patch8:		net-tools-1.60-interface_stack.patch
# statistics for SCTP
Patch9:		net-tools-1.60-sctp-statistics.patch
# ifconfig crash when interface name is too long (#190703)
Patch10:	net-tools-1.60-ifconfig-long-iface-crasher.patch
# fixed tcp timers info in netstat (#466845)
Patch11:	net-tools-1.60-netstat-probe.patch
# kernel 3.6 removes linux/if_strip.h
Patch12:	net-tools-1.60-STRIP.patch
BuildRequires:	gettext
BuildRequires: systemd-units

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -q -c
%apply_patches

cp %{SOURCE2} ./config.h
cp %{SOURCE3} ./config.make
cp %{SOURCE4} ./ether-wake.c
cp %{SOURCE5} ./man/en_US/ether-wake.8
cp %{SOURCE6} ./mii-diag.c
cp %{SOURCE7} ./man/en_US/mii-diag.8
cp %{SOURCE8} ./man/en_US/iptunnel.8
cp %{SOURCE9} ./man/en_US/ipmaddr.8

%build
%setup_compile_flags
make CC=%{__cc}

%{__cc} %{optflags} %{ldflags} -o ether-wake ether-wake.c
%{__cc} %{optflags} %{ldflags} -o mii-diag mii-diag.c

%install
mv man/de_DE man/de
mv man/fr_FR man/fr
mv man/pt_BR man/pt

make BASEDIR=%{buildroot} mandir=%{_mandir} install

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

rm -rf %{buildroot}%{_mandir}/de/man1
rm -rf %{buildroot}%{_mandir}/fr/man1
rm -rf %{buildroot}%{_mandir}/man1
rm -rf %{buildroot}%{_mandir}/pt/man1

# install systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE10} %{buildroot}%{_unitdir}

%find_lang %{name} --all-name --with-man


%files -f %{name}.lang
%doc COPYING
%config(noreplace) %{_unitdir}/arp-ethers.service
/bin/*
/sbin/*
%{_mandir}/man[58]/*

