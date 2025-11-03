
from dataclasses import dataclass
from .mascota import Mascota
@dataclass
class MascotaEnVenta(Mascota):
    precio: float = 0.0
    def mostrar_datos(self) -> str:
        return f"[VENTA] {self.nombre} • {self.raza} • ${self.precio:,.0f}"
