%define epoch		0

%define name		umfpack
%define NAME		UMFPACK
%define version		5.2.0
%define release		%mkrel 2
%define major		%{version}
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Routines for solving unsymmetric sparse linear systems
Group:		System/Libraries
License:	GPL
URL:		http://www.cise.ufl.edu/research/sparse/umfpack/
Source0:	http://www.cise.ufl.edu/research/sparse/umfpack/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/ufconfig/UFconfig-3.1.0.tar.gz
BuildRequires:	amd-devel >= 2.0.0
BuildRequires:	blas-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

%package -n %{libname}
Summary:	Library of routines for solving unsymmetric sparse linear systems
Group:		System/Libraries
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname %name 4.6
Obsoletes:	%mklibname %name 5.1.0
Obsoletes:	%mklibname %name 5

%description -n %{libname}
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{develname}
Summary:	C routines for solving unsymmetric sparse linear systems
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes: 	%mklibname %name 4.6 -d
Obsoletes:	%mklibname %name 5 -d

%description -n %{develname}
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
pushd Lib
    %make -f GNUmakefile CC=%__cc CFLAGS="$RPM_OPT_FLAGS -fPIC -I/usr/include/suitesparse" INC=
    %__cc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lamd -lblas -lm *.o
popd

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_libdir} 
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog Doc/License %{buildroot}%{_docdir}/%{name}

%clean
%__rm -rf %{buildroot}

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
