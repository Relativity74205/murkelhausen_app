import os
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto

from github import Github, Auth, Repository


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


def get_github_repo() -> Repository:
    github_token = os.environ["GITHUB_TOKEN"]
    auth = Auth.Token(github_token)

    g = Github(auth=auth)

    return g.get_repo("Relativity74205/murkelhausen_app")


def get_last_tag(repo: Repository) -> tuple[Tag | None, datetime | None]:
    tags = repo.get_tags()
    try:
        last_tag = sorted(tags, key=lambda x: x.name)[-1]
        return Tag.from_tag_name(last_tag.name), last_tag.commit.commit.author.date
    except IndexError:
        return None, None


def get_commit_messages_since_tag(
    repo: Repository, last_tag_datetime: datetime
) -> list[str]:
    if last_tag_datetime is None:
        commits_since_tag = repo.get_commits()
    else:
        commits_since_tag = repo.get_commits(since=last_tag_datetime)
    return [commit.commit.message for commit in commits_since_tag]


def get_commit_summaries_since_tag(repo: Repository, last_tag: Tag) -> list[str]:
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
    print("Start.")
    github_repo = get_github_repo()
    last_tag, last_tag_datetime = get_last_tag(github_repo)
    print(f"{last_tag=} with {last_tag_datetime=}")
    commit_messages = get_commit_messages_since_tag(github_repo, last_tag_datetime)

    next_tag = calculate_next_tag(commit_messages, last_tag)
    print(f"{next_tag=}")

    os.environ["NEXT_TAG"] = next_tag
    os.environ["CHANGELOG"] = "\n".join(commit_messages)


if __name__ == "__main__":
    main()
