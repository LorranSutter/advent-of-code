import os
import re
from typing import Dict, List, Tuple
from collections.abc import Callable
from dataclasses import dataclass

from utils.timer import timer

"""
Preprocessing:
- We read the input file and parse it into two main components: a dictionary of workflows and a list of ratings.
- For ratings, we create a Rating dataclass to store the x, m, a, and s values in separate variables for easy access.
- For workflows, we implement a more sophisticated approach using callable functions:
    - Each workflow is parsed into a Workflow dataclass containing its name, a list of rule functions, and a default destination.
    - The rule() function converts rule strings (like 'a<2006:qkq') into callable functions that evaluate ratings.
    - Each rule function takes a Rating object and returns either a destination string if the condition is met, or None otherwise.
    - This functional approach allows us to automatically evaluate ratings against workflow rules without manual condition checking.

Part 1:
- We model the workflow evaluation as a state machine, where each rating starts at the "in" workflow and 
  transitions through workflows until reaching a terminal state ("A" for accepted or "R" for rejected).

              _ state2 -> rule1 -> rule2 ->... -> R
             /
  in -> rule1 -> rule2 
                      \_ state3 -> rule1 -> ... -> A

- For each rating, we iterate through workflows by calling evaluate_workflow() with the current workflow and rating.
- The evaluate_workflow() function checks each rule in sequence until one matches, then returns the destination workflow name.
- If no rules match, it returns the workflow's default destination.
- We continue this process, updating the current workflow name based on each evaluation result, until we reach "A" or "R".
- We track all ratings that reach the "A" state and sum their total values (x + m + a + s) to get the final answer.

Part 2:
-
"""


@dataclass
class Workflow:
    name: str
    rules: List[Callable]
    default_rule: str


@dataclass
class Rating:
    x: int
    m: int
    a: int
    s: int

    def total(self) -> int:
        return self.x + self.m + self.a + self.s


@timer
def part1():
    workflows, ratings = parse_file("input.txt")

    approved_ratings = []
    for rating in ratings:
        name = "in"
        while name not in ["A", "R"]:
            name = evaluate_workflow(workflows[name], rating)
            print(f"Next workflow: {name}")
        if name == "A":
            approved_ratings.append(rating)

    print(f"Total approved ratings: ", sum(rating.total() for rating in approved_ratings))


@timer
def part2():
    # TODO: Implement part 2
    lines = parse_file("input_sample.txt")
    pass


def rule(rule_str: str):
    """
    Converts a rule string like 'a<2006:qkq' into a function that evaluates the rule.

    Args:
        rule_str: Rule in format 'rate<operand:destination' or 'rate>operand:destination'

    Returns:
        A function that takes a Rating object and returns the destination string if true, None otherwise
    """
    # Parse the rule string
    match = re.match(r"([xmas])([<>])(\d+):(\w+)", rule_str)
    if not match:
        return None

    rate, op, operand, destination = match.groups()
    operand = int(operand)

    def evaluate(rating: Rating) -> str:
        # Get the value from the rating based on the rate letter
        value = getattr(rating, rate)

        # Perform the comparison
        if op == "<":
            return destination if value < operand else None
        else:  # op == '>'
            return destination if value > operand else None

    return evaluate


def evaluate_workflow(workflow: Workflow, rating: Rating) -> str:
    """
    Evaluates a workflow against a rating and returns the destination.

    Args:
        workflow: The workflow to evaluate
        rating: The rating to check

    Returns:
        The destination string (next workflow name or 'A'/'R')
    """
    # Check each rule in order
    for rule_func in workflow.rules:
        result = rule_func(rating)
        if result is not None:
            return result

    # If no rule matched, return the default
    return workflow.default_rule


def parse_file(file_name: str) -> Tuple[Dict[str, Workflow], List[Rating]]:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    workflow_pattern = r"(\w*)\{(.*)\}"
    rating_pattern = r"{x=(\d*),m=(\d*),a=(\d*),s=(\d*)}"

    workflows = dict()
    ratings = []
    with open(abs_file_path, "r") as f:
        file = f.read().split("\n\n")
        file_workflows = file[0].split("\n")
        file_ratings = file[1].split("\n")

        for workflow in file_workflows:
            worflow_name, rules = re.search(workflow_pattern, workflow).groups()
            rules = rules.split(",")
            rules, default_rule = rules[:-1], rules[-1]  # Default rule is the last rule
            rules = [rule(r) for r in rules]
            workflows[worflow_name] = Workflow(
                name=worflow_name, rules=rules, default_rule=default_rule
            )

        for rating in file_ratings:
            rating_groups = re.search(rating_pattern, rating).groups()
            ratings.append(Rating(*map(int, rating_groups)))
    return workflows, ratings


part1()
# part2()
