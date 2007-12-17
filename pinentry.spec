%define version 0.7.4
%define release %mkrel 1

Summary: 	Collection of simple PIN or passphrase entry dialogs
Name: 		pinentry
Version: 	%{version}
Release: 	%{release}
Source0: 	ftp://ftp.gnupg.org/gcrypt/%{name}/%{name}-%{version}.tar.gz
Source1:	%{SOURCE0}.sig
Patch0:		pinentry-0.7.3-fix-info-header.patch
License: 	GPL
Group: 		System/Kernel and hardware
URL: 		http://www.gnupg.org/

Requires(post): info-install
Requires(preun):info-install

BuildRequires:	libgtk+2.0-devel
#BuildRequires:	libcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	qt3-devel

%description 
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

%package	gtk
Summary:	GTK+ interface of pinentry
Group: 		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	gtk
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides GTK+ interface of the dialog.

%package	qt
Summary:	QT interface of pinentry
Group: 		System/Kernel and hardware
Requires:	%{name} = %{version}-%{release}

%description	qt
%{name} is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project.

This package provides QT interface of the dialog.

%prep
%setup -q
#%patch0 -p1 -b .headerfix

%build
%configure2_5x \
	--disable-pinentry-gtk \
	--enable-pinentry-gtk2 \
	--disable-rpath
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#Remove link we will use update alternative
rm -f %{buildroot}%{_bindir}/pinentry

%post 
%_install_info %{name}.info
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-curses 10

%preun 
%_remove_install_info %{name}.info
update-alternatives --remove pinentry /usr/bin/pinentry-curses

%post gtk
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-gtk-2 20

%postun gtk
update-alternatives --remove pinentry /usr/bin/pinentry-gtk-2

%post qt
update-alternatives --install /usr/bin/pinentry pinentry /usr/bin/pinentry-qt 30

%postun qt
update-alternatives --remove pinentry /usr/bin/pinentry-qt

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README TODO ChangeLog NEWS AUTHORS THANKS
%{_bindir}/pinentry-curses
%{_infodir}/*.info*

%files gtk
%defattr(-,root,root)
%_bindir/pinentry-gtk-2

%files qt
%defattr(-,root,root)
%{_bindir}/pinentry-qt
