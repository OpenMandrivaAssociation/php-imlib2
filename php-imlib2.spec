%define modname imlib2
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A37_%{modname}.ini

Summary:	Provides an image manipulation interface using libimlib2 for PHP
Name:		php-%{modname}
Version:	0.1.00
Release:	%mkrel 27
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/imlib2
Source0:	imlib2-%{version}.tar.bz2
Source1:	%{inifile}.bz2
Patch0:		imlib2-0.1.00-lib64.diff
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	imlib2-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
imlib2 is a very fast image manipulation library, but without the support for
as many image formats as other libraries such as imagemagick.

%prep

%setup -q -n imlib2-%{version}
%patch0 -p0

bzcat %{SOURCE1} > %{inifile}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

# nuke rpath
chrpath -d %{soname}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/

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
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc docs CREDITS imlib2.php readme.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
