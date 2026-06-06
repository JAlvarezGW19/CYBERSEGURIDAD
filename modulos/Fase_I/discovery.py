# Grupo 3: Descubrimiento de Hosts (3 estudiantes - listo el pull request)
import datetime
import ipaddress
import subprocess
import platform
import socket

try:
    from scapy.all import IP, TCP, sr1, send  # type: ignore
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

def _resolver_objetivo(target: str) -> str:
    """Utilidad interna: Resuelve dominios a IP o retorna la IP/CIDR original."""
    try:
        # Verifica si ya es una IP o rango válido
        ipaddress.ip_network(target, strict=False)
        return target
    except ValueError:
        try:
            return socket.gethostbyname(target)
        except socket.gaierror:
            raise ValueError(f"No se pudo resolver el dominio: {target}")

def ping_sweep(target_range: str, timeout: int = 10) -> dict:
    """
    Estudiante 1: Implementa un ping sweep utilizando el comando ping para identificar hosts activos en una red.

    Args:
        target_range (str): El rango de red en formato CIDR
        timeout (int): Timeout en ms para cada ping en Windows (default: 10 ms).
    
    Returns:
        dict: Resultados de la auditoría, cumpliendo con el esquema definido.
    """
    resultado = {
        "modulo": "Discovery",
        "grupo": 3,
        "estudiante": "E1",
        "target": target_range,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {"hosts_activos": []},
        "error_message": None
    }
    try:
        objetivo_resuelto = _resolver_objetivo(target_range)
        red = ipaddress.ip_network(objetivo_resuelto, strict=False)
        sistema = platform.system().lower()
        
        for host in red.hosts():
            direccion = str(host)
            # Adaptación para compatibilidad multiplataforma
            if sistema == "windows":
                comando = ["ping", "-n", "1", "-w", str(timeout), direccion]
            else:
                # En Linux/macOS usamos -c para count y -W para timeout en segundos
                comando = ["ping", "-c", "1", "-W", "1", direccion]
                
            respuesta = subprocess.run(comando, capture_output=True, text=True)
            if respuesta.returncode == 0:
                print(f"  [+] Host activo (Ping Echo): {direccion}")
                resultado["data"]["hosts_activos"].append(direccion)
                
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
        
    return resultado

def ping_tcp_syn(target_range: str) -> dict:
    """
    Estudiante 2: Realiza un escaneo de descubrimiento mediante TCP SYN a un puerto común (80).

    Args:
        target_range (str): El rango de red a escanear en notación CIDR.

    Returns:
        dict: Resultados del escaneo siguiendo el esquema JSON definido.
    """
    resultado = {
        'modulo': 'Discovery',
        'grupo': 3,
        'estudiante': 'E2',
        'target': target_range,
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'success', 
        'data': {'hosts_activos': []}, 
        'error_message': None
    }

    if not HAS_SCAPY:
        resultado['status'] = 'error'
        resultado['error_message'] = "La librería 'scapy' no está instalada. Ejecute: pip install scapy"
        return resultado

    try:
        objetivo_resuelto = _resolver_objetivo(target_range)
        red = ipaddress.ip_network(objetivo_resuelto, strict=False)
        hosts_activos = []

        for host in red.hosts():
            paquete = IP(dst=str(host))/TCP(dport=80, flags="S")
            respuesta = sr1(paquete, timeout=1, verbose=0)

            if respuesta and respuesta.haslayer(TCP):
                if respuesta.getlayer(TCP).flags == 0x12: # 0x12 es SYN-ACK
                    print(f"  [+] Host activo (SYN-ACK): {host}")
                    hosts_activos.append(str(host))
                    # Enviamos RST para cerrar la conexión amablemente
                    send(IP(dst=str(host))/TCP(dport=80, flags="R"), verbose=0)

        resultado['data']['hosts_activos'] = hosts_activos

    except Exception as e:
        resultado['status'] = 'error'
        resultado['error_message'] = str(e)

    return resultado

def ping_tcp_ack(target_range: str) -> dict:
    """
    Estudiante 3: Realiza un descubrimiento de hosts que responden con un paquete RST (TCP ACK Scan).
    Es necesario tener permisos de administrador.
    """
    resultado = {
        "modulo": "Discovery",
        "grupo": 3,
        "estudiante": "E3",
        "target": target_range,
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "success",
        "data": {"hosts_activos": []},
        "error_message": None
    }

    if not HAS_SCAPY:
        resultado['status'] = 'error'
        resultado['error_message'] = "La librería 'scapy' no está instalada. Ejecute: pip install scapy"
        return resultado

    try:
        objetivo_resuelto = _resolver_objetivo(target_range)
        red = ipaddress.ip_network(objetivo_resuelto, strict=False)
        for host in red.hosts():
            pkt = IP(dst=str(host))/TCP(dport=80, flags="A")
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x4:  # RST
                print(f"  [+] Host activo (RST recibido): {host}")
                resultado["data"]["hosts_activos"].append(str(host))
    except Exception as e:
        resultado["status"] = "error"
        resultado["error_message"] = str(e)
    return resultado
