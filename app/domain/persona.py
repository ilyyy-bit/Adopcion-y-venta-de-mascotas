
from dataclasses import dataclass, field
from typing import List, Optional
@dataclass
class Persona:
    id: str
    nombre: str
    identificacion: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    historial: List[str] = field(default_factory=list)
