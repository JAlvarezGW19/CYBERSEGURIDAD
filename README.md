# Suite de Auditoría de Seguridad Informática

Este proyecto es una herramienta modular de auditoría desarrollada de forma colaborativa por los 13 estudiantes del curso de **Seguridad Informática**.

## 🚀 Guía de Trabajo en Paralelo y Colaboración

Para maximizar la eficiencia y evitar cuellos de botella, el proyecto utiliza una arquitectura desacoplada. Esto permite que los 4 grupos trabajen simultáneamente sin depender del progreso de los demás.

### 1. Independencia por Módulos
Cada grupo tiene su propio archivo de desarrollo en la carpeta `modulos/`.

**Fase I: Recopilación y Escaneo (Semanas 1-4)**
- **Grupo 1 (DNS):** `modulos/Fase_I/dns_recon.py`
- **Grupo 2 (OSINT):** `modulos/Fase_I/osint.py`
- **Grupo 3 (Discovery):** `modulos/Fase_I/discovery.py`
- **Grupo 4 (Scanning):** `modulos/Fase_I/scanning.py`

**Fase II: Enumeración y Ataques (Semanas 5-7)**
- **Grupo 1 (Banner Grabbing):** `modulos/Fase_II/banner_grabber.py`
- **Grupo 2 (NetBIOS/SMB):** `modulos/Fase_II/smb_enumerator.py`
- **Grupo 3 (Fuerza Bruta FTP):** `modulos/Fase_II/bruteforce_ftp.py`
- **Grupo 4 (Fuerza Bruta Web):** `modulos/Fase_II/bruteforce_web.py`

**Fase III: Aplicaciones Web y Reportes (Semanas 8-10)**
- **Grupo 1 (Web Crawler):** `modulos/web_crawler.py`
- **Grupo 2 (Reportes e Integración):** Expansión de `auditoria.py` (Orquestador) y generación de reportes.
- **Grupo 3 (Escáner SQLi):** `modulos/vuln_sqli.py`
- **Grupo 4 (Escáner XSS/LFI):** `modulos/vuln_xss_lfi.py`

**Regla de Oro:** Está estrictamente prohibido modificar los archivos de otros grupos. La alteración de `auditoria.py` y cualquier modificación a la carpeta oculta `.agent/` está reservada de manera exclusiva al **Prof. César Rodríguez**. Cualquier *Pull Request* que altere estos archivos será rechazado.

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

## 🧠 Base de Conocimiento y Sistema RAG

Esta suite cuenta con un "segundo cerebro" o sistema RAG (*Retrieval-Augmented Generation*) impulsado por ChromaDB. Está diseñado para almacenar y recuperar colaborativamente soluciones a errores comunes encontrados durante el desarrollo (LaTeX, Python, configuración, fallos en los módulos, etc.).

- **Para consultar un error rápidamente:** Ejecuta `python knowledge_db.py -c <tema> -q "tu error en lenguaje natural"` (por ejemplo: `-c auditoria`).
- **Documentación completa:** Para aprender a alimentar esta base de datos manualmente o mediante el flujo de autodiagnóstico del orquestador, consulta la guía oficial en `docs/guia_rag.pdf` (compilada desde `docs/guia_rag.tex`).

## 🔄 Flujo de Trabajo (Git)

Para sincronizar tu trabajo, utiliza el script proporcionado:
```bash
python3 git_update.py "Descripción breve de tu cambio"
```
Esto realizará el commit de tus cambios, descargará las actualizaciones de tus compañeros y subirá tu trabajo al repositorio de forma segura.

---
*Propiedad del Curso de Seguridad Informática - Prof. César Rodríguez*