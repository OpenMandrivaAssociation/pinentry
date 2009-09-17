%bcond_with qt3

Name: pinentry
Version: 0.7.6
Release: %mkrel 3
Summary: Collection of simple PIN or passphrase entry dialogs
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.gz
Source1: %{SOURCE0}.sig
# Build with QT 4.5: http://bugs.gentoo.org/show_bug.cgi?id=274999#c2
Patch0: pinentry-0.7.6-moc.patch
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
BuildRequires: gettext-devel

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
%if ! %with qt3
Obsoletes: %name-qt < 0.7.6-3
%endif
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

%if %with qt3
%package qt
Summary: QT3 interface of pinentry
Group: System/Kernel and hardware
Provides: %{name} = %{version}-%{release}
Requires: %{name}-curses = %{version}-%{release}
BuildRequires: qt3-devel

%description qt
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT3 interface of the dialog.

%post qt
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-qt 10 --slave /usr/bin/pinentry-qt pinentry-qt /usr/bin/pinentry-qt

%postun qt
if [ "$1" = "0" ]; then
   update-alternatives --remove pinentry /usr/bin/pinentry-qt3
fi

%files qt
%defattr(-,root,root)
%{_bindir}/pinentry-qt

%endif

#-----------------------------------------------------------------------------------------

%prep
%setup -q 
%patch0 -p1 -b .moc

%build
./autogen.sh

%configure2_5x \
	--disable-pinentry-gtk \
%if	%with qt3
	--enable-pinentry-qt \
    --with-qt-dir=%qt3dir \
%else
	--disable-pinentry-qt \
%endif
	--enable-pinentry-qt4 \
	--enable-pinentry-gtk2 \
    --with-qt4-dir=%qt4dir \
	--disable-rpath

%make
%install
rm -rf %{buildroot}
%makeinstall_std

#Remove link we will use update alternative
rm -f %{buildroot}%{_bindir}/pinentry

%clean
rm -rf %{buildroot}


