#!/bin/bash

set -e

git config --global --add safe.directory '*'
python /semver_tagging.py

echo "next_tag=${NEXT_TAG}" >> $GITHUB_OUTPUT
echo "changelog_delta=${CHANGELOG}" >> $GITHUB_OUTPUT