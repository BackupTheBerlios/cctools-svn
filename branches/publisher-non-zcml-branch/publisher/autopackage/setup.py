from distutils.core import setup
import platform

# packages to include with the bootstrap script
packages = []

if platform.system().lower() == 'windows':
    import py2exe

setup(name='apBoot',
      version='1.0',
      description = "Bootstrap script",
      long_description="",
      url='http://creativecommons.org',
      author='Nathan R. Yergler',
      author_email='nathan@creativecommons.org',
      scripts=['apboot.py',],
      windows=['apboot.py',],
      packages=packages,
      )
