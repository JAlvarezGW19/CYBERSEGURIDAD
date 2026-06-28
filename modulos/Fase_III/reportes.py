import os
import json
import csv
import datetime
from typing import Dict, Any, List, Tuple

class GeneradorReportes:
    """
    Grupo 2: Módulo de Generación de Reportes.
    Responsable de recibir el historial de auditoría y exportarlo a formatos legibles 
    (HTML, CSV, TXT) para su presentación final.
    """
    def __init__(self, resultados: List[Dict[str, Any]], output_dir: str = "reportes") -> None:
        """Inicializa el generador de reportes.

        Args:
            resultados (List[Dict[str, Any]]): Historial de resultados de la auditoría.
            output_dir (str): Directorio donde se guardarán los reportes generados.
        """
        self.resultados = resultados
        self.output_dir = output_dir
        
        # Crear el directorio de reportes si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _generar_html_dinamico(self, data: Any) -> str:
        """Método auxiliar recursivo para convertir diccionarios y listas anidadas en tablas HTML.

        Args:
            data (Any): Estructura de datos a convertir (dict, list o tipo simple).

        Returns:
            str: Código HTML generado para representar los datos.
        """
        if isinstance(data, dict):
            if not data:
                return "<span class='text-muted'>Sin datos</span>"
            html = "<table class='table table-sm table-bordered mt-2'><tbody>"
            for key, value in data.items():
                html += f"<tr><th class='bg-light w-25'>{key.replace('_', ' ').capitalize()}</th>"
                html += f"<td>{self._generar_html_dinamico(value)}</td></tr>"
            html += "</tbody></table>"
            return html
            
        elif isinstance(data, list):
            if not data:
                return "<span class='text-muted'>Vacío</span>"
                
            # Si es una lista de diccionarios (Ej. detalles de puertos escaneados)
            if isinstance(data[0], dict):
                keys = data[0].keys()
                html = "<table class='table table-sm table-striped mt-2'><thead class='table-dark'><tr>"
                for k in keys:
                    html += f"<th>{k.replace('_', ' ').capitalize()}</th>"
                html += "</tr></thead><tbody>"
                for item in data:
                    html += "<tr>"
                    for k in keys:
                        html += f"<td>{item.get(k, '')}</td>"
                    html += "</tr>"
                html += "</tbody></table>"
                return html
            else:
                # Si es una lista simple (Ej. correos, subdominios, o vulnerabilidades)
                html = "<ul class='list-group list-group-flush'>"
                for item in data:
                    html += f"<li class='list-group-item py-1'>{item}</li>"
                html += "</ul>"
                return html
        else:
            return str(data)

    def generar_html(self) -> str:
        """Genera un reporte dinámico y estructurado en formato HTML.

        Returns:
            str: Ruta del archivo HTML creado.
        """
        print("[*] (G2-E2) Generando reporte HTML gerencial...")
        html_path = os.path.join(self.output_dir, "reporte_auditoria.html")
        timestamp_reporte = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_modulos = len(self.resultados)
        errores = sum(1 for item in self.resultados if item.get("status") == "error")

        # Plantilla Base HTML con CDN de Bootstrap 5
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Ejecutivo - Auditoría de Seguridad</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; }}
        .card-header {{ font-weight: bold; }}
        .modulo-success {{ border-left: 5px solid #198754; }}
        .modulo-error {{ border-left: 5px solid #dc3545; }}
    </style>
</head>
<body>
    <div class="container my-5">
        <div class="text-center mb-5">
            <h1 class="display-5 fw-bold text-dark">Suite de Auditoría de Seguridad</h1>
            <p class="lead text-muted">Reporte Ejecutivo de Vulnerabilidades y Reconocimiento</p>
        </div>

        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title text-muted">Fecha del Reporte</h5>
                        <h3 class="card-text">{timestamp_reporte}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title text-muted">Módulos Ejecutados</h5>
                        <h3 class="card-text text-primary">{total_modulos}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title text-muted">Errores Detectados</h5>
                        <h3 class="card-text {'text-danger' if errores > 0 else 'text-success'}">{errores}</h3>
                    </div>
                </div>
            </div>
        </div>

        <h3 class="mb-4 border-bottom pb-2">Detalle de Resultados por Módulo</h3>
"""

        # Iterar sobre el historial y crear una tarjeta por cada ejecución
        for res in self.resultados:
            status = res.get("status", "error")
            color_class = "modulo-success" if status == "success" else "modulo-error"
            badge_color = "bg-success" if status == "success" else "bg-danger"
            
            modulo = res.get("modulo", "Desconocido")
            target = res.get("target", "Desconocido")
            data_html = self._generar_html_dinamico(res.get("data", {}))
            error_msg = res.get("error_message")

            html_content += f"""
        <div class="card mb-4 shadow-sm {color_class}">
            <div class="card-header d-flex justify-content-between align-items-center bg-white">
                <span>Módulo: <span class="text-primary">{modulo}</span></span>
                <span class="badge {badge_color}">{status.upper()}</span>
            </div>
            <div class="card-body">
                <h6 class="card-subtitle mb-3 text-muted">Objetivo Evaluado: {target}</h6>
"""
            if error_msg:
                html_content += f'<div class="alert alert-danger" role="alert"><strong>Error Registrado:</strong> {error_msg}</div>'
            
            html_content += f"""
                <div>{data_html}</div>
            </div>
            <div class="card-footer text-muted text-end" style="font-size: 0.85rem;">
                Grupo: {res.get("grupo", "N/A")} | Auditor: {res.get("estudiante", "N/A")} | Ejecución: {res.get("timestamp", "N/A")[:19]}
            </div>
        </div>
"""

        # Cierre del HTML
        html_content += """
    </div>
</body>
</html>
"""
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return html_path

    def generar_csv_txt(self) -> Tuple[str, str]:
        """Exporta los datos de auditoría a formatos CSV y TXT.

        Returns:
            Tuple[str, str]: Rutas de los archivos CSV y TXT creados, respectivamente.
        """
        print("[*] (G2-E3) Generando reportes planos (CSV/TXT)...")
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
        """Ejecuta la generación de todos los reportes (HTML, CSV, TXT).

        Returns:
            Dict[str, Any]: Diccionario que cumple con el contrato de datos.
        """
        rutas_generadas = {}
        
        try:
            # Integración total del E2 y E3
            html_path = self.generar_html()
            csv_path, txt_path = self.generar_csv_txt()
            
            rutas_generadas['html'] = html_path
            rutas_generadas['csv'] = csv_path
            rutas_generadas['txt'] = txt_path
            
        except Exception as e:
            return {
                "modulo": "REPORTES",
                "grupo": 2,
                "estudiante": "Grupo 2",
                "target": "Múltiples (Historial)",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "error",
                "error_message": str(e),
                "data": {}
            }

        return {
            "modulo": "REPORTES",
            "grupo": 2,
            "estudiante": "Grupo 2",
            "target": "Múltiples (Historial)",
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "error_message": None,
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
        "data": {"vulnerabilities_sqli": ["Inyección exitosa en el parámetro cat=1"]},
        "timestamp": "2026-06-25T14:30:00"
    }]
    generador = GeneradorReportes(datos_prueba)
    resultado = generador.run()
    print(json.dumps(resultado, indent=4, ensure_ascii=False))