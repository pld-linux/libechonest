#
# Conditional build:
%bcond_with	tests		# build with tests. tests need active internet connection

Summary:	C++ wrapper for the Echo Nest API
Name:		libechonest
Version:	2.1.0
Release:	1
License:	GPL v2+
Source0:	http://files.lfranchi.com/%{name}-%{version}.tar.bz2
# Source0-md5:	96d98dbc5b3b155b277a9901d1133c5e
Group:		Libraries
URL:		https://projects.kde.org/projects/playground/libs/libechonest
BuildRequires:	QtNetwork-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig
BuildRequires:	qjson-devel
BuildRequires:	qt4-build
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbol __stack_chk_fail in libechonest.so.2.1.0
%ifarch i486
%define	skip_post_check_so	libechonest.so.%{version}
%endif

%description
libechonest is a collection of C++/Qt classes designed to make a
developer's life easy when trying to use the APIs provided by The Echo
Nest.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
install -d %{_target_platform}
cd %{_target_platform}
%cmake ..
%{__make}

%if %{with tests}
export PKG_CONFIG_PATH=$(pwd)
test "$(pkg-config --modversion libechonest)" = "%{version}"
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C %{_target_platform} install/fast \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README TODO
%attr(755,root,root) %{_libdir}/libechonest.so.*.*.*
# yes, SONAME is "libechonest.so.2.1"
%ghost %{_libdir}/libechonest.so.2.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/echonest/
%{_libdir}/libechonest.so
%{_pkgconfigdir}/libechonest.pc
