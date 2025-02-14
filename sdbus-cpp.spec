#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	tests		# build without tests
#
Summary:	High-level C++ D-Bus library
Name:		sdbus-cpp
Version:	2.1.0
Release:	1
License:	LGPL
Source0:	https://github.com/Kistler-Group/sdbus-cpp/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ed9c6b8f1d93ecc9392b95b426b53cb1
URL:		https://github.com/Kistler-Group/sdbus-cpp
BuildRequires:	cmake >= 3.12
BuildRequires:	doxygen
BuildRequires:	expat-devel
%{?with_tests:BuildRequires:	gmock-devel >= 1.10.0}
BuildRequires:	libstdc++-devel
BuildRequires:	systemd-devel >= 236

%description
High-level C++ D-Bus library for Linux designed to provide easy-to-use
yet powerful API in modern C++

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package apidocs
Summary:	API documentation for %{name} library
Summary(pl.UTF-8):	Dokumentacja API biblioteki %{name}
Group:		Documentation
# if not arch-dependent
BuildArch:	noarch

%description apidocs
API documentation for %{name} library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki %{name}.

%package tools
Summary:	Stub code generator for sdbus-c++
Requires:	%{name} = %{version}-%{release}

%description tools
The stub code generator for generating the adapter and proxy
interfaces out of the D-Bus IDL XML description.

%prep
%setup -q

%build
mkdir -p build
cd build
%cmake ../ \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/sdbus-c++ \
	-DSDBUSCPP_BUILD_CODEGEN=ON \
	%{cmake_on_off apidocs SDBUSCPP_BUILD_DOCS} \
	%{cmake_on_off apidocs SDBUSCPP_BUILD_DOXYGEN_DOCS} \
	%{cmake_on_off tests SDBUSCPP_BUILD_TESTS}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libsdbus-c++.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsdbus-c++.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsdbus-c++.so
%{_includedir}/sdbus-c++
%{_pkgconfigdir}/sdbus-c++.pc
%{_pkgconfigdir}/sdbus-c++-tools.pc
%{_libdir}/cmake/sdbus-c++
%{_libdir}/cmake/sdbus-c++-tools

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/sdbus-c++

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sdbus-c++-xml2cpp
