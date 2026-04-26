# Evidencia de validación - Grupo 2 Estudiante 1

## Integrante
Daniel - Estudiante 1

## Módulo
OSINT y Huella Digital

## Archivo revisado
modulos/osint.py

## Función validada
get_whois_data(domain)

## Prueba ejecutada

python auditoria.py google.com --whois

## Resultado obtenido

[OK] Validacion de esquema exitosa para: OSINT (Estudiante: E1)

## Descripción
Se validó la función WHOIS del Grupo 2, Estudiante 1. La función consulta información administrativa del dominio usando python-whois y retorna un diccionario compatible con docs/schema_resultados.json.
