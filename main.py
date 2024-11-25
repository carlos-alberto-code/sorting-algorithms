import time
from typing import List
from threading import Thread

from sorting_algorithms.algorithms import *
from hilos import ejecutar_algoritmos_en_hilos
from util.logger import Logger
from util.numbers_generator import generate_numbers


logger = Logger()
logger.limpiar_log()

cases = ["best", "average", "worst"]
elements = [100, 1_000]

for case in cases:
    for n in elements:
        try:
            nums = generate_numbers(case, n)
            algorithms = crear_algoritmos(nums)
        except ValueError as e:
            print(f'Error al generar los números: {e}')
            continue

        print(f'Iniciando caso {case} con {n} elementos\n')
        ejecutar_algoritmos_en_hilos(algorithms, logger, case, n)
        print()
