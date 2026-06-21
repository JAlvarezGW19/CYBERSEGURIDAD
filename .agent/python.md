# Base de Conocimientos: Python y Librerías

Este documento contiene problemas frecuentes al ejecutar scripts de Python o al utilizar librerías de terceros.

**Nota de Entorno:** Todas las configuraciones, comandos y soluciones documentadas en esta base de conocimientos asumen que el sistema operativo utilizado para el desarrollo y las pruebas es **GNU/Linux**.

## Error de permisos (Operation not permitted) al usar Scapy en Linux
**El Problema:** Al ejecutar módulos que usan la librería `scapy` (como la inyección TCP SYN/ACK del Grupo 3), el script falla en Linux arrojando un error como `PermissionError: [Errno 1] Operation not permitted` o quejándose sobre sockets de bajo nivel.
**La Solución:** Scapy requiere forjar paquetes de red a bajo nivel (Raw Sockets). En sistemas operativos Linux/macOS, esta acción requiere permisos de superusuario. Para que estos escaneos funcionen, debes ejecutar el orquestador principal con privilegios elevados anteponiendo la palabra `sudo`. Ejemplo de uso correcto: `sudo python auditoria.py objetivo.com --tcp-syn`.

## Error de importación (Cannot find module 'scapy.all') y de resolución del intérprete en VS Code

**El Problema:** El editor de VS Code (linter Pylance/Pyright) muestra un aviso de importación fallida como `Cannot find module 'scapy.all'` o un error al resolver la ruta por defecto del intérprete (`Default interpreter path ... could not be resolved`), a pesar de tener la librería correctamente instalada en el entorno Conda (`cyber_env`).

**La Solución:** Este comportamiento en sistemas Linux suele deberse a dos causas:

1. **Aislamiento por Sandbox (Flatpak / Snap):** Si VS Code fue instalado por medio de Flatpak o Snap, se ejecuta de manera aislada y no tiene acceso a las rutas locales del sistema fuera de tu carpeta personal básica, bloqueando la lectura de `/home/cero/anaconda3`.
   * **Si es Flatpak:** Concede permisos de acceso al directorio de Anaconda ejecutando en tu terminal de Linux:
     ```bash
     flatpak override com.visualstudio.code --filesystem=/home/cero/anaconda3
     ```
   * **Si es Snap:** Reinstala VS Code con la confinación clásica para otorgar acceso al sistema de archivos:
     ```bash
     sudo snap install code --classic
     ```
2. **Conflicto de Enlaces Simbólicos:** A veces VS Code no resuelve correctamente los enlaces simbólicos genéricos como `bin/python` que apuntan a versiones específicas de Python.
   * **Solución:** Modifica el archivo `.vscode/settings.json` del espacio de trabajo para apuntar directamente al ejecutable binario de Python en lugar del enlace simbólico. Ejemplo:
     ```json
     {
         "python.defaultInterpreterPath": "/home/cero/anaconda3/envs/cyber_env/bin/python3.11"
     }
     ```
3. **Recarga de VS Code:** Para forzar a VS Code a revaluar el intérprete y los imports, abre la paleta de comandos (`Ctrl + Shift + P`) y ejecuta **`Developer: Reload Window`** (o **`Python: Restart Language Server`**).
4. **Falsos Positivos del Linter (Pylance / Pyright):** Dado que Scapy construye muchos de sus módulos dinámicamente en tiempo de ejecución, el análisis estático a veces falla en reconocerlos, arrojando el falso error `Cannot find module 'scapy.all'`, aunque el script funcione perfectamente en la terminal.
   * **Solución:** Puedes silenciar visualmente este falso positivo indicándole al linter que ignore la línea agregando el comentario `# type: ignore`:
     ```python
     from scapy.all import IP, TCP, sr1, send  # type: ignore
     ```