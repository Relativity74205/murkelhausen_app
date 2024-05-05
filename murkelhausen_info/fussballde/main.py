from datetime import date, datetime

import requests
from babel.dates import format_date
from bs4 import BeautifulSoup


VFB_SPELDORF_ID = "00ES8GN8VS000030VV0AG08LVUPGND5I"
F2_JUNIOREN = "011MIBB3NK000000VTVG0001VTR8C1K7"


def parse_next_games(html_content: str) -> list[dict]:
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.find("tbody")
    next_row = body.findNext("tr")

    games = []
    while next_row is not None:
        game = {}
        meta = next_row.findNext("td").text.split(" | ")
        gamedate, time = meta[0].split(",")[1].strip().split(" - ")

        game["day"] = format_date(
            datetime.strptime(gamedate, "%d.%m.%Y").date(),
            format="EEE, d.M.yyyy",
            locale="de_DE",
        )
        # creates a date object from the string
        game["weekday"] = datetime.strptime(gamedate, "%d.%m.%Y").date().strftime("%A")
        game["time"] = time
        game["team"] = meta[1].strip()
        game_details = next_row.findNext("tr").findNext("tr")
        clubs = game_details.find_all("div", class_="club-name")
        game["home_team"] = clubs[0].text.strip()
        game["away_team"] = clubs[1].text.strip()
        result = game_details.find("span", class_="info-text")
        if result is not None:
            game["result"] = result.text.strip()
        else:
            game["result"] = None

        next_row = game_details.findNext("tr")
        games.append(game)

    return games


def get_speldorf_next_games() -> list[dict]:
    r = requests.get(
        f"https://www.fussball.de/ajax.club.next.games/-/id/{VFB_SPELDORF_ID}/"
    )

    return parse_next_games(r.text)


def get_erik_next_games() -> list[dict]:
    r = requests.get(
        f"https://www.fussball.de/ajax.team.next.games/-/mode/PAGE/team-id/{F2_JUNIOREN}"
    )

    return parse_next_games(r.text)


def get_speldorf_next_home_games() -> list[dict]:
    games = get_speldorf_next_games()
    return [game for game in games if "Speldorf" in game["home_team"]]


#
#
# speldorf_next_games = get_speldorf_next_games()
# print(speldorf_next_games)
#
# erik_next_games = get_erik_next_games()
# print(erik_next_games)
