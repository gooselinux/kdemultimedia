Name: kdemultimedia
Epoch: 6
Version: 4.3.4
Release: 3%{?dist}
Summary: KDE Multimedia applications
Group: Applications/Multimedia
# see also: http://techbase.kde.org/Policies/Licensing_Policy
License: GPLv2+
URL: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdemultimedia-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# disable mplayerthumbs
Patch1: kdemultimedia-4.2.85-nomplayerthumbs.patch

# enable kscd doc only if MUSICBRAINZ is found
Patch2: kdemultimedia-4.3.2-kscd_doc.patch

# 4.3 upstream patches
Patch100: kdemultimedia-4.3.5.patch

BuildRequires: alsa-lib-devel
BuildRequires: cdparanoia-devel cdparanoia
BuildRequires: flac-devel
BuildRequires: glib2-devel
BuildRequires: kdebase-workspace-devel >= %{version}
BuildRequires: kdelibs-experimental-devel
BuildRequires: libtheora-devel
BuildRequires: libvorbis-devel
BuildRequires: taglib-devel

Requires: %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: kdelibs4 >= %{version}
Requires: kdebase-workspace >= %{version}

%description
The %{name} package contains multimedia applications, including:
* dragonplayer (a simple video player)
* juk (a music manager and player)
* kmix (an audio mixer)

%package libs
License: LGPLv2+ and GPLv2+
Summary: Runtime libraries for %{name}
Group: System Environment/Libraries
Obsoletes: %{name}-extras-libs < %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
%{summary}.

%package devel
Group: Development/Libraries
Summary: Developer files for %{name}
License: LGPLv2+ and GPLv2+
Requires: %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: kdelibs4-devel

%description devel
%{summary}.


%prep
%setup -q

%patch1 -p1 -b .nomplayerthumbs
%patch2 -p1 -b .kscd_doc

# 4.3 upstream patches
%patch100 -p1 -b .kde435

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_bindir}/*
%{_kde4_appsdir}/dragonplayer/
%{_kde4_appsdir}/juk/
%{_kde4_appsdir}/kmix/
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/konqsidebartng/
%{_kde4_appsdir}/solid/actions/dragonplayer-opendvd.desktop
%{_kde4_configdir}/dragonplayerrc
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/autostart/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/config.kcfg/*
%{_datadir}/dbus-1/interfaces/*
%{_kde4_docdir}/HTML/en/dragonplayer/
%{_kde4_docdir}/HTML/en/juk/
%{_kde4_docdir}/HTML/en/kmix/
%{_kde4_docdir}/HTML/en/kioslave/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/actions/player-volume-muted.*
%{_kde4_libdir}/libkdeinit*.so

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*
%{_kde4_libdir}/kde4/*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/audiocdencoder.h
%{_kde4_includedir}/libkcddb/
%{_kde4_includedir}/libkcompactdisc/
%{_kde4_libdir}/lib*.so
%exclude %{_kde4_libdir}/libkdeinit*.so


%changelog
* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 6:4.3.4-3
- rebuilt against qt 4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 6:4.3.4-2
- backport 4.3.5 fixes

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Tue Nov 10 2009 Than Ngo <than@redhat.com> - 4.3.3-2
- rhel cleanup
- don't install kscd doc if it's not built

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Sat Jul 11 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Fri Jun 05 2009 Than Ngo <than@redhat.com> - 4.2.90-2
- fix build issue without xine-lib

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Mon May 18 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-2
- Disable BR pulseaudio-libs-devel, KMix PA integration does not work yet.

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Sun Feb 22 2009 Tejas Dinkar <tejas@gja.in> - 4.2.0-3
- fix kde#165249 No sound after second video file in Dragon Player (from 4.2.1)

* Sat Jan 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-2
- unowned dirs (#483516)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Sat Dec 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.85-2
- restore BR libtunepimp-devel libmusicbrainz-devel for now, needed by Kscd

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Fri Nov 28 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-3
- dragon documentation disappeared (at least with my mock build), update file
  lists
- add kioslave documentation to file lists

* Thu Nov 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.80-3
- -devel: drop Req: kdebase-workspace-devel

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Wed Sep 17 2008 Than Ngo <than@redhat.com> 4.1.1-2
- backport from trunk to fix dragon kpart crash in the embedding application

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Thu Jun 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.0.80-3
- some of the libraries are clearly LGPLv2+, correct license tags for libs and devel

* Thu Jun 05 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.80-2
- License: GPLv2+

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Sat May 10 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72
- drop backported kmix-systray patch
- Obsoletes/Provides dragonplayer, add it to description and file list
- add BR xine-lib-devel for dragonplayer

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Tue Apr 01 2008 Lukáš Tinkl <ltinkl@redhat.com>
- fix kmix systray volume control tooltip

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- Rebuild for NDEBUG

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Wed Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0.0-1
- kde-4.0.0
- drop upstreamed cdparanoia patch

* Wed Jan 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-4
- don't mention kaudiocreator in description, it's not actually there
- apply patch by Alex Merry to support FLAC 1.1.3+ in kio_audiocd
- apply patch by Allen Winter to fix cdparanoia detection
- list audiocdencoder.h in file list (-devel)

* Fri Dec 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.97.0-3
- -libs: Obsoletes: -extras(-libs)
- cleanup BR's
- omit parallel-install symlink hacks

* Wed Dec 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 3.97.0-2
- rebuild for changed _kde4_includedir

* Mon Dec 10 2007 Than Ngo <than@redhat.com> 3.97.0-1
- 3.97.0

* Fri Nov 30 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.2-1
- kde-3.96.2

* Sat Nov 24 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.1-1
- kde-3.96.1

* Fri Nov 23 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-4
- libs subpkg
- also use epoch in changelog (also backwards)

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-3
- BR: kde-filesystem >= 4

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-2
- Requires: kdebase-workspace-devel
- BR: libXScrnSaver-devel
- BR: libXtst-devel

* Fri Nov 16 2007 Sebastian Vahl <fedora@deadbabylon.de> 6:3.96.0-1
- Initial version for Fedora
