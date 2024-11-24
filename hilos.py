import time
from typing import Callable
from threading  import Thread
from dataclasses import dataclass


@dataclass
class AlgorithmResult:
    name: str
    execution_time: float

class TimedThread(Thread):
    def __init__(self, target: Callable, args: tuple, name: str):
        super().__init__()
        self.target = target
        self.args = args
        self.algorithm_name = name
        self.execution_time = 0

    def run(self):
        print(f"Inicio del hilo: {self.algorithm_name}")
        start = time.time()
        self.target(*self.args)
        self.execution_time = time.time() - start
        print(f"Fin del hilo: {self.algorithm_name} - Tiempo de ejecución: {self.execution_time:.2f} segundos")
