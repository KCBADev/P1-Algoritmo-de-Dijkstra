"""Red metabólica simplificada de los macronutrientes.

Cada nodo es un metabolito y cada arista una conversión metabólica cuyo peso
es el número de reacciones enzimáticas que requiere. Es un modelo didáctico:
los conteos son aproximados y no distingue tejidos ni compartimentos
celulares.

Simplificaciones importantes:
- El ciclo de Krebs se modela como un destino final (oxidación completa),
  porque el oxalacetato del ciclo se regenera y no hay síntesis neta. Por eso
  el modelo respeta que los ácidos grasos no pueden convertirse en glucosa.
- Cada ciclo de la ácido graso sintasa y de la beta-oxidación cuenta como
  un paso.
"""

from __future__ import annotations

from typing import NamedTuple

from grafo import Grafo


class Conversion(NamedTuple):
    """Conversión de un metabolito en otro."""

    sustrato: str
    producto: str
    pasos: int
    via: str


CONVERSIONES: tuple[Conversion, ...] = (
    # Carbohidratos
    Conversion("Glucosa", "Glucosa-6-fosfato", 1, "hexocinasa"),
    Conversion("Glucosa-6-fosfato", "Glucosa", 1, "glucosa-6-fosfatasa"),
    Conversion("Glucosa-6-fosfato", "Piruvato", 9, "glucólisis"),
    Conversion("Glucosa-6-fosfato", "Glucógeno", 3, "glucogénesis"),
    Conversion("Glucógeno", "Glucosa-6-fosfato", 2, "glucogenólisis"),
    Conversion("Glucosa-6-fosfato", "Ribosa-5-fosfato", 4, "vía de las pentosas"),
    Conversion("Fructosa", "Glucosa-6-fosfato", 2, "hexocinasa e isomerasa"),
    Conversion("Fructosa", "Piruvato", 8, "fructólisis hepática"),
    # Destinos del piruvato
    Conversion("Piruvato", "Lactato", 1, "lactato deshidrogenasa"),
    Conversion("Lactato", "Piruvato", 1, "lactato deshidrogenasa"),
    Conversion("Piruvato", "Alanina", 1, "alanina aminotransferasa"),
    Conversion("Alanina", "Piruvato", 1, "alanina aminotransferasa"),
    Conversion("Piruvato", "Acetil-CoA", 1, "piruvato deshidrogenasa"),
    # Gluconeogénesis
    Conversion("Piruvato", "Oxalacetato", 1, "piruvato carboxilasa"),
    Conversion("Oxalacetato", "Glucosa-6-fosfato", 9, "gluconeogénesis"),
    # Destinos del acetil-CoA
    Conversion("Acetil-CoA", "CO2 + ATP", 8, "ciclo de Krebs"),
    Conversion("Acetil-CoA", "Malonil-CoA", 1, "acetil-CoA carboxilasa"),
    Conversion("Acetil-CoA", "HMG-CoA", 2, "tiolasa y HMG-CoA sintasa"),
    # Lípidos
    Conversion("Malonil-CoA", "Ácido palmítico", 7, "ácido graso sintasa"),
    Conversion("Ácido palmítico", "Acetil-CoA", 8, "beta-oxidación"),
    Conversion("Ácido palmítico", "Triglicéridos", 5, "esterificación"),
    Conversion("Triglicéridos", "Ácido palmítico", 3, "lipólisis"),
    Conversion("HMG-CoA", "Cuerpos cetónicos", 1, "HMG-CoA liasa"),
    Conversion("Cuerpos cetónicos", "Acetil-CoA", 2, "cetólisis"),
    Conversion("HMG-CoA", "Mevalonato", 1, "HMG-CoA reductasa"),
    Conversion("Mevalonato", "Colesterol", 28, "síntesis de colesterol"),
)


def construir_red_metabolica() -> Grafo:
    """Crea el grafo dirigido con todas las conversiones metabólicas."""
    red = Grafo(dirigido=True)
    for conversion in CONVERSIONES:
        red.agregar_arista(
            conversion.sustrato, conversion.producto, conversion.pasos
        )
    return red
