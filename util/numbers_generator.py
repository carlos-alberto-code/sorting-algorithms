import random
from typing import List


def generate_numbers(case: str, n: int) -> List[int]:
    case = case.lower()
    if case not in ["best", "average", "worst"]:
        raise ValueError("Case must be 'best', 'average' or 'worst'")
    if n < 1:
        raise ValueError("n must be a positive integer")
    cases = {
        "best": lambda n: list(range(1, n+1)),
        "average": lambda n: random.sample(range(1, n+1), n),
        "worst": lambda n: list(range(n, 0, -1)),
    }
    return cases[case](n)
