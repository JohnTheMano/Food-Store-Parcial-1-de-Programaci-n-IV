from dataclasses import FrozenInstanceError

from catalogo import (
    Categoria,
    ProductoSimple,
    ProductoPorPeso,
    ProductoCombo,
    UnidadMedida,
)


print("=== PRUEBA 1: UnidadMedida inmutable ===")

kg = UnidadMedida("Kilogramo", "kg", "masa")

print(kg)
print(kg.simbolo)

try:
    kg.simbolo = "g"
except FrozenInstanceError:
    print("OK: UnidadMedida es inmutable.")


print("\n=== PRUEBA 2: Categoria ===")

bebidas = Categoria("Bebidas", "Bebidas envasadas")
gaseosas = Categoria("Gaseosas")
fiambres = Categoria("Fiambrería")

print(bebidas.nombre)
print(bebidas.descripcion)


print("\n=== PRUEBA 3: ProductoSimple ===")

coca = ProductoSimple(
    nombre="Coca-Cola",
    precio_base=1000,
    stock_cantidad=10,
    categoria_principal=bebidas,
    unidad_venta=UnidadMedida("Unidad", "u", "unidad"),
)

print("Nombre:", coca.nombre)
print("Precio base:", coca.precio_base)
print("Precio publicado:", coca.precio_publicado)
print("Disponible:", coca.disponible)
print("Precio por 3:", coca.precio_final(3))

coca.deshabilitar()
print("Disponible después de deshabilitar:", coca.disponible)

coca.habilitar()
print("Disponible después de habilitar:", coca.disponible)


print("\n=== PRUEBA 4: Clasificaciones ===")

coca.clasificar_en(gaseosas)

print("Cantidad de clasificaciones:", len(coca.categorias()))
print("Categoría principal:", coca.categoria_principal().nombre)

try:
    coca.clasificar_en(gaseosas)
except ValueError as error:
    print("OK:", error)


print("\n=== PRUEBA 5: ProductoPorPeso ===")

jamon = ProductoPorPeso(
    nombre="Jamón",
    precio_base=8000,
    stock_cantidad=5,
    categoria_principal=fiambres,
    unidad_venta=kg,
)

print("Nombre:", jamon.nombre)
print("Precio publicado:", jamon.precio_publicado)
print("Precio por 0.250 kg:", jamon.precio_final(0.250))
print("Precio por 1.5 kg:", jamon.precio_final(1.5))


print("\n=== PRUEBA 6: ProductoCombo ===")

combo = ProductoCombo(
    nombre="Combo Merienda",
    componentes=[coca, jamon],
    descuento=0.10,
    categoria_principal=bebidas,
    unidad_venta=UnidadMedida("Unidad", "u", "unidad"),
)

print("Nombre:", combo.nombre)
print("Precio base derivado:", combo.precio_base)
print("Precio publicado:", combo.precio_publicado)
print("Stock disponible del combo:", combo._stock_actual())
print("Precio del combo por 1:", combo.precio_final(1))
print("Precio del combo por 2:", combo.precio_final(2))


print("\n=== PRUEBA 7: Agregación ===")

print("Componentes del combo:")

for componente in combo.componentes():
    print("-", componente.nombre)

print("Stock de Coca-Cola:", coca._stock_actual())
print("Stock de Jamón:", jamon._stock_actual())

print("Los componentes siguen existiendo fuera del combo.")

otro_combo = ProductoCombo(
    nombre="Otro Combo",
    componentes=[coca, jamon],
    descuento=0.20,
    categoria_principal=bebidas,

)
