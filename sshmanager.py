import os
import json

from pprint import pprint

class SshManager:
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
        if len(args) < 2:
            self._print_hierarchy(self.config)
        if len(args) == 2:
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
        args = ['ssh']

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

        if 'command' in connection and connection['command'] is not None:
            args.append(connection['command'])
        
        os.execvp('ssh', args)

    def _print_hierarchy(self, item, indent=0):
        for key in item:
            print("  " * indent + '-' + key)
            if not 'host' in item[key]:
                self._print_hierarchy(item[key], indent + 1)
    
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
