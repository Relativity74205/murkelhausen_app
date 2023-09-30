import os
from dataclasses import dataclass
from enum import StrEnum, auto

from git import Repo

from pathlib import Path


repo = Repo.init(Path.cwd())


@dataclass
class Tag:
    major: int
    minor: int
    patch: int

    @classmethod
    def from_tag_name(cls, tag_name: str) -> "Tag":
        major, minor, patch = tag_name.split(".")
        return cls(int(major), int(minor), int(patch))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def as_string(major: int, minor: int, patch: int):
        return f"{major}.{minor}.{patch}"

    def return_next_major(self):
        return self.as_string(self.major + 1, 0, 0)

    def return_next_minor(self):
        return self.as_string(self.major, self.minor + 1, 0)

    def return_next_patch(self):
        return self.as_string(self.major, self.minor, self.patch + 1)


class UpgradeType(StrEnum):
    MAJOR = auto()
    MINOR = auto()
    PATCH = auto()
    NONE = auto()


def get_last_tag(repo: Repo) -> Tag | None:
    for tag in repo.tags:
        print(tag)
    try:
        last_tag_string = repo.tags[-1].name
        return Tag.from_tag_name(last_tag_string)
    except IndexError:
        return None


def get_commit_messages_since_tag(repo: Repo, last_tag: Tag) -> list[str]:
    if last_tag is None:
        commits_since_tag = list(repo.iter_commits("HEAD"))
    else:
        commits_since_tag = list(repo.iter_commits(f"{last_tag}..HEAD"))
    return [commit.message for commit in commits_since_tag]


def get_commit_summaries_since_tag(repo: Repo, last_tag: Tag) -> list[str]:
    if last_tag is None:
        commits_since_tag = list(repo.iter_commits("HEAD"))
    else:
        commits_since_tag = list(repo.iter_commits(f"{last_tag}..HEAD"))
    return [commit.summary for commit in commits_since_tag]


def get_conventional_commits_prefix(commit_message: str) -> str | None:
    try:
        return commit_message.split(":")[0]
    except IndexError:
        return None


def is_breaking_change(commit_message: str) -> bool:
    return "BREAKING" in commit_message


def get_upgrade_type(commit_messages: list[str]) -> UpgradeType:
    for commit_message in commit_messages:
        if is_breaking_change(commit_message):
            return UpgradeType.MAJOR

    for commit_message in commit_messages:
        if get_conventional_commits_prefix(commit_message) == "feat":
            return UpgradeType.MINOR

    for commit_message in commit_messages:
        if get_conventional_commits_prefix(commit_message) == "fix":
            return UpgradeType.PATCH

    return UpgradeType.NONE


def calculate_next_tag(commit_messages: list[str], last_tag: Tag) -> str:
    if last_tag is None:
        return "0.0.1"

    upgrade_type = get_upgrade_type(commit_messages)

    match upgrade_type:
        case UpgradeType.MAJOR:
            return last_tag.return_next_major()
        case UpgradeType.MINOR:
            return last_tag.return_next_minor()
        case UpgradeType.PATCH:
            return last_tag.return_next_patch()
        case _:
            ...

    return str(last_tag)


def main():
    last_tag = get_last_tag(repo)
    commit_messages = get_commit_messages_since_tag(repo, last_tag)

    next_tag = calculate_next_tag(commit_messages, last_tag)

    os.environ["NEXT_TAG"] = next_tag
    commit_summaries = get_commit_summaries_since_tag(repo, last_tag)
    os.environ["CHANGELOG"] = "\n".join(commit_summaries)


if __name__ == "__main__":
    main()
