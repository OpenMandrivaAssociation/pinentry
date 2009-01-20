
Name: pinentry
Version: 0.7.5
Release: %mkrel 6
Summary: Collection of simple PIN or passphrase entry dialogs
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.gz
Source1: %{SOURCE0}.sig
Patch0: pinentry-0.7.5-glib-fix.patch
Patch1: http://sources.gentoo.org/viewcvs.py/*checkout*/gentoo-x86/app-crypt/pinentry/files/pinentry-0.7.4-grab.patch
# svn diff -c 181 svn://cvs.gnupg.org/pinentry/trunk
Patch2: pinentry-0.7.5-realize-transient.patch
# Adapted to autotools from KDE 4 source
Patch3: pinentry-qt4-autotools.patch
License: GPLv2+
Group: System/Kernel and hardware
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL: http://www.gnupg.org/
Requires(post): info-install
Requires(preun):info-install
BuildRequires: libgtk+2.0-devel
BuildRequires: libcap-devel
BuildRequires: ncurses-devel
BuildRequires: qt4-devel

%description 
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

#-----------------------------------------------------------------------------------------

%package curses
Summary: Ncurses interface of pinentry
Group: System/Kernel and hardware
Provides: %{name} = %{version}-%{release}
Obsoletes: %{name} < 0.7.5

%description curses
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides Ncurses interface of the dialog.

%post curses
%_install_info %{name}.info
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-curses 10

%preun curses
%_remove_install_info %{name}.info
if [ "$1" = "0" ]; then
   update-alternatives --remove pinentry /usr/bin/pinentry-curses
fi

%files curses
%defattr(-,root,root)
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry-curses
%{_infodir}/*.info*

#-----------------------------------------------------------------------------------------

%package gtk2
Summary: GTK+ interface of pinentry
Group: System/Kernel and hardware
Provides: %{name} = %{version}-%{release}
Requires: %{name}-curses = %{version}-%{release}
Obsoletes: pinentry-gtk

%description gtk2
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%post gtk2
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-gtk-2 20 --slave /usr/bin/pinentry-gtk pinentry-gtk /usr/bin/pinentry-gtk-2

%postun gtk2
if [ "$1" = "0" ]; then
   update-alternatives --remove pinentry /usr/bin/pinentry-gtk-2
fi

%files gtk2
%defattr(-,root,root)
%_bindir/pinentry-gtk-2

#-----------------------------------------------------------------------------------------

%package qt4
Summary: QT4 interface of pinentry
Group: System/Kernel and hardware
Provides: %{name} = %{version}-%{release}
Requires: %{name}-curses = %{version}-%{release}
Obsoletes: pinentry-qt

%description qt4
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT4 interface of the dialog.

%post qt4
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-qt4 30 --slave /usr/bin/pinentry-qt pinentry-qt /usr/bin/pinentry-qt4

%postun qt4
if [ "$1" = "0" ]; then
   update-alternatives --remove pinentry /usr/bin/pinentry-qt4
fi

%files qt4
%defattr(-,root,root)
%{_bindir}/pinentry-qt4

#-----------------------------------------------------------------------------------------

%prep
%setup -q 
%patch0 -p0 -b .glib-fix
%patch1 -p1 -b .grab
%patch2 -p0 -b .realize-transient
%patch3 -p1 -b .qt4

%build
./autogen.sh

%configure2_5x \
	--disable-pinentry-gtk \
	--disable-pinentry-qt \
	--enable-pinentry-qt4 \
	--enable-pinentry-gtk2 \
	--disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#Remove link we will use update alternative
rm -f %{buildroot}%{_bindir}/pinentry


%clean
rm -rf %{buildroot}


