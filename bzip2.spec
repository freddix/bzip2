# based on PLD Linux spec git://git.pld-linux.org/packages/bzip2.spec
Summary:	High-quality data compressor
Name:		bzip2
Version:	1.0.6
Release:	6
License:	BSD-like
Group:		Core/Applications
Source0:	http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	00b516f4704d4a7cb50a1d97e6e8e15b
Patch0:		%{name}-libtoolizeautoconf.patch
Patch1:		%{name}-bzgrep.patch
Patch2:		%{name}-bzip2recover.patch
URL:		http://www.bzip.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags   -O3

%description
bzip2 is a freely available, patent free, high-quality data compressor.
It typically compresses files to within 10% to 15% of the best
available techniques (the PPM family of statistical compressors),
whilst being around twice as fast at compression and six times faster
at decompression.

%package libs
Summary:	libbz2 library
Group:		Core/Libraries
%ifarch %{x8664}
Provides:	libbz2.so.1.0()(64bit)
%else
Provides:	libbz2.so.1.0
%endif

%description libs
libbz2 library.

%package devel
Summary:	libbz2 library header files
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Libbz2 library header files.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__libtoolize}
%{__automake}
%{__autoconf}
%configure \
	CFLAGS="%{rpmcflags} -D_FILE_OFFSET_BITS=64" \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# standard soname was libbz2.so.1.0, libtoolizeautoconf patch broke it,
# but ABI has not changed - provide symlink for binary compatibility
ln -sf libbz2.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libbz2.so.1.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES LICENSE README*
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libbz2.so.1
%attr(755,root,root) %{_libdir}/libbz2.so.*.*.*
%attr(755,root,root) %{_libdir}/libbz2.so.1.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbz2.so
%{_libdir}/libbz2.la
%{_includedir}/*.h

