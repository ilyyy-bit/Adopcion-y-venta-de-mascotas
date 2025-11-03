
from typing import List, Optional
from app.persistence.file_table import read_all, append_one, overwrite_all_atomic
from app.persistence.codecs import to_dict, from_dict
from app.domain.alianza import Alianza
from app.config import ALIANZAS_FILE
class AlianzasFileRepo:
    def create(self, a: Alianza) -> Alianza:
        append_one(ALIANZAS_FILE, to_dict(a)); return a
    def list_all(self) -> List[Alianza]:
        return [from_dict(d) for d in read_all(ALIANZAS_FILE)]
    def get(self, id_: str) -> Optional[Alianza]:
        for d in read_all(ALIANZAS_FILE):
            if d.get("id") == id_: return from_dict(d)
        return None
    def update(self, a: Alianza) -> None:
        rows = read_all(ALIANZAS_FILE)
        for i, d in enumerate(rows):
            if d.get("id") == a.id: rows[i] = to_dict(a); break
        overwrite_all_atomic(ALIANZAS_FILE, rows)
    def delete(self, id_: str) -> None:
        rows = [d for d in read_all(ALIANZAS_FILE) if d.get("id") != id_]
        overwrite_all_atomic(ALIANZAS_FILE, rows)
