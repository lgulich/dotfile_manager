import os
import unittest
from pathlib import Path

from dotfile_manager.cli import create_parser, get_default_dotfiles_path


class CliTest(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_dotfiles_path(self):
        args = self.parser.parse_args(['-d', '/tmp/foo', 'install'])
        self.assertEqual(args.verb, 'install')
        self.assertEqual(args.dotfiles, Path('/tmp/foo'))

        args = self.parser.parse_args(['install'])
        self.assertEqual(args.verb, 'install')
        self.assertEqual(args.dotfiles, get_default_dotfiles_path())

    def test_install(self):
        args = self.parser.parse_args(['install'])
        self.assertEqual(args.verb, 'install')
        self.assertEqual(args.verb, 'install')
        self.assertEqual(args.project, None)

        args = self.parser.parse_args(['install', 'topic_a'])
        self.assertEqual(args.verb, 'install')
        self.assertEqual(args.project, 'topic_a')

    def test_setup(self):
        args = self.parser.parse_args(['setup'])
        self.assertEqual(args.verb, 'setup')


if __name__ == '__main__':
    unittest.main()
