%define NAME	UMFPACK
%define major	5
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	Routines for solving unsymmetric sparse linear systems
Name:		umfpack
Version:	5.6.2
Release:	6
Epoch:		1
Group:		System/Libraries
License:	GPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/umfpack/
Source0:	http://www.cise.ufl.edu/research/sparse/umfpack/%{NAME}-%{version}.tar.gz
BuildRequires:	amd-devel
BuildRequires:	cholmod-devel
BuildRequires:	blas-devel
BuildRequires:	camd-devel
BuildRequires:	colamd-devel
BuildRequires:	ccolamd-devel
BuildRequires:	suitesparse-common-devel >= 4.0.0

%description
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

%package -n %{libname}
Summary:	Library of routines for solving unsymmetric sparse linear systems
Group:		System/Libraries
%define	oldname	%{mklibname %{name} 5.6.2}
%rename		%{oldname}

%description -n %{libname}
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for solving unsymmetric sparse linear systems
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Requires:	blas-devel
Requires:	amd-devel
Requires:	suitesparse-common-devel >= 4.0.0

%description -n %{devname}
UMFPACK provides a set of routines for solving unsymmetric sparse
linear systems Ax=b using the Unsymmetric MultiFrontal method. It is
written in ANSI/ISO C. Note that "UMFPACK" is pronounced in two
syllables, "Umph Pack"; it is not "You Em Ef Pack".

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
cd %{NAME}
find . -perm 0640 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
pushd Lib
    %make -f GNUmakefile CC=%{__cc} CFLAGS="%{optflags} -fPIC -I%{_includedir}/suitesparse" INC=
    %{__cc} %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lsuitesparseconfig -lamd -lblas -lm -lcholmod -lcamd -lcolamd -lccolamd *.o
popd

%install
cd %{NAME}

for f in Lib/*.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Doc/*.txt Doc/*.pdf Doc/ChangeLog Doc/License %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}.a
