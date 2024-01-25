%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:                 python-systemd
Version:              234
Release:              8%{?dist}
Summary:              Python module wrapping systemd functionality

License:              LGPLv2+
URL:                  https://github.com/systemd/python-systemd
Source0:              https://github.com/systemd/python-systemd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz


%bcond_with docs

BuildRequires:        systemd-devel
%if %{with python2}
BuildRequires:        python2-devel
BuildRequires:        python2-pytest
%endif # with python2

BuildRequires:        python3-devel
%if %{with doc}
BuildRequires:        python3-sphinx
%endif #{with doc}
BuildRequires:        web-assets-devel
BuildRequires:        python3-pytest

%global _description \
Python module for native access to the systemd facilities.\
Functionality includes sending of structured messages to the journal\
and reading journal files, querying machine and boot identifiers and a\
lists of message identifiers provided by systemd. Other functionality\
provided by libsystemd is also wrapped.

%description %_description

%if %{with python2}
%package -n python2-systemd
Summary:              %{summary}

%{?python_provide:%python_provide python2-systemd}
Provides:             systemd-python = %{version}-%{release}
Provides:             systemd-python%{?_isa} = %{version}-%{release}
Obsoletes:            systemd-python < 230
Recommends:           %{name}-doc

%description -n python2-systemd %_description
%endif # with python2

%package -n python3-systemd
Summary:              %{summary}

%{?python_provide:%python_provide python3-systemd}
Provides:             systemd-python3 = %{version}-%{release}
Provides:             systemd-python3%{?_isa} = %{version}-%{release}
Obsoletes:            systemd-python3 < 230
Recommends:           %{name}-doc

%description -n python3-systemd %_description

%if %{with doc}
%package doc
Summary:              HTML documentation for %{name}
Requires:             js-jquery

%description doc
%{summary}.
%endif #{with doc}

%prep
%autosetup -p1
sed -i 's/py\.test/pytest/' Makefile

%build
%if %{with python2}
make PYTHON=%{__python2} build
%endif # with python2
make LIBSYSTEMD_VERSION=`pkg-config --modversion libsystemd | sed 's/^\([0-9]*\)\(.*\)$/\1/'` PYTHON=%{__python3} build      # https://bugzilla.redhat.com/show_bug.cgi?id=1862714
%if %{with doc}
make PYTHON=%{__python3} SPHINX_BUILD=sphinx-build-3 sphinx-html
rm -r build/html/.buildinfo build/html/.doctrees
%endif #{with doc}

%install
%if %{with python2}
%make_install PYTHON=%{__python2}
%endif # with python2
%make_install PYTHON=%{__python3}
%if %{with doc}
mkdir -p %{buildroot}%{_pkgdocdir}
cp -rv build/html %{buildroot}%{_pkgdocdir}/
ln -vsf %{_jsdir}/jquery/latest/jquery.min.js %{buildroot}%{_pkgdocdir}/html/_static/jquery.js
cp -p README.md NEWS %{buildroot}%{_pkgdocdir}/
%endif #{with doc}

%check
# if the socket is not there, skip doc tests
test -f /run/systemd/journal/stdout || \
     sed -i 's/--doctest[^ ]*//g' pytest.ini
%if %{with python2}
make PYTHON=%{__python2} check
%endif # with python2
make TESTFLAGS="-k 'not test_notify_no_socket'" PYTHON=%{__python3} check    # Skip test that is failing due to permissions - https://bugzilla.redhat.com/show_bug.cgi?id=1793022

%if %{with python2}
%files -n python2-systemd
%license LICENSE.txt
%exclude %{_pkgdocdir}/html
%{python2_sitearch}/systemd/
%{python2_sitearch}/systemd_python*.egg-info
%endif # with python2

%files -n python3-systemd
%license LICENSE.txt
%exclude %{_pkgdocdir}/html
%{python3_sitearch}/systemd/
%{python3_sitearch}/systemd_python*.egg-info

%if %{with doc}
%files doc
%license LICENSE.txt
%doc %{_pkgdocdir}
%doc %{_pkgdocdir}/html
%endif #{with doc}

%changelog
* Thu Jan 25 2024 Skip Grube <regrube@ncsu.edu> - 234
- Fixes for systemd version and test failure - research from Michael Young.

* Mon Jul 09 2018 Charalampos Stratakis <cstratak@redhat.com> - 234-8
- Conditionalize the python2 subpackage

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 234-7
- Conditionalize the doc subpackage

* Mon Jun 25 2018 Petr Viktorin <pviktori@redhat.com> - 234-6
- Allow Python 2 for build

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 234-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov  1 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-4
- Use separate license and documentation directories

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 234-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 234-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 234-1
- Update to latest version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 232-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 232-2
- Rebuild for Python 3.6

* Thu Sep 22 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 232-1
- Update to latest version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 231-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 231-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@bupkis> - 231-4
- Bugfixes for seek_monotonic and Python 2 compat

* Sun Nov 15 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 231-3
- Split out doc subpackage (#1242619)
- Do not allow installation of python-systemd in different versions

* Sat Nov 07 2015 Robert Kuska <rkuska@redhat.com> - 231-2
- Rebuilt for Python3.5 rebuild

* Tue Oct 27 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 231-1
- Update to latest version

* Mon Jul  6 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@laptop> - 230-1
- Initial packaging
