%define ver	138.0
%define rel	1
%define prefix	/usr

Summary:	Poker hand evalutor library
Name:		libpoker-eval
Version:	%ver
Release:	%rel
Copyright:	GPL
Source:         %{name}-%{version}.tar.bz2  
URL:            http://gna.org/projects/pokersource/
Group:		Games/Cards		
BuildRoot:	/tmp/%{name}-%{version}-%{rel}-root
Docdir:		%{prefix}/doc

%description
poker hand evaluator library
This package is a free (GPL) toolkit for writing programs which
simulate or analyze poker games.

Authors:
	Michael Maurer <mjmaurer@yahoo.com>
	Brian Goetz <brian@quiotix.com>
	Tim Showalter <tjs@psaux.com>
	Loic Dachary <loic@dachary.org>

%package devel

Summary: Poker hand evalutor library developpement files
Group: Games/Cards		
#Buildrequires: poker-eval

%description devel
poker hand evaluator library developpement files
This package is a free (GPL) toolkit for writing programs which
simulate or analyze poker games.

Authors:
	Michael Maurer <mjmaurer@yahoo.com>
	Brian Goetz <brian@quiotix.com>
	Tim Showalter <tjs@psaux.com>
	Loic Dachary <loic@dachary.org>

%prep
#%setup -n %{name}-%{version}
%setup -q -a 0

%build
# Needed for snapshot releases.
if [ ! -f configure ]; then
	if [ ! -f bootstrap ]; then
	       CFLAGS="$RPM_OPT_FLAGS" autoconf
        else
	       ./bootstrap
	fi
fi

CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{prefix} --disable-java

PATH=$PATH:.
( cd lib ; make build_tables ) ; make 

%install
[ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=${RPM_BUILD_ROOT}

%clean
(cd ..; rm -rf %{name}-%{version} ${RPM_BUILD_ROOT})

%files
%defattr(-,root,root)
%{prefix}/lib/libpoker-eval.so.*
%{prefix}/lib/libpoker-eval.so
%{prefix}/lib/libpoker-eval.a
%doc README COPYING NEWS

%files devel
%defattr (-, root, root)
%{prefix}/include/poker-eval/
%{prefix}/lib/pkgconfig/poker-eval.pc
%{prefix}/lib/libpoker-eval.la

%changelog
* Wed Oct 29 2004 Jean-Christophe Duberga <jeanchristophe.duber@free.fr>
- initial spec file for RedHat/Mandrake/... rpm based distributions.
