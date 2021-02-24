#!/bin/env python

import os
import json
import re
import subprocess
from colorama import Fore, Style

defaultconstraint = 2
excludes = ('php')
basedir = '..'
srcdir = os.path.join(basedir, 'nextcloud')
outdir = basedir
jsonfiles = ('3rdparty/composer.json', 'apps/files_external/3rdparty/composer.json')

constraintmap = ('any', 'loose', 'strict', 'exact')

def eval_version(version, constraint=3):
    version = version.replace('v', '')
    if version == '*':
        constraint = 0
        version = '0'
    elif version.startswith('^'):
        constraint = 1
        version = version.strip('^')
    elif version.startswith('~'):
        constraint = 2
        version = version.strip('~')

    if re.search('[^.0-9]', version):
        print('Unparseable version:', version)
        version = '0.0.0'
        constraint = 3

    return version, constraint

def get_requires(name, version, constraint):
    splitver = version.split('.')

    if constraint == 0:
        requires = 'php-composer(' + name + ')'
    elif constraint == 1:
        wipe = False
        for i in range(0, len(splitver)):
            if splitver[i] == '0' or wipe:
                splitver[i] = '0'
            else:
                splitver[i] = str(int(splitver[i]) + 1)
                wipe = True
            requires = '(php-composer(' + name + ') >= ' + version + ' with php-composer(' + name + ') < ' + '.'.join(splitver) + ')'
    elif constraint == 2:
        splitver[-1] = '0'
        splitver[-2] = str(int(splitver[-2]) + 1)
        requires = '(php-composer(' + name + ') >= ' + version + ' with php-composer(' + name + ') < ' + '.'.join(splitver) + ')'
    else:
        requires = 'php-composer(' + name + ') = ' + version
    return requires

def repoquery(query):
    stdout = subprocess.run(['dnf', 'repoquery', '-q', '--whatprovides', requires], stdout=subprocess.PIPE, universal_newlines=True, check = True).stdout
    return stdout

requirefile = open(os.path.join(outdir, 'require.pkgtmp'), 'w')
requirefile.write('# PHP composer dependencies\n')

providefile = open(os.path.join(outdir, 'provide.pkgtmp'), 'w')
providefile.write('# Bundled libraries\n')


for file in jsonfiles:
    requirefile.write(f"# From {file}\n")
    providefile.write(f"# From {file}\n")
    
    with open(os.path.join(srcdir, file)) as f:
        jsondata = json.load(f)
        packages = jsondata['require'].items()

    print(f"\n{Style.BRIGHT}Parsing '{file}'...{Style.RESET_ALL}")
    for name, verrange in packages:
        if name in excludes:
            print(f"{name} {verrange} -> in exclude list, skipping.")
            continue

        version, constraint = eval_version(verrange, defaultconstraint)

        requires = get_requires(name, version, constraint)
        package = repoquery(requires)

        color = Fore.GREEN
        found = True
        while len(package) == 0:
            color = Fore.YELLOW
            constraint -= 1
            if constraint < 0:
                constraint = 0
                color = Fore.RED
                package = 'none\n'
                found = False
                break
            requires = get_requires(name, version, constraint)
            package = repoquery(requires)

        print(f"{name} {verrange} -> {Style.BRIGHT}{color}{package.rstrip()}{Style.RESET_ALL} ({constraintmap[constraint]})")
        
        if found:
            requirefile.write(f"Requires: {requires}\n")
        else:
            providefile.write(f"Provides: bundled(php-composer({name})) = {version}\n")

