#
# spec file for package mbpfand
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# norootforbuild

Name:           mbpfand
BuildRequires:  gcc make
Requires:       coreutils
License:        GPL v2
Group:          System/Kernel
Autoreqprov:    on
Summary:        Simple Apple fan control daemon
Version:        0.4
Release:        2
Source:         %{name}-%{version}.tar.gz
Source1:        mbpfan.conf
Source2:        mbpfand.1
Source3:        mbpfan
Source4:        coretemp.conf
#URL:
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description -n mbpfand
This is a daemon that uses input from coretemp module and sets the fan speed using the applesmc module.


%prep
%setup -q -n %{name}
%build
make 

%install
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/etc/modules-load.d
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install -m 0644 %{S:1} $RPM_BUILD_ROOT/etc/
install -m 0644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man1/
install -m 0755 mbpfand $RPM_BUILD_ROOT/usr/sbin/
install -m 0755 %{S:3} $RPM_BUILD_ROOT/etc/init.d/
install -m 0644 %{S:4} $RPM_BUILD_ROOT/etc/modules-load.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %_prefix
%dir %_prefix/sbin
%dir %_prefix/share
%dir %_prefix/share/man
%dir %_prefix/share/man/man1
%config  /etc/mbpfan.conf
/etc/init.d/mbpfan
/etc/modules-load.d/coretemp.conf
%_prefix/share/man/man1/mbpfand.1.gz
%_prefix/sbin/mbpfand

%changelog
* Sat Mar 10 2012 santiagoangel@gmail.com
- Version 0.4  include temperature measure from /sys/devices/platform/coretemp.0/temp1_input.

* Sat Mar 10 2012 santiagoangel@gmail.com
- Version 0.3  setting low_temp=50, high_temp=58 & max_temp=78.

* Sat Mar 10 2012 santiagoangel@gmail.com
- Version 0.2 fan speed and temperatures adjusted.

* Sat Mar 10 2012 santiagoangel@gmail.com
- Version 0.1 from https://github.com/rvega/Fan-Control-Daemon

