
from typing import List, Optional
from app.persistence.file_table import read_all, append_one, overwrite_all_atomic
from app.persistence.codecs import to_dict, from_dict
from app.domain.registro import Registro
from app.config import REGISTROS_FILE
class RegistrosFileRepo:
    def create(self, r: Registro) -> Registro:
        append_one(REGISTROS_FILE, to_dict(r)); return r
    def list_all(self) -> List[Registro]:
        return [from_dict(d) for d in read_all(REGISTROS_FILE)]
    def get(self, id_: str) -> Optional[Registro]:
        for d in read_all(REGISTROS_FILE):
            if d.get("id") == id_: return from_dict(d)
        return None
    def update(self, r: Registro) -> None:
        rows = read_all(REGISTROS_FILE)
        for i, d in enumerate(rows):
            if d.get("id") == r.id: rows[i] = to_dict(r); break
        overwrite_all_atomic(REGISTROS_FILE, rows)
    def delete(self, id_: str) -> None:
        rows = [d for d in read_all(REGISTROS_FILE) if d.get("id") != id_]
        overwrite_all_atomic(REGISTROS_FILE, rows)
