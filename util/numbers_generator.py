import random
from typing import List


def generate_numbers(case: str, n: int) -> List[int]:
    """Genera una lista de números en función del caso. Los casos posibles son:
    - best: Lista ordenada de menor a mayor.
    - average: Lista de números aleatorios.
    - worst: Lista ordenada de mayor a menor.
    n es el número de elementos de la lista.

    La lista va de 1 a n.

    Se generan excepciones cuando el caso no es válido o n no es un número positivo.
    """
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
