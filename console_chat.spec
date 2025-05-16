Name:           console-chat
Version:        1.0
Release:        1%{?dist}
Summary:        Console-based chat application with server and client

License:        MIT
URL:            https://github.com/your-repo/console-chat
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
Requires:       python3 >= 3.6

%description
A console-based chat application with server and client components.

%prep
%setup -q

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/doc/%{name}

install -m 755 console_chat_server.py %{buildroot}/usr/bin/console_chat_server
install -m 755 console_chat_client.py %{buildroot}/usr/bin/console_chat_client
install -m 644 README.md %{buildroot}/usr/share/doc/%{name}/

%files
/usr/bin/console_chat_server
/usr/bin/console_chat_client
/usr/share/doc/%{name}/README.md

%changelog
* Tue May 6 2025 Lev Gorbenko <levgor14@gmail.com> - 1.0-1
- Initial package build
