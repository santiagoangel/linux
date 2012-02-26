Packager: Magnus Glantz
Summary: Spotify Version 0.6.6.10.gbd39032.58
Name: spotify
Version: 0.6.6
Release: 10.gbd39032.58
Vendor: Magnus Glantz
Group: Applications/Multimedia
BuildArch: x86_64
BuildRoot: %_topdir/tmp/%{name}-%{version}
Source0: spotify_for_fedora-1.2.tar.gz
AutoReqProv: no
Requires: glibc libstdc++ qt-x11 qt qt-webkit libXScrnSaver alsa-lib libgcc libX11 glib2 libpng zlib freetype libSM libICE libXi libXrender libXrandr libXfixes libXcursor libXinerama fontconfig libXext sqlite phonon pulseaudio-libs-glib2 pulseaudio-libs dbus-libs openssl krb5-libs libcom_err libxcb libuuid expat pulseaudio-libs libXtst xcb-util tcp_wrappers-libs libsndfile libasyncns keyutils-libs libXau flac libvorbis libogg freetype libsndfile libasyncns keyutils-libs libXau
License: Proprietary
URL: http://www.spotify.com

%description
This package contains Spotify Version 0.6.6.10.gbd39032.58
Based on
spotify-client-gnome-support_0.5.2.84.g6d797eb-1_all.deb
spotify-client-qt_0.6.6.10.gbd39032.58-1_amd64.deb
from http://repository.spotify.com
With libssl and libcrypto bundled from openssl-0.9.8k-1

%prep
tar -xvzf %_topdir/SOURCES/spotify_for_fedora-1.2.tar.gz

%install
cd spotify_for_fedora-1.2
mkdir %{buildroot}
cp -Rp *  %{buildroot}/

%clean 
rm -rf %{buildroot}/

%post
ln -s /usr/lib64/libssl.so.0.9.8k /usr/lib64/libssl.so.0.9.8
ln -s /usr/lib64/libcrypto.so.0.9.8k /usr/lib64/libcrypto.so.0.9.8

%postun
rm -f /usr/lib64/libssl.so.0.9.8
rm -f /usr/lib64/libcrypto.so.0.9.8

%files
%defattr(-,root,root)
%doc /usr/share/doc/spotify-client-qt
%doc /usr/share/doc/spotify-client-gnome-support
/usr/share/pixmaps/spotify-linux-512x512.png
/usr/share/applications/spotify.desktop
/usr/share/spotify
/usr/bin/spotify
/usr/lib64/libssl.so.0.9.8k
/usr/lib64/libcrypto.so.0.9.8k

%changelog
* Sun Feb 26 2012 Santiago Angel <santiagoangel@gmail.com> 1.2
- spotify-client-qt_0.6.6.10.gbd39032.58-1_amd64


* Sat Oct 15 2011 Magnus Glantz <open.grieves@gmail.com> 1.0-1
- Initial release.
