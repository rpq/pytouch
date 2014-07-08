import glob
import os
import unittest
import tempfile
import pytouch

if __name__ == '__main__':

    class BaseDirectoryPathTest(unittest.TestCase):

        def test_base_path(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(base_path, bp.base_path)

        def test_name(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(name, bp.name)

        def test_empty_tail(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(None, bp.tail)

        def test_non_empty_tail(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            tail = 'bin'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)
            self.assertEqual(tail, bp.tail)

        def test_get_full_path(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            tail = 'bin'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)
            self.assertEqual('/usr/local/bin', bp.get_full_path())

        def test_is_symlink(self):
            base_path = '/tmp'
            tail = 'blablah.symlink'
            name = 'blah blah symlink'
            regular_file = '/tmp/blah'

            # clean up from old tests
            if os.path.isfile(regular_file):
                os.remove(regular_file)

            b = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)

            # clean up from old tests
            if os.path.islink(b.get_full_path()):
                os.remove(b.get_full_path())

            os.system('touch {}'.format(regular_file))
            self.assertTrue(os.path.isfile(regular_file))
            self.assertTrue(not os.path.islink(b.get_full_path()))
            os.symlink(regular_file, b.get_full_path())
            self.assertTrue(os.path.islink(b.get_full_path()))
            self.assertTrue(b.is_symlink())
            os.remove(regular_file)
            os.remove(b.get_full_path())

        def test_remove(self):
            name = 'blah'
            base_path = '/tmp'
            tail = 'blah'
            regular_file = '/tmp/blah'

            # clean up from old tests
            if os.path.isfile(regular_file):
                os.remove(regular_file)

            os.system('touch {}'.format(regular_file))
            self.assertTrue(os.path.isfile(regular_file))
            b = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)
            b.remove()
            self.assertTrue(not os.path.islink(b.get_full_path()))

    class PythonEnvironmentBinaryTest(object):

        def test_base_path(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(base_path, bp.base_path)

        def test_name(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(name, bp.name)

        def test_empty_tail(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path)
            self.assertEqual(None, bp.tail)

        def test_non_empty_tail(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            tail = 'bin'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)
            self.assertEqual(tail, bp.tail)

        def test_get_full_path(self):
            name = 'test usr/local'
            base_path = '/usr/local'
            tail = 'bin'
            bp = pytouch.BaseDirectoryPath(name=name,
                base_path=base_path, tail=tail)
            self.assertEqual('/usr/local/bin', bp.get_full_path())

    class PythonEnvironmentTest(unittest.TestCase):

        def test_base_path(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)
            self.assertEqual(p.base_path, base_path)

        def test_version(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)
            self.assertEqual(p.version, version)

        def test_compile_paths_binaries(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)

            self.assertEqual(len(p.binaries), 4)

        def test_compile_paths_binaries_name_equal(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)

            for binary in p.binaries:
                self.assertIn(binary.name,
                    [p['name'] for p in pytouch.PythonEnvironment.INIT_BINARIES])

        def test_compile_paths_binaries_name_equal(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)

            for binary in p.binaries:
                self.assertIn(binary.name,
                    [p['name'] for p in pytouch.PythonEnvironment.INIT_BINARIES])

        def test_compile_paths_binaries_tail_equal(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)

            for binary in p.binaries:
                self.assertIn(binary.tail,
                    [p['tail'] for p in pytouch.PythonEnvironment.INIT_BINARIES])

        def test_iter(self):
            base_path = '/tmp/test.symlink'
            version = '2.7.3'
            p = pytouch.PythonEnvironment(base_path=base_path,
                version=version)

            self.assertTrue(iter(p))

    class PythonSymlinkerTest(unittest.TestCase):

        def test_base_path(self):
            base_path = '/tmp'
            version = '2.7.1'
            env = pytouch.PythonEnvironment(base_path=base_path,
                version=version)
            sym = pytouch.PythonSymlinker(base_path=base_path,
                python_environment=env)
            self.assertEqual(sym.base_path, base_path)

        def test_python_environment(self):
            base_path = '/tmp'
            version = '2.7.1'
            env = pytouch.PythonEnvironment(base_path=base_path,
                version=version)
            sym = pytouch.PythonSymlinker(base_path=base_path,
                python_environment=env)
            self.assertEqual(sym.python_environment, env)

        def test_symlink_no_files_in_dir(self):
            base_python_path = os.path.expanduser(
                '~/.local/usr/local/python-2.7.5/')
            base_path = '/tmp'
            base_path_prefix = 'test_pytouch'
            base_path_abs = os.path.join(base_path, base_path_prefix)

            if not os.path.isdir(base_path_abs):
                os.mkdir(base_path_abs)

            env = pytouch.PythonEnvironment(base_path=base_python_path,
                    version='2.7.5')
            sym = pytouch.PythonSymlinker(base_path=base_path_abs,
                python_environment=env)
            sym.symlink()

            for binary in sym.python_environment.binaries:
                self.assertTrue(os.path.islink(
                    sym.generate_path(binary.get_file_name())))

            if os.path.isdir(base_path_abs):
                for binary in sym.get_symlink_paths():
                    os.remove(binary.get_full_path())
                os.rmdir(base_path_abs)

        def test_symlink_existing_files_in_dir(self):
            pass

    unittest.main()
