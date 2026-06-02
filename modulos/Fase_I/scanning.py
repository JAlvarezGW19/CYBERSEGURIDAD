import datetime
import socket
from typing import Dict, Any

def scan_ports_dispatcher(target: str, ports: str) -> Dict[str, Any]:
    """
    Realiza un escaneo de puertos TCP real a un objetivo específico,
    cumpliendo con el contrato estricto del proyecto.
    """
    resultado = {
        "modulo": "Scanning",
        "grupo": 4,
        "estudiante": "E1", 
        "target": target,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {},
        "error_message": None
    }

    try:
        # Procesar la cadena de puertos
        puertos_lista = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        resultados_puertos = []
        
        print(f"\n  [G4] Iniciando escaneo real de puertos por sockets en: {target}")
        
        # LÓGICA REAL DE ESCANEO POR SOCKETS
        for puerto in puertos_lista:
            # Crear socket TCP
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)  # Tiempo de espera seguro
            
            # Intentar conexión
            conexion_codigo = s.connect_ex((target, puerto))
            
            # 0 significa que la conexión fue exitosa (Puerto Abierto)
            estado = "abierto" if conexion_codigo == 0 else "cerrado"
            
            resultados_puertos.append({
                "puerto": puerto,
                "estado": estado,
                "protocolo": "TCP"
            })
            
            # Cerrar el flujo del socket
            s.close()

        # Guardamos las estadísticas reales dentro del molde solicitado
        resultado["data"] = {
            "puertos_escaneados": puertos_lista,
            "detalles": resultados_puertos
        }
        
    except Exception as e:
        # Si algo falla, atrapamos el error para que el sistema no muera
        resultado["status"] = "error"
        resultado["error_message"] = f"Error en el escaneo de puertos: {str(e)}"

    return resultado

# Bloque de prueba local
if __name__ == "__main__":
    import json
    print("[*] Ejecutando auditoría real local...")
    resultado_prueba = scan_ports_dispatcher("127.0.0.1", "21, 22, 80, 443, 8080")
    print(json.dumps(resultado_prueba, indent=4))
