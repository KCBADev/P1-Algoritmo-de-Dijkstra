"""Pruebas del grafo, del algoritmo de Dijkstra y de la red metabólica."""

import math
import unittest

from grafo import Grafo, NodoNoEncontradoError, PesoNegativoError
from metabolismo import construir_red_metabolica


class RutaMasCortaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.grafo = Grafo()
        self.grafo.agregar_arista("A", "B", 1)
        self.grafo.agregar_arista("B", "C", 2)
        self.grafo.agregar_arista("A", "C", 10)
        self.grafo.agregar_nodo("Aislado")

    def test_prefiere_ruta_indirecta_mas_barata(self) -> None:
        resultado = self.grafo.ruta_mas_corta("A", "C")
        self.assertEqual(resultado.costo, 3)
        self.assertEqual(resultado.nodos, ("A", "B", "C"))

    def test_origen_igual_a_destino(self) -> None:
        resultado = self.grafo.ruta_mas_corta("A", "A")
        self.assertEqual(resultado.costo, 0)
        self.assertEqual(resultado.nodos, ("A",))

    def test_sin_ruta(self) -> None:
        resultado = self.grafo.ruta_mas_corta("A", "Aislado")
        self.assertFalse(resultado.existe)
        self.assertEqual(resultado.costo, math.inf)
        self.assertEqual(resultado.nodos, ())

    def test_nodo_inexistente(self) -> None:
        with self.assertRaises(NodoNoEncontradoError):
            self.grafo.ruta_mas_corta("A", "Z")

    def test_peso_negativo(self) -> None:
        with self.assertRaises(PesoNegativoError):
            self.grafo.agregar_arista("A", "D", -1)

    def test_grafo_no_dirigido_se_recorre_en_ambos_sentidos(self) -> None:
        self.assertEqual(self.grafo.ruta_mas_corta("C", "A").costo, 3)

    def test_grafo_dirigido_respeta_el_sentido(self) -> None:
        dirigido = Grafo(dirigido=True)
        dirigido.agregar_arista("A", "B", 1)
        self.assertTrue(dirigido.ruta_mas_corta("A", "B").existe)
        self.assertFalse(dirigido.ruta_mas_corta("B", "A").existe)


class RedMetabolicaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.red = construir_red_metabolica()

    def test_lipogenesis_desde_glucosa(self) -> None:
        resultado = self.red.ruta_mas_corta("Glucosa", "Ácido palmítico")
        self.assertEqual(resultado.costo, 19)
        self.assertEqual(
            resultado.nodos,
            (
                "Glucosa",
                "Glucosa-6-fosfato",
                "Piruvato",
                "Acetil-CoA",
                "Malonil-CoA",
                "Ácido palmítico",
            ),
        )

    def test_fructosa_usa_la_fructolisis_directa(self) -> None:
        resultado = self.red.ruta_mas_corta("Fructosa", "Piruvato")
        self.assertEqual(resultado.costo, 8)
        self.assertEqual(resultado.nodos, ("Fructosa", "Piruvato"))

    def test_gluconeogenesis_desde_alanina(self) -> None:
        self.assertEqual(self.red.ruta_mas_corta("Alanina", "Glucosa").costo, 12)

    def test_acidos_grasos_no_se_convierten_en_glucosa(self) -> None:
        resultado = self.red.ruta_mas_corta("Ácido palmítico", "Glucosa")
        self.assertFalse(resultado.existe)


if __name__ == "__main__":
    unittest.main()
