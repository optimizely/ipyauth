#!/usr/bin/env bash

# Prior to running this script, bump version in ipyauth/js/package.json and in __meta__.py

# Create Python package
rm -fr dist
python setup.py sdist
python setup.py bdist_wheel --universal

# Create JS package
cd ipyauth/js
npm install
npm pack
cd -

# Move packages
rm -fr assets
mkdir assets
mv dist/* assets/
mv ipyauth/js/*.tgz assets/
