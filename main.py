from typing import List, Literal
from dataclasses import dataclass

from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import crear_algoritmos
from util.logger import Logger, GroupedStrategy, BattleStrategy
from hilos import ejecutar_algoritmos_en_hilos, AlgorithmContext


@dataclass
class RaceConfig:
    race_type: Literal["grouped", "battle_royale"]
    cases: List[str]
    elements: List[int]


def setup_logger(config: RaceConfig) -> Logger:
    strategy = (
        GroupedStrategy() if config.race_type == "grouped"
        else BattleStrategy()
    )
    logger = Logger(race_strategy=strategy)
    logger.clear_log()
    return logger


def prepare_algorithms(config: RaceConfig) -> List[AlgorithmContext]:
    """Prepara los algoritmos con su contexto original"""
    all_contexts = []

    for case in config.cases:
        for n in config.elements:
            try:
                nums = generate_numbers(case, n)
                algorithms = crear_algoritmos(nums)

                if config.race_type == "grouped":
                    # Para carreras agrupadas
                    contexts = [
                        AlgorithmContext(algo, case, n)
                        for algo in algorithms
                    ]
                    logger.set_expected_algorithms(case, n, len(contexts))
                    ejecutar_algoritmos_en_hilos(contexts, logger)
                else:
                    # Para battle royale, acumulamos los contextos
                    contexts = [
                        AlgorithmContext(algo, case, n)
                        for algo in algorithms
                    ]
                    all_contexts.extend(contexts)
            except ValueError as e:
                print(f'Error al generar los números para {case} con {n} elementos: {e}')
                continue

    return all_contexts


if __name__ == "__main__":
    # Configuración de la carrera
    config = RaceConfig(
        race_type="battle_royale",  # o "grouped" para el comportamiento original
        cases=["best", "average", "worst"],
        elements=[1_000, 5_000]
    )

    # Configurar el logger según el tipo de carrera
    logger = setup_logger(config)

    # Preparar y ejecutar los algoritmos
    all_contexts = prepare_algorithms(config)

    # Si es battle royale, ejecutar todos los algoritmos juntos
    if config.race_type == "battle_royale" and all_contexts:
        total_algorithms = len(all_contexts)
        print(f'\nIniciando Battle Royale con {total_algorithms} algoritmos...\n')
        logger.set_expected_algorithms('battle_royale', 0, total_algorithms)
        ejecutar_algoritmos_en_hilos(all_contexts, logger)
