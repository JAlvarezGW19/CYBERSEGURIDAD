# Base de Conocimientos: Errores Comunes en LaTeX

Este documento contiene los errores frecuentes al compilar documentos LaTeX en el proyecto y sus respectivas soluciones.

## Conflicto entre babel (español) y tikz
**El Problema:** Al usar el paquete `babel` en español junto con `tikz`, las flechas, diagramas u otros elementos gráficos no se renderizan correctamente o la compilación falla con errores extraños.
**La Solución:** Para evitar conflictos con los caracteres activos del español, debes cargar la librería de babel específica para tikz añadiendo `\usetikzlibrary{babel}` en el preámbulo de tu documento LaTeX.

## Error Missing $ inserted o caracteres especiales no reconocidos
**El Problema:** Al escribir texto que contiene guiones bajos (`_`), porcentajes (`%`), ampersands (`&`), entre otros, LaTeX arroja errores de compilación asumiendo que se entró en modo matemático o hay comandos mal formados.
**La Solución:** Debes escapar estos caracteres especiales usando una barra invertida (ej. `\_`, `\%`, `\&`) o envolver el texto en un entorno de fuente monoespaciada usando `\texttt{tu_texto_aqui}`.

## Problemas al renderizar bloques de código
**El Problema:** El código fuente incluido en el documento no respeta los saltos de línea, no tiene sintaxis coloreada o el texto se sale de los márgenes de la página.
**La Solución:** Utiliza el entorno proporcionado por el paquete `listings`. Asegúrate de incluir `\usepackage{listings}` en el preámbulo y configurar el bloque de código adecuadamente con `\begin{lstlisting}[language=Python] ... \end{lstlisting}`.

## Formateo incorrecto de unidades técnicas
**El Problema:** Las unidades de medida (como bytes, ms, Mbps, etc.) no tienen la separación estándar respecto al número o cambian de tipografía incorrectamente a lo largo del documento.
**La Solución:** Utiliza el paquete `siunitx` para estandarizar esto. Importa el paquete en el preámbulo y utiliza el comando `\qty{}{}` para las medidas. Por ejemplo: `\qty{100}{MB}`.

## Conflicto de comillas dobles con babel en español
**El Problema:** Al usar comillas dobles (`""`) dentro de un bloque `\texttt{""}` o texto normal, el paquete `babel` en español las interpreta como caracteres de taquigrafía (shorthands) y genera caracteres extraños, dobles comillas angulares o errores de compilación.
**La Solución:** Asegúrate de incluir la codificación correcta de fuentes y de deshabilitar las comillas activas de babel en el preámbulo con las siguientes líneas:
```latex
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noquoting]{babel}
```