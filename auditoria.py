# auditoria.py
import argparse
import sys
import json
import os

try:
    from jsonschema import validate
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

from modulos import dns_recon   # Grupo 1
from modulos import osint       # Grupo 2
from modulos import discovery   # Grupo 3
from modulos import scanning    # Grupo 4

def validar_resultado(resultado):
    """
    Verifica si el diccionario retornado por un modulo cumple con el esquema oficial.
    """
    if resultado is None:
        return

    if not HAS_JSONSCHEMA:
        print("  [!] Aviso: Libreria 'jsonschema' no encontrada. Omitiendo validacion estricta.")
        print("      Instale con: pip install jsonschema")
        return

    schema_path = os.path.join(os.path.dirname(__file__), "docs/schema_resultados.json")
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        validate(instance=resultado, schema=schema)
        print(f"  [OK] Validacion de esquema exitosa para: {resultado.get('modulo')} (Estudiante: {resultado.get('estudiante')})")
    except Exception as e:
        print(f"  [X] ERROR DE CONTRATO en modulo '{resultado.get('modulo', 'Desconocido')}':")
        print(f"      Detalle: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Suite de Auditoria de Seguridad Informatica - Python",
        epilog="Uso: python auditoria.py target.com --dns-all"
    )
    
    parser.add_argument("target", help="Dominio o IP objetivo")

    # Grupo para Recopilacion de Informacion
    recon_group = parser.add_argument_group('Recopilacion de Informacion')
    recon_group.add_argument("--dns-all", action="store_true", help="Ejecuta todos los checks DNS/WHOIS")
    recon_group.add_argument("--dns-a", action="store_true", help="Registros A/AAAA (G1-E1)")
    recon_group.add_argument("--dns-mxns", action="store_true", help="Registros MX/NS (G1-E2)")
    recon_group.add_argument("--dns-txtsoa", action="store_true", help="Registros TXT/SOA (G1-E3)")
    
    # Grupo OSINT (Grupo 2)
    osint_group = parser.add_argument_group('OSINT y Huella Digital')
    osint_group.add_argument("--whois", action="store_true", help="Consulta WHOIS (G2-E1)")
    osint_group.add_argument("--dorks", action="store_true", help="Búsqueda de subdominios/dorks (G2-E2/E3)")

    # Grupo para Escaneo
    scan_group = parser.add_argument_group('Escaneo de Puertos')
    scan_group.add_argument("--scan", metavar="PUERTOS", help="Escaneo TCP/UDP (Grupo 4)")
    scan_group.add_argument("--ping-sweep", action="store_true", help="Descubrimiento de hosts (Grupo 3)")

    args = parser.parse_args()

    print(f"[*] Iniciando auditoria para: {args.target}")

    try:
        # Logica para DNS (Semana 1)
        try:
            if args.dns_all:
                validar_resultado(dns_recon.get_a_records(args.target))
                validar_resultado(dns_recon.get_mx_ns_records(args.target))
                validar_resultado(dns_recon.get_txt_soa_records(args.target))
            
            if args.dns_a:
                validar_resultado(dns_recon.get_a_records(args.target))
                
            if args.dns_mxns:
                validar_resultado(dns_recon.get_mx_ns_records(args.target))
                
            if args.dns_txtsoa:
                validar_resultado(dns_recon.get_txt_soa_records(args.target))

            if args.whois:
                validar_resultado(osint.get_whois_data(args.target))

            if args.ping_sweep:
                validar_resultado(discovery.ping_sweep(args.target))

            if args.scan:
                validar_resultado(scanning.scan_ports_dispatcher(args.target, args.scan))

        except (NotImplementedError, AttributeError) as e:
            print(f"\n[!] Característica no disponible: {e}")

    except KeyboardInterrupt:
        print("\n[!] Auditoria interrumpida por el usuario.")
        sys.exit(1)

if __name__ == "__main__":
    main()