
from dataclasses import dataclass
from typing import Optional
from .base_types import TipoBanner
@dataclass
class BannerPromocion:
    id: str
    tipo: TipoBanner
    texto: Optional[str] = None
    imagen_path: Optional[str] = None
    inicio: Optional[str] = None
    fin: Optional[str] = None
    activo: bool = False
    destacado_mascota_id: Optional[str] = None
    def activar(self): self.activo = True
    def desactivar(self): self.activo = False
    def mostrar_banner(self) -> str:
        base = f"({self.tipo.name}) "
        if self.texto: base += self.texto
        if self.destacado_mascota_id: base += f" | Destacado: {self.destacado_mascota_id}"
        return base
