%bcond_with qt3

Name: pinentry
Version: 0.8.0
Release: %mkrel 2
Summary: Collection of simple PIN or passphrase entry dialogs
Source0: ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.gz
Source1: %{SOURCE0}.sig
Source2: pinentry-wrapper
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
Obsoletes:     %name-curses < 0.8.0-2

%description 
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

%pre
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-curses ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-gtk ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt ||:
%{_sbindir}/update-alternatives --remove pinentry %{_bindir}/pinentry-qt4 ||:

%files 
%defattr(-,root,root)
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry
%{_bindir}/pinentry-curses
%{_infodir}/*.info*

#-----------------------------------------------------------------------------------------

%package gtk2
Summary: GTK+ interface of pinentry
Group: System/Kernel and hardware
Provides: %{name}-gui = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Obsoletes: pinentry-gtk

%description gtk2
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%files gtk2
%defattr(-,root,root)
%_bindir/pinentry-gtk-2

#-----------------------------------------------------------------------------------------

%package qt4
Summary: QT4 interface of pinentry
Group: System/Kernel and hardware
Provides: %{name}-gui = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%if ! %with qt3
Obsoletes: %name-qt < 0.7.6-3
%endif
%description qt4
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT4 interface of the dialog.

%files qt4
%defattr(-,root,root)
%{_bindir}/pinentry-qt4

#-----------------------------------------------------------------------------------------

%if %with qt3
%package qt
Summary: QT3 interface of pinentry
Group: System/Kernel and hardware
Provides: %{name}-gui = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
BuildRequires: qt3-devel

%description qt
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT3 interface of the dialog.

%files qt
%defattr(-,root,root)
%{_bindir}/pinentry-qt

%endif

#-----------------------------------------------------------------------------------------

%prep
%setup -q 

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

install -p -m755 -D %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/pinentry 

%clean
rm -rf %{buildroot}


