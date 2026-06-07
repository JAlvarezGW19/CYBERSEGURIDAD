import datetime
from typing import Dict, Any

def get_a_records(domain: str) -> Dict[str, Any]:
    """
    Consulta los registros DNS de tipo A y AAAA para un dominio.

    Args:
        domain (str): El nombre de dominio a investigar (ej. 'google.com').

    Returns:
        Dict[str, Any]: Diccionario con los resultados de la auditoría,
        cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    # 1. Definir la estructura base requerida por el contrato
    resultado = {
        "modulo": "DNS",
        "grupo": 1,
        "estudiante": "E1",
        "target": domain,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }

    try:
        # 2. Aquí va la lógica real (ej. import dns.resolver)
        # Para este ejemplo, simularemos una respuesta exitosa
        
        ips_encontradas = ["192.168.1.100", "10.0.0.5"] # Simulación
        
        # 3. Guardar los hallazgos técnicos en la clave "data"
        resultado["data"] = {
            "registros_a": ips_encontradas,
            "registros_aaaa": []
        }
        
    except Exception as e:
        # 4. Manejo de errores: Si algo falla, la aplicación NO debe caerse.
        # Se actualiza el estado y se registra el error.
        resultado["status"] = "error"
        resultado["error_message"] = f"Error al consultar DNS: {str(e)}"

    return resultado

# Bloque de prueba local para el estudiante
if __name__ == "__main__":
    import json
    print("[*] Ejecutando prueba local...")
    resultado_prueba = get_a_records("ejemplo.com")
    print(json.dumps(resultado_prueba, indent=4))