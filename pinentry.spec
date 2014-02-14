%bcond_with bootstrap

Summary:	Collection of simple PIN or passphrase entry dialogs
Name:		pinentry
Version:	0.8.2
Release:	6
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://www.gnupg.org/
Source0:	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
Source2:	pinentry-wrapper
BuildRequires:	cap-devel
BuildRequires:	gettext-devel
%if !%{with bootstrap}
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
BuildRequires:	pkgconfig(ncurses)
Obsoletes:	%{name}-curses < 0.8.0-2
Suggests:	%{name}-gui

%description 
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

%pre
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-curses ||:
%if !%{with bootstrap}
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gtk ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt4 ||:
%endif

%files 
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry
%{_bindir}/pinentry-curses
%{_infodir}/*.info*

#------------------------------------------------------------------------------

%if !%{with bootstrap}
%package	gtk2
Summary:	GTK+ interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-gtk

%description	gtk2
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%files		gtk2
%_bindir/pinentry-gtk-2

#------------------------------------------------------------------------------

%package	qt4
Summary:	QT4 interface of pinentry
Group:		System/Kernel and hardware
Provides:	%{name}-gui = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-qt < 0.7.6-3

%description	qt4
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT4 interface of the dialog.

%files		qt4
%{_bindir}/pinentry-qt*
%endif
#------------------------------------------------------------------------------

%prep
%setup -q 
./autogen.sh

%build
%configure2_5x \
%if !%{with bootstrap}
	--disable-pinentry-gtk \
	--disable-pinentry-qt \
	--enable-pinentry-qt4 \
	--enable-pinentry-gtk2 \
	--with-qt4-dir=%qt4dir \
%endif

%make

%install
%makeinstall_std

install -p -m755 -D %{SOURCE2} %{buildroot}%{_bindir}/pinentry 

%if !%{with bootstrap}
pushd %{buildroot}%{_bindir}
ln -s pinentry-qt4 pinentry-qt
popd
%endif
