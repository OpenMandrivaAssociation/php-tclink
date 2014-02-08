%define modname tclink
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A13_%{modname}.ini

%define debug_package %{nil}

Summary:	TCLink enables credit card processing via the TrustCommerce payment gateway
Name:		php-%{modname}
Version:	3.4.5
Release:	19
Group:		Development/PHP
License:	LGPL
URL:		http://www.trustcommerce.com/tclink.html
Source0:	http://www.trustcommerce.com/downloads/tclink-%{version}-php.tar.gz
Patch0:		TCLink-3.4.0-lib64.diff
Patch1:		tclink-3.4.5-php-54x.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	tclink-devel >= 3.4.4
BuildRequires:	openssl-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package provides a module for using TCLink directly from PHP scripts.
TCLink is a thin client library to allow your e-commerce servers to connect to
the TrustCommerce payment gateway.

%prep

%setup -q -n tclink-%{version}-php

# fix strange attribs
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

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


%changelog
* Wed May 02 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-17mdv2012.0
+ Revision: 795003
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-16
+ Revision: 761123
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-15
+ Revision: 696375
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-14
+ Revision: 695320
- rebuilt for php-5.3.7

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-13
+ Revision: 667743
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-12
+ Revision: 646559
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-11mdv2011.0
+ Revision: 629747
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-10mdv2011.0
+ Revision: 628053
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-9mdv2011.0
+ Revision: 600185
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-8mdv2011.0
+ Revision: 588724
- rebuild

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 1:3.4.5-7mdv2010.1
+ Revision: 533372
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-6mdv2010.1
+ Revision: 514666
- rebuilt for php-5.3.2

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-5mdv2010.1
+ Revision: 511618
- rebuilt against openssl-0.9.8m

* Sun Feb 21 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-4mdv2010.1
+ Revision: 509093
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-3mdv2010.1
+ Revision: 485266
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-2mdv2010.1
+ Revision: 468093
- rebuilt against php-5.3.1

* Wed Oct 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.5-1mdv2010.0
+ Revision: 455472
- 3.4.5
- rebuild
- rebuild
- rebuilt against php-5.3.0RC2

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-10mdv2009.1
+ Revision: 346642
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-9mdv2009.1
+ Revision: 341515
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-8mdv2009.1
+ Revision: 321956
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-7mdv2009.1
+ Revision: 310225
- rebuilt against php-5.2.7

* Tue Jul 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-6mdv2009.0
+ Revision: 235883
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-5mdv2009.0
+ Revision: 200119
- rebuilt against php-5.2.6

* Tue Feb 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-4mdv2008.1
+ Revision: 166100
- rpmlint fixes

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-3mdv2008.1
+ Revision: 161955
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-2mdv2008.1
+ Revision: 107578
- restart apache if needed

* Sun Oct 28 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.4-1mdv2008.1
+ Revision: 102770
- 3.4.4

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-18mdv2008.0
+ Revision: 77463
- rebuilt against php-5.2.4

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-17mdv2008.0
+ Revision: 64307
- use the new %%serverbuild macro

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-16mdv2008.0
+ Revision: 39390
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-15mdv2008.0
+ Revision: 33785
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-14mdv2008.0
+ Revision: 21034
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 3.4.0-13mdv2007.0
+ Revision: 117539
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-12mdv2007.0
+ Revision: 78333
- fix deps
- bunzip patches

* Tue Nov 07 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-11mdv2007.0
+ Revision: 77402
- rebuilt for php-5.2.0

* Thu Nov 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-10mdv2007.1
+ Revision: 75369
- Import php-tclink

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-10
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-9mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-8mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-7mdk
- rebuilt for php-5.1.3

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-6mdk
- new group (Development/PHP) and iurt rebuild

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-5mdk
- rebuilt against php-5.1.2

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-4mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-3mdk
- rebuilt against php-5.1.0

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-2mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 1:3.4.0-1mdk
- rebuilt against php-5.1.0RC4
- fix versioning

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_3.4.0-0.RC1.3mdk
- rebuilt to provide a -debug package too

* Thu Oct 06 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_3.4.0-0.RC1.2mdk
- forgot to add that new libname (lib64) fix

* Mon Oct 03 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_3.4.0-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_3.4.0-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_3.4.0-1mdk
- 5.0.4

* Sat Apr 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_3.4.0-5mdk
- lib64 fixes

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_3.4.0-4mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_3.4.0-3mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_3.4.0-2mdk
- rebuild due to hardened-php-0.2.6

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_3.4.0-1mdk
- rebuilt for php-5.0.3

* Sat Sep 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.2_3.4.0-1mdk
- rebuilt for php-5.0.2

* Sun Aug 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.1_3.4.0-1mdk
- rebuilt for php-5.0.1

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.0_3.4.0-1mdk
- rebuilt for php-5.0.0
- major cleanups

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_3.4.0-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_3.4.0-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_3.4.0-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_3.4.0-1mdk
- initial cooker contrib (broken out from the tclink package)

