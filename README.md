# 🛒 Food Store — Parcial 1 de Programación IV

> Modelo orientado a objetos para un catálogo de productos de una tienda de alimentos.

**UTN · Programación IV · Parcial 1**

---

## 📋 Descripción

Este proyecto implementa un catálogo de productos utilizando **Python 3.12+** y exclusivamente la biblioteca estándar.

El modelo aplica conceptos de Programación Orientada a Objetos como:

- Herencia y abstracción
- Polimorfismo
- Encapsulamiento
- Composición
- Agregación
- Asociación
- Protocolos estructurales
- Dataclasses inmutables
- Type hints
- Validación de datos
- Manejo de stock y disponibilidad

El sistema funciona completamente en memoria y no utiliza bases de datos ni dependencias externas.

---

## 🗂️ Estructura del proyecto

| Archivo | Descripción |
|:---|:---|
| `catalogo.py` | Modelo principal del catálogo |
| `libreria_externa.py` | Simulación de una librería de terceros |
| `main.py` | Demo ejecutable del parcial |
| `prueba_catalogo.py` | Pruebas auxiliares |
| `uml/modelo_final.md` | Diagrama UML final en Mermaid |
| `README.md` | Documentación del proyecto |

---

## 🧱 Modelo de clases

`Producto` es una clase abstracta que concentra el comportamiento común de los productos y define el método abstracto `precio_final()`.

Sus especializaciones son:

| Clase | Descripción |
|:---|:---|
| `ProductoSimple` | Productos vendidos por unidades enteras |
| `ProductoPorPeso` | Productos vendidos por cantidades que pueden ser decimales |
| `ProductoCombo` | Producto compuesto por otros productos |

La estructura de herencia es:

```text
                         Producto
                            ▲
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      ProductoSimple  ProductoPorPeso  ProductoCombo

📦 Productos
ProductoSimple trabaja con cantidades enteras, ProductoPorPeso permite cantidades decimales y ProductoCombo utiliza productos existentes como componentes.

🗃️ Categorías
Los productos pueden pertenecer a varias categorías, manteniendo una única categoría principal.

La clasificación se realiza mediante clasificar_en() y se consulta mediante categorias().

🧩 Relaciones
Composición
Producto crea y administra internamente sus objetos ProductoCategoria.

self._clasificaciones: list[ProductoCategoria] = []

Agregación
ProductoCombo recibe productos ya existentes como componentes.

self._componentes = list(componentes)

Los componentes pueden existir independientemente del combo.

Asociación
Producto puede utilizar una UnidadMedida existente:

unidad_venta: UnidadMedida | None

📏 UnidadMedida
Se implementa como una dataclass inmutable mediante frozen=True.

La demo verifica esta propiedad intentando modificar su símbolo.

⭐ Productos destacados
No se utiliza una subclase ProductoDestacado.

La funcionalidad se incorpora directamente en Producto mediante _orden_vidriera, destacar() y quitar_destacado().

📊 Stock y precios
Cada producto administra su stock y disponibilidad.

Los tres tipos implementan su propia versión de precio_final().

En ProductoCombo, el precio se calcula a partir de sus componentes y el descuento aplicado.

📤 Exportación con Protocol
El proyecto define el contrato:

class Exportable(Protocol):
    def exportar(self) -> str:
        ...

Producto y FichaPuntoDeVenta cumplen el contrato de forma estructural.

La función exportar_catalogo() permite exportar ambos tipos de objetos sin modificar la librería externa.

🔌 Librería externa
libreria_externa.py simula una clase desarrollada por un tercero.

FichaPuntoDeVenta no hereda de Exportable, pero posee el método exportar(), por lo que cumple estructuralmente con el Protocol.

🧠 Abstracción y polimorfismo
Producto hereda de ABC y declara precio_final() como método abstracto.

Cada subclase implementa su propia regla de cálculo.

La demo también verifica que no se pueda instanciar Producto ni una subclase que no implemente precio_final().

▶️ Ejecución
Para ejecutar la demo:

python main.py

La ejecución muestra las principales funcionalidades del modelo y finaliza con:

=== FIN DE LA DEMO ===

📐 Diagrama UML
El diagrama final se encuentra en:

uml/modelo_final.md

Representa la estructura de clases, herencia, relaciones, multiplicidades y contratos del modelo.

🛠️ Tecnologías
Tecnología	Uso
Python 3.12+	Lenguaje
abc	Clase abstracta
dataclasses	UnidadMedida inmutable
typing.Protocol	Contrato Exportable
Mermaid	Diagrama UML
Git / GitHub	Control de versiones

👨‍💻 Autor
Pablo de la Puente

UTN · Programación IV · Parcial 1

