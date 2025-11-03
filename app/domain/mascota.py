
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
@dataclass
class Mascota(ABC):
    id: str
    nombre: str
    especie: str
    edad: int
    raza: str
    estado_salud: str
    disponible: bool = True
    imagen_path: Optional[str] = None
    def marcar_no_disponible(self) -> None:
        self.disponible = False
    @abstractmethod
    def mostrar_datos(self) -> str: ...
