%bcond_without qt5
%bcond_without gtk2
%bcond_without ncurses
%define _disable_lto 1

Summary:	Collection of simple PIN or passphrase entry dialogs
Name:		pinentry
Version:	1.1.0
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source2:	pinentry-wrapper
#Patch0:		pinentry-0.9.7-compile.patch
Patch1:		pinentry-0.9.7-default-qt.patch
Requires(pre):	chkconfig
BuildRequires:	cap-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	libassuan-devel
%if %{with qt5}
BuildRequires:	qt5-devel
%endif

%if %{with gtk2}
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libsecret-1)
%endif
%if %{with ncurses}
BuildRequires:	pkgconfig(ncurses)
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
%if !%{with qt5}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt5 ||:
%endif

%files
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry
%if %{with ncurses}
%{_bindir}/pinentry-curses
%{_infodir}/*.info*

#------------------------------------------------------------------------------

%if %{with gtk2}
%package gtk2
Summary:	GTK+ interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-gtk

%description gtk2
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%files gtk2
%_bindir/pinentry-gtk-2
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

This package provides QT4 interface of the dialog.

%files qt5
%{_bindir}/pinentry-qt*
%endif
#------------------------------------------------------------------------------

%prep
%setup -q
%apply_patches
./autogen.sh

#% if !%{with bootstrap}
#for f in qt4/*.moc; do
#	%{_bindir}/moc ${f/.moc/.h} > ${f}
#done
#% endif

%build
%configure \
%if %{with qt5}
	--enable-pinentry-qt \
%endif
%if %{with gtk2}
	--enable-pinentry-gtk2 \
%endif
	--enable-libsecret

%make

%install
%makeinstall_std

install -p -m755 -D %{SOURCE2} %{buildroot}%{_bindir}/pinentry 

%if %{with qt5}
pushd %{buildroot}%{_bindir}
ln -s pinentry-qt pinentry-qt5
popd
%endif
