%define git 20120702git

Summary:	The basic tools for setting up networking
Name:		net-tools
Version:	1.60
# Don't increase 37 here
Release:	37.%{git}.1
License:	GPL
Group:		System/Configuration/Networking
URL:		http://net-tools.sourceforge.net
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
Patch100:	net-tools-1.60-format_not_a_string_literal_and_no_format_arguments.diff
BuildRequires:	gettext

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -q -c
%patch1 -p1 -b .cycle
%patch2 -p1 -b .ipx
%patch3 -p1 -b .inet6-lookup
%patch4 -p1 -b .man
%patch5 -p1 -b .interface
%patch6 -p1 -b .dup-tcp
%patch7 -p1 -b .statalias
%patch8 -p1 -b .stack
%patch9 -p1 -b .sctp
%patch10 -p1 -b .long_iface
%patch11 -p1 -b .probe
%patch12 -p1 -b .STRIP

cp %{SOURCE2} ./config.h
cp %{SOURCE3} ./config.make
cp %{SOURCE4} ./ether-wake.c
cp %{SOURCE5} ./man/en_US/ether-wake.8
cp %{SOURCE6} ./mii-diag.c
cp %{SOURCE7} ./man/en_US/mii-diag.8
cp %{SOURCE8} ./man/en_US/iptunnel.8
cp %{SOURCE9} ./man/en_US/ipmaddr.8

%patch100 -p1 -b .format_not_a_string_literal_and_no_format_arguments

%build
export CFLAGS="%{optflags} $CFLAGS"
export LDFLAGS="%{ldflags} $LDFLAGS"

make

gcc %{optflags} %{ldflags} -o ether-wake ether-wake.c
gcc %{optflags} %{ldflags} -o mii-diag mii-diag.c

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

%post
%systemd_post arp-ethers.service

%files -f %{name}.lang
%doc COPYING
%config(noreplace) %{_unitdir}/arp-ethers.service
/bin/*
/sbin/*
%{_mandir}/man[58]/*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.60-34mdv2011.0
+ Revision: 666607
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.60-33mdv2011.0
+ Revision: 606818
- rebuild

* Sat Dec 12 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.60-32mdv2010.1
+ Revision: 477635
- sync patch set with fedora

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.60-31mdv2010.0
+ Revision: 426250
- rebuild

* Tue Feb 03 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.60-30mdv2009.1
+ Revision: 337202
- keep bash completion in its own package

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 1.60-29mdv2009.1
+ Revision: 317504
- rediffed some fuzzy patches
- fix build with -Werror=format-security (P65)
- use %%ldflags

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.60-28mdv2009.0
+ Revision: 223344
- rebuild

* Thu Mar 06 2008 Andreas Hasenack <andreas@mandriva.com> 1.60-27mdv2008.1
+ Revision: 181083
- adjust bin.netstat profile so netstat -p works

* Thu Feb 28 2008 Andreas Hasenack <andreas@mandriva.com> 1.60-26mdv2008.1
+ Revision: 176459
- updated apparmor profile for netstat

* Wed Feb 27 2008 Olivier Blin <oblin@mandriva.com> 1.60-25mdv2008.1
+ Revision: 175721
- sync with RH patches (should fix stack smashing with ifconfig/netstat, #34220)
- do not check if buildroot is /

* Fri Feb 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.60-24mdv2008.1
+ Revision: 168917
- fix bash completion

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.60-23mdv2008.1
+ Revision: 153282
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 1.60-21mdv2008.0
+ Revision: 91194
- ship apparmor profile and use it if apparmor is in effect

* Wed Aug 29 2007 Oden Eriksson <oeriksson@mandriva.com> 1.60-20mdv2008.0
+ Revision: 74521
- added one hunk in net-tools-1.60-netdevice.patch from fc8


* Sun Jan 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.60-19mdv2007.0
+ Revision: 108811
- uncompress all patches and additional sources
- add bash completion
- Import net-tools

* Fri Jan 27 2006 Olivier Blin <oblin@mandriva.com> 1.60-18mdk
- split out netplug, we don't want it by default

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.60-17mdk
- fix typo in initscript

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 1.60-16mdk
- convert parallel init to LSB

* Tue Jan 03 2006 Thierry Vignaud <tvignaud@mandriva.com> 1.60-15mdk
- patch 42: add support for parallel init
- disable parallel build (broken)

* Mon Nov 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.60-14mdk
- drop P0 (netplug_def_runlevel) as we don't want to start 
  it by default

* Mon Jul 25 2005 Olivier Blin <oblin@mandriva.com> 1.60-13mdk
- remove translated rarp man pages (obsolete, #12238)

* Tue Jun 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.60-12mdk
- sync with fedora (1.60-54)
- added P0 (netplug_def_runlevel)
- misc rpmlint fixes

* Wed Jun 09 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.60-11mdk
- fix gcc-3.4 build (P15)
- fix non-conffile-in-etc
- spec cosmetics

* Mon Mar 15 2004 Florin <florin@mandrakesoft.com> 1.60-10mdk
- merge with RH
- add the x25 patch (gb)

