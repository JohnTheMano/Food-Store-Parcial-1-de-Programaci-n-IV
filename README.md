🛒 Food Store — Parcial 1 de Programación IV
Modelo orientado a objetos para un catálogo de productos de una tienda de alimentos.

UTN · Programación IV · Parcial 1

📋 Descripción
Este proyecto implementa un catálogo de productos utilizando Python 3.12+ y exclusivamente la biblioteca estándar.

El objetivo es aplicar conceptos de Programación Orientada a Objetos y resolver los requerimientos planteados en el parcial:

Herencia

Abstracción

Polimorfismo

Encapsulamiento

Composición

Agregación

Asociación

Protocolos estructurales

Dataclasses inmutables

Type hints

Validación de datos

Manejo de stock y disponibilidad

El modelo funciona completamente en memoria, sin utilizar bases de datos, ORM ni frameworks web.

🗂️ Estructura del proyecto
Archivo	Descripción
catalogo.py	Contiene el modelo principal del catálogo
libreria_externa.py	Simula una clase provista por una librería de terceros
main.py	Demo ejecutable del parcial
prueba_catalogo.py	Pruebas iniciales de las clases del modelo
uml/modelo_final.md	Diagrama UML final realizado en Mermaid
README.md	Documentación del proyecto

🧱 Modelo de clases
La clase abstracta Producto concentra el comportamiento común de todos los productos y define el método abstracto precio_final().

Sus especializaciones son:

Clase	Representa	Forma de venta
ProductoSimple	Producto vendido por unidad	Cantidades enteras
ProductoPorPeso	Producto vendido por peso	Cantidades decimales
ProductoCombo	Producto compuesto por otros productos	Componentes + descuento

La estructura de herencia principal es:

                         Producto
                            ▲
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
      ProductoSimple  ProductoPorPeso  ProductoCombo

Producto es abstracta, por lo que no puede instanciarse directamente.

📦 Productos
ProductoSimple
Representa productos comercializados por unidades enteras.

Ejemplo utilizado en la demo:

coca = ProductoSimple(
    nombre="Coca-Cola",
    precio_base=1000,
    stock_cantidad=10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

El precio final se obtiene multiplicando el precio base por la cantidad solicitada.

ProductoPorPeso
Representa productos cuyo precio depende de una cantidad que puede ser decimal.

Ejemplo:

jamon = ProductoPorPeso(
    nombre="Jamón",
    precio_base=8000,
    stock_cantidad=5,
    categoria_principal=fiambres,
    unidad_venta=kilogramo,
)

Permite calcular precios como:

Cantidad	Precio
0.250 kg	$ 2000.00
1.5 kg	$ 12000.00

ProductoCombo
Representa un producto formado por otros productos existentes.

Ejemplo:

combo = ProductoCombo(
    nombre="Combo Merienda",
    componentes=[coca, pan],
    descuento=0.10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

El precio base del combo se deriva de los precios de sus componentes y posteriormente se aplica el descuento.

🗃️ Categorías
El modelo cuenta con la clase Categoria, que representa las categorías del catálogo.

Cada categoría posee:

Nombre.

Descripción.

En la demo se utilizan:

Categoría	Descripción
Bebidas	Bebidas envasadas
Gaseosas	Sin descripción específica
Fiambrería	Sin descripción específica
Almacén	Sin descripción específica

Un producto puede estar clasificado en varias categorías.

🔗 ProductoCategoria
ProductoCategoria representa el vínculo entre un producto y una categoría.

La clase permite indicar si determinada categoría es la categoría principal del producto.

La relación se crea internamente desde:

producto.clasificar_en(...)

El cliente obtiene los vínculos mediante:

producto.categorias()

Esto permite mantener encapsulada la creación de los objetos ProductoCategoria.

Además, el modelo garantiza que un producto tenga una única categoría principal.

Por ejemplo:

coca.clasificar_en(gaseosas)

coca.clasificar_en(
    almacen,
    es_principal=True,
)

Luego Almacén pasa a ser la nueva categoría principal.

🧩 Composición
La relación entre Producto y ProductoCategoria se modela como composición.

En Producto se mantiene internamente:

self._clasificaciones: list[ProductoCategoria] = []

Los objetos ProductoCategoria son creados por el propio Producto mediante clasificar_en().

Esto representa una relación fuerte entre el producto y sus vínculos de clasificación.

En el UML:

Producto "1" *-- "1..*" ProductoCategoria

🔄 Agregación
ProductoCombo mantiene una colección de productos como componentes:

self._componentes = list(componentes)

Los componentes existen independientemente del combo.

Por ejemplo, Coca-Cola y Pan Lactal pueden existir antes de crear el combo y también pueden reutilizarse en otro combo:

combo = ProductoCombo(
    ...,
    componentes=[coca, pan],
)

otro_combo = ProductoCombo(
    ...,
    componentes=[coca, pan],
)

Esto representa una agregación.

En el UML:

ProductoCombo "1" o-- "2..*" Producto

El mínimo de dos componentes se valida al crear el combo.

🔗 Asociaciones
El modelo también contiene asociaciones entre distintas clases.

Producto — UnidadMedida
Un producto puede tener una unidad de venta:

unidad_venta: UnidadMedida | None

Por ejemplo:

Coca-Cola → u

Jamón → kg

Agua Mineral → L

En el UML:

Producto "0..*" --> "0..1" UnidadMedida

ProductoCategoria — Categoria
Cada objeto ProductoCategoria referencia una Categoria:

self._categoria = categoria

En el UML:

ProductoCategoria "0..*" --> "1" Categoria

📏 UnidadMedida
UnidadMedida se implementa como una dataclass inmutable:

@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str

El uso de frozen=True impide modificar sus atributos después de la creación.

La demo verifica este comportamiento:

try:
    kilogramo.simbolo = "g"
except FrozenInstanceError:
    print("OK: UnidadMedida es inmutable.")

Las unidades utilizadas en la demo son:

Nombre	Símbolo	Tipo
Unidad	u	unidad
Kilogramo	kg	masa
Litro	L	volumen

⭐ Productos destacados
El concepto de producto destacado no se modeló mediante una subclase ProductoDestacado.

En cambio, el comportamiento se incorporó directamente a Producto mediante:

_orden_vidriera

y los métodos:

destacar(orden)
quitar_destacado()

Esto permite que cualquier producto pueda ser destacado sin convertirlo en un tipo diferente de producto.

Ejemplo:

coca.destacar(1)
jamon.destacar(2)
combo.destacar(3)

Y para quitar un producto de la vidriera:

combo.quitar_destacado()

📊 Stock y disponibilidad
Cada producto mantiene una cantidad de stock:

_stock_cantidad

La propiedad:

disponible

indica si el producto está habilitado y posee stock disponible.

El producto puede habilitarse o deshabilitarse mediante:

producto.habilitar()
producto.deshabilitar()

En el caso de ProductoCombo, el stock se obtiene a partir del menor stock disponible entre sus componentes.

Por ejemplo, si un combo contiene:

Producto	Stock
Coca-Cola	10
Pan Lactal	8

el stock disponible del combo será:

8

💰 Precios
Los precios se manejan utilizando float, según lo requerido por la consigna.

El precio publicado utiliza el formato:

f"$ {precio:.2f}"

Ejemplos de la demo:

Producto	Precio publicado
Coca-Cola	$ 1000.00 / u
Agua Mineral	$ 700.00 / L
Jamón	$ 8000.00 / kg
Pan Lactal	$ 1500.00 / u
Combo Merienda	$ 2500.00 / u

📤 Exportación con Protocol
El proyecto utiliza un contrato estructural mediante Protocol:

class Exportable(Protocol):
    def exportar(self) -> str:
        ...

Producto implementa el método:

def exportar(self) -> str:

Por lo tanto, los productos cumplen estructuralmente con Exportable.

Además, se utiliza una clase proveniente de una librería externa:

class FichaPuntoDeVenta:
    ...
    
    def exportar(self) -> str:
        return f"POS|{self._codigo}|{self._detalle}"

No es necesario modificarla ni hacer que herede de Exportable.

Al implementar exportar(), cumple el protocolo de manera estructural.

🔌 Librería externa
El archivo libreria_externa.py simula una clase desarrollada por un tercero.

La clase:

FichaPuntoDeVenta

no hereda de ninguna clase del modelo.

Esto permite demostrar la utilidad de Protocol: una clase externa puede cumplir el contrato simplemente proporcionando el método requerido.

En la demo se incorpora junto con los productos:

catalogo = [
    coca,
    agua,
    jamon,
    pan,
    combo,
    ficha,
]

Luego todos pueden exportarse mediante:

exportar_catalogo(catalogo)

🧠 Abstracción y polimorfismo
Producto hereda de ABC y define:

@abstractmethod
def precio_final(self, cantidad: float) -> float:
    ...

Esto obliga a las subclases concretas a proporcionar su propia implementación.

Clase	Implementación de precio_final()
ProductoSimple	Precio por cantidad entera
ProductoPorPeso	Precio según cantidad decimal
ProductoCombo	Precio de componentes con descuento

La demo verifica que Producto no pueda instanciarse directamente y que tampoco pueda instanciarse una subclase que no implemente precio_final().

🧪 Demo de main.py
El archivo main.py contiene una demostración completa del modelo.

La ejecución recorre:

Sección	Funcionalidad
1	Categorías y unidades
2	Inmutabilidad de UnidadMedida
3	Creación de productos
4	Clasificaciones
5	Precios y disponibilidad
6	Producto combo
7	Agregación
8	Productos destacados
9	Composición
10	Clase abstracta
11	Exportación del catálogo

La ejecución actual finaliza correctamente con:

=== FIN DE LA DEMO ===

▶️ Ejecución
El proyecto no requiere instalar paquetes externos.

Con Python 3.12 o superior:

python main.py

También se puede ejecutar la prueba auxiliar:

python prueba_catalogo.py

No se utiliza:

Base de datos.

ORM.

Flask.

Django.

FastAPI.

SQLAlchemy.

Dependencias externas.

📐 Diagrama UML
El diagrama final se encuentra en:

uml/modelo_final.md

Está realizado utilizando Mermaid.

El diagrama representa:

Herencia.

Composición.

Agregación.

Asociación.

Conformidad con Exportable.

Multiplicidades.

Atributos.

Métodos públicos.

Clases abstractas.

Clase externa FichaPuntoDeVenta.

Relaciones principales:

Producto <|-- ProductoSimple
Producto <|-- ProductoPorPeso
Producto <|-- ProductoCombo

Producto "1" *-- "1..*" ProductoCategoria

ProductoCombo "1" o-- "2..*" Producto

Producto "0..*" --> "0..1" UnidadMedida

ProductoCategoria "0..*" --> "1" Categoria

Producto ..|> Exportable

FichaPuntoDeVenta ..|> Exportable

📋 Requisitos técnicos
Requisito	Estado
Python 3.12 o superior	✅
Biblioteca estándar	✅
abc	✅
typing / Protocol	✅
dataclasses	✅
Precios con float	✅
Formato con f-strings	✅
Sin ORM	✅
Sin framework web	✅
Sin base de datos	✅
Modelo en memoria	✅
Sin dependencias externas	✅
Type hints en firmas públicas	✅
PEP 8	✅

🎥 Defensa del parcial
El proyecto está preparado para la defensa oral mediante una demo ejecutable.

Durante la presentación se pueden mostrar:

La ejecución completa de main.py.

La clase abstracta Producto.

Las clases derivadas.

La composición entre Producto y ProductoCategoria.

La agregación entre ProductoCombo y Producto.

Las asociaciones con Categoria y UnidadMedida.

La implementación de Exportable mediante Protocol.

La integración con FichaPuntoDeVenta.

La decisión de diseño para los productos destacados.

El diagrama UML final.

🛠️ Tecnologías utilizadas
Tecnología	Uso
Python 3.12+	Lenguaje de programación
abc	Clases abstractas
dataclasses	UnidadMedida inmutable
typing.Protocol	Contrato estructural Exportable
Mermaid	Diagrama UML
Git / GitHub	Control de versiones y entrega

👨‍💻 Autor
Pablo de la Puente

UTN · Programación IV · Parcial 1

✅ Estado del proyecto
Proyecto funcional y listo para presentación.

La demo principal ejecuta correctamente las funcionalidades implementadas y finaliza sin errores.