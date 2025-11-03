
from typing import List, Optional
from app.persistence.file_table import read_all, append_one, overwrite_all_atomic
from app.persistence.codecs import to_dict, from_dict
from app.domain.mascota import Mascota
from app.config import MASCOTAS_FILE
class MascotasFileRepo:
    def create(self, m: Mascota) -> Mascota:
        append_one(MASCOTAS_FILE, to_dict(m)); return m
    def list_all(self) -> List[Mascota]:
        return [from_dict(d) for d in read_all(MASCOTAS_FILE)]
    def list_disponibles(self) -> List[Mascota]:
        return [m for m in self.list_all() if m.disponible]
    def get(self, id_: str) -> Optional[Mascota]:
        for d in read_all(MASCOTAS_FILE):
            if d.get("id") == id_: return from_dict(d)
        return None
    def update(self, m: Mascota) -> None:
        rows = read_all(MASCOTAS_FILE)
        for i, d in enumerate(rows):
            if d.get("id") == m.id: rows[i] = to_dict(m); break
        overwrite_all_atomic(MASCOTAS_FILE, rows)
    def delete(self, id_: str) -> None:
        rows = [d for d in read_all(MASCOTAS_FILE) if d.get("id") != id_]
        overwrite_all_atomic(MASCOTAS_FILE, rows)
