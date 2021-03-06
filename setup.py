from distutils.core import setup
setup(
  name = 'bitforge',
  packages = ['bitforge', 'bitforge.utils'], # this must be the same as the name above
  version = '0.3',
  description = 'A python bitcoin library',
  author = 'Yemel Jardi',
  author_email = 'angel.jardi@gmail.com',
  url = 'https://github.com/muun/bitforge', # use the URL to the github repo
  download_url = 'https://github.com/muun/bitforge/tarball/0.3', # I'll explain this in a second
  keywords = ['bitcoin', 'altcoin'], # arbitrary keywords
  classifiers = [],
  install_requires = ['enum34==1.0.4', 'ecdsa==0.13', 'pytest==2.7.0', 'nose==1.3.6']
)
