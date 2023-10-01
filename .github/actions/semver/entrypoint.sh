#!/bin/bash

set -e

echo "foo"

git config --global --add safe.directory '*'

git tag

echo "bar"

foo=$(python /semver_tagging.py)
echo "foo=${foo}"

echo "baz"

# shellcheck disable=SC2086
echo NEXT_TAG=${NEXT_TAG}
echo CHANGELOG="${CHANGELOG}"
echo "next_tag=${NEXT_TAG}" >> "$GITHUB_OUTPUT"
# shellcheck disable=SC2086
echo "changelog_delta=${CHANGELOG}" >> $GITHUB_OUTPUT

echo "qux"
