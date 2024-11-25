from threading      import Lock
from datetime       import datetime
from dataclasses    import dataclass
from typing         import Dict, List, Tuple
from abc            import ABC, abstractmethod


@dataclass
class RaceResult:
    algorithm_name: str
    time_taken: float
    case: str
    elements: int


class RaceStrategy(ABC):
    @abstractmethod
    def format_results(self, results: List[RaceResult]) -> str:
        pass

    @abstractmethod
    def get_race_key(self, result: RaceResult) -> Tuple:
        pass


class GroupedStrategy(RaceStrategy):
    def get_race_key(self, result: RaceResult) -> Tuple:
        return (result.case, result.elements)

    def format_results(self, results: List[RaceResult]) -> str:
        if not results:
            return ""

        case = results[0].case
        elements = results[0].elements

        case_names = {
            "best": "MEJOR CASO",
            "average": "CASO PROMEDIO",
            "worst": "PEOR CASO"
        }

        sorted_results = sorted(results, key=lambda x: x.time_taken)
        output = []

        output.append(f"\nCarrera en {case_names.get(case, case)}")
        if elements > 0:  # Solo mostrar elementos si es una carrera agrupada
            output.append(f"Elementos: {elements:,}")
        output.append("-" * 50)

        output.append(f"{'Posición':<10}{'Algoritmo':<20}{'Tiempo':<15}")
        output.append("-" * 50)

        for position, result in enumerate(sorted_results, 1):
            output.append(f"{position:<10}{result.algorithm_name:<20}{result.time_taken:.4f} seg")

        output.append("=" * 50)
        output.append(f"\nGanador: {sorted_results[0].algorithm_name}")
        output.append(f"Diferencia con el último: {sorted_results[-1].time_taken - sorted_results[0].time_taken:.4f} seg")
        output.append("\n" + "=" * 50 + "\n")

        return "\n".join(output)


class BattleStrategy(RaceStrategy):
    def get_race_key(self, result: RaceResult) -> Tuple:
        return ('battle_royale',)  # Una única clave para todos los resultados

    def format_results(self, results: List[RaceResult]) -> str:
        if not results:
            return ""

        sorted_results = sorted(results, key=lambda x: x.time_taken)
        output = []

        output.append("\nBATTLE ROYALE - Todos contra Todos")
        output.append("-" * 50)
        output.append(f"{'Pos':<5}{'Algoritmo':<20}{'Elementos':<12}{'Caso':<15}{'Tiempo':<10}")
        output.append("-" * 50)

        for position, result in enumerate(sorted_results, 1):
            output.append(
                f"{position:<5}"
                f"{result.algorithm_name:<20}"
                f"{result.elements:<12}"
                f"{result.case:<15}"
                f"{result.time_taken:.4f} seg"
            )

        output.append("=" * 50)
        output.append(f"\nGanador absoluto: {sorted_results[0].algorithm_name}")
        output.append(f"Con {sorted_results[0].elements} elementos en caso {sorted_results[0].case}")
        output.append(f"Tiempo: {sorted_results[0].time_taken:.4f} seg")
        output.append("\n" + "=" * 50 + "\n")

        return "\n".join(output)


class TournamentStrategy(RaceStrategy):
    def get_race_key(self, result: RaceResult) -> Tuple:
        # Agrupamos por rondas del torneo
        return ('tournament', result.elements)

    def format_results(self, results: List[RaceResult]) -> str:
        if not results:
            return ""

        # Organizamos los resultados por casos para simular rondas
        cases = {'best': [], 'average': [], 'worst': []}
        for result in results:
            cases[result.case].append(result)

        output = []
        output.append("\nTORNEO DE ALGORITMOS")
        output.append(f"Elementos: {results[0].elements:,}")
        output.append("=" * 50)

        # Procesamos cada ronda
        for case, round_results in cases.items():
            if not round_results:
                continue

            round_name = {
                'best': 'RONDA 1 - Mejor Caso',
                'average': 'RONDA 2 - Caso Promedio',
                'worst': 'RONDA 3 - Peor Caso'
            }[case]

            output.append(f"\n{round_name}")
            output.append("-" * 50)

            # Ordenamos por tiempo para esta ronda
            sorted_round = sorted(round_results, key=lambda x: x.time_taken)

            # Mostramos resultados de la ronda
            for position, result in enumerate(sorted_round, 1):
                output.append(
                    f"{position}. {result.algorithm_name:<15} "
                    f"Tiempo: {result.time_taken:.4f} seg"
                )

            # Calculamos puntos para esta ronda
            points = {
                result.algorithm_name: len(sorted_round) - position
                for position, result in enumerate(sorted_round)
            }

            output.append("\nPuntos de la ronda:")
            for algo, pts in sorted(points.items(), key=lambda x: x[1], reverse=True):
                output.append(f"{algo:<15} {pts} pts")

        # Calculamos ganador general
        total_points = {}
        for round_results in cases.values():
            sorted_round = sorted(round_results, key=lambda x: x.time_taken)
            for position, result in enumerate(sorted_round):
                if result.algorithm_name not in total_points:
                    total_points[result.algorithm_name] = 0
                total_points[result.algorithm_name] += len(sorted_round) - position

        output.append("\n" + "=" * 50)
        output.append("\nRESULTADOS FINALES DEL TORNEO")
        output.append("-" * 50)

        # Mostramos tabla final de posiciones
        sorted_final = sorted(total_points.items(), key=lambda x: x[1], reverse=True)
        for position, (algo, points) in enumerate(sorted_final, 1):
            output.append(f"{position}. {algo:<15} {points} pts")

        output.append("\n" + "=" * 50)
        output.append(f"CAMPEÓN DEL TORNEO: {sorted_final[0][0]}")
        output.append(f"Puntos totales: {sorted_final[0][1]}")
        output.append("=" * 50 + "\n")

        return "\n".join(output)


class Logger:
    def __init__(self, log_file: str = "log.txt", race_strategy: RaceStrategy = GroupedStrategy()):
        self.log_file = log_file
        self.race_strategy = race_strategy
        self._lock = Lock()
        self._current_races: Dict[Tuple, List[RaceResult]] = {}
        self._expected_counts: Dict[Tuple, int] = {}

    def set_race_strategy(self, strategy: RaceStrategy):
        self._lock.acquire()
        self.race_strategy = strategy
        self._current_races.clear()
        self._expected_counts.clear()
        self._lock.release()

    def clear_log(self):
        with open(self.log_file, "w", encoding="utf-8") as log_file:
            log_file.write("=== CARRERA DE ALGORITMOS DE ORDENAMIENTO ===\n")
            log_file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    def set_expected_algorithms(self, case: str, elements: int, count: int):
        key = self.race_strategy.get_race_key(RaceResult("", 0, case, elements))
        with self._lock:
            self._expected_counts[key] = count

    def log_finish(self, case: str, elements: int, algorithm_name: str, time_taken: float):
        result = RaceResult(algorithm_name, time_taken, case, elements)
        key = self.race_strategy.get_race_key(result)

        with self._lock:
            if key not in self._current_races:
                self._current_races[key] = []
            self._current_races[key].append(result)

            expected_count = self._expected_counts.get(key)
            if expected_count and len(self._current_races[key]) == expected_count:
                self._write_race_results(key)
                del self._current_races[key]
                del self._expected_counts[key]

    def _write_race_results(self, race_key: Tuple):
        results = self._current_races[race_key]
        formatted_results = self.race_strategy.format_results(results)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted_results)
