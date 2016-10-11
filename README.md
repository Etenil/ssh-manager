# SSH connections manager
Ssh manager in terminal

# Requirements
- Python3
- SSH

# Install

## With pip
```bash
pip install ssh-manager
```

## From source
```bash
python3 setup.py install
```

# Usage

## Listing connections
```bash
sshm.py
📂 amazon
  🖳 web1
  🖳 web2
📂 azure
  📂 web
    🖳 node1
    🖳 node2
  🖳 db
```

## List connections for a specific environment
```bash
sshm.py azure/web
🖳 node1
🖳 node2
```

## Connect to a server
```bash
sshm.py azure/web/node1
```

## View a connection value
```bash
sshm.py azure/web/node1
host: webnode1.azure.com
user: bob
```

## Set or add a connection
```bash
sshm.py amazon/db/server1 user@db1.amazon.com
user: user
host: db1.amazon.com
```

Supported connection string format:
```
[user@]host[:port]
```

Connections support calling commands, but these must be configured by editing the config file (see below).

## Delete a connection
```bash
sshm.py -d amazon/db/server1
```

# Config
`~/.config/sshm.json` file will be created after first run.
Edit it as you need.
