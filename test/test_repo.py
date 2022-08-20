import os
import unittest
from pathlib import Path
import glob
import shutil

from dotfile_manager.repo import DotfilesRepo



class DotfilesRepoTest(unittest.TestCase):

    def setUp(self):
        repo_path = Path(__file__).parent / 'test_data/dotfiles_repo'
        self.repo = DotfilesRepo(repo_path)
        self._clean()

    def tearDown(self):
        self._clean()

    def _clean(self):
        install_markers = glob.glob('topic_*_install_*.txt', recursive=False)
        for marker_file in install_markers:
            os.remove(marker_file)
        shutil.rmtree(self.repo.path/'generated', ignore_errors=True)

    def test_install_macos(self):
        self.repo.install('macos')
        self.assertTrue(os.path.exists('topic_a_install_macos.txt'))
        self.assertTrue(os.path.exists('topic_b_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_install_ubuntu(self):
        self.repo.install('ubuntu')
        self.assertTrue(os.path.exists('topic_a_install_ubuntu.txt'))
        self.assertTrue(os.path.exists('topic_b_install_ubuntu.txt'))
        self.assertFalse(os.path.exists('topic_c_install_macos.txt'))
        self.assertFalse(os.path.exists('topic_c_install_ubuntu.txt'))

    def test_setup(self):
        self.repo.setup()

        # Test that binaries are available:
        self.assertTrue(os.path.exists(self.repo.get_path()/'generated/bin/executable_from_a.sh'))
        self.assertTrue(os.path.exists(self.repo.get_path()/'generated/bin/executable_from_b.sh'))
        self.assertFalse(os.path.exists(self.repo.get_path()/'generated/bin/executable_from_c.sh'))

        # TODO(lgulich): Test that proper files are sourced:

        # Test that symlinks are available:
        self.assertTrue(os.path.exists('~/symlink_replica_from_a.txt'))
        self.assertTrue(os.path.exists('~/symlink_replica_from_b.txt'))
        self.assertFalse(os.path.exists('~/symlink_replica_from_c.txt'))



if __name__ == '__main__':
    unittest.main()