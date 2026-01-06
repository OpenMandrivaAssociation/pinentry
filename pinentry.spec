%bcond_without qt5
%bcond_without qt6
%bcond_without gtk2
%bcond_without gnome
%bcond_without ncurses
%bcond_without fltk

#define gitdate 20240225

Summary:	Collection of simple PIN or passphrase entry dialogs
Name:		pinentry
Version:	1.3.1
Release:	%{?gitdate:0.%{gitdate}.}2
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		https://www.gnupg.org/
%if 0%{?gitdate:1}
Source0:	https://github.com/gpg/pinentry/archive/refs/heads/master.tar.gz#/%{name}-%{gitdate}.tar.gz
%else
Source0:	https://gnupg.org/ftp/gcrypt/%{name}/%{name}-%{version}.tar.bz2
%endif
Source2:	pinentry-wrapper
Patch0:		https://src.fedoraproject.org/rpms/pinentry/raw/rawhide/f/pinentry-1.1.1-coverity.patch
Patch1:		pinentry-0.9.7-default-qt.patch
Requires(pre):	/bin/sh
Requires(pre):	coreutils
Requires(pre):	util-linux
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	pkgconfig(libcap)
BuildRequires:	gettext-devel
BuildRequires:	texinfo
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(libassuan)
BuildRequires:	git-core
%if %{with qt5}
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5X11Extras)
BuildRequires:	cmake(KF5Wayland)
%endif
%if %{with qt6}
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Test)
BuildRequires:	pkgconfig(KF6WindowSystem)
%endif
%if %{with gtk2}
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libsecret-1)
%endif
%if %{with ncurses}
BuildRequires:	pkgconfig(ncurses)
%endif
%if %{with gnome}
BuildRequires:	pkgconfig(gcr-3)
%endif
%if %{with fltk}
BuildRequires:	fltk-devel
%endif
Obsoletes:	%{name}-curses < 0.8.0-2
Suggests:	%{name}-gui

%description
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

%pre
%if %{with ncurses}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-curses ||:
%endif
%if !%{with gtk2}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gtk ||:
%endif
%if !%{with gnome}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gnome3 ||:
%endif
%if !%{with qt5}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt5 ||:
%endif
%if !%{with fltk}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-fltk ||:
%endif

%files
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry
%{_bindir}/pinentry-tty
%if %{with ncurses}
%{_bindir}/pinentry-curses
%doc %{_infodir}/*.info*
%endif
#------------------------------------------------------------------------------

%if %{with gtk2}
%package gtk2
Summary:	GTK+ interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-gtk < 1.2.1

%description gtk2
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%files gtk2
%{_bindir}/pinentry-gtk-2
%endif

#------------------------------------------------------------------------------

%if %{with qt5}
%package qt5
Summary:	QT5 interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{EVRD}
Obsoletes:	%{name}-qt < 0.7.6-3
# (tpg) upgrade from 2014.x
Obsoletes:	%{name}-qt4 < 0.8.2-4
Provides:	%{name}-qt4 = 0.8.2-5

%description qt5
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT5 interface of the dialog.

%files qt5
%{_bindir}/pinentry-qt5
%{_datadir}/applications/org.gnupg.pinentry-qt5.desktop
%endif

#------------------------------------------------------------------------------

%if %{with qt6}
%package qt6
Summary:	QT6 interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{EVRD}
Obsoletes:	%{name}-qt < 0.7.6-3

%description qt6
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT5 interface of the dialog.

%files qt6
%{_bindir}/pinentry-qt
%{_datadir}/applications/org.gnupg.pinentry-qt.desktop
%{_datadir}/pixmaps/pinentry.png
%endif

#------------------------------------------------------------------------------

%if %{with gnome}
%package gnome
Summary:	GNOME 3 interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description gnome
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GNOME 3 interface of the dialog.

%files gnome
%{_bindir}/pinentry-gnome3
%endif

#------------------------------------------------------------------------------

%if %{with fltk}
%package fltk
Summary:	FLTK interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description fltk
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides an FLTK interface of the dialog.

%files fltk
%{_bindir}/pinentry-fltk
%endif

#------------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?gitdate:master}%{!?gitdate:%{version}}
%if 0%{?gitdate:1}
cat >doc/version.texi <<EOF
@set UPDATED 25 August 2021
@set UPDATED-MONTH August 2021
@set EDITION %{version}
@set VERSION %{version}
EOF
%endif

./autogen.sh

%build
%configure \
%if %{with qt6}
	--enable-pinentry-qt \
%else
	--disable-pinentry-qt \
%endif
%if %{with qt5}
	--enable-pinentry-qt5 \
%else
	--disable-pinentry-qt5 \
%endif
%if %{with gtk2}
	--enable-pinentry-gtk2 \
%else
	--disable-pinentry-gtk2 \
%endif
%if %{with gnome}
	--enable-pinentry-gnome3 \
%else
	--disable-pinentry-gnome3 \
%endif
%if %{with fltk}
	--enable-pinentry-fltk \
%else
	--disable-pinentry-fltk \
%endif
	--disable-pinentry-efl \
	--enable-libsecret \
	--enable-pinentry-tty

%make_build

%install
%make_install

install -p -m755 -D %{SOURCE2} %{buildroot}%{_bindir}/pinentry
