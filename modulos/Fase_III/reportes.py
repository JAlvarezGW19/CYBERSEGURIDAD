import os
import json
import csv
from typing import Dict, Any, List, Tuple

class GeneradorReportes:
    """
    Grupo 2: Módulo de Generación de Reportes.
    Responsable de recibir el historial de auditoría y exportarlo a formatos legibles 
    (HTML, CSV, TXT) para su presentación final.
    """
    def __init__(self, resultados: List[Dict[str, Any]], output_dir: str = "reportes"):
        self.resultados = resultados
        self.output_dir = output_dir
        
        # Crear el directorio de reportes si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generar_html(self) -> str:
        """
        (Estudiante 2) Genera un reporte dinámico y estructurado en formato HTML.
        Retorna la ruta absoluta o relativa del archivo creado.
        """
        # TODO: Implementar lógica de iteración sobre self.resultados 
        # y construcción del HTML (usando cadenas formateadas o Jinja2)
        raise NotImplementedError("Estudiante 2: Implementar Generación de Reporte HTML")

    def generar_csv_txt(self) -> Tuple[str, str]:
        """
        (Estudiante 3) Exporta los datos a formatos tabulares CSV y texto plano TXT.
        Retorna una tupla con las rutas de los archivos creados (csv_path, txt_path).
        """
        csv_path = os.path.join(self.output_dir, "reporte.csv")
        txt_path = os.path.join(self.output_dir, "reporte.txt")

        # 1. Generación de Reporte CSV
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Modulo", "Grupo", "Estudiante", "Target", "Timestamp", "Status", "Datos", "Error"])
            for res in self.resultados:
                data_str = json.dumps(res.get("data", {}), ensure_ascii=False)
                writer.writerow([
                    res.get("modulo", "N/A"),
                    res.get("grupo", "N/A"),
                    res.get("estudiante", "N/A"),
                    res.get("target", "N/A"),
                    res.get("timestamp", "N/A"),
                    res.get("status", "N/A"),
                    data_str,
                    res.get("error_message") or ""
                ])

        # 2. Generación de Reporte TXT
        with open(txt_path, mode="w", encoding="utf-8") as txt_file:
            txt_file.write("==================================================\n")
            txt_file.write("         REPORTE DE AUDITORÍA DE SEGURIDAD        \n")
            txt_file.write("==================================================\n\n")
            
            for res in self.resultados:
                txt_file.write(f"Módulo: {res.get('modulo', 'N/A')} (Grupo: {res.get('grupo', 'N/A')})\n")
                txt_file.write(f"Auditor: {res.get('estudiante', 'N/A')}\n")
                txt_file.write(f"Objetivo: {res.get('target', 'N/A')}\n")
                txt_file.write(f"Fecha/Hora: {res.get('timestamp', 'N/A')}\n")
                txt_file.write(f"Estado: {str(res.get('status', 'N/A')).upper()}\n")
                
                error_msg = res.get("error_message")
                if error_msg:
                    txt_file.write(f"Error registrado: {error_msg}\n")
                
                data_val = res.get("data", {})
                if data_val:
                    txt_file.write("Datos detallados:\n")
                    for k, v in data_val.items():
                        txt_file.write(f"  - {k}: {v}\n")
                
                txt_file.write("-" * 50 + "\n\n")

        return csv_path, txt_path

    def run(self) -> Dict[str, Any]:
        """
        Ejecuta la generación de todos los reportes y retorna un diccionario 
        con el estado de la operación y las rutas de los archivos generados.
        """
        rutas_generadas = {}
        
        try:
            csv_path, txt_path = self.generar_csv_txt()
            rutas_generadas['csv'] = csv_path
            rutas_generadas['txt'] = txt_path
        except Exception as e:
            return {
                "modulo": "REPORTES",
                "estudiante": "Grupo 2",
                "target": "Múltiples (Historial)",
                "status": "error",
                "error_message": str(e),
                "data": {}
            }

        return {
            "modulo": "REPORTES",
            "estudiante": "Grupo 2",
            "target": "Múltiples (Historial)",
            "status": "success",
            "data": rutas_generadas
        }

if __name__ == "__main__":
    # Área de pruebas aisladas para el Grupo 2
    print("[*] Iniciando prueba local del Generador de Reportes...")
    datos_prueba = [{
        "modulo": "VULN_SQLI",
        "estudiante": "Grupo 3",
        "target": "http://testphp.vulnweb.com",
        "status": "success",
        "data": {"vulnerabilities_sqli": ["Inyección exitosa en el parámetro cat=1"]}
    }]
    generador = GeneradorReportes(datos_prueba)
    resultado = generador.run()
    print(resultado)