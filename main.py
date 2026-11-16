"""Ruta metabólica más corta entre dos metabolitos (algoritmo de Dijkstra).

Uso:
    py -3 main.py                         # consultas de ejemplo
    py -3 main.py "Glucosa" "Colesterol"  # consulta propia
"""

from __future__ import annotations

import argparse
import sys

from grafo import Grafo, NodoNoEncontradoError, ResultadoRuta
from metabolismo import construir_red_metabolica

CONSULTAS_DE_EJEMPLO: tuple[tuple[str, str], ...] = (
    ("Glucosa", "Ácido palmítico"),
    ("Fructosa", "Triglicéridos"),
    ("Glucosa", "Colesterol"),
    ("Alanina", "Glucosa"),
    ("Lactato", "Glucógeno"),
    ("Ácido palmítico", "Glucosa"),
)
SEPARADOR_DE_RUTA = " -> "
CODIGO_DE_ERROR = 1


def formatear_resultado(
    origen: str, destino: str, resultado: ResultadoRuta
) -> str:
    """Devuelve el texto que describe el resultado de una consulta."""
    encabezado = f"Origen: {origen}  |  Destino: {destino}"
    if not resultado.existe:
        return f"{encabezado}\n  No existe una ruta metabólica entre ellos."
    return (
        f"{encabezado}\n"
        f"  Costo total: {resultado.costo:g} reacciones enzimáticas\n"
        f"  Recorrido: {SEPARADOR_DE_RUTA.join(resultado.nodos)}"
    )


def leer_argumentos() -> argparse.Namespace:
    """Lee origen y destino opcionales desde la línea de comandos."""
    analizador = argparse.ArgumentParser(
        description="Ruta metabólica más corta entre dos metabolitos."
    )
    analizador.add_argument("origen", nargs="?", help="metabolito inicial")
    analizador.add_argument("destino", nargs="?", help="metabolito final")
    argumentos = analizador.parse_args()
    if (argumentos.origen is None) != (argumentos.destino is None):
        analizador.error("indica origen y destino, o ninguno de los dos")
    return argumentos


def ejecutar_consultas(red: Grafo, consultas: tuple[tuple[str, str], ...]) -> None:
    """Calcula e imprime la ruta más corta de cada consulta."""
    for origen, destino in consultas:
        resultado = red.ruta_mas_corta(origen, destino)
        print(formatear_resultado(origen, destino, resultado), end="\n\n")


def main() -> int:
    """Punto de entrada del programa; devuelve el código de salida."""
    # La consola de Windows no siempre usa UTF-8 y deformaría los acentos.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    argumentos = leer_argumentos()
    red = construir_red_metabolica()
    if argumentos.origen is None:
        consultas = CONSULTAS_DE_EJEMPLO
    else:
        consultas = ((argumentos.origen, argumentos.destino),)

    print("=== Ruta metabólica más corta (Dijkstra) ===\n")
    try:
        ejecutar_consultas(red, consultas)
    except NodoNoEncontradoError as error:
        print(f"Error: {error}.", file=sys.stderr)
        print(
            f"Metabolitos disponibles: {', '.join(red.nombres_de_nodos)}",
            file=sys.stderr,
        )
        return CODIGO_DE_ERROR
    return 0


if __name__ == "__main__":
    sys.exit(main())
