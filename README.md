# Console Chat Application

![Python Version](https://img.shields.io/badge/python-3.14-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![RPM Package](https://img.shields.io/badge/RPM-supported-orange)

A TCP-based console chat application with server-client architecture, designed for Oracle Linux with RPM packaging support.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Method 1: Install Pre-built RPM](#method-1-install-pre-built-rpm)
  - [Method 2: Manual Installation](#method-2-manual-installation)
- [Usage](#usage)
  - [Server](#server)
  - [Client](#client)
  - [Chat Commands](#chat-commands)
- [Building from Source](#building-from-source)
- [RPM Packaging](#rpm-packaging)
  - [Build Environment Setup](#build-environment-setup)
  - [Create Source Tarball](#create-source-tarball)
  - [Build RPM](#build-rpm)
  - [Install Built RPM](#install-built-rpm)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

- 🚀 **Multi-client support** (2+ simultaneous connections)  
- 🔒 **Private messaging** (`@username message` format)  
- ✔️ **Message delivery confirmation**  
- 📝 **Automatic logging** (`/var/log/chat_server.log`)  
- 📦 **RPM package** for easy deployment  
- 🔧 **Systemd service** integration (optional)

---

## Installation

### Prerequisites

- Oracle Linux 8/9  
- Python 3.14  
- RPM build tools (for packaging)

### Method 1: Install Pre-built RPM

```bash
sudo dnf install -y https://example.com/path/to/console-chat-1.0-1.el8.x86_64.rpm
```

---

## Usage

### Server

```bash
<python3.14 env name> console_chat_server.py [options]
```

**Options:**

- `-p PORT`, `--port PORT` : Specify port (default: 5555)  
- `-l FILE`, `--log FILE` : Set log file path

### Client

```bash
<python3.14 env name> console_chat_client.py [options]
```

**Options:**

- `-s HOST`, `--server HOST` : Server IP (default: 127.0.0.1)  
- `-p PORT`, `--port PORT` : Server port (default: 5555)  
- `-u NAME`, `--username NAME` : Your chat username

### Chat Commands

| Command         | Description        |
|----------------|--------------------|
| `@username msg` | Private message    |
| `exit`          | Quit application   |
| `/help`         | Show help          |

---

## Building from Source

### Install Dependencies

```bash
sudo dnf install -y python3-devel gcc openssl-devel
```

### Build and Install

```bash
./configure --enable-optimizations
make -j $(nproc)
sudo make altinstall
```

---

## RPM Packaging

### Build Environment Setup

```bash
sudo dnf install -y rpm-build rpmdevtools
rpmdev-setuptree
```

### Create Source Tarball

```bash
tar -czvf ~/rpmbuild/SOURCES/console-chat-1.0.tar.gz \
    --transform 's,^,console-chat-1.0/,' \
    *.py README.md
```

### Build RPM

```bash
rpmbuild -ba SPECS/console-chat.spec
```

### Install Built RPM

```bash
sudo dnf install -y ~/rpmbuild/RPMS/x86_64/console-chat-1.0-1.el8.x86_64.rpm
```

---

## File Structure

```
/usr/
├── bin/
│   ├── console_chat_server
│   └── console_chat_client
└── share/
    ├── doc/console-chat/
    │   └── README.md
    └── man/man1/
        ├── console_chat_server.1.gz
        └── console_chat_client.1.gz

/var/
└── log/chat_server.log
```

---

## Troubleshooting

### Common Issues

| Error                   | Solution                                                                 |
|-------------------------|--------------------------------------------------------------------------|
| Address already in use  | Change port: `console_chat_server -p 5556`                               |
| Connection refused      | Verify server is running: `systemctl status chat-server`                |
| Python 3.14 not found   | Install or link Python:<br>`sudo ln -s /usr/local/bin/python3.14 /usr/bin/python3.14` |

### Logs

- **Server logs**: `/var/log/chat_server.log`  
- **Client errors**: Printed to console

---

## License

This project is licensed under the MIT License.
