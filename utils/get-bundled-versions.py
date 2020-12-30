#!/bin/env python

import os
import json

for root, dirs, files in os.walk("apps"):
    for file in files:
        if file == 'composer.lock':
            with open(os.path.join(root, file)) as f:
                lockdata = json.load(f)
                try:
                    for i in lockdata['packages']:
                        print("Provides: bundled(php-composer(" + i['name'] + ")) = " + i['version'].strip('v'))
                except KeyError:
                    pass

for root, dirs, files in os.walk("3rdparty"):
    for file in files:
        if file == 'composer.lock':
            with open(os.path.join(root, file)) as f:
                lockdata = json.load(f)
                try:
                    for i in lockdata['packages']:
                        print("Provides: bundled(php-composer(" + i['name'] + ")) = " + i['version'].strip('v'))
                except KeyError:
                    pass
