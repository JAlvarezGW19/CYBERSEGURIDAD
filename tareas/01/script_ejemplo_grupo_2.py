import datetime
from typing import Dict, Any

def get_whois_data(domain: str) -> Dict[str, Any]:
    """
    Consulta información WHOIS para obtener datos administrativos del dominio.

    Args:
        domain (str): El dominio o IP a consultar.

    Returns:
        Dict[str, Any]: Diccionario con los resultados de la auditoría,
        cumpliendo con el esquema definido en docs/schema_resultados.json.
    """
    # 1. Estructura base
    resultado = {
        "modulo": "OSINT",
        "grupo": 2,
        "estudiante": "E1",
        "target": domain,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }

    try:
        # 2. Lógica principal (Aquí iría la llamada a python-whois)
        
        # 3. Guardar datos en el formato adecuado
        resultado["data"] = {
            "registrar": "Ejemplo Registrar, Inc.",
            "creation_date": "1997-09-15 04:00:00",
            "expiration_date": "2028-09-14 04:00:00",
            "name_servers": ["ns1.ejemplo.com", "ns2.ejemplo.com"]
        }
        
    except Exception as e:
        # 4. Manejo de excepciones
        resultado["status"] = "error"
        resultado["error_message"] = f"Error en consulta WHOIS: {str(e)}"

    return resultado

# Bloque de prueba local para el estudiante
if __name__ == "__main__":
    import json
    print("[*] Ejecutando prueba local...")
    resultado_prueba = get_whois_data("ejemplo.com")
    print(json.dumps(resultado_prueba, indent=4))