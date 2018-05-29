# Created by pyp2rpm-3.2.2
%global pypi_name ansible-runner

Name:           python-%{pypi_name}
Version:        1.0.2
Release:        1%{?dist}
Summary:        A tool and python library to interface with Ansible

License:        ASL 2.0
URL:            https://github.com/ansible/ansible-runner
# ansible-runner doesn't include the LICENSE file in the tarball on pythonhosted yet.
# pulling from github intil the pythonhosted tarball is updated
# Source0:        https://files.pythonhosted.org/packages/source/a/%%{pypi_name}/%%{pypi_name}-%%{version}.tar.gz
Source0:        https://github.com/ansible/%{pypi_name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-daemon
%if 0%{?el7}
BuildRequires:  python-devel
BuildRequires:  python-mock
BuildRequires:  python-psutil
BuildRequires:  pexpect >= 4.5
BuildRequires:  python2-pytest
BuildRequires:  PyYAML
BuildRequires:  python-setuptools
BuildRequires:  python-six
%else
BuildRequires:  python2-devel
BuildRequires:  %{py2_dist mock}
BuildRequires:  %{py2_dist psutil}
BuildRequires:  %{py2_dist pexpect} >= 4.5
BuildRequires:  %{py2_dist pytest}
BuildRequires:  %{py2_dist PyYAML}
BuildRequires:  %{py2_dist setuptools}
BuildRequires:  %{py2_dist six}
%endif

%if 0%{?el7}
BuildRequires:  python34-devel
BuildRequires:  python34-mock
BuildRequires:  python34-psutil
BuildRequires:  python34-pexpect >= 4.5
BuildRequires:  python34-pytest
BuildRequires:  python34-PyYAML
BuildRequires:  python34-setuptools
BuildRequires:  python34-six
%else
BuildRequires:  python3-devel
BuildRequires:  python3dist(pexpect) >= 4.5
BuildRequires:  python3dist(psutil)
BuildRequires:  python3dist(python-daemon)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six)
%endif

%description
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}


Requires:       ansible >= 2.5
Requires:       python-daemon
%if 0%{?el7}
Requires:       pexpect >= 4.5
Requires:       python-psutil
Requires:       PyYAML
Requires:       python-setuptools
Requires:       python-six
%else
Requires:       %{py2_dist pexpect} >= 4.5
Requires:       %{py2_dist psutil}
Requires:       %{py2_dist PyYAML}
Requires:       %{py2_dist setuptools}
Requires:       %{py2_dist six}
%endif

%description -n python2-%{pypi_name}
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       ansible >= 2.5
Requires:       python-daemon
%if 0%{?el7}
Requires:       pexpect >= 4.5
Requires:       python-psutil
Requires:       PyYAML
Requires:       python-setuptools
Requires:       python-six
%else
Requires:       python3dist(pexpect) >= 4.5
Requires:       python3dist(psutil)
Requires:       python3dist(python-daemon)
Requires:       python3dist(pyyaml)
Requires:       python3dist(setuptools)
Requires:       python3dist(six)
%endif

%description -n python3-%{pypi_name}
Ansible Runner is a tool and python library that helps when interfacing with
Ansible from other systems whether through a container image interface, as a
standalone tool, or imported into a python project.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the subpackages' install first because the scripts in /usr/bin are
# overwritten with every setup.py install.

%py2_install
cp %{buildroot}/%{_bindir}/ansible-runner %{buildroot}/%{_bindir}/ansible-runner-%{python2_version}
ln -s %{_bindir}/ansible-runner-%{python2_version} %{buildroot}/%{_bindir}/ansible-runner-2

%py3_install
cp %{buildroot}/%{_bindir}/ansible-runner %{buildroot}/%{_bindir}/ansible-runner-%{python3_version}
ln -s %{_bindir}/ansible-runner-%{python3_version} %{buildroot}/%{_bindir}/ansible-runner-3

%check
%{__python2} setup.py test ||:
%{__python3} setup.py test ||:

%files -n python2-%{pypi_name}
%license LICENSE.md
%doc README.md
%{_bindir}/ansible-runner
%{_bindir}/ansible-runner-2
%{_bindir}/ansible-runner-%{python2_version}
%{python2_sitelib}/ansible_runner
%{python2_sitelib}/test
%{python2_sitelib}/ansible_runner-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}
%license LICENSE.md
%doc README.md
%{_bindir}/ansible-runner
%{_bindir}/ansible-runner-3
%{_bindir}/ansible-runner-%{python3_version}
%{python3_sitelib}/ansible_runner
%{python3_sitelib}/test
%{python3_sitelib}/ansible_runner-%{version}-py?.?.egg-info

%changelog
* Tue May 29 2018 Dan Radez <dradez@redhat.com> - 1.0.2-1
- Updating to version 1.0.2
- Package Requires versions updated
- added py3 support
* Fri May 11 2018 Dan Radez <dradez@redhat.com> - 1.0.1-2
- Adding conditionals so the same spec can be built on fedora and el7
* Fri May 04 2018 Dan Radez <dradez@redhat.com> - 1.0.1-1
- Initial package. Python 2 support only initially.
