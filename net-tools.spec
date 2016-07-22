%define date 20160722

Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	2.0
Release:	1.%{date}.2
License:	GPLv2
Group:		System/Configuration/Networking
Url:		http://net-tools.sourceforge.net
# (tpg) https://github.com/ecki/net-tools
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
Patch0:		net-tools-cycle.patch
# various man page fixes merged into one patch
Patch1:		net-tools-man.patch
# use all interfaces instead of default (#1003875)
Patch2:		ether-wake-interfaces.patch

BuildRequires:	gettext
BuildRequires:	systemd
BuildRequires:	pkgconfig(bluez)
BuildRequires:	kernel-headers

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -qn %{name}-%{version}-%{date}

cp %{SOURCE1} ./config.h
cp %{SOURCE2} ./config.make
cp %{SOURCE3} .
cp %{SOURCE4} ./man/en_US
cp %{SOURCE5} .
cp %{SOURCE6} ./man/en_US
cp %{SOURCE7} ./man/en_US
cp %{SOURCE8} ./man/en_US

%apply_patches

touch ./config.h

%build
%serverbuild_hardened
%setup_compile_flags
%make CC=%{__cc}
%make CC=%{__cc} ether-wake
%{__cc} %{optflags} %{ldflags} -o mii-diag mii-diag.c

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
mkdir -p %{buildroot}%{_systemunitdir}
install -m 644 %{SOURCE9} %{buildroot}%{_systemunitdir}

%find_lang %{name} --all-name --with-man

%files -f %{name}.lang
%doc COPYING
%{_systemunitdir}/arp-ethers.service
/bin/*
/sbin/*
%{_mandir}/man[58]/*
