# Grupo 2: OSINT y Huella Digital (3 estudiantes)
import whois

def get_whois_data(domain):
    """Estudiante 1: Consulta WHOIS"""
    print(f"  [G2-E1] Obteniendo información WHOIS para: {domain}")
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        print(f"  [!] Error en WHOIS: {e}")