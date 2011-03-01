Summary: @DESCR@
Name: @NAME@
Version: @VERSION@
Vendor: EDG / CERN
Release: @RELEASE@
License: http://www.eu-datagrid.org/license.html
Group: @GROUP@/System
Source: @TARFILE@
BuildArch: noarch
BuildRoot: /var/tmp/%{name}-build
Packager: @AUTHOR@
URL: @QTTR_URL@

Requires: rpm >= 4.2.1
Requires: rpm-python

%description
@DESCR@

%package selinux
Summary: SELinux policy for rpmt-py
Group: @GROUP@/System

%description selinux
SELinux policy for rpmt-py, needed in RH6-based systems.

%prep
%setup

%build
make


%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

%post selinux
if [ "$1" == 1 ]
then
    semodule -i /usr/share/selinux/targeted/rpmt-py.pp
elif [ "$1" == 2 ]
    semodule -u /usr/share/selinux/targeted/rpmt-py.pp
fi

%preun selinux
if [ "$1" == 0 ]
then
    semodule -r rpmtpy
fi

%files
%defattr(-,root,root)
@QTTR_BIN@/@COMP@
@QTTR_PYTHLIB@/rpmt/
%doc @QTTR_DOC@/
%doc @QTTR_MAN@/man@MANSECT@/@COMP@.@MANSECT@.gz
%dir @RPMT_CACHE@

%clean
rm -rf $RPM_BUILD_ROOT

%files selinux
/usr/share/selinux/targeted/*
