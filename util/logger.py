def log_results(case: str, element: int, algorithm: str, time_taken: float, is_last_algorithm: bool):
    # Mapeo de casos a sus títulos en el log
    case_titles = {
        "best": "MEJOR DE LOS CASOS",
        "average": "CASO PROMEDIO",
        "worst": "PEOR DE LOS CASOS"
    }

    with open("log.txt", "r", encoding="utf-8") as check_file:
        content = check_file.read()

    with open("log.txt", "a", encoding="utf-8") as log_file:
        # Si es un nuevo caso, agregar el encabezado del caso
        if case_titles[case] not in content:
            log_file.write(f"=== {case_titles[case]} ===\n\n")

        # Buscar si ya existe una sección para este elemento en el caso actual
        current_case_content = content.split(f"=== {case_titles[case]} ===")[-1].split("===")[0]
        section_header = f"--- Elementos: {element:,} ---"

        # Si no encontramos el header para estos elementos en el caso actual, lo agregamos
        if section_header not in current_case_content:
            log_file.write(f"{section_header}\n")

        # Registra el resultado del algoritmo
        log_file.write(f"{algorithm:<15}{time_taken:.2f} Segundos\n")

        # Solo agregar línea en blanco si es el último algoritmo del grupo
        if is_last_algorithm:
            log_file.write("\n")
