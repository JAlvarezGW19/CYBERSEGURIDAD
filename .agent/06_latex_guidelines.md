# Guías y Soluciones para LaTeX

- **Contexto:** El proyecto utiliza LaTeX extensivamente para la documentación (`.tex`).
- **Errores Comunes:** Se ha creado un registro de errores y soluciones en `.agent/latex.md`. Consúltalo antes de proponer soluciones a problemas de compilación de LaTeX.
- **Puntos Clave a Recordar:**
    - Conflicto `babel` (español) con `tikz`: Usar `\usetikzlibrary{babel}`.
    - Caracteres especiales: Escapar `_`, `%`, `&`, etc., con `\` o usar `\texttt{}`.
    - Bloques de código: Usar el entorno `listings`.
    - Unidades técnicas: Usar el paquete `siunitx` y el comando `\qty{}{}`.
    - Comillas y `babel`: Usar `\usepackage[T1]{fontenc}` y `\usepackage[spanish,es-noquoting]{babel}` para evitar conflictos con `\texttt{""}`.