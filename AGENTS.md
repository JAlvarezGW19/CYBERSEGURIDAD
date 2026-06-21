# CYBERSEGURIDAD - Suite de Auditoría de Seguridad Informática

## Visión General

Suite modular de auditoría de seguridad ofensiva en Python. El proyecto permite ejecutar módulos independientes de reconocimiento, enumeración, escaneo y explotación sobre un objetivo, coordinados por un orquestador central (`auditoria.py`).

## Estructura del Proyecto

```
/
├── auditoria.py                 # Orquestador principal (CLI entry point)
├── knowledge_db.py              # Sistema RAG con ChromaDB
├── exportar_errores_json.py     # Exporta errores al RAG
├── clean_latex.py               # Limpieza de auxiliares LaTeX
├── git_update.py                # Wrapper Python para git
├── requirements.txt             # Dependencias Python
├── passwords.txt                # Diccionario de contraseñas
├── users.txt                    # Diccionario de usuarios
├── modulos/
│   ├── Fase_I/                  # Reconocimiento y escaneo
│   │   ├── dns_recon.py         # G1: Consultas DNS
│   │   ├── osint.py             # G2: OSINT / WHOIS / Google Dorking
│   │   ├── discovery.py         # G3: Descubrimiento (ping sweep, TCP)
│   │   └── scanning.py          # G4: Escaneo de puertos (nmap)
│   ├── Fase_II/                 # Enumeración y ataques
│   │   ├── banner_grabber.py    # G1: Captura de banners
│   │   ├── smb_enumerator.py    # G2: Enumeración SMB
│   │   ├── bruteforce_ftp.py    # G3: Fuerza bruta FTP
│   │   └── bruteforce_web.py    # G4: Fuerza bruta HTTP
│   └── Fase_III/                # Aplicaciones web y reportes
│       ├── web_crawler.py       # G1: Crawling web
│       ├── generador_reportes.py# G2: Generación de reportes
│       ├── vuln_sqli.py         # G3: Escáner SQLi
│       └── vuln_xss_lfi.py      # G4: Escáner XSS / LFI
├── docs/                        # Documentación LaTeX
├── .agent/                      # Archivos markdown con instrucciones para el agente AI (solo profesor)
├── chroma_db/                   # Base vectorial ChromaDB (gitignored)
└── historial_auditoria.json     # Resultados de ejecuciones
```

## Stack Tecnológico

- **Lenguaje:** Python 3.11
- **Librerías principales:** dnspython, scapy, python-nmap, requests, pysmb, impacket, beautifulsoup4, chromadb
- **Documentación:** LaTeX
- **CI/CD:** GitHub Actions
- **Vector DB:** ChromaDB + LangChain + Groq (Llama 3)

## Convenciones de Código

1. **Type hints** obligatorios en todas las funciones
2. **Docstrings estilo Google** con `Args:` y `Returns:`
3. **Manejo de errores** con `try-except`; nunca propagar excepciones
4. **Contrato de datos:** toda función retorna un `dict` con:
   - `modulo`, `grupo`, `estudiante`, `target`, `timestamp` (ISO 8601)
   - `status`: `"success"` o `"error"`
   - `data`: `dict` con resultados
   - `error_message`: `str | None`
5. **Imports condicionales** para dependencias opcionales
6. **Cada módulo tiene `if __name__ == "__main__":`** para pruebas aisladas
7. **Prohibido modificar** `auditoria.py`, `.agent/` o archivos de otros grupos

## Grupos de Trabajo

| Grupo | Fase I | Fase II | Fase III |
|-------|--------|---------|----------|
| G1 | dns_recon.py | banner_grabber.py | web_crawler.py |
| G2 | osint.py | smb_enumerator.py | generador_reportes.py |
| G3 | discovery.py | bruteforce_ftp.py | vuln_sqli.py |
| G4 | scanning.py | bruteforce_web.py | vuln_xss_lfi.py |

## Orquestador

`auditoria.py` provee una CLI con flags como `--dns-all`, `--whois`, `--scan`, `--banner`, `--report`. Ejecuta los módulos por fase, valida resultados contra `docs/schema_resultados.json` y persiste en `historial_auditoria.json`.

## Sistema RAG

`knowledge_db.py` permite consultar soluciones a errores conocidos usando ChromaDB. Los errores se exportan desde `historial_auditoria.json` mediante `exportar_errores_json.py`.

## Comandos Útiles

```bash
# Ejecutar auditoría completa
python auditoria.py target.com --dns-all --scan 80,443 --whois --banner --report

# Consultar knowledge base
python knowledge_db.py -c "scapy" -q "error de permisos"

# Sincronizar con git
python3 git_update.py "mensaje del commit"

# Limpiar auxiliares LaTeX
python clean_latex.py
```

## Notas

- `auditoria.py` y `.agent/` son responsabilidad exclusiva del profesor (`cero97-ctrl`)
- Validar con el schema antes de hacer push
- No hay framework de tests formal; cada módulo se prueba con su bloque `if __name__ == "__main__":`
- La documentación del proyecto se debe realizar en formato LaTeX
