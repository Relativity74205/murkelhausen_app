#!/bin/bash

set -e

echo "foo"

git config --global --add safe.directory '*'

git tag

echo "bar"

python /semver_tagging.py

echo "baz"

# shellcheck disable=SC2086
# TODO get results from file
NEXT_TAG=$(jq .NEXT_TAG semver_result.json)
CHANGELOG=$(jq .CHANGELOG semver_result.json)
echo "next_tag=${NEXT_TAG}" >> "$GITHUB_OUTPUT"
# shellcheck disable=SC2086
echo "changelog_delta=${CHANGELOG}" >> $GITHUB_OUTPUT

echo "qux"
