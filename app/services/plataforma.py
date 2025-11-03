
from dataclasses import dataclass
from datetime import date
from typing import Protocol, Optional, List
from app.domain.base_types import TipoProceso, TipoAlianza, TipoBanner
from app.domain.persona import Persona
from app.domain.mascota_adopcion import MascotaEnAdopcion
from app.domain.mascota_venta import MascotaEnVenta
from app.domain.registro import Registro
from app.domain.alianza import Alianza
from app.domain.banner import BannerPromocion
from app.services.validators import validar_email, validar_identificacion
from app.utils.ids import new_id
class RepoPersonas(Protocol):
    def create(self, p: Persona) -> Persona: ...
    def list_all(self) -> List[Persona]: ...
    def get(self, id_: str) -> Optional[Persona]: ...
    def get_by_identificacion(self, identificacion: str) -> Optional[Persona]: ...
    def update(self, p: Persona) -> None: ...
class RepoMascotas(Protocol):
    def create(self, m): ...
    def list_all(self): ...
    def list_disponibles(self): ...
    def get(self, id_: str): ...
    def update(self, m) -> None: ...
    def delete(self, id_: str) -> None: ...
class RepoRegistros(Protocol):
    def create(self, r: Registro) -> Registro: ...
    def list_all(self) -> List[Registro]: ...
    def get(self, id_: str) -> Optional[Registro]: ...
    def delete(self, id_: str) -> None: ...
class RepoAlianzas(Protocol):
    def create(self, a: Alianza) -> Alianza: ...
    def list_all(self) -> List[Alianza]: ...
    def get(self, id_: str) -> Optional[Alianza]: ...
    def update(self, a: Alianza) -> None: ...
    def delete(self, id_: str) -> None: ...
class RepoBanners(Protocol):
    def create(self, b: BannerPromocion) -> BannerPromocion: ...
    def list_all(self) -> List[BannerPromocion]: ...
    def update(self, b: BannerPromocion) -> None: ...
    def delete(self, id_: str) -> None: ...
@dataclass
class Plataforma:
    personas: RepoPersonas
    mascotas: RepoMascotas
    registros: RepoRegistros
    alianzas: RepoAlianzas
    banners: RepoBanners
    def registrar_persona(self, nombre: str, identificacion: str, telefono: str = "", email: str = "") -> Persona:
        if not validar_identificacion(identificacion): raise ValueError("Identificación inválida")
        if not validar_email(email): raise ValueError("Email inválido")
        if self.personas.get_by_identificacion(identificacion): raise ValueError("La persona ya está registrada")
        p = Persona(id=new_id(), nombre=nombre, identificacion=identificacion, telefono=telefono or None, email=email or None)
        return self.personas.create(p)
    def registrar_mascota_adopcion(self, nombre: str, especie: str, edad: int, raza: str, estado_salud: str, imagen_path: str | None = None):
        m = MascotaEnAdopcion(id=new_id(), nombre=nombre, especie=especie, edad=int(edad), raza=raza, estado_salud=estado_salud, imagen_path=imagen_path)
        return self.mascotas.create(m)
    def registrar_mascota_venta(self, nombre: str, especie: str, edad: int, raza: str, estado_salud: str, precio: float, imagen_path: str | None = None):
        m = MascotaEnVenta(id=new_id(), nombre=nombre, especie=especie, edad=int(edad), raza=raza, estado_salud=estado_salud, precio=float(precio), imagen_path=imagen_path)
        return self.mascotas.create(m)
    def eliminar_mascota(self, id_: str) -> None:
        self.mascotas.delete(id_)
    def listar_mascotas_disponibles(self):
        return self.mascotas.list_disponibles()
    def listar_mascotas_todas(self):
        return self.mascotas.list_all()
    def crear_registro(self, tipo: TipoProceso, persona_id: str, mascota_id: str, monto: float | None = None) -> Registro:
        persona = self.personas.get(persona_id)
        if not persona: raise ValueError("Persona inexistente")
        mascota = self.mascotas.get(mascota_id)
        if not mascota or not mascota.disponible: raise ValueError("Mascota no disponible")
        if tipo == TipoProceso.VENTA and monto is None: raise ValueError("Monto requerido para venta")
        reg = Registro(id=new_id(), fecha=str(date.today()), tipo=tipo, persona_id=persona_id, mascota_id=mascota_id, monto=monto)
        self.registros.create(reg)
        mascota.marcar_no_disponible(); self.mascotas.update(mascota)
        persona.historial.append(reg.id); self.personas.update(persona)
        return reg
    def eliminar_registro(self, id_: str) -> None:
        self.registros.delete(id_)
    def listar_registros(self):
        return self.registros.list_all()
    def registrar_alianza(self, nombre: str, tipo: TipoAlianza, comision: float) -> Alianza:
        a = Alianza(id=new_id(), nombre=nombre, tipo=tipo, comision=float(comision))
        return self.alianzas.create(a)
    def actualizar_alianza(self, a: Alianza) -> None:
        self.alianzas.update(a)
    def eliminar_alianza(self, id_: str) -> None:
        self.alianzas.delete(id_)
    def crear_banner(self, tipo: TipoBanner, texto: str = "", imagen_path: str | None = None, inicio: str | None = None, fin: str | None = None, activo: bool = False, destacado_mascota_id: str | None = None) -> BannerPromocion:
        b = BannerPromocion(id=new_id(), tipo=tipo, texto=texto or None, imagen_path=imagen_path, inicio=inicio, fin=fin, activo=activo, destacado_mascota_id=destacado_mascota_id)
        return self.banners.create(b)
    def activar_banner(self, banner: BannerPromocion) -> None:
        banner.activar(); self.banners.update(banner)
    def desactivar_banner(self, banner: BannerPromocion) -> None:
        banner.desactivar(); self.banners.update(banner)
    def eliminar_banner(self, id_: str) -> None:
        self.banners.delete(id_)
    def listar_banners(self):
        return self.banners.list_all()
