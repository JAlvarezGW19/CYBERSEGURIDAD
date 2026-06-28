"""
Grupo 2 - Fase III - Estudiante 1
Archivo: main_auditor.py

Este módulo principal integra la generación de reportes del Grupo 2.
Carga los resultados desde historial_auditoria.json y llama al generador
ubicado en modulos/Fase_III/reportes.py.
"""

import argparse
import datetime
import json
import os
from typing import Any, Dict, List

from modulos.Fase_III.reportes import GeneradorReportes


def cargar_historial(ruta_historial: str) -> List[Dict[str, Any]]:
    """
    Carga el historial de auditoría desde un archivo JSON.

    Args:
        ruta_historial (str): Ruta del archivo historial_auditoria.json.

    Returns:
        List[Dict[str, Any]]: Lista de resultados cargados.
    """
    if not os.path.isfile(ruta_historial):
        print(f"[!] No existe el archivo: {ruta_historial}")
        return []

    try:
        with open(ruta_historial, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if isinstance(datos, list):
            return datos

        print("[!] El historial no tiene formato de lista.")
        return []

    except json.JSONDecodeError as error:
        print(f"[!] Error leyendo JSON: {error}")
        return []
    except Exception as error:
        print(f"[!] Error inesperado: {error}")
        return []


def ejecutar_reportes(ruta_historial: str, output_dir: str) -> Dict[str, Any]:
    """
    Ejecuta el generador de reportes del Grupo 2.

    Args:
        ruta_historial (str): Archivo de historial de auditoría.
        output_dir (str): Carpeta de salida para los reportes.

    Returns:
        Dict[str, Any]: Resultado estructurado de la ejecución.
    """
    resultados = cargar_historial(ruta_historial)

    if not resultados:
        return {
            "modulo": "MAIN_AUDITOR",
            "grupo": 2,
            "estudiante": "E1",
            "target": ruta_historial,
            "status": "error",
            "data": {},
            "error_message": "No hay datos disponibles para generar reportes."
        }

    try:
        generador = GeneradorReportes(resultados, output_dir=output_dir)
        resultado_reporte = generador.run()

        return {
            "modulo": "MAIN_AUDITOR",
            "grupo": 2,
            "estudiante": "E1",
            "target": ruta_historial,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "data": {
                "resultados_procesados": len(resultados),
                "reportes": resultado_reporte
            },
            "error_message": None
        }

    except Exception as error:
        return {
            "modulo": "MAIN_AUDITOR",
            "grupo": 2,
            "estudiante": "E1",
            "target": ruta_historial,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "error",
            "data": {},
            "error_message": str(error)
        }


def main() -> None:
    """
    Punto de entrada del módulo principal de reportes.
    """
    parser = argparse.ArgumentParser(
        description="Main Auditor - Grupo 2 Fase III"
    )

    parser.add_argument(
        "--historial",
        default="historial_auditoria.json",
        help="Ruta del archivo historial_auditoria.json"
    )

    parser.add_argument(
        "--output",
        default="reportes",
        help="Carpeta donde se guardarán los reportes"
    )

    args = parser.parse_args()

    print("[*] Ejecutando main_auditor.py")
    print(f"[*] Historial: {args.historial}")
    print(f"[*] Salida: {args.output}")

    resultado = ejecutar_reportes(args.historial, args.output)

    print(json.dumps(resultado, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()