# -*- python -*-     -*- encoding: Latin-1 -*-
#
# Extention of distutils for straw.
#
# Written by Terje Røsten <terjeros@phys.ntnu.no> Nov. 2003.


import sys
import os
import os.path
import re
import glob
import types
import commands

from distutils.core import Command
from distutils.command.build import build
from distutils.command.install import install
from distutils.command.install_data import install_data
from distutils.dep_util import newer
from distutils.dist import Distribution
from distutils.core import setup


try:
    from dsextras import BuildExt
except ImportError:
    try:
        from gtk.dsextras import BuildExt
    except ImportError:
        sys.exit('Error: Can not find dsextras or gtk.dsextras')

import msgfmt

class straw_build(build):
    def has_po_files(self):
        return self.distribution.has_po_files()

    def has_desktop_file(self):
        return self.distribution.has_desktop_file()

    sub_commands = []
    sub_commands.extend(build.sub_commands)
    sub_commands.append(('build_mo', has_po_files))
    sub_commands.append(('build_desktop', has_desktop_file))

class build_mo(Command):

    description = 'build binary message catalog'

    user_options = [
        ('build-base=', 'b', 'directory to build to')]

    def initialize_options(self):
        self.build_base = None
        self.translations = self.distribution.translations
        self.force = None
    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'),
                                   ('force', 'force'))
    def run(self):
        self.announce('Building binary message catalog')
        if self.distribution.has_po_files():
            for mo, po in self.translations:
                dest = os.path.normpath(self.build_base + '/' + mo)
                self.mkpath(os.path.dirname(dest))
                if not self.force and not newer(po, dest):
                    self.announce("not building %s (up-to-date)" % dest)
                else:
                    msgfmt.make(po, dest)

class straw_install(install):
    user_options = []
    user_options.extend(install.user_options)    
    _user_options = [
        ('sysconfdir=', None, 'specify SYSCONFDIR [default=PREFIX/etc]'),
        ('disable-modules-check', None,
         'do not check that necessary modules is installed'),
        ('enable-modules-check', None,
         'check that necessary modules is installed  [default]'),
        ('disable-schemas-install', None,
         'do not install schema files. Setting the variable '
         'GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL will prevent this too.'),
        ('enable-schemas-install', None,
         'install schema files. [default]'),
        ('with-gconftool=', None,
         'specify path to the gconftool executable. Can also be set by'
         'the variable GCONFTOOL. [default=gconftool-2]' ),
        ('with-gconf-source=', None,
         'Config database for installing schema files. Can also be set by '
         'the variable GCONF_SCHEMA_CONFIG_SOURCE. Setting to `auto\' is '
         'short for `$(gconftool-2 --get-default-source)\'. '),
        ('with-gconf-schema-file-dir=', None,
         'Directory for installing schema files. Can also be set by the '
         'variable GCONF_SCHEMA_FILE_DIR. [default=SYSCONFDIR/gconf/schemas]'),
        ('with-desktop-file-dir=', None,
         'specify directory for the straw.desktop file [default=PREFIX/share/applications')]
    

    user_options.extend(_user_options)

    boolean_options = []
    boolean_options.extend(install.boolean_options)
    boolean_options.extend([
        'disable-schemas-install', 'disable-modules-check' ])

    negative_opt = {}
    try:
        negative_opt.update(install.negative_opt)
    except AttributeError:
        pass
    negative_opt.update({'enable-schemas-install' : 'disable-schemas-install',
                         'enable-modules-check' : 'disable-modules-check'})
    
    def initialize_options(self):
        install.initialize_options(self)
        self.prefix = '/usr/local'
        # if self.sysconfdir is not a absolute path it will
        # be prefixed by self.prefix
        self.sysconfdir = 'etc'
        self.disable_modules_check = 0
        self.disable_schemas_install = os.environ.get(
            'GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL', 0)
        self.with_gconftool = os.environ.get(
            'GCONFTOOL', commands.getoutput('which gconftool-2'))
        self.with_gconf_source = os.environ.get(
            'GCONF_SCHEMA_CONFIG_SOURCE', 'auto')
        self.with_gconf_schema_file_dir = os.environ.get(
            'GCONF_SCHEMA_FILE_DIR', None)
        self.with_desktop_file_dir = 'share/applications'
        
    def finalize_options(self):

        if self.prefix == 'auto':
            cmd = 'pkg-config --variable=prefix libgnome2.0'
            err, val = commands.getstatusoutput(cmd)
            if not err:
                self.prefix = val
            else:
                sys.exit('Cannot find prefix: %s. pkgconfig not installed?'
                         % val)

        self.sysconfdir = os.path.join(self.prefix, self.sysconfdir)
        if self.root:
            self.sysconfdir = os.path.normpath(self.root + '/' + self.sysconfdir)

        if self.root and self.with_gconf_schema_file_dir:
            self.with_gconf_schema_file_dir = os.path.normpath(
                self.root + '/' + self.with_gconf_schema_file_dir)

        if not self.disable_schemas_install:
            # Sanity check
            if not os.path.exists(self.with_gconftool):
                print 'gconftool-2 executable not found in your path ' + \
                      '- should be installed with GConf'
                sys.exit(1)

            if self.with_gconf_source == 'auto':
                cmd = '%s --get-default-source' % self.with_gconftool
                self.with_gconf_source = commands.getoutput(cmd)

            if self.with_gconf_source and self.root:
                self.with_gconf_source = self.with_gconf_source.replace(
                        'xml::','xml::%s' % self.root)
            elif not self.with_gconf_source:
                fmt = 'xml::%s/gconf/gconf.xml.defaults'
                self.with_gconf_source = fmt % self.sysconfdir

        # Run this after we (possibly) have changed prefix.
        install.finalize_options(self)
        
    def has_gconf(self):
        return self.distribution.has_gconf()

    def has_modules_check(self):
        return self.distribution.has_modules_check()

    def has_config_files(self):
        return self.distribution.has_config_files()

    def has_po_files(self):
        return self.distribution.has_po_files()

    def has_desktop_file(self):
        return self.distribution.has_desktop_file()

    sub_commands = []
    # Check modules before we start to install files
    sub_commands.append(('install_modules_check', has_modules_check))
    sub_commands.extend(install.sub_commands)
    sub_commands.append(('install_mo', has_po_files))
    sub_commands.append(('install_config', has_config_files))
    sub_commands.append(('install_gconf', has_gconf))
    sub_commands.append(('install_desktop', has_desktop_file))

class install_mo(install_data):

    description = 'install generated binary message catalog'

    def initialize_options(self):
        install_data.initialize_options(self)
        self.translations = self.distribution.translations
        self.has_po_files = self.distribution.has_po_files
        self.install_dir = None
        self.build_dir = None
        self.skip_build = None
        self.outfiles = []
        
    def finalize_options(self):
        install_data.finalize_options(self)
        self.set_undefined_options('build_mo', ('build_base', 'build_dir'))
        self.set_undefined_options('install',
                                   ('install_data', 'install_dir'),
                                   ('skip_build', 'skip_build'))
    def run(self):
        if not self.skip_build:
            self.run_command('build_mo')
        if self.has_po_files():
            for mo, po in self.translations:
                src = os.path.normpath(self.build_dir + '/' + mo)
                if not os.path.isabs(mo):
                    dest =  os.path.normpath(self.install_dir + '/' + mo)
                elif self.root:
                    dest = self.root + mo
                else:
                    dest = mo
                self.mkpath(os.path.dirname(dest))
                (out, _) = self.copy_file(src, dest)
                self.outfiles.append(out)

    def get_outputs (self):
        return self.outfiles

    def get_inputs (self):
        return [ po for mo, po in self.translations ]
        
class install_gconf(Command):

    description = 'install generated gconf files'
    user_options = []

    def initialize_options(self):
        self.disable_schemas_install = None
        self.with_gconftool = None
        self.with_gconf_source = None
        self.with_gconf_schema_file_dir = None

    def finalize_options(self):
        self.set_undefined_options(
            'install',
            ('disable_schemas_install', 'disable_schemas_install'),
            ('with_gconftool', 'with_gconftool'),
            ('with_gconf_source', 'with_gconf_source'))
        self.set_undefined_options(
            'install_config',
            ('with_gconf_schema_file_dir', 'with_gconf_schema_file_dir'))      

    def install_schema(self):
        os.putenv('GCONF_CONFIG_SOURCE', self.with_gconf_source)
        cmd = '%s --makefile-install-rule data/straw.schemas'\
                % self.with_gconftool
        err, out = commands.getstatusoutput(cmd)
        if out:
            print out
        if err:
            print 'Error: installation of gconf schema files failed: %s' % out

    def run(self):
        if not self.disable_schemas_install:
            self.install_schema()

    def get_outputs(self):
        return []

    def get_inputs(self):
        return []

class install_config(install_data):
    '''
    Same as install_data but using <sysconfdir> instead of
    <prefix>. If <sysconfdir> is not absolute, <prefix> is prefixed
    <sysconfdir>. If the tuple has length 3 and the option in the last
    element is known, the value of the option is used as dest
    directory. On the other hand if option is None, the value of the
    option is set to value of the first element in the tuple.
    '''
    
    description = 'install config files'

    user_options = [
        ('sysconfdir', None,
         'specify SYSCONFDIR [default=PREFIX/etc]')]        

    def initialize_options(self):
        install_data.initialize_options(self)
        self.sysconfdir = None
        self.data_files = self.distribution.config_files
        self.with_gconf_schema_file_dir = None

    def option_to_dir(self):
        data_files = []
        for tup in self.data_files:
            if len(tup) == 2:
                data_files.append(tup)            
            elif len(tup) == 3:
                option = tup[2].replace('-','_')
                dest = getattr(self, option, None)
                if dest:
                    data_files.append((dest, tup[1]))
                else:
                    data_files.append((tup[0], tup[1]))
                    dest = os.path.normpath(self.install_dir + '/' + tup[0])
                    setattr(self, option, dest)

        self.data_files = data_files

    def finalize_options(self):
        install_data.finalize_options(self)
        self.set_undefined_options(
            'install',
            ('sysconfdir', 'sysconfdir'),
            ('with_gconf_schema_file_dir', 'with_gconf_schema_file_dir'))

        self.install_dir = self.sysconfdir
        self.option_to_dir()
        
class install_modules_check(Command):

    description = 'check that all necessary Python modules are installed'

    user_options = [
        ('disable-modules-check', None,
         'do not check that necessary modules is installed'),
        ('enable-modules-check', None,
         'check that necessary modules is installed  [default]')]

    boolean_options = []
    boolean_options.append('disable-modules-check')

    negative_opt = {'enable-modules-check' : 'disable-modules-check'}

    def initialize_options(self):
        self.disable_modules_check = None
        self.modules_check = self.distribution.modules_check

    def finalize_options(self):
        self.set_undefined_options(
            'install',
            ('disable_modules_check', 'disable_modules_check'))

    def run(self):
        if self.disable_modules_check:
            self.announce('Modules not checked')
        elif self.modules_check:
            self.modules_check()
            self.announce('All nescessary modules installed')

    def get_outputs(self):
        return []
    def get_inputs(self):
        return []

class build_desktop(Command):

    description = 'builds the desktop file'
    user_options = [('build-base=', 'b', 'directory to build to')]

    def initialize_options(self):
        self.build_base = None
        self.intl_merge = commands.getoutput('which intltool-merge')

    def finalize_options(self):
        if not os.path.exists(self.intl_merge):
            sys.exit('intltool-merge does not exist in your PATH. ' + \
                     'Make sure it exists in your PATH..')
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'))

    def run(self):
        self.announce("Building straw.desktop file....")
        dest = os.path.normpath(os.path.join(self.build_base, 'share/applications'))
        self.mkpath(dest, 1)
        cmd = '%s -d -u po straw.desktop.in %s/straw.desktop' % (self.intl_merge, dest)
        err, val = commands.getstatusoutput(cmd)
        if err:
            sys.exit('Error merging translation in straw.desktop')
        print "%s" % val


class install_desktop(install_data):

    description = 'Installs generated desktop file'

    user_options = [
        ('with-desktop-file-dir=', None,
         'specify directory for the straw.desktop file [default=PREFIX/share/applications]')]
    
    def initialize_options(self):
        install_data.initialize_options(self)
        self.outfiles = []
        self.build_dir = None
        self.install_dir = None
        self.skip_build = None
        self.with_desktop_file_dir = None

    def finalize_options(self):
        install_data.finalize_options(self)
        self.set_undefined_options('build_desktop', ('build_base', 'build_dir'))
        self.set_undefined_options('install',('install_data','install_dir'),
                                   ('skip_build', 'skip_build'))

        self.set_undefined_options('install',
                                   ('with_desktop_file_dir',
                                    'with_desktop_file_dir'))

    def run(self):
        if not self.skip_build:
            self.run_command('build_desktop')

        src = os.path.normpath(os.path.join(
            self.build_dir, 'share/applications/straw.desktop'))
        dest = os.path.normpath(self.install_dir + '/' + self.with_desktop_file_dir)
        self.mkpath(dest)
        (out, _) = self.copy_file(src, dest)
        self.outfiles.append(out)

    def get_outputs (self):
        return self.outfiles

    def get_inputs (self):
        return (os.path.join(self.build_dir, 'share/applications/straw.desktop'))

class translate(Command):

    description = 'update pot file and merge po files'
    user_options = [('pot', 'p', 'only update the pot file (no merge)')]
    user_options.extend([('dist=', 'd','Merge LANGCODE.po with existing PO template.')])
    boolean_options = ['pot']

    def initialize_options(self):
        self.intl_update = commands.getoutput('which intltool-update')
        self.pot = 0
        self.dist = None
        self.pot_file = self.distribution.pot_file
        self.translations = self.distribution.translations

    def finalize_options(self):
        if not os.path.exists(self.intl_update):
            sys.exit('intltool-update does not exist in your PATH. ' + \
                     'Make sure it exists in your PATH..')

        if self.pot and self.dist:
            sys.exit('You can only specify one option at time...\n' + \
                     "'python setup.py translate --help' for more info")

    def run(self):
        if os.path.exists('./po/'):
            os.chdir('./po/')
        else:
            sys.exit('po/ directory not found.. not continuing...')

        if self.pot:
            cmd = '%s --pot' % self.intl_update
            err, val = commands.getstatusoutput(cmd)
            if err:
                sys.exit('Error generating template file %s' % self.pot_file)
            print "%s" % val

        if self.dist:
            cmd = '%s %s' % (self.intl_update, self.dist)
            err, val = commands.getstatusoutput(cmd)
            if err:
                sys.exit('Error merging %s.po with %s' % (self.dist,self.pot_file))
            print "%s" % val

        os.chdir('../')

class StrawDistribution(Distribution):
    def __init__(self, attrs = None):
        self.modules_check = 0
        self.gconf = 1
        self.msg_sources = None
        self.pot_file = None
        self.translations = []
        self.config_files = []
        self.desktop_file = None
        Distribution.__init__(self, attrs)
        self.cmdclass = {
            'install' : straw_install,
            'install_modules_check' : install_modules_check,
            'install_config' : install_config,
            'install_mo' : install_mo,
            'install_gconf' : install_gconf,
            'install_desktop' : install_desktop,
            'build' : straw_build,
            'build_mo' : build_mo,
            'translate' : translate,
            'build_desktop': build_desktop,
            'build_ext': BuildExt}

    def has_po_files(self):
        return len(self.translations) > 0
    
    def has_gconf(self):
        return self.gconf
    
    def has_modules_check(self):
        return isinstance(self.modules_check, types.FunctionType)

    def has_config_files(self):
        return len(self.config_files) > 0

    def has_desktop_file(self):
        return len(self.desktop_file) > 0

def setup(**kwds):
    from distutils.core import setup
    kwds['distclass'] = StrawDistribution
    setup(**kwds)
