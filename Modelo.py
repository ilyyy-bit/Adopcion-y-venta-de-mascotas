import random

class Mascota:
    def __init__(self, id_animal, nombre, especie, edad, raza, estado_salud):
        self.id_animal = id_animal
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.raza = raza
        self.estado_salud = estado_salud
        self.disponible = True

    def marcar_no_disponible(self):
        self.disponible = False

    def mostrar_datos(self):
        return f"{self.nombre} ({self.especie}, {self.raza}) - {self.estado_salud}"


class Persona:
    def __init__(self, id_persona, nombre, contacto):
        self.id_persona = id_persona
        self.nombre = nombre
        self.contacto = contacto

    def mostrar_info(self):
        return f"{self.nombre} - {self.contacto}"


class Registro:
    def __init__(self, id_registro, tipo, mascota, persona, monto=0):
        self.id_registro = id_registro
        self.tipo = tipo  # adopción o venta
        self.mascota = mascota
        self.persona = persona
        self.monto = monto

    def mostrar_registro(self):
        return f"{self.tipo.upper()} | Mascota: {self.mascota.nombre} | Persona: {self.persona.nombre}"


class Alianza:
    def __init__(self, nombre, tipo, porcentaje_comision):
        self.nombre = nombre
        self.tipo = tipo
        self.porcentaje_comision = porcentaje_comision

    def mostrar_info(self):
        return f"Alianza con {self.nombre} ({self.tipo}) - Comisión: {self.porcentaje_comision}%"


class BannerPromocion:
    def __init__(self, texto, fecha_inicio, fecha_fin, activo=True):
        self.texto = texto
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.activo = activo

    def mostrar_banner(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"{self.texto} ({estado})"


class RuletaDescuento:
    def __init__(self):
        self.descuentos = [0.5, 5, 10, 20]

    def girar(self):
        descuento = random.choice(self.descuentos)
        return f"¡Felicidades! Obtuviste un {descuento}% de descuento."


class PlataformaMascotas:
    def __init__(self):
        self.mascotas = []
        self.personas = []
        self.registros = []

    def registrar_mascota(self, mascota):
        self.mascotas.append(mascota)

    def registrar_persona(self, persona):
        self.personas.append(persona)

    def crear_registro(self, tipo, mascota, persona, monto=0):
        registro = Registro(len(self.registros) + 1, tipo, mascota, persona, monto)
        self.registros.append(registro)
        mascota.marcar_no_disponible()
        return registro

    def mostrar_animales_disponibles(self):
        return [m.mostrar_datos() for m in self.mascotas if m.disponible]
