# Módulo desarrollado por el Grupo 2
# Fase II: Enumeración NetBIOS/SMB

import datetime
import logging
from typing import Any, Dict, List, Optional

try:
    from smb.SMBConnection import SMBConnection
    HAS_PYSMB = True
except ImportError:
    HAS_PYSMB = False


class SMBEnumerator:
    """
    Clase para realizar enumeración básica SMB/NetBIOS.

    Esta clase intenta establecer una sesión nula contra un objetivo autorizado
    y, si la conexión es exitosa, enumera los recursos compartidos disponibles.
    """

    def __init__(self, ip_address: str, port: int = 445) -> None:
        """
        Inicializa el enumerador SMB.

        Args:
            ip_address (str): Dirección IP o dominio del objetivo autorizado.
            port (int): Puerto SMB. Normalmente 445 o 139.
        """
        self.ip_address = ip_address
        self.port = port
        self.shares: List[Dict[str, Any]] = []
        self.users: List[str] = []
        self.connection: Optional[SMBConnection] = None
        self.null_session_established = False
        self.error_message: Optional[str] = None

    def establish_null_session(self) -> bool:
        """
        Intenta establecer una sesión nula SMB.

        Returns:
            bool: True si la conexión anónima fue exitosa, False en caso contrario.
        """
        if not HAS_PYSMB:
            self.error_message = "La librería pysmb no está instalada. Ejecute: pip install pysmb"
            print(f"[!] {self.error_message}")
            return False

        try:
            print(f"[*] Intentando sesión nula SMB en {self.ip_address}:{self.port}")

            self.connection = SMBConnection(
                "",
                "",
                "python_client",
                self.ip_address,
                use_ntlm_v2=True,
                is_direct_tcp=(self.port == 445)
            )

            self.null_session_established = self.connection.connect(
                self.ip_address,
                self.port,
                timeout=5
            )

            return self.null_session_established

        except Exception as e:
            self.error_message = f"No se pudo establecer sesión nula: {str(e)}"
            logging.debug(f"Error en sesión nula hacia {self.ip_address}: {e}")
            return False

    def enumerate_shares(self) -> List[Dict[str, Any]]:
        """
        Enumera los recursos compartidos SMB disponibles.

        Returns:
            List[Dict[str, Any]]: Lista de recursos compartidos encontrados.
        """
        if not self.connection:
            return self.shares

        try:
            print("[*] Enumerando recursos compartidos SMB...")

            shares = self.connection.listShares(timeout=5)

            for share in shares:
                self.shares.append({
                    "name": share.name,
                    "comments": share.comments,
                    "type": str(share.type)
                })

        except Exception as e:
            self.error_message = f"No se pudieron enumerar recursos compartidos: {str(e)}"
            logging.debug(f"Error enumerando shares en {self.ip_address}: {e}")

        return self.shares

    def close_connection(self) -> None:
        """
        Cierra la conexión SMB si está activa.
        """
        try:
            if self.connection:
                self.connection.close()
        except Exception:
            pass

    def run(self) -> Dict[str, Any]:
        """
        Ejecuta la enumeración SMB completa.

        Returns:
            Dict[str, Any]: Resultado siguiendo el contrato de datos del proyecto.
        """
        print(f"[*] Iniciando enumeración SMB en {self.ip_address}:{self.port}")

        try:
            if self.establish_null_session():
                print("[+] Sesión nula establecida con éxito.")
                self.enumerate_shares()
            else:
                print("[!] No se logró establecer sesión nula.")

        finally:
            self.close_connection()

        return {
            "modulo": "Enumeracion SMB",
            "grupo": 2,
            "estudiante": "E1",
            "target": self.ip_address,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "data": {
                "port": self.port,
                "null_session_established": self.null_session_established,
                "shares": self.shares,
                "users": self.users
            },
            "error_message": self.error_message
        }


if __name__ == "__main__":
    import json
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"

    enum = SMBEnumerator(target)
    resultados = enum.run()

    print(json.dumps(resultados, indent=4, ensure_ascii=False))