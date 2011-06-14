%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# -- header -----------------------------------------------------------------------

Name:		    bonkbot
Version:        1.0.4
Release:	    1%{?dist}
Summary:	    Python IRC chat bot

Group:		    Development/Tools
License:	    GPLv2
URL:		    https://github.com/jdob/bonkbot
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires:  python-setuptools
Requires:	    python >= 2.4


%description
Pluggable Python based IRC client.


%prep
%setup -q


# -- build -----------------------------------------------------------------------

%build
pushd src
%{__python} setup.py build
popd


# -- install ---------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# Python setup
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
rm -f $RPM_BUILD_ROOT%{python_sitelib}/bonkbot*egg-info/requires.txt

# Configuration
mkdir -p %{buildroot}/etc/bonkbot
cp etc/bonkbot/bonk.conf %{buildroot}/etc/bonkbot/

mkdir -p %{buildroot}/etc/bonkbot/conf.d
cp etc/bonkbot/conf.d/* %{buildroot}/etc/bonkbot/conf.d/

mkdir -p %{buildroot}/etc/bonkbot/plugins
cp src/plugins/* %{buildroot}/etc/bonkbot/plugins/


# -- clean -----------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT


# -- files -----------------------------------------------------------------------

%files
%defattr(-,root,root,-)
%{python_sitelib}/bonkbot/*
%{python_sitelib}/bonkbot*.egg-info
%config(noreplace) /etc/bonkbot/bonk.conf
%{_sysconfdir}/bonkbot/plugins/*
%{_sysconfdir}/bonkbot/conf.d/*
%{_bindir}/bonkbot


# -- changelog -------------------------------------------------------------------

%changelog
* Tue Jun 14 2011 Jay Dobies <jason.dobies@redhat.com> 1.0.4-1
- Minor code formatting cleanups (jason.dobies@redhat.com)
- Fixed decorators to store the wrapped function name for logging purposes
  (jason.dobies@redhat.com)
- Fixed config lookup (jason.dobies@redhat.com)
- Added overridable log file location (jason.dobies@redhat.com)
- Fixes to karma plugin (jason.dobies@redhat.com)

* Sun May 15 2011 Jay Dobies <jason.dobies@redhat.com> 1.0.3-1
- Missed binary in the files list (jason.dobies@redhat.com)

* Sun May 15 2011 Jay Dobies <jason.dobies@redhat.com> 1.0.2-1
- Need to copy conf.d files, not the dir itself (jason.dobies@redhat.com)

* Sun May 15 2011 Jay Dobies <jason.dobies@redhat.com> 1.0.1-1
- new package built with tito


