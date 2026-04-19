# Grupo 2: OSINT y Huella Digital (3 estudiantes)
import datetime
import whois

def get_whois_data(domain: str) -> dict:
    """
    Estudiante 1: Consulta WHOIS para obtener información administrativa.
    
    Args:
        domain (str): El dominio o IP a consultar.
        
    Returns:
        dict: Resultado siguiendo el esquema oficial en docs/schema_resultados.json.
    """
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
        print(f"  [G2-E1] Obteniendo información WHOIS para: {domain}")
        w = whois.whois(domain)
        
        resultado["data"] = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date) if w.creation_date else "N/A",
            "expiration_date": str(w.expiration_date) if w.expiration_date else "N/A",
            "name_servers": w.name_servers if w.name_servers else []
        }
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
    
    return resultado