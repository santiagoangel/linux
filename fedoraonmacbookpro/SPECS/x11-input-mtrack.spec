# norootforbuild

Name:           x11-input-mtrack
BuildRequires:  mtdev-devel pkgconfig xorg-x11-proto-devel xorg-x11-server-sdk
BuildRequires:  autoconf automake libtool
Requires:       mtdev
Summary:        An Xorg driver for multitouch trackpads
Version:        0.2.0
Release:        3.1
License:        GPL-2.0
Group:          System/X11/Servers/XF86_4
Source:         xf86-input-mtrack-0.2.0-1-g71abf32.tar.bz2
Source1:        mtrack.conf
Patch:          multitouch-missing-include.diff
ExcludeArch:    s390 s390x
Conflicts:      x11-input-multitouch
Url:            http://github.com/BlueDragonX/xf86-input-mtrack
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
An Xorg driver for multitouch trackpads. Supports any trackpad whose kernel driver uses the slotted multitouch protocol. For more information on the protocol see the kernel documentation.

This driver is compatible with Xorg server versions 1.7, 1.8, and 1.10. It requires the mtdev library to operate.

%prep
%setup -q -n xf86-input-mtrack
%patch -p1

%build
autoreconf -v --install ||exit 1
%configure
%{__make}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p" 
# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT/etc/X11/xorg.conf.d
# higher priority than synaptics (50-synaptics.conf), apparently the last
# driver entry wins ...
install -c -m 0644 %{S:1} $RPM_BUILD_ROOT/etc/X11/xorg.conf.d/60-mtrack.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc COPYING README.md
%{_libdir}/xorg/modules/input/*
/etc/X11/xorg.conf.d/*.conf

%changelog
* Thu Jan 12 2012 cfarrell@suse.com
- license update: GPL-2.0
  SPDX format
* Tue Jan 10 2012 sndirsch@suse.com
- reworked mtrack.conf
- give the driver higher priority in /etc/X11/xorg.conf.d than the
  synaptics one; removed the voodoo of synaptics driver config
  renaming
* Thu Aug 11 2011 tiwai@suse.de
- initial version: 0.2.0
- add xorg.conf file
