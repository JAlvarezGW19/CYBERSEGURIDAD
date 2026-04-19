#!/usr/bin/env python3
import subprocess
import os
import sys

def run(cmd, check=True):
    """Ejecuta un comando de sistema."""
    return subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)

def main():
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if not os.path.exists("./update_repo.sh"):
        print(f"Error: update_repo.sh no encontrado en {script_dir}")
        sys.exit(1)

    # Detectar rama actual
    try:
        branch = run("git symbolic-ref --short HEAD").stdout.strip()
    except subprocess.CalledProcessError:
        branch = "main"

    print(f"[*] Iniciando actualización en rama: {branch}")

    # Guardar cambios locales (WIP)
    run("git add -A")
    staged = run("git diff --staged --quiet", check=False)
    
    if staged.returncode != 0:
        msg = sys.argv[1] if len(sys.argv) > 1 else "WIP: guardar cambios antes de pull"
        print(f"[*] Committing: {msg}")
        run(f'git commit -m "{msg}"')
    else:
        print("[*] No hay cambios locales para guardar.")

    # Ejecutar el script de sincronización
    subprocess.run(["bash", "./update_repo.sh", "--remote", "origin", "--branch", branch, "--push"])

if __name__ == "__main__":
    main()