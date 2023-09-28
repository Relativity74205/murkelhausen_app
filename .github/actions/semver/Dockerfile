# Container image that runs your code
FROM python:3.11-slim

RUN pip install GitPython

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh
COPY semver_tagging.py /semver_tagging.py
COPY .git /.git

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
