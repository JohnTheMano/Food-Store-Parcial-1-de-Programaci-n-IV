from dataclasses import FrozenInstanceError

from catalogo import (
    Categoria,
    Producto,
    ProductoCombo,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


print("=== FOOD STORE - DEMO DEL PARCIAL ===")


# ============================================================
# 1. CATEGORÍAS Y UNIDADES
# ============================================================

print("\n=== 1. CATEGORÍAS Y UNIDADES ===")

bebidas = Categoria("Bebidas", "Bebidas envasadas")
gaseosas = Categoria("Gaseosas")
fiambres = Categoria("Fiambrería")
almacen = Categoria("Almacén")

unidad = UnidadMedida("Unidad", "u", "unidad")
kilogramo = UnidadMedida("Kilogramo", "kg", "masa")
litro = UnidadMedida("Litro", "L", "volumen")

print("Categorías:")
print("-", bebidas.nombre)
print("-", gaseosas.nombre)
print("-", fiambres.nombre)
print("-", almacen.nombre)

print("\nUnidades:")
print("-", unidad)
print("-", kilogramo)
print("-", litro)


# ============================================================
# 2. UNIDADMEDIDA INMUTABLE
# ============================================================

print("\n=== 2. UNIDADMEDIDA INMUTABLE ===")

try:
    kilogramo.simbolo = "g"
except FrozenInstanceError:
    print("OK: UnidadMedida es inmutable.")


# ============================================================
# 3. PRODUCTOS
# ============================================================

print("\n=== 3. PRODUCTOS ===")

coca = ProductoSimple(
    nombre="Coca-Cola",
    precio_base=1000,
    stock_cantidad=10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

agua = ProductoSimple(
    nombre="Agua Mineral",
    precio_base=700,
    stock_cantidad=20,
    categoria_principal=bebidas,
    unidad_venta=litro,
)

jamon = ProductoPorPeso(
    nombre="Jamón",
    precio_base=8000,
    stock_cantidad=5,
    categoria_principal=fiambres,
    unidad_venta=kilogramo,
)

pan = ProductoSimple(
    nombre="Pan Lactal",
    precio_base=1500,
    stock_cantidad=8,
    categoria_principal=almacen,
    unidad_venta=unidad,
)

print("Productos creados:")
print("-", coca.nombre)
print("-", agua.nombre)
print("-", jamon.nombre)
print("-", pan.nombre)


# ============================================================
# 4. CLASIFICACIONES
# ============================================================

print("\n=== 4. CLASIFICACIONES ===")

coca.clasificar_en(gaseosas)

print("Producto:", coca.nombre)
print("Categorías:")

for vinculo in coca.categorias():
    print("-", vinculo.categoria.nombre)

print("Categoría principal:", coca.categoria_principal().nombre)

# Cambiamos la categoría principal.
coca.clasificar_en(almacen, es_principal=True)

print(
    "Nueva categoría principal después de reclasificar:",
    coca.categoria_principal().nombre,
)


# ============================================================
# 5. PRECIOS Y DISPONIBILIDAD
# ============================================================

print("\n=== 5. PRECIOS Y DISPONIBILIDAD ===")

print(coca.nombre, "->", coca.precio_publicado)
print("Precio por 3:", coca.precio_final(3))

print(jamon.nombre, "->", jamon.precio_publicado)
print("Precio por 0.250 kg:", jamon.precio_final(0.250))

print(pan.nombre, "->", pan.precio_publicado)

print("\nDisponible Coca-Cola:", coca.disponible)

coca.deshabilitar()
print(
    "Disponible Coca-Cola después de deshabilitar:",
    coca.disponible,
)

coca.habilitar()
print(
    "Disponible Coca-Cola después de habilitar:",
    coca.disponible,
)


# ============================================================
# 6. PRODUCTO COMBO
# ============================================================

print("\n=== 6. PRODUCTO COMBO ===")

combo = ProductoCombo(
    nombre="Combo Merienda",
    componentes=[coca, pan],
    descuento=0.10,
    categoria_principal=bebidas,
    unidad_venta=unidad,
)

print("Nombre:", combo.nombre)
print("Precio base derivado:", combo.precio_base)
print("Precio publicado:", combo.precio_publicado)
print("Stock disponible:", combo.stock)
print("Precio final por 1:", combo.precio_final(1))
print("Precio final por 2:", combo.precio_final(2))


# ============================================================
# 7. AGREGACIÓN
# ============================================================

print("\n=== 7. AGREGACIÓN ===")

print("Componentes del combo:")

for componente in combo.componentes():
    print("-", componente.nombre)

print("\nLos componentes existen independientemente del combo:")
print("-", coca.nombre)
print("-", pan.nombre)

otro_combo = ProductoCombo(
    nombre="Otro Combo",
    componentes=[coca, pan],
    descuento=0.20,
    categoria_principal=almacen,
    unidad_venta=unidad,
)

print("\nSe creó otro combo reutilizando los mismos componentes:")
print("-", otro_combo.nombre)


# ============================================================
# 8. PRODUCTOS DESTACADOS
# ============================================================

print("\n=== 8. PRODUCTOS DESTACADOS ===")

coca.destacar(1)
jamon.destacar(2)
combo.destacar(3)

print(coca.nombre, "-> orden", coca.orden_vidriera)
print(jamon.nombre, "-> orden", jamon.orden_vidriera)
print(combo.nombre, "-> orden", combo.orden_vidriera)

combo.quitar_destacado()

print(
    combo.nombre,
    "después de quitar destacado ->",
    combo.orden_vidriera,
)


# ============================================================
# 9. COMPOSICIÓN
# ============================================================

print("\n=== 9. COMPOSICIÓN ===")

print(
    "ProductoCategoria se crea internamente mediante "
    "clasificar_en()."
)

print(
    "El cliente obtiene los vínculos solamente mediante "
    "categorias()."
)

print(
    "Cantidad de clasificaciones de Coca-Cola:",
    len(coca.categorias()),
)


# ============================================================
# 10. CLASE ABSTRACTA
# ============================================================

print("\n=== 10. CLASE ABSTRACTA ===")

try:
    Producto(
        nombre="Producto inválido",
        precio_base=1000,
        stock_cantidad=1,
        categoria_principal=bebidas,
    )
except TypeError as error:
    print("OK: no se puede instanciar Producto.")
    print(error)


class ProductoIncompleto(Producto):
    pass


try:
    ProductoIncompleto(
        nombre="Producto incompleto",
        precio_base=1000,
        stock_cantidad=1,
        categoria_principal=bebidas,
    )
except TypeError as error:
    print("OK: una subclase sin precio_final tampoco se puede instanciar.")
    print(error)


# ============================================================
# 11. EXPORTACIÓN DEL CATÁLOGO
# ============================================================

print("\n=== 11. EXPORTACIÓN DEL CATÁLOGO ===")

ficha = FichaPuntoDeVenta(
    codigo="POS-001",
    detalle="Ficha generada por el sistema de caja",
)

catalogo = [
    coca,
    agua,
    jamon,
    pan,
    combo,
    ficha,
]

for linea in exportar_catalogo(catalogo):
    print(linea)


print("\n=== FIN DE LA DEMO ===")
