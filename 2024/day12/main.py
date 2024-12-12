import os
import collections

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    grid = generate_grid_with_borders()
    regions = get_regions(grid)
    total_price = calculate_total_price(regions, discount=False)

    print("Total price:", total_price)


def part2():
    grid = generate_grid_with_borders()
    regions = get_regions(grid)
    total_price = calculate_total_price(regions, discount=True)

    print("Total price:", total_price)


def read_file():
    grid = []
    with open(abs_file_path) as f:
        for row in f:
            grid.append(row.rstrip("\n").split())
    return grid


def generate_grid_with_borders():
    """
    * * * *
    * A A *
    ...
    * Z Z *
    * * * *
    """
    grid = []
    with open(abs_file_path) as f:
        for row in f:
            row = ["*"] + [plant for plant in row.rstrip("\n")] + ["*"]
            grid.append(row)

    size = len(grid[0])
    border = ["*" for _ in range(size)]
    grid.insert(0, border)
    grid.append(border)

    return grid


def get_regions(grid):
    regions = collections.defaultdict(lambda: None)
    visited = collections.defaultdict(lambda: None)
    size = len(grid)

    # Exclude borders
    for x in range(1, size - 1):
        for y in range(1, size - 1):
            if visited[(x, y)]:
                continue

            plant_type = grid[x][y]
            if not regions[plant_type]:
                regions[plant_type] = [[]]
            else:
                regions[plant_type].append([])

            get_region(
                grid, regions, len(regions[plant_type]) - 1, visited, plant_type, x, y
            )
    return regions


def get_region(grid, regions, region_id, visited, plant_type, x, y):
    if visited[(x, y)] or grid[x][y] != plant_type or grid[x][y] == "*":
        return

    visited[(x, y)] = True
    regions[plant_type][region_id].append((x, y))

    get_region(grid, regions, region_id, visited, plant_type, x + 1, y)
    get_region(grid, regions, region_id, visited, plant_type, x - 1, y)
    get_region(grid, regions, region_id, visited, plant_type, x, y + 1)
    get_region(grid, regions, region_id, visited, plant_type, x, y - 1)


def calculate_total_price(regions, discount):
    total_price = 0

    for region_set in regions.values():
        for region in region_set:
            total_price += (
                calculate_region_price_2(region)
                if discount
                else calculate_region_price_1(region)
            )

    return total_price


def calculate_region_price_1(region):
    perimeter = 0
    for x, y in region:
        if (x + 1, y) not in region:
            perimeter += 1
        if (x - 1, y) not in region:
            perimeter += 1
        if (x, y + 1) not in region:
            perimeter += 1
        if (x, y - 1) not in region:
            perimeter += 1

    return perimeter * len(region)


def calculate_region_price_2(region):
    # If border was visited in a given direction
    visited = collections.defaultdict(lambda: None)

    sides = 0
    for x, y in region:
        '''
        * * * *
        * |   *
        * A A *
        '''
        if not visited[((x + 1, y), (1, 0))] and (x + 1, y) not in region:
            sides += 1
            visit(region, visited, (x, y), (0, 1), (1, 0))
            visit(region, visited, (x, y - 1), (0, -1), (1, 0))
        '''
        * * * *
        * A A *
        * |   *
        '''
        if not visited[((x - 1, y), (-1, 0))] and (x - 1, y) not in region:
            sides += 1
            visit(region, visited, (x, y), (0, 1), (-1, 0))
            visit(region, visited, (x, y - 1), (0, -1), (-1, 0))
        '''
        * * * *
        * A - *
        * A   *
        '''
        if not visited[((x, y + 1), (0, 1))] and (x, y + 1) not in region:
            sides += 1
            visit(region, visited, (x, y), (1, 0), (0, 1))
            visit(region, visited, (x - 1, y), (-1, 0), (0, 1))
        '''
        * * * *
        * - A *
        *   A *
        '''
        if not visited[((x, y - 1), (0, -1))] and (x, y - 1) not in region:
            sides += 1
            visit(region, visited, (x, y), (1, 0), (0, -1))
            visit(region, visited, (x - 1, y), (-1, 0), (0, -1))

    return sides * len(region)


def visit(region, visited, pos, direction, normal):
    border = add(pos, normal)

    # Border already visited
    if visited[(border, normal)]:
        return

    if pos in region and border not in region:
        visited[(border, normal)] = True
        visit(region, visited, add(pos, direction), direction, normal)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


part2()
