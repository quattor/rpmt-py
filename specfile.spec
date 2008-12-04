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


%prep
%setup

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

%files
%defattr(-,root,root)
@QTTR_BIN@/@COMP@
@QTTR_PYTHLIB@/rpmt/
%doc @QTTR_DOC@/
%doc @QTTR_MAN@/man@MANSECT@/@COMP@.@MANSECT@.gz
%dir @RPMT_CACHE@

%clean
rm -rf $RPM_BUILD_ROOT
