import os
import re
from typing import Dict, List, Tuple
from collections.abc import Callable
from dataclasses import dataclass, replace

from utils.timer import timer

"""
Preprocessing:
- We read the input file and parse it into two main components: a dictionary of workflows and a list of ratings.
- For ratings, we create a Rating dataclass to store the x, m, a, and s values in separate variables for easy access.
- For workflows, we create a Workflow dataclass to store the rule functions and default destination.

Part 1:
- We model the workflow evaluation as a state machine, where each rating starts at the "in" workflow and 
  transitions through workflows until reaching a terminal state ("A" for accepted or "R" for rejected).

              _ state2 -> rule1 -> rule2 ->... -> R
            //
  in -> rule1 -> rule2 
                     \\_ state3 -> rule1 -> ... -> A

- For each workflow, we implement a more sophisticated approach using callable functions:
    - The rule() function converts rule strings (like 'a<2006:qkq') into callable functions that evaluate ratings.
    - Each rule function takes a Rating object and returns either a destination string if the condition is met, or None otherwise.
    - This functional approach allows us to automatically evaluate ratings against workflow rules without manual condition checking.
- For each rating, we iterate through workflows by calling evaluate_workflow() with the current workflow and rating.
- The evaluate_workflow() function checks each rule in sequence until one matches, then returns the destination workflow name.
- If no rules match, it returns the workflow's default destination.
- We continue this process, updating the current workflow name based on each evaluation result, until we reach "A" or "R".
- We track all ratings that reach the "A" state and sum their total values (x + m + a + s) to get the final answer.

Part 2:
- Instead of evaluating individual ratings, we work with rating ranges where each attribute (x, m, a, s) has a range [min, max].
- We start with a single RatingRange covering all possible values: x=[1,4000], m=[1,4000], a=[1,4000], s=[1,4000].
- We use a queue-based approach to process rating ranges through workflows, similar to Part 1's state machine but with range splitting.

                    _ state2 -> rule1 (match: [1,1000]) -> ... -> R
                  //          \\_ rule1 (complement: [1001,4000]) -> ... -> A
                //
  in -> rule1 (split range)
                \\
                  \\_ state3 -> rule1 (match: [2000,4000]) -> ... -> A
                             \\_ rule1 (complement: [1,1999]) -> ... -> R

- For each workflow rule, we use rule_range() to create functions that split rating ranges into two parts:
    - The matching range that satisfies the rule condition (sent to the rule's destination)
    - The complement range that doesn't satisfy the condition (continues to the next rule)
- The evaluate_workflow_range() function processes each rule sequentially:
    - For each matching rule, it creates a new path (destination, matching_range) and adds it to the queue
    - The complement range continues to be evaluated against subsequent rules
    - Any remaining range after all rules is sent to the workflow's default destination
- We continue processing until all ranges reach terminal states ("A" or "R").
- For each accepted range ("A"), we calculate the total number of distinct combinations by multiplying the size of each attribute range.
- The final answer is the sum of all possible combinations across all accepted rating ranges.
"""


@dataclass
class Workflow:
    rules: List[Callable | str]
    default_rule: str


@dataclass
class Rating:
    x: int
    m: int
    a: int
    s: int

    def __str__(self) -> str:
        return f"(x={self.x:4d}, m={self.m:4d}, a={self.a:4d}, s={self.s:4d})"

    def total(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclass
class RatingRange:
    x: List[int]
    m: List[int]
    a: List[int]
    s: List[int]

    def __str__(self) -> str:
        return f"(x=[{self.x[0]:4d},{self.x[1]:4d}], m=[{self.m[0]:4d},{self.m[1]:4d}], a=[{self.a[0]:4d},{self.a[1]:4d}], s=[{self.s[0]:4d},{self.s[1]:4d}])"

    def total(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )


@timer
def part1():
    workflows, ratings = parse_file("input.txt")

    convert_rules_to_functions(workflows)

    approved_ratings = []
    for rating in ratings:
        name = "in"
        while name not in ["A", "R"]:
            name = evaluate_workflow(workflows[name], rating)
        if name == "A":
            approved_ratings.append(rating)

    total_approved_ratings = sum(rating.total() for rating in approved_ratings)
    print(f"Total approved ratings:", total_approved_ratings)


@timer
def part2():    
    workflows, _ = parse_file("input.txt")

    convert_rules_to_functions(workflows, with_range=True)

    approved_ratings = []
    rating_paths = [
        ("in", RatingRange(x=[1, 4000], m=[1, 4000], a=[1, 4000], s=[1, 4000]))
    ]
    while rating_paths:
        wf, rating = rating_paths.pop(0)
        if wf == "A":
            approved_ratings.append(rating)
            continue
        elif wf == "R":
            continue

        new_rating_paths = evaluate_workflow_range(workflows[wf], rating)
        rating_paths.extend(new_rating_paths)

    total = sum(rating.total() for rating in approved_ratings)
    print(f"Total combinations of approved ratings:", total)


def convert_rules_to_functions(
    workflows: Dict[str, Workflow], with_range: bool = False
) -> None:
    """
    Converts rule strings in workflows to callable functions for evaluation.
    """
    for name, workflow in workflows.items():
        if with_range:
            workflows[name].rules = [rule_range(r) for r in workflow.rules]
        else:
            workflows[name].rules = [rule(r) for r in workflow.rules]


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


def rule_range(rule_str: str):
    """
    Converts a rule string into a function that evaluates rating ranges and splits them based on the rule condition.

    This function parses a rule string (e.g., 'a<2006:qkq') and returns a callable that takes a RatingRange object.
    When called, the returned function splits the rating range into two parts: one that satisfies the rule condition
    (sent to the specified destination) and its complement (the remaining range that doesn't satisfy the condition).

    Args:
        rule_str: Rule string in format 'rate<operand:destination' or 'rate>operand:destination',
                 where rate is one of [x, m, a, s], operand is an integer threshold,
                 and destination is the target workflow name.

    Returns:
        A callable function that takes a RatingRange object and returns a tuple of:
            - str: The destination workflow name for the matching range
            - RatingRange: The rating range that satisfies the rule condition
            - RatingRange: The complement rating range that doesn't satisfy the condition
        Returns None if the rule string doesn't match the expected format or if the rating range
        doesn't satisfy the rule condition.
    """
    # Parse the rule string
    match = re.match(r"([xmas])([<>])(\d+):(\w+)", rule_str)
    if not match:
        return None

    rate, op, operand, destination = match.groups()
    operand = int(operand)

    def evaluate(rating: RatingRange) -> Tuple[str, RatingRange, RatingRange]:
        # Get the value from the rating based on the rate letter
        value = getattr(rating, rate)

        if op == "<":
            if value[0] < operand:
                rating = replace(rating, **{rate: [value[0], operand - 1]})
                complement_rating = replace(rating, **{rate: [operand, value[1]]})
                return destination, rating, complement_rating
            return None
        else:  # op == '>'
            if value[1] > operand:
                rating = replace(rating, **{rate: [operand + 1, value[1]]})
                complement_rating = replace(rating, **{rate: [value[0], operand]})
                return destination, rating, complement_rating
            return None

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


def evaluate_workflow_range(
    workflow: Workflow, rating: Rating
) -> List[Tuple[str, Rating]]:
    """
    Evaluates a workflow against a rating range and returns all possible destination paths with their corresponding rating ranges.

    This function processes each rule in the workflow sequentially, splitting the rating range into matching and non-matching
    portions. For each rule that matches, it creates a new path with the matching range and continues processing the
    remaining (complement) range against subsequent rules. Finally, any remaining range is assigned to the workflow's
    default destination.

    Args:
        workflow: The workflow containing rules to evaluate and a default destination
        rating: The rating range to evaluate against the workflow rules

    Returns:
        A list of tuples, where each tuple contains:
            - str: The destination workflow name (or 'A'/'R' for terminal states)
            - Rating: The rating range that should be sent to that destination
    """
    results = []
    # Check each rule in order
    for rule_func in workflow.rules:
        result = rule_func(rating)
        if result is not None:
            # Append the destination, new rating
            results.append(result[:2])
            # Complement the rating
            rating = result[2]

    # # If no rule matched, return the default
    # return workflow.default_rule
    results.append((workflow.default_rule, rating))

    return results


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
            workflows[worflow_name] = Workflow(rules[:-1], rules[-1])

        for rating in file_ratings:
            rating_groups = re.search(rating_pattern, rating).groups()
            ratings.append(Rating(*map(int, rating_groups)))
    return workflows, ratings


part1()
part2()
