# Grupo 2: OSINT y Huella Digital (3 estudiantes)
import datetime
import whois
import requests
from googlesearch import search


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

def check_archivos_expuestos(target: str) -> dict:
    """
    Estudiante 3: Detección de archivos expuestos en el target usando Google Dorks.
    
    Realiza una búsqueda pasiva en Google buscando archivos sensibles 
    (ej: filetype:log, filetype:ini) indexados para el dominio especificado.
    
    Args:
        target (str): El dominio a consultar (ej: dominio.com).
        
    Returns:
        dict: Resultado siguiendo el esquema oficial en docs/schema_resultados.json.
    """
    # preparamos el diccionario de retorno
    resultado = {
        "modulo": "OSINT",
        "grupo": 2,
        "estudiante": "E3",
        "target": target,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }
    
    # Limpiar el target por si pasaron http:// o https://
    dominio = target.replace("http://", "").replace("https://", "").strip("/")
    
    # Los dorks solicitados
    dorks = [
        f"site:{dominio} filetype:log",
        f"site:{dominio} filetype:ini",
        f"site:{dominio} filetype:env",
        f"site:{dominio} filetype:sql"
    ]
    
    enlaces_encontrados = []
    
    try:
        print(f"  [G2-E3] Realizando búsqueda pasiva (Google Dorks) para: {dominio}")
        
        for dork in dorks:
            print(f"    -> Buscando: {dork}")
            # Buscamos en google, num_results limita la busqueda para no tardar tanto
            try:
                for resultado_busqueda in search(dork, num_results=5, sleep_interval=5):
                    enlaces_encontrados.append(resultado_busqueda)
            except Exception as search_err:
                if "429" in str(search_err):
                    print("    [!] Google ha bloqueado temporalmente las consultas automatizadas (Error 429).")
                    # Rompemos el ciclo porque Google ya nos bloqueó la IP temporalmente
                    break
                else:
                    raise search_err
                
        # Eliminamos duplicados por si acaso
        enlaces_unicos = list(set(enlaces_encontrados))
                
        resultado["data"] = {
            "total_encontrados": len(enlaces_unicos),
            "archivos_indexados": enlaces_unicos,
            "nota": "Búsqueda completada o interrumpida por rate-limit de Google."
        }
        
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
        
    return resultado