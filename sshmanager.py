import os
import json

class SshManager:
    """
    Manages SSH connections.
    """
    CONFIG_PATH = "~/.config/sshm.json"
    config = None

    def __init__(self):
        # Load configuration
        self._load_config_file()

    def _load_config_file(self):
        """ Load saved connections """
        if os.path.isfile(self._get_config_file_path()):
            with open(self._get_config_file_path(), 'r') as data_file:
                self.config = json.load(data_file)
        else:
            self.config = {}

    def _save_config_file(self):
        with open(self._get_config_file_path(), 'w') as data_file:
            json.dump(self.config, data_file, indent=4, sort_keys=True)

    def process(self, args):
        """
        Performs ssh-related actions.
        """
        if len(args) < 2:
            self._print_hierarchy(self.config)
        if len(args) == 2 and args[1] == '-l':
            self._print_list(self.config)
        elif len(args) == 2:
            connection = self._read_connection(args[1])
            if 'host' in connection:
                self._run(connection)
            else:
                self._print_hierarchy(connection)
        elif len(args) == 3 and args[1] == '-d':
            self._del_connection(args[2])
            self._save_config_file()
        elif len(args) == 3 and args[1] == '-p':
            connection = self._read_connection(args[2])
            if 'host' in connection:
                self._print_connection(connection)
            else:
                self._print_hierarchy(connection)
        elif len(args) == 3 and args[1] == '-f':
            self._print_hierarchy(self._filter_hierarchy(self.config, args[2]))
        elif len(args) == 3 and args[1] == '-l':
            self._print_list(self._filter_hierarchy(self.config, args[2]))
        elif len(args) == 3:
            self._write_connection(args[1], self._parse_connection_string(args[2]))
            self._save_config_file()
            self._print_connection(self._read_connection(args[1]))

    def _read_connection(self, path):
        current_conf = self.config
        for key in path.split('/'):
            if key in current_conf:
                current_conf = current_conf[key]
            else:
                current_conf = None
                break
        return current_conf

    def _write_connection(self, path, value):
        current_conf = self.config
        path_keys = path.split('/')[:-1]
        last_key = path.split('/')[-1]
        for key in path_keys:
            if not key in current_conf:
                current_conf[key] = {}
            current_conf = current_conf[key]
        current_conf[last_key] = value

    def _del_connection(self, path):
        current_conf = self.config
        path_keys = path.split('/')[:-1]
        last_key = path.split('/')[-1]
        for key in path_keys:
            if key in current_conf:
                current_conf = current_conf[key]
            else:
                current_conf = None
                break
        del(current_conf[last_key])

    def _run(self, connection):
        """ Run command with args """
        args = []
        command = 'ssh'

        if not 'host' in connection:
            print('Connection has no host defined')
            self._print_connection(connection)
            return

        host = connection['host']

        if 'user' in connection and connection['user'] is not None:
            host = '{}@{}'.format(connection['user'], connection['host'])
        if 'port' in connection and connection['port'] is not None:
            args.append('-p')
            args.append(connection['port'])

        args.append(host)

        if 'password' in connection and connection['password'] is not None:
            command = 'sshpass'
            args.insert(0, 'ssh')
            args.insert(0, connection['password'])
            args.insert(0, '-p')
            args.insert(0, 'sshpass')
        else:
            args.insert(0, 'ssh')

        if 'command' in connection and connection['command'] is not None:
            args.append(connection['command'])

        os.execvp(command, args)

    def _filter_hierarchy(self, item, fragment):
        items = {}
        for key in item:
            if 'host' in item[key] and fragment in key:
                items[key] = item[key]
            elif not 'host' in item[key]:
                subitems = self._filter_hierarchy(item[key], fragment)
                if len(subitems) > 0:
                    items[key] = subitems
        return items

    def _print_hierarchy(self, item, indent=0):
        for key in item:
            if not 'host' in item[key]:
                print("  " * indent + b'\xf0\x9f\x93\x82'.decode('utf8') + ' ' + key)
                self._print_hierarchy(item[key], indent + 1)
            else:
                print("  " * indent + b'\xf0\x9f\x92\xbb'.decode('utf8') + ' ' + key)

    def _print_list(self, item, path=''):
        for key in item:
            if path == '':
                mypath = key
            else:
                mypath = path + '/' + key
            if not 'host' in item[key]:
                self._print_list(item[key], mypath)
            else:
                print(mypath)

    def _print_connection(self, connection):
        for key in connection:
            if connection[key] is not None:
                print('{:<10}{}'.format(key + ':', connection[key]))

    def _parse_connection_string(self, connection_string):
        connection = {
            'user': None,
            'port': None,
            'host': connection_string,
            'command': None
        }
        if '@' in connection_string:
            (user, host) = connection_string.split('@')
            connection['user'] = user
            connection['host'] = host

        if ':' in connection['host']:
            (host, port) = connection['host'].split(':')
            connection['port'] = port
            connection['host'] = host

        return connection

    def _get_config_file_path(self):
        """ Return config file path"""
        return os.path.join(os.path.expanduser(self.CONFIG_PATH))
