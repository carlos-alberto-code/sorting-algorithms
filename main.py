from typing import List, Literal
from dataclasses import dataclass

from util.numbers_generator import generate_numbers
from sorting_algorithms.algorithms import crear_algoritmos
from hilos import ejecutar_algoritmos_en_hilos, AlgorithmContext
from util.logger import Logger, GroupedStrategy, BattleStrategy, TournamentStrategy


@dataclass
class RaceConfig:
    race_type: Literal["grouped", "battle_royale", "tournament"]
    cases: List[str]
    elements: List[int]


def get_strategy(race_type: str):
    strategies = {
        "grouped": GroupedStrategy(),
        "battle_royale": BattleStrategy(),
        "tournament": TournamentStrategy()
    }
    return strategies.get(race_type)


def setup_logger(config: RaceConfig) -> Logger:
    strategy = get_strategy(config.race_type)
    if not strategy:
        raise ValueError(f"Tipo de carrera no válido: {config.race_type}")

    logger = Logger(race_strategy=strategy)
    logger.clear_log()
    return logger


def prepare_algorithms(config: RaceConfig, logger: Logger) -> List[AlgorithmContext]:
    all_contexts = []

    for n in config.elements:
        current_contexts = []

        for case in config.cases:
            try:
                nums = generate_numbers(case, n)
                algorithms = crear_algoritmos(nums)

                contexts = [
                    AlgorithmContext(algo, case, n)
                    for algo in algorithms
                ]

                if config.race_type == "grouped":
                    # Ejecución inmediata para carreras agrupadas
                    logger.set_expected_algorithms(case, n, len(contexts))
                    ejecutar_algoritmos_en_hilos(contexts, logger)
                else:
                    # Acumular contextos para battle_royale o tournament
                    current_contexts.extend(contexts)

            except ValueError as e:
                print(f'Error al generar los números para {case} con {n} elementos: {e}')
                continue

        if config.race_type == "tournament" and current_contexts:
            # Para torneo, ejecutamos cada grupo de elementos por separado
            logger.set_expected_algorithms('tournament', n, len(current_contexts))
            ejecutar_algoritmos_en_hilos(current_contexts, logger)
        elif config.race_type == "battle_royale":
            # Para battle royale, acumulamos todos los contextos
            all_contexts.extend(current_contexts)

    return all_contexts


if __name__ == "__main__":
    # Configuración de ejemplo para diferentes tipos de carreras
    configs = [
        RaceConfig(
            race_type="grouped",
            cases=["best", "average", "worst"],
            elements=[1_000]
        ),
        RaceConfig(
            race_type="battle_royale",
            cases=["best", "average", "worst"],
            elements=[1_000, 5_000]
        ),
        RaceConfig(
            race_type="tournament",
            cases=["best", "average", "worst"],
            elements=[1_000]
        )
    ]

    # Ejecutar cada configuración
    for config in configs:
        print(f"\nIniciando carrera tipo: {config.race_type}")
        print(f"Elementos: {config.elements}")
        print(f"Casos: {config.cases}\n")

        logger = setup_logger(config)
        all_contexts = prepare_algorithms(config, logger)

        # Manejar battle_royale que requiere ejecución conjunta
        if config.race_type == "battle_royale" and all_contexts:
            total_algorithms = len(all_contexts)
            print(f'Iniciando Battle Royale con {total_algorithms} algoritmos...\n')
            logger.set_expected_algorithms('battle_royale', 0, total_algorithms)
            ejecutar_algoritmos_en_hilos(all_contexts, logger)
