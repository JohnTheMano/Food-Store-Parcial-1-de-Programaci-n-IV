from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Exportable(Protocol):
    def exportar(self) -> str:
        ...


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")

        if not isinstance(descripcion, str):
            raise ValueError("La descripción debe ser una cadena.")

        self._nombre = nombre
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


class ProductoCategoria:
    def __init__(
        self,
        categoria: Categoria,
        es_principal: bool,
    ) -> None:
        if not isinstance(categoria, Categoria):
            raise TypeError("categoria debe ser una Categoria.")

        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


class Producto(ABC):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        categoria_principal: Categoria,
        unidad_venta: UnidadMedida | None = None,
        habilitado: bool = True,
    ) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if not isinstance(precio_base, (int, float)) or isinstance(
            precio_base, bool
        ):
            raise ValueError("El precio base debe ser numérico.")

        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo.")

        if not isinstance(stock_cantidad, (int, float)) or isinstance(
            stock_cantidad, bool
        ):
            raise ValueError("El stock debe ser numérico.")

        if stock_cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")

        if not isinstance(categoria_principal, Categoria):
            raise TypeError("La categoría principal debe ser una Categoria.")

        if unidad_venta is not None and not isinstance(
            unidad_venta, UnidadMedida
        ):
            raise TypeError(
                "La unidad de venta debe ser una UnidadMedida o None."
            )

        if not isinstance(habilitado, bool):
            raise TypeError("habilitado debe ser bool.")

        self._nombre = nombre
        self._precio_base = float(precio_base)
        self._stock_cantidad = float(stock_cantidad)
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones: list[ProductoCategoria] = []
        self._orden_vidriera: int | None = None

        self.clasificar_en(categoria_principal, es_principal=True)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_actual() > 0

    @property
    def precio_publicado(self) -> str:
        precio = f"$ {self.precio_base:.2f}"

        if self._unidad_venta is not None:
            precio += f" / {self._unidad_venta.simbolo}"

        return precio

    @property
    def orden_vidriera(self) -> int | None:
        return self._orden_vidriera

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def destacar(self, orden: int) -> None:
        if isinstance(orden, bool) or not isinstance(orden, int):
            raise ValueError("El orden de vidriera debe ser un entero.")

        if orden < 1:
            raise ValueError(
                "El orden de vidriera debe ser mayor o igual a 1."
            )

        self._orden_vidriera = orden

    def quitar_destacado(self) -> None:
        self._orden_vidriera = None

    def clasificar_en(
        self,
        categoria: Categoria,
        es_principal: bool = False,
    ) -> None:
        if not isinstance(categoria, Categoria):
            raise TypeError("categoria debe ser una Categoria.")

        for vinculo in self._clasificaciones:
            if vinculo.categoria is categoria:
                raise ValueError(
                    "El producto ya está clasificado en esa categoría."
                )

        if es_principal:
            for vinculo in self._clasificaciones:
                vinculo._marcar_principal(False)

        vinculo = ProductoCategoria(categoria, es_principal)
        self._clasificaciones.append(vinculo)

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for vinculo in self._clasificaciones:
            if vinculo.es_principal:
                return vinculo.categoria

        raise RuntimeError(
            "El producto debe tener exactamente una categoría principal."
        )

    def exportar(self) -> str:
        return (
            f"PRODUCTO|{self.nombre}|{self.precio_publicado}|"
            f"Disponible: {self.disponible}"
        )

    @property
    def stock(self) -> float:
        return self._stock_actual()

    def _stock_actual(self) -> float:
        return self._stock_cantidad


    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        ...


class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
            or cantidad < 1
            or not float(cantidad).is_integer()
        ):
            raise ValueError(
                "La cantidad de un ProductoSimple debe ser "
                "un entero mayor o igual a 1."
            )

        return self.precio_base * cantidad


class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
            or cantidad <= 0
        ):
            raise ValueError(
                "La cantidad de un ProductoPorPeso debe ser "
                "mayor que cero."
            )

        return round(self.precio_base * cantidad, 2)


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        componentes: list[Producto],
        descuento: float,
        categoria_principal: Categoria,
        unidad_venta: UnidadMedida | None = None,
        habilitado: bool = True,
    ) -> None:
        if len(componentes) < 2:
            raise ValueError(
                "Un ProductoCombo debe tener al menos "
                "dos componentes."
            )

        if not isinstance(descuento, (int, float)) or isinstance(
            descuento, bool
        ):
            raise ValueError("El descuento debe ser numérico.")

        if not 0 <= descuento < 1:
            raise ValueError("El descuento debe estar entre 0 y 1.")

        for componente in componentes:
            if not isinstance(componente, Producto):
                raise TypeError(
                    "Todos los componentes deben ser Productos."
                )

        self._componentes = list(componentes)
        self._descuento = float(descuento)

        super().__init__(
            nombre=nombre,
            precio_base=0,
            stock_cantidad=0,
            categoria_principal=categoria_principal,
            unidad_venta=unidad_venta,
            habilitado=habilitado,
        )

    @property
    def precio_base(self) -> float:
        return sum(
            componente.precio_final(1)
            for componente in self._componentes
        )

    def componentes(self) -> tuple[Producto, ...]:
        return tuple(self._componentes)

    def _stock_actual(self) -> float:
        return min(
            componente.stock
            for componente in self._componentes
        )

    def precio_final(self, cantidad: float) -> float:
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
            or cantidad < 1
            or not float(cantidad).is_integer()
        ):
            raise ValueError(
                "La cantidad de un ProductoCombo debe ser "
                "un entero mayor o igual a 1."
            )

        precio_componentes = sum(
            componente.precio_final(1)
            for componente in self._componentes
        )

        return precio_componentes * (1 - self._descuento) * cantidad


def exportar_catalogo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]
