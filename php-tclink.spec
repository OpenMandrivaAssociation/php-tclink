%define modname tclink
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A13_%{modname}.ini

Summary:	TCLink enables credit card processing via the TrustCommerce payment gateway
Name:		php-%{modname}
Version:	3.4.4
Release:	%mkrel 3
Group:		Development/PHP
License:	LGPL
URL:		http://www.trustcommerce.com/tclink.html
Source0:	http://www.trustcommerce.com/downloads/tclink-%{version}-php.tar.gz
Patch0:		TCLink-3.4.0-lib64.diff
Patch1:		tclink-correct_version.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	tclink-devel >= 3.4.4
BuildRequires:	openssl-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package provides a module for using TCLink directly from PHP scripts.
TCLink is a thin client library to allow your e-commerce servers to connect to
the TrustCommerce payment gateway.

%prep

%setup -q -n tclink-%{version}-php
%patch0 -p0
%patch1 -p0

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix} \
    --with-ssl=%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc LICENSE README tcexample.php tctest.php doc/*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
