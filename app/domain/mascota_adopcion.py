
from dataclasses import dataclass
from .mascota import Mascota
@dataclass
class MascotaEnAdopcion(Mascota):
    def mostrar_datos(self) -> str:
        return f"[ADOPCIÓN] {self.nombre} • {self.especie} • {self.edad} años"
