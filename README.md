# Ruta metabólica más corta con Dijkstra

Implementación en Python del algoritmo de Dijkstra sobre un grafo ponderado, aplicada a Nutrición: encuentra la vía con menos reacciones enzimáticas para convertir un metabolito en otro.

## El modelo

- **Nodos**: metabolitos (Glucosa, Piruvato, Acetil-CoA, Ácido palmítico, Colesterol...).
- **Aristas**: conversiones metabólicas (glucólisis, gluconeogénesis, beta-oxidación...).
- **Peso**: número de reacciones enzimáticas de la conversión.
- **Grafo dirigido**: las reacciones irreversibles solo se recorren en un sentido. Por eso, por ejemplo, no hay ruta de ácidos grasos a glucosa.

Es un modelo didáctico: los conteos de reacciones son aproximados y no se distinguen tejidos ni compartimentos celulares.

## Estructura

| Archivo | Contenido |
|---|---|
| `grafo.py` | Clases `Nodo` y `Grafo`, y el algoritmo de Dijkstra (`Grafo.ruta_mas_corta`) |
| `metabolismo.py` | Datos de la red metabólica |
| `main.py` | Programa principal |
| `test_grafo.py` | Pruebas automatizadas |

## Uso

Requiere Python 3.9 o superior, sin dependencias externas.

```
py -3 main.py                         # consultas de ejemplo
py -3 main.py "Glucosa" "Colesterol"  # consulta propia
py -3 -m unittest -v                  # pruebas
```

## Ejemplo de salida

```
Origen: Glucosa  |  Destino: Ácido palmítico
  Costo total: 19 reacciones enzimáticas
  Recorrido: Glucosa -> Glucosa-6-fosfato -> Piruvato -> Acetil-CoA -> Malonil-CoA -> Ácido palmítico

Origen: Ácido palmítico  |  Destino: Glucosa
  No existe una ruta metabólica entre ellos.
```
