#!/env/bin python

import os
import sys

class BaseDirectoryPath(object):

    def __init__(self, base_path, name, tail=None):
        self.base_path = base_path
        self.name = name
        self.tail = tail

    def get_full_path(self):
        return os.path.expanduser(os.path.join(self.base_path, self.tail))

    def exists(self):
        return os.path.exists(self.get_full_path())

    def is_symlink(self):
        return os.path.islink(self.get_full_path())

    def get_tail(self):
        return os.path.split(self.get_full_path())

    def remove(self):
        return os.remove(self.get_full_path())

class PythonEnvironmentBinary(object):

    def __init__(self, base_path, name, tail):
        self.name = name
        self.base_path = base_path
        self.tail = tail

    def get_full_path(self):
        return os.path.expanduser(os.path.join(self.base_path, self.tail))

    def get_file_name(self):
        return os.path.split(self.get_full_path())[1]

class PythonEnvironment(object):

    PYTHON_BIN_PATH = 'bin/python'
    PYTHON_EASY_INSTALL_BIN_PATH = 'bin/easy_install'
    PYTHON_PIP_BIN_PATH = 'bin/pip'
    PYTHON_VIRTUALENV_BIN_PATH = 'bin/virtualenv'

    INIT_BINARIES = [
        { 'name': 'Python Binary', 'tail': PYTHON_BIN_PATH },
        { 'name': 'Easy Install Binary',
            'tail': PYTHON_EASY_INSTALL_BIN_PATH },
        { 'name': 'PIP Binary', 'tail': PYTHON_PIP_BIN_PATH },
        { 'name': 'VirtualEnv Binary', 'tail': PYTHON_VIRTUALENV_BIN_PATH },
    ]

    def __init__(self, base_path, version):
        self.base_path = base_path
        self.version = version
        self.binaries = []
        self.compile_paths()

    def compile_paths(self):
        v = self.version
        b = self.base_path

        for init_binary in self.INIT_BINARIES:
            self.binaries.append(PythonEnvironmentBinary(
                base_path=b, **init_binary))

    def __iter__(self):
        return iter(self.binaries)

class PythonSymlinker(object):

    def __init__(self, base_path, python_environment):
        self.base_path = base_path
        self.python_environment = python_environment
        self.get_symlink_paths()

    def symlink(self):
        for binary in self.python_environment.binaries:
            temp_binary = BaseDirectoryPath(base_path=self.base_path,
                tail=binary.get_file_name(), name=binary.name)
            if temp_binary.exists() and not temp_binary.is_symlink():
                raise Exception('Error symlinking, base path symlink is not a symlink')
            if temp_binary.is_symlink():
                print '>> Removing old symlink, {} => {}'.format(
                    temp_binary.get_full_path(),
                    os.path.realpath(temp_binary.get_full_path()))
                temp_binary.remove()
            print '>> Symlinking, {} => {}'.format(
                temp_binary.get_full_path(),
                binary.get_full_path())
            #os.symlink(binary.get_full_path(), temp_binary.get_full_path())
            os.system('ln -s {} {}'.format(binary.get_full_path(),
                temp_binary.get_full_path()))

    def get_symlink_paths(self):
        self.symlink_paths = []
        for binary in self.python_environment.binaries:
            self.symlink_paths.append(
                BaseDirectoryPath(base_path=self.base_path,
                    tail=binary.get_file_name(), name=binary.name))
        return self.symlink_paths

    def generate_path(self, file_name):
        return os.path.join(self.base_path, file_name)

if __name__ == '__main__':
    def message_and_exit():
        print 'Please supply valid python version'
        exit()

    PYTHONS = [
        {
            'path': os.path.expanduser('~/.local/usr/local/python-2.7.5'),
            'version': '2.7.5'
        },
        {
            'path': os.path.expanduser('~/.local/usr/local/python-2.7.7'),
            'version': '2.7.7'
        },
    ]

    MAIN_LOCATION = '~/.local/bin'


    if len(sys.argv) != 2:
        message_and_exit()

    SWITCH_TO_VERSION_ARG = sys.argv[1]
    PYTHON_VERSION_VALID = any([p['version'] == SWITCH_TO_VERSION_ARG for p in PYTHONS])
    if not PYTHON_VERSION_VALID:
        message_and_exit()

    GOT_PYTHON = [p for p in PYTHONS if p['version'] == SWITCH_TO_VERSION_ARG][0]

    pyenv = PythonEnvironment(version=GOT_PYTHON['version'],
        base_path=GOT_PYTHON['path'])
    pysym = PythonSymlinker(base_path=MAIN_LOCATION,
        python_environment=pyenv)
    pysym.symlink()
