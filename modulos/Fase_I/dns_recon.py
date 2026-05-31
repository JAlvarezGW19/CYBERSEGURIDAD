# Grupo 1: Reconocimiento DNS (3 estudiantes)
import dns.resolver
from typing import Dict, Any
from datetime import datetime

def get_a_records(domain: str) -> Dict[str, Any]:
    """
    Consulta los registros DNS de tipo A (IPv4) y AAAA (IPv6) para un dominio.

    Args:
        domain (str): El nombre de dominio a investigar (ej. 'google.com').

    Returns:
        Dict[str, Any]: Diccionario con los resultados de la auditoria, 
        siguiendo el formato definido en schema_resultados.json.
    """
    print(f"  [G1-E1] Consultando registros A/AAAA para: {domain}")
    
    resultado = {
        "modulo": "Reconocimiento DNS",
        "grupo": 1,
        "estudiante": "E1",
        "target": domain,
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "A": [],
            "AAAA": []
        },
        "status": "success",
        "error_message": None
    }

    # Consulta DNS tipo A
    try:
        respuestas_a = dns.resolver.resolve(domain, 'A')
        for rdata in respuestas_a:
            resultado["data"]["A"].append(str(rdata.address))
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        resultado["status"] = "error"
        resultado["error_message"] = f"El dominio '{domain}' no existe (NXDOMAIN)."
        return resultado
    except dns.resolver.NoNameservers:
        resultado["status"] = "error"
        resultado["error_message"] = f"No se pudo contactar con los servidores DNS para '{domain}'."
        return resultado
    except dns.resolver.Timeout:
        resultado["status"] = "error"
        resultado["error_message"] = f"Timeout al consultar registros A de '{domain}'."
        return resultado
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = f"Error inesperado consultando A: {str(e)}"
        return resultado

    # Consulta DNS tipo AAAA
    try:
        respuestas_aaaa = dns.resolver.resolve(domain, 'AAAA')
        for rdata in respuestas_aaaa:
            resultado["data"]["AAAA"].append(str(rdata.address))
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NXDOMAIN:
        resultado["status"] = "error"
        resultado["error_message"] = f"El dominio '{domain}' no existe (NXDOMAIN) durante consulta AAAA."
        return resultado
    except dns.resolver.NoNameservers:
        resultado["status"] = "error"
        resultado["error_message"] = f"No se pudo contactar con los servidores DNS para '{domain}' (AAAA)."
        return resultado
    except dns.resolver.Timeout:
        resultado["status"] = "error"
        resultado["error_message"] = f"Timeout al consultar registros AAAA de '{domain}'."
        return resultado
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = f"Error inesperado consultando AAAA: {str(e)}"
        return resultado

    # Si ambas listas están vacías, el contrato dicta que status debe seguir siendo "success" 
    # y lists vacías, se eliminó la validación "empty" y "querytype".
    return resultado

def get_mx_ns_records(domain: str) -> Dict[str, Any]:
    """Estudiante 2: Consulta registros MX y NS"""
    print(f"  [G1-E2] Consultando registros MX/NS para: {domain}")
    resultado = {"modulo": "Reconocimiento DNS", "grupo": 1, "estudiante": "E2", "target": domain, "timestamp": datetime.utcnow().isoformat(), "data": {"MX": [], "NS": []}, "status": "success", "error_message": None}
    try:
        for tipo in ['MX', 'NS']:
            try:
                resultado["data"][tipo] = [r.to_text() for r in dns.resolver.resolve(domain, tipo)]
            except dns.resolver.NoAnswer:
                pass
    except Exception as e:
        resultado["status"] = "error"; resultado["error_message"] = str(e)
    return resultado

def get_txt_soa_records(domain: str) -> Dict[str, Any]:
    """Estudiante 3: Consulta registros TXT y SOA"""
    print(f"  [G1-E3] Consultando registros TXT/SOA para: {domain}")
    resultado = {"modulo": "Reconocimiento DNS", "grupo": 1, "estudiante": "E3", "target": domain, "timestamp": datetime.utcnow().isoformat(), "data": {"TXT": [], "SOA": []}, "status": "success", "error_message": None}
    try:
        for tipo in ['TXT', 'SOA']:
            try:
                resultado["data"][tipo] = [r.to_text() for r in dns.resolver.resolve(domain, tipo)]
            except dns.resolver.NoAnswer:
                pass
    except Exception as e:
        resultado["status"] = "error"; resultado["error_message"] = str(e)
    return resultado