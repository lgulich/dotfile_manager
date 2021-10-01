from pathlib import Path

import setuptools

from src.dotfile_manager.version import __version__

file_path = Path(__file__)
with open(file_path.parent / 'README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='dotfile_manager',
    version=__version__,
    author='Lionel Gulich',
    author_email='lgulich@ethz.ch',
    url='https://github.com/lgulich/dotfile_manager',
    description= 'A tool for managing dotfiles for linux and macos.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    install_requires=['pyyaml'],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
    ],
    license='Closed',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    include_package_data=True,
    package_data={'dotfile_manager': ['py.typed']},
    scripts=[
        'scripts/dotfile_manager',
    ],
    python_requires='>=3.8',
)
