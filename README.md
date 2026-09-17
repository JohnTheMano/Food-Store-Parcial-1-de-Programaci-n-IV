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
ProductoSimple
Representa productos vendidos por unidades enteras.

Ejemplo utilizado en la demo:

coca = ProductoSimple(
    nombre="Coca-Cola",
    precio_base=1000,
    stock_cantidad=10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

El precio final se obtiene multiplicando el precio base por la cantidad.

ProductoPorPeso
Permite trabajar con cantidades decimales.

Ejemplo:

jamon = ProductoPorPeso(
    nombre="Jamón",
    precio_base=8000,
    stock_cantidad=5,
    categoria_principal=fiambres,
    unidad_venta=kilogramo,
)

En la demo:

0.250 kg → $ 2000.00

ProductoCombo
Representa un producto compuesto por otros productos existentes.

combo = ProductoCombo(
    nombre="Combo Merienda",
    componentes=[coca, pan],
    descuento=0.10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

El precio base se obtiene a partir de los precios de sus componentes y luego se aplica el descuento correspondiente.

🗃️ Categorías
La clase Categoria representa las categorías del catálogo.

En la demo se utilizan:

Bebidas

Gaseosas

Fiambrería

Almacén

Un producto puede pertenecer a varias categorías, manteniendo una única categoría principal.

La clasificación se realiza mediante:

producto.clasificar_en(...)

y los vínculos pueden consultarse mediante:

producto.categorias()

🧩 Composición
Producto mantiene internamente sus objetos ProductoCategoria:

self._clasificaciones: list[ProductoCategoria] = []

Los vínculos son creados por el propio producto mediante clasificar_en().

Por este motivo, la relación se modela como composición:

Producto "1" *-- "1..*" ProductoCategoria

🔄 Agregación
ProductoCombo mantiene productos existentes como componentes:

self._componentes = list(componentes)

Los componentes pueden existir independientemente del combo y pueden reutilizarse en otros combos.

Por ejemplo:

combo = ProductoCombo(
    ...,
    componentes=[coca, pan],
)

otro_combo = ProductoCombo(
    ...,
    componentes=[coca, pan],
)

La relación se modela como agregación:

ProductoCombo "1" o-- "2..*" Producto

El combo exige como mínimo dos componentes.

🔗 Asociaciones
El modelo contiene dos asociaciones principales.

Producto — UnidadMedida
Un producto puede tener una unidad de venta:

unidad_venta: UnidadMedida | None

Ejemplos:

Coca-Cola     → u
Jamón         → kg
Agua Mineral  → L

ProductoCategoria — Categoria
Cada ProductoCategoria mantiene una referencia a su Categoria.

Estas relaciones aparecen en el UML como:

Producto "0..*" --> "0..1" UnidadMedida
ProductoCategoria "0..*" --> "1" Categoria

📏 UnidadMedida
UnidadMedida se implementa como una dataclass inmutable:

@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str

El uso de frozen=True impide modificar sus atributos después de crear una instancia.

La demo verifica esta propiedad intentando modificar el símbolo de una unidad.

⭐ Productos destacados
No se creó una subclase ProductoDestacado.

El comportamiento se incorporó directamente a Producto mediante:

_orden_vidriera

y los métodos:

destacar(orden)
quitar_destacado()

De esta manera, cualquier producto puede ser destacado sin convertirse en un tipo diferente de producto.

📊 Stock y disponibilidad
Cada producto mantiene una cantidad de stock mediante:

_stock_cantidad

La propiedad:

disponible

indica si el producto está habilitado y posee stock.

También se puede modificar su estado mediante:

producto.habilitar()
producto.deshabilitar()

En ProductoCombo, el stock disponible se calcula tomando el menor stock de sus componentes.

En la demo:

Coca-Cola  → 10
Pan Lactal → 8

Stock del combo → 8

💰 Precios
Los precios se manejan utilizando float.

El formato de publicación utiliza:

f"$ {precio:.2f}"

Ejemplos de la demo:

Coca-Cola     → $ 1000.00 / u
Agua Mineral  → $ 700.00 / L
Jamón         → $ 8000.00 / kg
Pan Lactal    → $ 1500.00 / u
Combo Merienda → $ 2500.00 / u

📤 Exportación con Protocol
El proyecto define el contrato estructural:

class Exportable(Protocol):
    def exportar(self) -> str:
        ...

Tanto Producto como FichaPuntoDeVenta cumplen este contrato mediante la implementación de exportar().

Esto permite utilizar objetos de ambas clases mediante:

exportar_catalogo(catalogo)

sin necesidad de que compartan una clase base.

🔌 Librería externa
libreria_externa.py simula una clase desarrollada por un tercero:

class FichaPuntoDeVenta:
    ...

La clase no hereda de Exportable ni de ninguna clase del modelo.

Sin embargo, posee:

def exportar(self) -> str:

Por lo tanto, cumple estructuralmente con el Protocol.

Esto demuestra la utilidad de Protocol para trabajar con clases externas que no pueden ser modificadas.

🧠 Abstracción y polimorfismo
Producto hereda de ABC y define:

@abstractmethod
def precio_final(self, cantidad: float) -> float:
    ...

Cada subclase proporciona su propia implementación:

Clase	Implementación
ProductoSimple	Precio según cantidad entera
ProductoPorPeso	Precio según cantidad decimal
ProductoCombo	Precio de componentes con descuento

La demo también verifica que Producto no pueda instanciarse directamente y que una subclase sin precio_final() tampoco pueda instanciarse.

▶️ Ejecución
El proyecto requiere únicamente Python 3.12 o superior.

No es necesario instalar paquetes externos.

Desde la carpeta del proyecto:

python main.py

La demo ejecuta las distintas funcionalidades del modelo y finaliza con:

=== FIN DE LA DEMO ===

📐 Diagrama UML
El diagrama final se encuentra en:

uml/modelo_final.md

Está realizado con Mermaid y representa:

Herencia

Composición

Agregación

Asociación

Conformidad con Exportable

Multiplicidades

Atributos

Métodos públicos

Clases abstractas

FichaPuntoDeVenta

🛠️ Tecnologías
Tecnología	Uso
Python 3.12+	Lenguaje
abc	Clase abstracta Producto
dataclasses	UnidadMedida inmutable
typing.Protocol	Contrato Exportable
Mermaid	Diagrama UML
Git / GitHub	Control de versiones

👨‍💻 Autor
Pablo de la Puente

UTN · Programación IV · Parcial 1

✅ Estado
Proyecto funcional.

La demo principal ejecuta correctamente el modelo y sus funcionalidades principales.