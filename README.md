# SSH connections manager
Ssh manager in terminal

# Requirements
- Python3+
- SSH

# Install

## With pip
```bash
pip install ssh-manager
```

## From source
```bash
cd ssh-manager
pip install .
```

# Usage

## Listing connections
```bash
sshm.py
📂 amazon
  💻 web1
  💻 web2
📂 azure
  📂 web
    💻 node1
    💻 node2
  💻 db
```

It's also possible to list connections as an ascii list like so:
```bash
sshm.py -l
amazon/web1
amazon/web2
azure/web/node1
azure/web/node2
azure/db
```

## List connections for a specific environment
```bash
sshm.py azure/web
💻 node1
💻 node2
```

## Filter connections
Once you have configured many connections, it becomes a chore to find the one
that's needed. It's possible to filter out connections like so:

```bash
sshm.py -f node
📂 azure
  📂 web
    💻 node1
    💻 node2
```

This is also possible with as an ascii list like so:

```bash
sshm.py -l node
azure/web/node1
azure/web/node2
```

## Connect to a server
```bash
sshm.py azure/web/node1
```

## View a connection value
```bash
sshm.py -p azure/web/node1
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

## Adding passwords
If `sshpass` is installed on your machine, ssh-manager supports saving ssh passwords.
To add a passwords, edit `~/.config/sshm.json` and add a `password` value to your
connection.

Obviously this is not safe nor is it cyphered. Use with care.

# Bash completion for connections
This can be easily added with the following snippet in your `$HOME/.bashrc` file:

```bash
_sshm()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    things=`sshm.py -l`
    COMPREPLY=( $(compgen -W "$things" -- $cur) )
}
complete -F _sshm sshm.py
```
