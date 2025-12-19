import os

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    games = read_file()

    red_limit, green_limit, blue_limit = 12, 13, 14

    valid_games = 0
    for i, game in enumerate(games, 1):
        valid_games += i
        for set_game in game:
            if (
                set_game[0] > red_limit
                or set_game[1] > green_limit
                or set_game[2] > blue_limit
            ):
                valid_games -= i
                break

    print("Sum possible games:", valid_games)


@timer
def part2():
    games = read_file()

    total_power = 0
    for game in games:
        min_red, min_green, min_blue = 0, 0, 0
        for set_game in game:
            if set_game[0] > min_red:
                min_red = set_game[0]
            if set_game[1] > min_green:
                min_green = set_game[1]
            if set_game[2] > min_blue:
                min_blue = set_game[2]

        total_power += min_red * min_green * min_blue

    print("Total game power:", total_power)


def read_file():
    games = []
    with open(abs_file_path) as f:
        for line in f:
            line = line.rstrip("\n").split(":")
            line = line[
                1
            ]  # only games (3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green)
            line_games = line.split(
                ";"
            )  # separate games [[3 blue, 4 red], [1 red, 2 green, 6 blue], [2 green]]

            new_set_game = []
            for game in line_games:
                game = game.split(",")  # [[3 blue], [4 red]]
                new_game = [0 for _ in range(3)]
                for cubes in game:
                    cubes = cubes.strip().split(" ")  # [3,blue]
                    if cubes[1] == "red":
                        new_game[0] = int(cubes[0])
                    if cubes[1] == "green":
                        new_game[1] = int(cubes[0])
                    if cubes[1] == "blue":
                        new_game[2] = int(cubes[0])

                new_set_game.append(new_game)

            games.append(new_set_game)

    return games


part2()
