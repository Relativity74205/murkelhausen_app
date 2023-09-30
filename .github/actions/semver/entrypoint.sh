#!/bin/bash

set -e

echo "foo"

git config --global --add safe.directory '*'

git tag

echo "bar"

python /semver_tagging.py

echo "baz"

echo "next_tag=${NEXT_TAG}" >> $GITHUB_OUTPUT
echo "changelog_delta=${CHANGELOG}" >> $GITHUB_OUTPUT

echo "qux"
