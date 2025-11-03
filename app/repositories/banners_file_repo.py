
from typing import List, Optional
from app.persistence.file_table import read_all, append_one, overwrite_all_atomic
from app.persistence.codecs import to_dict, from_dict
from app.domain.banner import BannerPromocion
from app.config import BANNERS_FILE
class BannersFileRepo:
    def create(self, b: BannerPromocion) -> BannerPromocion:
        append_one(BANNERS_FILE, to_dict(b)); return b
    def list_all(self) -> List[BannerPromocion]:
        return [from_dict(d) for d in read_all(BANNERS_FILE)]
    def get(self, id_: str) -> Optional[BannerPromocion]:
        for d in read_all(BANNERS_FILE):
            if d.get("id") == id_: return from_dict(d)
        return None
    def update(self, b: BannerPromocion) -> None:
        rows = read_all(BANNERS_FILE)
        for i, d in enumerate(rows):
            if d.get("id") == b.id: rows[i] = to_dict(b); break
        overwrite_all_atomic(BANNERS_FILE, rows)
    def delete(self, id_: str) -> None:
        rows = [d for d in read_all(BANNERS_FILE) if d.get("id") != id_]
        overwrite_all_atomic(BANNERS_FILE, rows)
