%define name	umfpack
%define NAME	UMFPACK
%define version	5.1.0
%define release	%mkrel 1
%define major	%{version}
%define libname	%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Approximate minimum degree ordering
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/umfpack/
Source0:	http://www.cise.ufl.edu/research/sparse/umfpack/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/ufconfig/UFconfig-3.0.0.tar.gz
BuildRequires:	amd-devel >= 1.2-2mdk

%description
UMFPACK is a set of routines for solving unsymmetric sparse linear systems,
Ax=b, using the Unsymmetric MultiFrontal method. Written in ANSI/ISO C, with a
MATLAB (Version 6.0 and later) interface. Appears as a built-in routine (for
lu, backslash, and forward slash) in MATLAB.  Includes a MATLAB interface, a
C-callable interfance, and a Fortran-callable interface. Note that "UMFPACK" is
pronounced in two syllables, "Umph Pack". It is not "You Em Ef Pack".

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{develname}
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:  %{mklibname %name 4.6 -d}

%description -n %{develname}
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
cd Lib
    %{__make} -f GNUmakefile CFLAGS="$RPM_OPT_FLAGS -fPIC" INC=""
    gcc -shared -Wl,-soname,lib%{name}.so.%{major} -o ../Lib/lib%{name}.so.%{version} -lamd `ls *.o`
cd ..
cd Doc
    %{__make}
cd ..

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_libdir}
install -m 755 Lib/lib%{name}.so.%{version} %{buildroot}%{_libdir}
install -m 644 Lib/lib%{name}.a %{buildroot}%{_libdir}
(cd %{buildroot}%{_libdir} && ln -s lib%{name}.so.%{version} lib%{name}.so)

install -d -m 755 %{buildroot}%{_includedir}
install -m 644 Include/*.h %{buildroot}%{_includedir}

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.pdf %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_docdir}/%{name}
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a


