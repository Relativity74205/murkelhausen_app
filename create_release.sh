#!/usr/bin/env bash

curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_ACCESS_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/Relativity74205/murkelhausen_app/actions/workflows/71455949/dispatches \
  -d '{"ref":"main"}'

#curl -L \
#  -H "Accept: application/vnd.github+json" \
#  -H "Authorization: Bearer ${GITHUB_ACCESS_TOKEN}" \
#  -H "X-GitHub-Api-Version: 2022-11-28" \
#  https://api.github.com/repos/Relativity74205/murkelhausen_app/actions/workflows