#
# Conditional build:
%bcond_with	tests	# run tests (need active Internet connection)
%bcond_without	qt4	# Qt4 library
%bcond_without	qt5	# Qt5 library

Summary:	C++/Qt4 wrapper for the Echo Nest API
Summary(pl.UTF-8):	Obudowanie C++/Qt4 dla API Echo Nest
Name:		libechonest
Version:	2.3.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://files.lfranchi.com/%{name}-%{version}.tar.bz2
# Source0-md5:	d8c60545b056145dc66882971a0acf9c
URL:		https://projects.kde.org/projects/playground/libs/libechonest
BuildRequires:	cmake >= 2.6
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
%if %{with qt4}
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtNetwork-devel >= 4
%{?with_tests:BuildRequires:	QtXml-devel >= 4}
BuildRequires:	qjson-devel
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-qmake >= 4
%endif
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
%{?with_tests:BuildRequires:	Qt5Xml-devel >= 5}
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%endif
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbol __stack_chk_fail in libechonest.so.2.1.0
%ifarch i486
%define	skip_post_check_so	libechonest.so.%{version}
%endif

%description
libechonest is a collection of Qt4 classes designed to make a
developer's life easy when trying to use the APIs provided by The Echo
Nest.

%description -l pl.UTF-8
libechonest to zbiór klas Qt4 zaprojektuwany, aby ułatwić życie
programiście przy używaniu API udostępnianych przez The Echo Nest.

%package devel
Summary:	Development files for libechonest library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libechonest
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore-devel >= 4
Requires:	QtNetwork-devel >= 4

%description devel
This package contains the header files for developing applications
that use libechonest library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libechonest.

%package -n libechonest-qt5
Summary:	C++/Qt5 wrapper for the Echo Nest API
Summary(pl.UTF-8):	Obudowanie C++/Qt5 dla API Echo Nest
Group:		Libraries

%description -n libechonest-qt5
libechonest is a collection of Qt5 classes designed to make a
developer's life easy when trying to use the APIs provided by The Echo
Nest.

%description -n libechonest-qt5 -l pl.UTF-8
libechonest to zbiór klas Qt5 zaprojektuwany, aby ułatwić życie
programiście przy używaniu API udostępnianych przez The Echo Nest.

%package -n libechonest-qt5-devel
Summary:	Development files for libechonest5 library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libechonest5
Group:		Development/Libraries
Requires:	Qt5Core-devel >= 5
Requires:	Qt5Network-devel >= 5
Requires:	libechonest-qt5 = %{version}-%{release}

%description -n libechonest-qt5-devel
This package contains the header files for developing applications
that use libechonest5 library.

%description -n libechonest-qt5-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libechonest5.

%prep
%setup -q

%build
%if %{with qt4}
install -d build-qt4
cd build-qt4
%cmake \
	-DBUILD_WITH_QT4:BOOL=ON \
	-DECHONEST_BUILD_TESTS:BOOL=%{?with_tests:ON}%{!?with_tests:OFF} \
	..
%{__make}

%if %{with tests}
export PKG_CONFIG_PATH=$(pwd)
test "$(pkg-config --modversion libechonest)" = "%{version}"
%{__make} test ARGS="--timeout 300 --output-on-failure"
%endif

cd ..
%endif

%if %{with qt5}
install -d build-qt5
cd build-qt5
%cmake \
	-DBUILD_WITH_QT4:BOOL=OFF \
	-DECHONEST_BUILD_TESTS:BOOL=%{?with_tests:ON}%{!?with_tests:OFF} \
	..
%{__make}

%if %{with tests}
export PKG_CONFIG_PATH=$(pwd)
test "$(pkg-config --modversion libechonest5)" = "%{version}"
%{__make} test ARGS="--timeout 300 --output-on-failure"
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with qt4}
%{__make} -C build-qt4 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with qt5}
%{__make} -C build-qt5 install/fast \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libechonest-qt5 -p /sbin/ldconfig
%postun	-n libechonest-qt5 -p /sbin/ldconfig

%if %{with qt4}
%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_libdir}/libechonest.so.*.*.*
# yes, SONAME is "libechonest.so.2.3"
%attr(755,root,root) %ghost %{_libdir}/libechonest.so.2.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libechonest.so
%{_includedir}/echonest
%{_pkgconfigdir}/libechonest.pc
%endif

%if %{with qt5}
%files -n libechonest-qt5
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_libdir}/libechonest5.so.*.*.*
# yes, SONAME is "libechonest5.so.2.3"
%attr(755,root,root) %ghost %{_libdir}/libechonest5.so.2.3

%files -n libechonest-qt5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libechonest5.so
%{_includedir}/echonest5
%{_pkgconfigdir}/libechonest5.pc
%endif
