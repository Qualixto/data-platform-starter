#!/bin/sh
# Fails when a Python version pin drifts from .python-version.
set -eu

expected=$(cat .python-version)
dockerfile=$(sed -n 's/^ARG PYTHON_VERSION=//p' Dockerfile)

if [ "$dockerfile" != "$expected" ]; then
    echo "Dockerfile pins Python $dockerfile, but .python-version is $expected" >&2
    exit 1
fi
