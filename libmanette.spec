#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	Simple GObject game controller library
Summary(pl.UTF-8):	Prosta biblioteka GObject do obsługi manipulatorów do gier
Name:		libmanette
Version:	0.2.11
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libmanette/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	1f9ebb6a8f56e458e4ee8db4d97067ec
URL:		https://gnome.pages.gitlab.gnome.org/libmanette/
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.50
BuildRequires:	hidapi-devel
BuildRequires:	libevdev-devel >= 1.4.5
BuildRequires:	meson >= 0.53.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 1:1.0
BuildRequires:	xz
Requires:	glib2 >= 1:2.50
Requires:	libevdev >= 1.4.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmanette is a small GObject library giving you simple access to game
controllers.

This library is intended for software needing a painless access to
game controllers from any programming language and with little
dependencies.

It supports the de-facto standard gamepads as defined by the W3C
standard Gamepad specification <https://www.w3.org/TR/gamepad/> or as
implemented by the SDL GameController
<https://wiki.libsdl.org/CategoryGameController>. More game controller
kinds could be supported in the future if needed. Mapping of the
devices is handled transparently and internally by the library using
the popular SDL mapping string format.

%description -l pl.UTF-8
libmanette to mała biblioteka GObject dająca prosty dostęp do
manipulatorów do gier.

Biblioteka jest przeznaczona dla oprogramowania potrzebującego
bezbolesnego dostępu do manipulatorów do gier z poziomu dowolnego
języka programowania i z możliwie małymi zależnościami.

Biblioteka obsługuje kontrolery standardu de facto, zdefiniowanego w
specyfikacji Gamepad standardu W3C <https://www.w3.org/TR/gamepad/>,
albo wg implementacji SDL GameController
<https://wiki.libsdl.org/CategoryGameController>. W przyszłości, w
miarę potrzeby, może być dodana obsługa kolejnych rodzajów
manipulatorów. Odwzorowanie urządzeń obsługiwane jest w sposób
przezroczysty, wewnętrznie w bibliotece, z użyciem popularnego formatu
łańcuchów odwzorowujących SDL.

%package devel
Summary:	Header files for libmanette library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmanette
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.50

%description devel
Header files for libmanette library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libmanette.

%package static
Summary:	Static libmanette library
Summary(pl.UTF-8):	Statyczna biblioteka libmanette
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmanette library.

%description static -l pl.UTF-8
Statyczna biblioteka libmanette.

%package -n vala-libmanette
Summary:	Vala API for libmanette library
Summary(pl.UTF-8):	API języka Vala do biblioteki libmanette
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala
BuildArch:	noarch

%description -n vala-libmanette
Vala API for libmanette library.

%description -n vala-libmanette -l pl.UTF-8
API języka Vala do biblioteki libmanette.

%package apidocs
Summary:	API documentation for libmanette library
Summary(pl.UTF-8):	Dokumentacja biblioteki libmanette
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libmanette library.

%description apidocs -l pl.UTF-8
Dokumentacja biblioteki libmanette.

%prep
%setup -q

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Ddoc=true} \
	-Dgudev=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libmanette $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README.md
%attr(755,root,root) %{_bindir}/manette-test
%attr(755,root,root) %{_libdir}/libmanette-0.2.so.0
%{_libdir}/girepository-1.0/Manette-0.2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmanette-0.2.so
%{_includedir}/libmanette
%{_datadir}/gir-1.0/Manette-0.2.gir
%{_pkgconfigdir}/manette-0.2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmanette-0.2.a
%endif

%files -n vala-libmanette
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/manette-0.2.deps
%{_datadir}/vala/vapi/manette-0.2.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libmanette
%endif
