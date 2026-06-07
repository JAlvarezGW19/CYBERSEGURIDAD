import datetime
from typing import Dict, Any

def scan_ports_dispatcher(target: str, ports: str) -> Dict[str, Any]:
    """
    Realiza un escaneo de puertos TCP/UDP a un objetivo específico.

    Args:
        target (str): La dirección IP o dominio a escanear.
        ports (str): Cadena con los puertos separados por comas (ej. '80,443,22').

    Returns:
        Dict[str, Any]: Diccionario con los resultados de la auditoría,
        cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    resultado = {
        "modulo": "Scanning",
        "grupo": 4,
        "estudiante": "E1", # En este caso el orquestador o estudiante a cargo
        "target": target,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }

    try:
        # Procesar entrada de puertos
        puertos_lista = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        resultados_puertos = []
        
        # Lógica real de escaneo de puertos (Ej. usando socket)
        # Simulación:
        for puerto in puertos_lista:
            estado = "abierto" if puerto in [80, 443] else "cerrado"
            resultados_puertos.append({
                "puerto": puerto,
                "estado": estado,
                "protocolo": "TCP"
            })

        resultado["data"] = {
            "puertos_escaneados": puertos_lista,
            "detalles": resultados_puertos
        }
        
    except Exception as e:
        # Manejo de error al parsear o escanear
        resultado["status"] = "error"
        resultado["error_message"] = f"Error en el escaneo de puertos: {str(e)}"

    return resultado

# Bloque de prueba local para el estudiante
if __name__ == "__main__":
    import json
    print("[*] Ejecutando prueba local...")
    resultado_prueba = scan_ports_dispatcher("8.8.8.8", "22, 80, 443")
    print(json.dumps(resultado_prueba, indent=4))