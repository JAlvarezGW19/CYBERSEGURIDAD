# Estándares de Código Python

1.  **Type Hinting Obligatorio:** Todas las firmas de funciones deben incluir tipos para los argumentos y el valor de retorno.
    - Ejemplo: `def get_a_records(domain: str) -> dict:`
2.  **Docstrings Estilo Google:** Toda función pública debe tener un docstring que siga el formato de Google, documentando `Args:` y `Returns:`.
3.  **Manejo de Errores Robusto:** Utiliza bloques `try-except` para capturar excepciones (ej. `socket.error`, `requests.exceptions.RequestException`) y evitar que un módulo fallido detenga la ejecución completa del orquestador. El módulo debe retornar un diccionario de error válido en caso de fallo.
4.  **No `raise NotImplementedError`:** El código entregado no debe contener esta instrucción.
5.  **Limitarse al Módulo Asignado:** Los desarrollos deben realizarse exclusivamente en el archivo `.py` asignado a cada grupo dentro de la carpeta `modulos/`. No se debe modificar `auditoria.py` ni los archivos de otros grupos.