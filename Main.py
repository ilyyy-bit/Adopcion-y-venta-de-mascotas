from Modelo import Mascota, Persona, Alianza, BannerPromocion, PlataformaMascotas

plataforma = PlataformaMascotas()

def registrar_mascota():
    print("\n🐾 REGISTRO DE MASCOTA")
    id_animal = len(plataforma.mascotas) + 1
    nombre = input("Nombre: ")
    especie = input("Especie: ")
    edad = int(input("Edad: "))
    raza = input("Raza: ")
    estado_salud = input("Estado de salud: ")

    mascota = Mascota(id_animal, nombre, especie, edad, raza, estado_salud)
    plataforma.registrar_mascota(mascota)


def registrar_persona():
    print("\n👤 REGISTRO DE PERSONA")
    id_persona = len(plataforma.personas) + 1
    nombre = input("Nombre completo: ")
    contacto = input("Correo o teléfono: ")

    persona = Persona(id_persona, nombre, contacto)
    plataforma.registrar_persona(persona)


def mostrar_animales():
    print("\n🐶 ANIMALES DISPONIBLES:")
    disponibles = plataforma.mostrar_animales_disponibles()
    for m in disponibles:
        print("-", m)


def crear_registro():
    print("\n📋 CREAR REGISTRO DE ADOPCIÓN/VENTA")

    if not plataforma.mascotas or not plataforma.personas:
        print("Primero debes registrar mascotas y personas.")
        return

    mostrar_animales()
    id_mascota = int(input("ID del animal (según el orden mostrado): ")) - 1
    tipo = input("Tipo de registro (adopción / venta): ").lower()

    print("\n personas registradas:")
    for p in plataforma.personas:
        print(f"{p.id_persona}. {p.nombre}")

    id_persona = int(input("ID de la persona: ")) - 1

    monto = 0
    if tipo == "venta":
        monto = float(input("Monto de la venta: "))

    try:
        mascota = plataforma.mascotas[id_mascota]
        persona = plataforma.personas[id_persona]
        plataforma.crear_registro(tipo, mascota, persona, monto)
    except IndexError:
        print("❌ ID inválido.")


def agregar_promocion():
    print("\n NUEVA PROMOCIÓN")
    texto = input("Texto del banner: ")
    inicio = input("Fecha inicio (AAAA-MM-DD): ")
    fin = input("Fecha fin (AAAA-MM-DD): ")

    banner = BannerPromocion(texto, inicio, fin)
    plataforma.agregar_promocion(banner)


def agregar_alianza():
    print("\n NUEVA ALIANZA")
    nombre = input("Nombre del aliado: ")
    tipo = input("Tipo (Albergue / Criadero): ")
    comision = float(input("Porcentaje de comisión: "))

    alianza = Alianza(nombre, tipo, comision)
    plataforma.agregar_alianza(alianza)


def girar_ruleta():
    print("\n🎡 RULETA DE DESCUENTOS")
    plataforma.girar_ruleta()


def mostrar_historial():
    print("\n HISTORIAL DE UNA PERSONA")
    if not plataforma.personas:
        print(" No hay personas registradas.")
        return

    for p in plataforma.personas:
        print(f"{p.id_persona}. {p.nombre}")

    id_persona = int(input("ID de la persona: ")) - 1
    try:
        persona = plataforma.personas[id_persona]
        if not persona.historial:
            print("No tiene registros todavía.")
        else:
            for r in persona.historial:
                print("-", r.mostrar_registro())
    except IndexError:
        print("❌ ID inválido.")


def menu():
    while True:
        print("\n========= MENÚ PRINCIPAL =========")
        print("1. Registrar mascota")
        print("2. Registrar persona")
        print("3. Mostrar animales disponibles")
        print("4. Crear adopción o venta")
        print("5. Mostrar historial de persona")
        print("6. Agregar promoción")
        print("7. Agregar alianza")
        print("8. Girar ruleta de descuentos")
        print("9. Salir")
        print("==================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_mascota()
        elif opcion == "2":
            registrar_persona()
        elif opcion == "3":
            mostrar_animales()
        elif opcion == "4":
            crear_registro()
        elif opcion == "5":
            mostrar_historial()
        elif opcion == "6":
            agregar_promocion()
        elif opcion == "7":
            agregar_alianza()
        elif opcion == "8":
            girar_ruleta()
        elif opcion == "9":
            print(" ¡Gracias por usar la plataforma de adopción y venta de mascotas!")
            break
        else:
            print(" Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu()
