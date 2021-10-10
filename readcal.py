#!/usr/bin/env python3

import yaml

with open('config.yaml') as foo:
    bar = yaml.safe_load(foo)

print(bar)
