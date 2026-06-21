# Resumen del Proyecto: Suite de Auditoría de Seguridad

- **Objetivo:** Construir una suite modular de auditoría de seguridad en Python.
- **Estructura:** El proyecto está dividido en módulos funcionales (`dns_recon`, `osint`, `discovery`, `scanning`) desarrollados en paralelo por 4 grupos de 13 estudiantes en total.
- **Orquestador:** Un script principal (`auditoria.py`) integra y ejecuta los módulos.
- **Base de Conocimiento:** El proyecto utiliza un sistema RAG (Retrieval-Augmented Generation) con ChromaDB para almacenar y consultar soluciones a problemas técnicos. La interacción se realiza a través de `knowledge_db.py`.
- **Colaboración:** El flujo de trabajo se basa en Git, con forks y Pull Requests, como se detalla en `docs/guia_pull_requests.tex`.