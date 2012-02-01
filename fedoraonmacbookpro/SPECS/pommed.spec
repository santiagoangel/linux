#
# spec file for package pommed (Version 1.30)
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           pommed
Summary:        Apple laptops hotkeys event handler
License:        GPL v2 only
Group:          Hardware/Mobile
Version:        1.40
Release:        1.1
Url:            http://technologeek.org/projects/pommed/
%if 0
# BuildRequires some package containing /usr/include/ofapi/of_api.h
ExclusiveArch:  ppc 
%endif
ExclusiveArch:  %ix86 x86_64
BuildRequires:  alsa-lib-devel audiofile-devel gtk2-devel libglade2-devel pciutils-devel desktop-file-utils
BuildRequires:  libX11-devel libXext-devel libXpm-devel xorg-x11-utils
BuildRequires:  dbus-glib-devel libconfuse-devel xorg-x11-server-devel
BuildRequires:  fdupes
Requires:       eject xorg-x11-server-Xorg
Source0:        %name-%version.tar.gz
Source1:        pommed.init
Source2:        gpomme.desktop
Source3:        gpommerc
Source4:        pommed-README.SuSE
Source5:        pommed-rpmlintrc
Source6:        pommed.conf
Patch1:         pommed-desktop.patch
Patch2:         pommed-hardcoded_libpci.patch
Patch3:         pommed-optflags.patch
Patch4:         pommed-dbus_policy.patch
Patch5:         pommed_cust.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

pommed also monitors the ambient light sensors to automatically light
up the keyboard backlight on the MacBook Pro and PowerBook.

Optional support for the Apple Remote control is available.



Authors:
--------
    Julien BLACHE <jb@jblache.org>

%package -n gpomme
License:        GPL v2 only
Summary:        Graphical client for pommed
Group:          Hardware/Mobile
Requires:       pommed
Requires:       dbus

%description -n gpomme
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

gpomme is a graphical client for pommed. It listens for signals sent by
pommed on DBus and displays the action taken by pommed along with the
current state associated to this action.



Authors:
--------
    Julien BLACHE <jb@jblache.org>

%package -n wmpomme
License:        GPL v2 only
Summary:        WindowMaker dockapp client for pommed
Group:          Hardware/Mobile
Requires:       pommed
Requires:       dbus

%description -n wmpomme
pommed handles the hotkeys found on the Apple MacBook Pro, MacBook and
PowerBook laptops and adjusts the LCD backlight, sound volume, keyboard
backlight or ejects the CD-ROM drive accordingly.

wmpomme is a dockapp client for pommed. It displays the current level
of each item controlled by pommed.



Authors:
--------
    Julien BLACHE <jb@jblache.org>

%prep
%setup -q
#%patch1
#%patch2
#%patch3 -p1 
%patch4
%patch5 -p1 

%build
# This package failed when testing with -Wl,-as-needed being default.
# So we disable it here, if you want to retest, just delete this comment and the line below.
export SUSE_ASNEEDED=0
export CFLAGS="$RPM_OPT_FLAGS"
make %{?jobs:-j%jobs}

%install
mkdir -p %buildroot/%_bindir %buildroot/%_sbindir %buildroot/%_sysconfdir/{init.d,dbus-1/system.d} 
mkdir -p %buildroot/%_datadir/{applications,autostart,icons,pixmaps,gpomme,locale} 
mkdir -p %buildroot/%_mandir/man1 %buildroot/%_datadir/kde4/config
install -m 755 pommed/pommed          %buildroot/%_sbindir
install -m644 %{SOURCE4} README.SuSE
%ifarch ppc ppc64
install -m 644 pommed.conf.pmac       %buildroot/%_sysconfdir/pommed.conf
%else
#install -m 644 pommed.conf.mactel     %buildroot/%_sysconfdir/pommed.conf
install -m 644 %{S:6}     %buildroot/%_sysconfdir/pommed.conf
%endif
install -m 644 dbus-policy.conf       %buildroot/%_sysconfdir/dbus-1/system.d/pommed.conf
install -m 755 %{S:1}                 %buildroot/%_sysconfdir/init.d/pommed
ln -sf %_sysconfdir/init.d/pommed %buildroot/%_sbindir/rcpommed
install -m 644 pommed.1               %buildroot/%_mandir/man1
# gpomme
install -m 755 gpomme/gpomme          %buildroot/%_bindir
install -m 644 gpomme/gpomme.1        %buildroot/%_mandir/man1
install -m 644 gpomme/*.desktop       %buildroot/%_datadir/applications
install -m 644 icons/gpomme*          %buildroot/%_datadir/icons
install -m 644 icons/gpomme_32x32.xpm %buildroot/%_datadir/pixmaps/gpomme.xpm
#install -m 644 gpomme/gpomme.glade    %buildroot/%_datadir/gpomme
cp -a gpomme/themes                   %buildroot/%_datadir/gpomme
rm -rfv %buildroot/%_datadir/gpomme/themes/src
for mo in gpomme/po/*.mo ; do
    lang=`basename $mo .mo`
    filename="gpomme.mo"
    install -d %buildroot/%_datadir/locale/$lang/LC_MESSAGES
    install -m 644 $mo %buildroot/%_datadir/locale/$lang/LC_MESSAGES/$filename
done
install -m 644 %{S:2} %buildroot/%_datadir/autostart
install -m 644 %{S:3} %buildroot/%_datadir/kde4/config
# wmpomme
install -m 755 wmpomme/wmpomme        %buildroot/%_bindir
install -m 644 wmpomme/wmpomme.1      %buildroot/%_mandir/man1
#desktop-file-install %buildroot/%_datadir/applications/gpomme-c.desktop
#desktop-file-install %buildroot/%_datadir/applications/gpomme.desktop

desktop-file-install                                    \
--add-category="System"                             \
--delete-original                                       \
--dir=%{buildroot}%{_datadir}/applications              \
%{buildroot}/%{_datadir}/applications/gpomme-c.desktop


desktop-file-install                                    \
--add-category="System"                             \
--delete-original                                       \
--dir=%{buildroot}%{_datadir}/applications              \
%{buildroot}/%{_datadir}/applications/gpomme.desktop

# enable videoswitch
mkdir -p %buildroot/%_sysconfdir/pommed
#%if 0%{?suse_version} > 1020
fdupes -s %buildroot
#%endif
install -m 644 icons/gpomme_32x32.xpm %buildroot/%_datadir/icons/wmpomme.xpm
install -m 644 icons/gpomme_32x32.xpm %buildroot/%_datadir/pixmaps/gpomme.xpm
%find_lang gpomme

%post
%{fillup_and_insserv -n %name %name}

%preun
%stop_on_removal %name

%postun
%restart_on_update %name
%{insserv_cleanup}

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc AUTHORS README TODO README.SuSE
%config(noreplace) /etc/pommed.conf
%config(noreplace) /etc/dbus-1/system.d/pommed.conf
%_sysconfdir/init.d/pommed
%_sbindir/pommed
%_sbindir/rcpommed
%_mandir/man1/po*

%files -n gpomme -f gpomme.lang
%defattr(-,root,root)
%_bindir/gpomme
%_datadir/applications/*.desktop
%_datadir/icons/gp*
%_datadir/pixmaps/gp*
%_datadir/gpomme
%_datadir/autostart
%dir %_datadir/kde4
%_datadir/kde4/config
%_mandir/man1/gpo*

%files -n wmpomme
%defattr(-,root,root)
%_bindir/wmpomme
%_datadir/icons/wm*
%_mandir/man1/wmpo*

%changelog
* Sat Jan 21 2012 santiagoangel@gmail.com
- version 1.40
* Mon Oct 18 2010 alinm.elena@gmail.com
- added new config file, customised for MacBook Pro 7,1
* Sat Oct 16 2010 alinm.elena@gmail.com
- initial commit to my local project... This I hope to be a temporary measure
* Sat Oct  9 2010 alinm.elena@gmail.com
- work on 1.34
  - added flag patches to my patches
* Sat Oct  9 2010 alinm.elena@gmail.com
- more work on 1.34
  - readded the no optimisation patch
  - added a pacth that allows one to disable the audio controls (kde does it well by default) and prevents video to fail preventing pommed to start on MacBookPro 7.1
* Fri Oct  8 2010 alinm.elena@gmail.com
- updated to 1.34
  - removed the patch3 for testing purposes I will readd it later if needed
  - removed one file from install that does not exist anymore
* Tue Nov 17 2009 meissner@suse.de
- rediffed for fuzz=0
* Wed Nov 11 2009 ro@suse.de
- update to 1.30:
  - pommed: fix a crasher in the i2c probe routine on pmac.
  - pommed: fix sysfs backlight driver to handle > 3-digit values.
- update to 1.29:
  - pommed: add support for newer nvidia backlight driver which
  changed the sysfs layout.
  - pommed: move VT state checking to pommed, exposed over DBus.
  - gpomme: switch to asking pommed for the state of the VT.
  - wmpomme: switch to asking pommed for the state of the VT.
- update to 1.28:
  - pommed: added support for the MacBookPro5,3 (15" MacBookPro
  June 2009)
* Sat Aug  1 2009 lrupp@suse.de
- update to 1.27:
  - pommed:
  + added support for the MacBook5,2 (white MacBook).
  + added support for the MacBookPro5,5
* Fri Jun 19 2009 coolo@novell.com
- disable as-needed for this package as it fails to build with it
* Sun May 24 2009 ro@suse.de
- update to 1.26
  - pommed: only keystrokes on the built-in keyboard should reset
    the keyboard idle timer.
  - pommed: add USB IDs for the Apple external aluminium mini
    keyboard.
  - pommed: switch to sysfs resource files for PCI memory access
    instead of mmaping /dev/mem.
- update to 1.25
  - pommed: check current hardware backlight level before setting AC
    or battery level. Do not act if the backlight is off.
  - pommed: do not reject the Apple Bluetooth keyboard because of
    advertised EV_ABS events.
  - pommed: fix DBus configuration snippet for newer, stricter
    version of DBus (allow clients to send messages).
- update to 1.24
  - pommed: add new path for fnmode setting for 2.6.28.
- update to 1.23
  - pommed: add backlight support for late 2008 laptops.
  - pommed: default to sysfs backlight driver for nVidia machines,
    with the mbp_nvidia_bl kernel driver; fall back to native
    nv8600mgt if not supported.
  - pommed: try to reconnect to DBus if DBus is not available at
    startup. Previously we would just drop it and live without DBus.
* Tue Jan 27 2009 ro@suse.de
- dbus-policy: add send_destination rule (bnc#469771)
* Tue Nov 11 2008 lrupp@suse.de
- update to 1.22:
  + pommed:
  ++ do not probe for LMU controller on pmac machines that do not
    have a backlit keyboard. Avoids a spurious error message.
  ++ factor out ADB & LMU write routines, avoids duplicated code in
    the kbd_{lmu,pmu}_backlight_set() routines.
  ++ use a common sysfs power class routine in power.c, add sysfs
    power class support for pmac machines.
  ++ added partial support for the October 2008 laptops (MacBook5,1,
    MacBookPro5,1, MacBookAir2,1), LCD backlight missing.
  + gpomme:
  ++ add japanese translation for gpomme, courtesy of
    Nobuhiro Iwamatsu
  + wmpomme:
  ++ turn wmpomme into an event-driven dockapp, eliminating the
    fixed update rate (and, thus, wakeups).
    Thanks to Kalle A. Sandström for the prodding.
- removed dbus-1-devel BuildReq (included in dbus-1-glib-devel)
* Fri Oct 17 2008 olh@suse.de
- add ExclusiveArch x86 x86_64
* Thu Sep  4 2008 ro@suse.de
- add Required-Stop to init script
* Mon Jul 21 2008 lrupp@suse.de
- update to 1.21:
  + Note that this version of pommed REQUIRES Linux 2.6.25 or
    later and WILL NOT WORK PROPERLY on earlier kernels
  + pommed: add support for the MacBookPro4,1.
  + pommed: add support for the MacBook4,1.
  + pommed: add support for the WellSpring keyboard+trackpad
    assembly ("MultiTouch"), found in the MacBookAir1,1 and
  MacBookPro4,1
  + fix array boundary check in check_machine_dmi().
  + use BUS_BLUETOOTH for the Apple wireless keyboard
  + gpomme: won't cause 10 wakeups/sec anymore
  + gpomme: use compositing if available, patch by Soeren Sonnenburg
- create the desktop icons after fdupes (otherwise they will
  be stale symlinks)
- remove libsmbios build dependency
- split the patch into it's pieces
* Sun Feb 24 2008 crrodriguez@suse.de
- use RPM_OPT_FLAGS
* Tue Feb 12 2008 ro@suse.de
- update to 1.15:
  - pommed: add preliminary support for the MacBook Air1,1;
    USB IDs missing.
  - pommed: add support for power_supply class to the ACPI code.
- remove symlink to grandr (dropped from xorg-x11)
* Thu Jan 17 2008 lrupp@suse.de
- update to 1.14:
  + fix error handling in the audio sample loading code to properly
    report failure, preventing nasty segfaults later on in case the
    sound file is not available.
  + make goutte.wav the default beep sound, add click.wav and remove
    the KDE beep sound.
  + add an option to disable the beep on volume change
  + add the videoSwitch DBus notification
  + add support for LCD backlight control on the Intel 965GM
    found in the MacBook3,1
  + rework the inotify code to handle several events at once and to
    handle events with long filenames (longer than
    sizeof(struct inotify_event)); pommed could enter a busy-loop
    when receiving an inotify event with
    ie->len > sizeof(struct inotify_event)
  + wpomme: added video switch support
  + gpomme: added video switch support
  + do not expect at least 3 evdevs at startup
  + adds partial support for the new MacBook Santa Rosa (MacBook3)
  + fixes bug with disappearing event devices after suspend
  + external Apple USB keyboards are now supported
  + beep on volume change per default
  + rework the event management.
    Use epoll() for event polling instead of poll().
  + add secondary locations for the uinput device node.
  + pommed: add a beeper feature as a substitute to the missing PC
    Speaker. The feature is disabled by default, as not all
    machines need it and not everybody wants it.
- added gpomme.desktop and gpommerc to start gpomme via KDE
- added %%pre and %%post scripts for pommed
- use fdupes to save space
- use /usr/bin/grandr for videoswitch option
- added README.SuSE for applesmc kernel module
- fix lang files so gpomme is tranlated
* Mon Sep 17 2007 ro@suse.de
- created package from pommed (version 1.9)
