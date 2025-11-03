
from dataclasses import dataclass
from .base_types import TipoAlianza
@dataclass
class Alianza:
    id: str
    nombre: str
    tipo: TipoAlianza
    comision: float
    def calcular_comision(self, venta: float) -> float:
        return round((self.comision/100.0)*float(venta), 2)
