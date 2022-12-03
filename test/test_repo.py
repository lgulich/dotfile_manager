import os
import unittest
from pathlib import Path
import glob
import shutil

from dotfile_manager.repo import Repo


class DotfilesRepoTest(unittest.TestCase):

    def setUp(self):
        repo_path = Path(__file__).parent / 'test_data/dotfiles_repo'
        self.repo = Repo(repo_path)
        self._clean()

    def tearDown(self):
        self._clean()

    def _clean(self):
        install_markers = glob.glob('topic_*_install_*.txt', recursive=False)
        for marker_file in install_markers:
            os.remove(marker_file)

        source_markers = glob.glob('topic_*_source.txt', recursive=False)
        for marker_file in source_markers:
            os.remove(marker_file)

        shutil.rmtree(self.repo.path / 'generated', ignore_errors=True)

    def test_install_all_macos(self):
        self.repo.install_all('macos')
        self.assertTrue(os.path.exists('topic_a_install_macos.txt'))
        self.assertTrue(os.path.exists('topic_b_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_install_macos(self):
        self.repo.install('topic_a', 'macos')
        self.assertTrue(os.path.exists('topic_a_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_b_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_install_all_ubuntu(self):
        self.repo.install_all('ubuntu')
        self.assertTrue(os.path.exists('topic_a_install_ubuntu.txt'))
        self.assertTrue(os.path.exists('topic_b_install_ubuntu.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_install_ubuntu(self):
        self.repo.install('topic_a', 'ubuntu')
        self.assertTrue(os.path.exists('topic_a_install_ubuntu.txt'))
        self.assertFalse(os.path.exists('topic_b_install_ubuntu.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_setup(self):
        self.repo.setup_all()

        # Test that generated symlinks to binaries are available:
        self.assertTrue(os.path.exists(self.repo.get_path() / 'generated/bin/executable_from_a.sh'))
        self.assertTrue(os.path.exists(self.repo.get_path() / 'generated/bin/executable_from_b.sh'))
        self.assertFalse(os.path.exists(self.repo.get_path() /
                                        'generated/bin/executable_from_c.sh'))

        # Test that generated symlinks to general files are available:
        home = Path.home()
        self.assertTrue(os.path.exists(home / 'symlink_replica_from_a.txt'))
        self.assertTrue(os.path.exists(home / 'symlink_replica_from_b.txt'))
        self.assertFalse(os.path.exists(home / 'symlink_replica_from_c.txt'))

        # Test that proper files are sourced:
        os.system(f'sh {self.repo.get_path()/"generated/sources.sh"}')
        self.assertTrue(os.path.exists('topic_a_source.txt'))
        self.assertTrue(os.path.exists('topic_b_source.txt'))
        self.assertFalse(os.path.exists('topic_c_source.txt'))


if __name__ == '__main__':
    unittest.main()
