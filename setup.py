from __future__ import print_function
try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from distutils.dir_util import mkpath, copy_tree
import glob
import io
import zipfile


class DownloadAndInstall(install):
    user_options = install.user_options + [
            ('corpora-zip-url=', None,
                'URL pointing to .zip file of corpora data ' +
                '(defaults to current master on GitHub)')
            ]

    def initialize_options(self, *args, **kwargs):
        install.initialize_options(self, *args, **kwargs)
        self.corpora_zip_url = None

    def run(self):
        if self.corpora_zip_url is None:
            self.corpora_zip_url = \
                "https://github.com/dariusk/corpora/archive/master.zip"
        print("Installing corpora data from " + self.corpora_zip_url)
        mkpath("./corpora-download")
        resp = urlopen(self.corpora_zip_url).read()
        remote = io.BytesIO(resp)
        zf = zipfile.ZipFile(remote, "r")
        zf.extractall("corpora-download")
        try:
            data_dir = glob.glob("./corpora-download/*/data")[0]
        except IndexError:
            raise IndexError(
                "malformed corpora archive: expecting a subdirectory '*/data'")
        copy_tree(data_dir, "pycorpora/data")
        install.run(self)


setup(
    name="pycorpora",
    version="0.1.2",
    packages=['pycorpora'],
    package_data={'pycorpora': ['data/*/*.json', 'data/*/*/*.json']},
    author="Allison Parrish",
    author_email="allison@decontextualize.com",
    description="A Python wrapper for Darius Kazemi's Corpora Project",
    url="https://github.com/aparrish/pycorpora",
    license="LICENSE.txt",
    long_description=open("README.rst").read(),
    keywords="nlp corpus text language",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Artistic Software",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"],
    cmdclass={'install': DownloadAndInstall},
)
