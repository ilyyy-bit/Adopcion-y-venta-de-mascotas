
from typing import List, Optional
from app.persistence.file_table import read_all, append_one, overwrite_all_atomic
from app.persistence.codecs import to_dict, from_dict
from app.domain.persona import Persona
from app.config import PERSONAS_FILE
class PersonasFileRepo:
    def create(self, p: Persona) -> Persona:
        append_one(PERSONAS_FILE, to_dict(p)); return p
    def list_all(self) -> List[Persona]:
        return [from_dict(d) for d in read_all(PERSONAS_FILE)]
    def get(self, id_: str) -> Optional[Persona]:
        for d in read_all(PERSONAS_FILE):
            if d.get("id") == id_: return from_dict(d)
        return None
    def get_by_identificacion(self, identificacion: str) -> Optional[Persona]:
        for d in read_all(PERSONAS_FILE):
            if d.get("identificacion") == identificacion: return from_dict(d)
        return None
    def update(self, p: Persona) -> None:
        rows = read_all(PERSONAS_FILE)
        for i, d in enumerate(rows):
            if d.get("id") == p.id: rows[i] = to_dict(p); break
        overwrite_all_atomic(PERSONAS_FILE, rows)
    def delete(self, id_: str) -> None:
        rows = [d for d in read_all(PERSONAS_FILE) if d.get("id") != id_]
        overwrite_all_atomic(PERSONAS_FILE, rows)
