# Suite de Auditoría de Seguridad Informática

Este proyecto es una herramienta modular de auditoría desarrollada de forma colaborativa por los 13 estudiantes del curso de **Seguridad Informática**.

## 🚀 Guía de Trabajo en Paralelo y Colaboración

Para maximizar la eficiencia y evitar cuellos de botella, el proyecto utiliza una arquitectura desacoplada. Esto permite que los 4 grupos trabajen simultáneamente sin depender del progreso de los demás.

### 1. Independencia por Módulos
Cada grupo tiene su propio archivo de desarrollo en la carpeta `modulos/`. 
- **Grupo 1 (DNS):** `modulos/dns_recon.py`
- **Grupo 2 (OSINT):** `modulos/osint.py`
- **Grupo 3 (Discovery):** `modulos/discovery.py`
- **Grupo 4 (Scanning):** `modulos/scanning.py`

**Regla de Oro:** Está estrictamente prohibido modificar `auditoria.py` o los archivos de otros grupos. Tu trabajo se limita exclusivamente a tu archivo asignado.

### 2. El Contrato de Datos (La Clave del Paralelismo)
No necesitas esperar a que los grupos de "Reconocimiento" terminen para que tu código de "Escaneo" funcione. La integración no depende del código de otros, sino del **cumplimiento del contrato de salida**.
- Todas las funciones deben devolver un diccionario que cumpla con el esquema definido en `docs/schema_resultados.json`.
- Mientras respetes este formato, el orquestador principal y el futuro módulo de reportes funcionarán correctamente.

### 3. Pruebas de Unidad
Puedes (y debes) probar tu funcionalidad de forma aislada usando objetivos de prueba conocidos (ej. `google.com` o `8.8.8.8`).
```bash
# Ejemplo: El Grupo 4 puede probar su escáner sin esperar al Grupo 1
python auditoria.py 8.8.8.8 --scan 80,443
```

## 🛠️ Configuración del Entorno

1. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
2. (Opcional pero recomendado) Instala la librería de validación para verificar tus contratos:
   ```bash
   pip install jsonschema
   ```

## 📝 Estándares de Código

Para asegurar la calidad profesional de la suite, cada entrega debe cumplir con:
1. **Type Hinting:** Todas las funciones deben declarar tipos de entrada y salida.
2. **Docstrings:** Uso obligatorio del estilo Google para documentar argumentos y retornos.
3. **Manejo de Errores:** Uso de bloques `try-except` para prevenir caídas del sistema.
4. **Validación:** Antes de realizar un `push`, verifica que tu retorno pase la validación de `auditoria.py`.

## 🔄 Flujo de Trabajo (Git)

Para sincronizar tu trabajo, utiliza el script proporcionado:
```bash
python3 git_update.py "Descripción breve de tu cambio"
```
Esto realizará el commit de tus cambios, descargará las actualizaciones de tus compañeros y subirá tu trabajo al repositorio de forma segura.

---
*Propiedad del Curso de Seguridad Informática - Prof. César Rodríguez*