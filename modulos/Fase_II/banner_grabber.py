# Módulo a desarrollar por el Grupo 1 (Fase II: Captura de Anuncios)
import socket
import ssl
import re
import logging
import datetime
from typing import List, Dict, Any, Optional

class BannerGrabber:
    def __init__(self, ip_address: str, ports: Optional[List[int]] = None, timeout: int = 3) -> None:
        self.ip_address = ip_address
        self.ports = ports if ports else [21, 22, 80, 443]
        self.timeout = timeout
        # Expresión regular para limpiar caracteres no imprimibles (útil para limpiar el banner)
        self.clean_regex = re.compile(r'[^a-zA-Z0-9\s\.\-\/\:]')

    def grab_port(self, port: int) -> Dict[str, Any]:
        """
        Intenta conectarse a un puerto TCP y obtener el anuncio de servicio (banner).
        Retorna un diccionario estandarizado para facilitar la generación de reportes.
        """
        banner_data = {
            'port': port,
            'status': 'closed',
            'banner': None
        }
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.ip_address, port))
                
                if result == 0:
                    banner_data['status'] = 'open'
                    
                    if port == 443:
                        # El puerto 443 requiere una envoltura SSL antes de enviar la petición HTTP
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        with context.wrap_socket(s, server_hostname=self.ip_address) as ss:
                            ss.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                            raw_banner = ss.recv(1024)
                    elif port == 80:
                        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                        raw_banner = s.recv(1024)
                    else:
                        raw_banner = s.recv(1024)
                        
                    # Leer respuesta y decodificar
                    if raw_banner:
                        decoded = raw_banner.decode('utf-8', errors='ignore').strip()
                        banner_data['banner'] = self.clean_regex.sub('', decoded)
                        
        except Exception as e:
            logging.debug(f"Error escaneando {self.ip_address}:{port} - {e}")
            
        return banner_data

    def run(self) -> Dict[str, Any]:
        """
        Orquesta la captura de banners en los puertos especificados y
        empaqueta los resultados usando el esquema oficial del proyecto.
        """
        print(f"[*] Iniciando Banner Grabbing en {self.ip_address}...")
        resultados_banners = []
        
        for p in self.ports:
            resultados_banners.append(self.grab_port(p))
            
        # REGLA DE ORO: Cumplir con schema_resultados.json
        return {
            "modulo": "Banner Grabbing",
            "grupo": 1,
            "estudiante": "E1", # Los estudiantes deben colocar su identificador (ej. E1)
            "target": self.ip_address,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "data": {
                "banners": resultados_banners
            },
            "error_message": None
        }

if __name__ == "__main__":
    # Área de pruebas independiente para el Grupo 1
    import json
    target = "127.0.0.1"
    grabber = BannerGrabber(target, ports=[21, 22, 80, 443])
    resultados = grabber.run()
    print(json.dumps(resultados, indent=4))