from threading  import Lock
from datetime   import datetime
from typing     import Dict, List, Tuple


class Logger:
    def __init__(self, log_file: str = "log.txt"):
        self.log_file = log_file
        self._lock = Lock()
        self._current_race: Dict[Tuple[str, int], List[Tuple[str, float]]] = {}
        self._expected_algorithms: Dict[Tuple[str, int], int] = {}  # Nuevo diccionario

    def clear_log(self):
        with open(self.log_file, "w", encoding="utf-8") as log_file:
            log_file.write("=== CARRERA DE ALGORITMOS DE ORDENAMIENTO ===\n")
            log_file.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    def set_expected_algorithms(self, case: str, elements: int, count: int):
        """Establece cuántos algoritmos se esperan para una carrera específica"""
        self._expected_algorithms[(case, elements)] = count

    def log_finish(self, case: str, elements: int, algorithm_name: str, time_taken: float):
        key = (case, elements)
        with self._lock:
            if key not in self._current_race:
                self._current_race[key] = []
            self._current_race[key].append((algorithm_name, time_taken))

            expected_count = self._expected_algorithms.get(key)
            if expected_count and len(self._current_race[key]) == expected_count:
                self._write_race_results(case, elements)
                del self._current_race[key]
                del self._expected_algorithms[key]

    def _write_race_results(self, case: str, elements: int):
        case_names = {
            "best": "MEJOR CASO",
            "average": "CASO PROMEDIO",
            "worst": "PEOR CASO"
        }

        results = sorted(self._current_race[(case, elements)], key=lambda x: x[1])

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\nCarrera en {case_names[case]}\n")
            f.write(f"Elementos: {elements:,}\n")
            f.write("-" * 50 + "\n")

            f.write(f"{'Posición':<10}{'Algoritmo':<20}{'Tiempo':<15}\n")
            f.write("-" * 50 + "\n")

            for position, (algorithm, time_taken) in enumerate(results, 1):
                f.write(f"{position:<10}{algorithm:<20}{time_taken:.4f} seg\n")

            f.write("=" * 50 + "\n\n")
            f.write(f"Ganador: {results[0][0]}\n")
            f.write(f"Diferencia con el último: {results[-1][1] - results[0][1]:.4f} seg\n")
            f.write("\n" + "=" * 50 + "\n\n")
