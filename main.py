from threading import Thread

from util.logger                    import Logger
from util.numbers_generator         import generate_numbers
from sorting_algorithms.algorithms  import crear_algoritmos
from hilos                          import ejecutar_algoritmos_en_hilos


logger = Logger()
logger.clear_log()

cases = ["best", "average"]
elements = [1_000, 10_000]

for case in cases:
    for n in elements:
        try:
            nums = generate_numbers(case, n)
            algorithms = crear_algoritmos(nums)
            # Informar al logger cuántos algoritmos esperar
            logger.set_expected_algorithms(case, n, len(algorithms))
        except ValueError as e:
            print(f'Error al generar los números: {e}')
            continue

        print(f'Iniciando caso {case} con {n} elementos\n')
        ejecutar_algoritmos_en_hilos(algorithms, logger, case, n)
