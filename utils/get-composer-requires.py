#!/bin/env python

import os
import json
import re
import subprocess

defaultconstraint = 2

constraintmap = ('any', 'loose', 'strict', 'exact')

def get_requires(name, version, constraint):
    version = version.split('.')

    if constraint == 0:
        requires = 'php-composer(' + name + ')'
    elif constraint == 1:
        wipe = False
        for i in range(0, len(version)):
            if version[i] == '0' or wipe:
                version[i] = '0'
            else:
                version[i] = str(int(version[i]) + 1)
                wipe = True
            requires = '(php-composer(' + name + ') >= ' + minver + ' with php-composer(' + name + ') < ' + '.'.join(version) + ')'
    elif constraint == 2:
        version[-1] = '0'
        version[-2] = str(int(version[-2]) + 1)
        requires = '(php-composer(' + name + ') >= ' + minver + ' with php-composer(' + name + ') < ' + '.'.join(version) + ')'
    else:
        requires = 'php-composer(' + name + ') = ' + minver
    return requires

def repoquery(query):
    stdout = subprocess.run(['dnf', 'repoquery', '-q', '--whatprovides', requires], stdout=subprocess.PIPE, universal_newlines=True, check = True).stdout
    return stdout


with open('3rdparty/composer.json') as f:
#with open('apps/files_external/3rdparty/composer.json') as f:
    depdata = json.load(f)
    for name, version in depdata['require'].items():
        if name == 'php':
            continue
        print(name, version, ':')
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
        else:
            constraint = defaultconstraint

        if re.search('[^.0-9]', version):
            print('Unparseable version:', version)
            continue
        else:
            minver = version

        requires = get_requires(name, version, constraint)
        print('  Constraint (' + constraintmap[constraint] + '): ' + requires)

        package = repoquery(requires)
        while len(package) == 0:
            constraint -= 1
            if constraint < 0:
                break
            requires = get_requires(name, version, constraint)
            print('  Constraint (' + constraintmap[constraint] + '): ' + requires)
            package = repoquery(requires)

        if len(package) == 0:
            print('    -> no providing package found\n')
        else:
            print('    -> ' + package)
