# Created by pyp2rpm-3.2.2
%global pypi_name ansible-runner

%if 0%{?fedora} || 0%{?rhel} > 7
%bcond_with    python2
%bcond_without python3
%else
%bcond_without python2
%bcond_with    python3
%endif

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        A tool and python library to interface with Ansible

License:        ASL 2.0
URL:            https://github.com/ansible/ansible-runner
# ansible-runner doesn't include the LICENSE file in the tarball on pythonhosted yet.
# pulling from github intil the pythonhosted tarball is updated
Source0:        https://files.pythonhosted.org/packages/source/a/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0:        https://github.com/ansible/%%{pypi_name}/archive/%%{version}/%%{pypi_name}-%%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  ansible >= 2.6
%if %{with python2}
BuildRequires:  python-daemon
%if 0%{?el7}
BuildRequires:  python-devel
BuildRequires:  python-mock
BuildRequires:  python-psutil
BuildRequires:  pexpect >= 4.6
BuildRequires:  python2-pytest
BuildRequires:  PyYAML
BuildRequires:  python-setuptools
BuildRequires:  python-six
%else
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist mock}
BuildRequires:  %{py2_dist psutil}
BuildRequires:  %{py2_dist pexpect} >= 4.6
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist PyYAML}
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist six}
%endif
%endif

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3dist(mock)
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(pexpect) >= 4.6
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)
BuildRequires:  python3dist(python-daemon)
BuildRequires:  python3dist(tox)
%endif

%description
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.

%if %{with python2}
%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}


Requires:       ansible >= 2.6
Requires:       python-daemon
%if 0%{?el7}
Requires:       pexpect >= 4.6
Requires:       python-psutil
Requires:       PyYAML
Requires:       python-setuptools
Requires:       python-six
%else
Requires:       %{py2_dist pexpect} >= 4.6
Requires:       %{py2_dist psutil}
Requires:       %{py2_dist PyYAML}
Requires:       %{py2_dist setuptools}
Requires:       %{py2_dist six}
%endif

%description -n python2-%{pypi_name}
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.
%endif

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       ansible >= 2.6
Requires:       python3-daemon
Requires:       python3dist(pexpect) >= 4.6
Requires:       python3dist(psutil)
Requires:       python3dist(pyyaml)
Requires:       python3dist(setuptools)
Requires:       python3dist(six)

%description -n python3-%{pypi_name}
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.

%if %{with python2}
%py2_install
cp %{buildroot}/%{_bindir}/ansible-runner %{buildroot}/%{_bindir}/ansible-runner-%{python2_version}
ln -s %{_bindir}/ansible-runner-%{python2_version} %{buildroot}/%{_bindir}/ansible-runner-2
%endif

%if %{with python3}
%py3_install
cp %{buildroot}/%{_bindir}/ansible-runner %{buildroot}/%{_bindir}/ansible-runner-%{python3_version}
ln -s %{_bindir}/ansible-runner-%{python3_version} %{buildroot}/%{_bindir}/ansible-runner-3
%endif

%check
%if %{with python2}
%{__python2} setup.py test ||:
%endif
%if %{with python3}
%{__python3} -m tox -e py3 --sitepackages
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE.md
%doc README.md
%{_bindir}/ansible-runner-2
%{_bindir}/ansible-runner-%{python2_version}
%{python2_sitelib}/ansible_runner
%{python2_sitelib}/test
%{python2_sitelib}/ansible_runner-%{version}-py?.?.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE.md
%doc README.md
%{_bindir}/ansible-runner-3
%{_bindir}/ansible-runner-%{python3_version}
%{python3_sitelib}/ansible_runner
%{python3_sitelib}/test
%{python3_sitelib}/ansible_runner-%{version}-py?.?.egg-info
%endif
%{_bindir}/ansible-runner

%changelog
* Wed Mar 20 2019 Dan Radez <dradez@redhat.com> - 1.3.0-1
- Updating to version 1.3
* Wed Feb 13 2019 Yatin Karel <ykarel@redhat.com> - 1.2.0-2
- Enable python2 build for CentOS <= 7
* Mon Feb 04 2019 Dan Radez <dradez@redhat.com> - 1.2.0-1
- Updating to version 1.2
- removing python 2 from the spec for F30
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Tue Oct 23 2018 Dan Radez <dradez@redhat.com> - 1.1.2-1
- Updating to version 1.1.2
* Wed Sep 12 2018 Dan Radez <dradez@redhat.com> - 1.1.0-1
- Updating to version 1.1.0
* Wed Jul 25 2018 Dan Radez <dradez@redhat.com> - 1.0.5-1
- Updating to version 1.0.5
* Wed Jul 25 2018 Dan Radez <dradez@redhat.com> - 1.0.4-4
- 1.0.4 requires pexepct 4.6
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Tue Jul 03 2018 Iryna Shcherbina - 1.0.4-2
- Fix Python 3 dependency from python2-ansible-runner
* Mon Jul 02 2018 Dan Radez <dradez@redhat.com> - 1.0.4-1
- Updating to version 1.0.4
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.3-4
- Rebuilt for Python 3.7
* Fri Jun 01 2018 Dan Radez <dradez@redhat.com> - 1.0.3-3
- skip py3 on non-fedora
* Thu May 31 2018 Dan Radez <dradez@redhat.com> - 1.0.3-1
- Updating to version 1.0.3
* Tue May 29 2018 Dan Radez <dradez@redhat.com> - 1.0.2-1
- Updating to version 1.0.2
- Package Requires versions updated
- added py3 support
* Fri May 11 2018 Dan Radez <dradez@redhat.com> - 1.0.1-2
- Adding conditionals so the same spec can be built on fedora and el7
* Fri May 04 2018 Dan Radez <dradez@redhat.com> - 1.0.1-1
- Initial package. Python 2 support only initially.
