
from typing import Any, Dict
from app.domain.mascota_adopcion import MascotaEnAdopcion
from app.domain.mascota_venta import MascotaEnVenta
from app.domain.persona import Persona
from app.domain.registro import Registro
from app.domain.alianza import Alianza
from app.domain.banner import BannerPromocion
from app.domain.base_types import TipoProceso, TipoAlianza, TipoBanner
def _enum_from_name(enum_cls, name: str):
    return enum_cls[name] if isinstance(name, str) else name
def to_dict(obj: Any) -> Dict:
    d = obj.__dict__.copy()
    d["type"] = obj.__class__.__name__
    if "tipo" in d and d["tipo"] is not None and hasattr(d["tipo"], "name"):
        d["tipo"] = d["tipo"].name
    return d
def from_dict(d: Dict) -> Any:
    t = d.get("type")
    if t == "MascotaEnAdopcion": return MascotaEnAdopcion(**{k:v for k,v in d.items() if k!="type"})
    if t == "MascotaEnVenta": return MascotaEnVenta(**{k:v for k,v in d.items() if k!="type"})
    if t == "Persona": return Persona(**{k:v for k,v in d.items() if k!="type"})
    if t == "Registro":
        dd = d.copy(); dd.pop("type", None); dd["tipo"] = _enum_from_name(TipoProceso, dd["tipo"]); return Registro(**dd)
    if t == "Alianza":
        dd = d.copy(); dd.pop("type", None); dd["tipo"] = _enum_from_name(TipoAlianza, dd["tipo"]); return Alianza(**dd)
    if t == "BannerPromocion":
        dd = d.copy(); dd.pop("type", None); dd["tipo"] = _enum_from_name(TipoBanner, dd["tipo"]); return BannerPromocion(**dd)
    raise ValueError(f"Tipo no soportado: {t}")
