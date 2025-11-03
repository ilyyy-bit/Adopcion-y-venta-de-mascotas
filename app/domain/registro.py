
from dataclasses import dataclass
from typing import Optional
from .base_types import TipoProceso
@dataclass
class Registro:
    id: str
    fecha: str
    tipo: TipoProceso
    persona_id: str
    mascota_id: str
    monto: Optional[float] = None
