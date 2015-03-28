try:
	from setuptools import setup
	from setuptools.command.install import install
except ImportError:
	from distutils.core import setup
	from distutils.command.install import install
from distutils.dir_util import mkpath, copy_tree
import io, urllib2, zipfile, glob

class DownloadAndInstall(install):
	user_options = install.user_options + [
			('corpora-zip-url=', None, 'URL pointing to .zip file of corpora data ' + \
					'(defaults to current master on GitHub)')
			]
	def initialize_options(self, *args, **kwargs):
		install.initialize_options(self, *args, **kwargs)
		self.corpora_zip_url = None
	def run(self):
		if self.corpora_zip_url is None:
			self.corpora_zip_url = \
				"https://github.com/dariusk/corpora/archive/master.zip"
		print "Installing corpora data from " + self.corpora_zip_url
		mkpath("./corpora-download")
		resp = urllib2.urlopen(self.corpora_zip_url).read()
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
	version="0.1.1",
	packages=['pycorpora'],
	package_data={'pycorpora': ['data/*/*.json', 'data/*/*/*.json']},
	author="Allison Parrish",
	author_email="allison@decontextualize.com",
	description="A Python wrapper for Darius Kazemi's Corpora Project",
	url="https://github.com/aparrish/pycorpora",
	license="LICENSE.txt",
	long_description=open("README.rst").read(),
	keywords="nlp corpus text language",
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Intended Audience :: Developers",
		"Intended Audience :: Education",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: MIT License",
		"Natural Language :: English",
		"Topic :: Artistic Software",
		"Topic :: Scientific/Engineering :: Artificial Intelligence"],
	cmdclass={'install': DownloadAndInstall},
)
