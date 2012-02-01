#
# spec file for package macfanctld
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

Name:           macfanctld
BuildRequires:  gcc make
PreReq:         coreutils grep
License:        GPL v2
Group:          System/Kernel
Autoreqprov:    on
Summary:        Apple fan control daemon
Version:        0.3
Release:        12.29
Source:         %{name}-%{version}.tar.bz2
Source1:        macfanctl.conf
Source2:        macfanctld.1
Source3:        macfanctld
Patch:          Makefile.patch
#URL:
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description -n macfanctld
macfanctld is a daemon that reads temperature sensors and adjust the fan(s) speed on MacBook's. macfanctld is configurable and logs temp and fan data to a file. macfanctld uses three sources to determine the fan speeed: 1) average temperature from all sensors, 2) sensor TC0P [CPU 0 Proximity Temp and 3] and sensor TG0P [GPU 0 Proximity Temp]. Each source's impact on fan speed can be individually adjusted to fine tune working temperature on different MacBooks.

Important: macfanctld depends on applesmc
%prep
%setup -q -n %{name}
%patch -p0
%build
make 

%install
mkdir -p $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install -m 0644 %{S:1} $RPM_BUILD_ROOT/etc/
install -m 0644 %{S:2} $RPM_BUILD_ROOT/usr/share/man/man1/
install -m 0755 macfanctld $RPM_BUILD_ROOT/usr/sbin/
install -m 0755 %{S:3} $RPM_BUILD_ROOT/etc/init.d/

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%dir %_prefix
%dir %_prefix/sbin
%dir %_prefix/share
%dir %_prefix/share/man
%dir %_prefix/share/man/man1
%config  /etc/macfanctl.conf
/etc/init.d/macfanctld
%_prefix/share/man/man1/macfanctld.1.gz
%_prefix/sbin/macfanctld

%changelog
* Mon Oct 18 2010 alinm.elena@gmail.com
  initial commit -
