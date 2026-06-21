# Contrato de Datos de Salida

**REGLA CRÍTICA:** Toda función desarrollada en los módulos de `modulos/` **DEBE** retornar un diccionario de Python.

- **Estructura:** Este diccionario debe ser serializable a JSON y cumplir con el esquema definido en `docs/schema_resultados.json`.
- **Propósito:** Este contrato es la clave para el desarrollo en paralelo y la integración desacoplada. Permite que el orquestador (`auditoria.py`) y los módulos de reporte procesen los resultados de manera uniforme.
- **En caso de error:** Si una función no puede completar su tarea, debe retornar un diccionario que también cumpla el esquema, pero indicando el estado de error y un mensaje descriptivo.