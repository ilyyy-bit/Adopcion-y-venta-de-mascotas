from Modelo import *

plataforma = PlataformaMascotas()

def menu():
    while True:
        print("\n🐾=== PLATAFORMA DE ADOPCIÓN Y VENTA DE MASCOTAS ===🐾")
        print("1. Registrar mascota")
        print("2. Registrar persona")
        print("3. Crear registro (adopción o venta)")
        print("4. Mostrar animales disponibles")
        print("5. Girar ruleta de descuento")
        print("6. Salir")

        opcion = input("\n👉 Elige una opción: ")

        if opcion == "1":
            registrar_mascota()
        elif opcion == "2":
            registrar_persona()
        elif opcion == "3":
            crear_registro()
        elif opcion == "4":
            mostrar_animales()
        elif opcion == "5":
            girar_ruleta()
        elif opcion == "6":
            print("\n ¡Gracias por usar la plataforma!")
            break
        else:
            print(" Opción no válida, intenta nuevamente.")


def registrar_mascota():
    print("\n--- Registrar Mascota ---")
    id_animal = len(plataforma.mascotas) + 1
    nombre = input("Nombre: ")
    especie = input("Especie: ")
    edad = int(input("Edad: "))
    raza = input("Raza: ")
    estado_salud = input("Estado de salud: ")

    mascota = Mascota(id_animal, nombre, especie, edad, raza, estado_salud)
    plataforma.registrar_mascota(mascota)
    print(f" Mascota '{nombre}' registrada con éxito.")


def registrar_persona():
    print("\n--- Registrar Persona ---")
    id_persona = len(plataforma.personas) + 1
    nombre = input("Nombre: ")
    contacto = input("Contacto: ")

    persona = Persona(id_persona, nombre, contacto)
    plataforma.registrar_persona(persona)
    print(f" Persona '{nombre}' registrada con éxito.")


def crear_registro():
    if not plataforma.mascotas or not plataforma.personas:
        print(" Debes tener al menos una mascota y una persona registradas.")
        return

    print("\n--- Crear Registro ---")
    print("Mascotas disponibles:")
    disponibles = plataforma.mostrar_animales_disponibles()

    for i, m in enumerate(disponibles, 1):
        print(f"{i}. {m}")

    if not disponibles:
        print("No hay animales disponibles.")
        return

    id_mascota = int(input("Selecciona una mascota (número): ")) - 1
    mascota = [m for m in plataforma.mascotas if m.disponible][id_mascota]

    print("\nPersonas registradas:")
    for i, p in enumerate(plataforma.personas, 1):
        print(f"{i}. {p.mostrar_info()}")

    id_persona = int(input("Selecciona una persona (número): ")) - 1
    persona = plataforma.personas[id_persona]

    tipo = input("Tipo de registro (Adopción/Venta): ").capitalize()
    monto = 0
    if tipo == "Venta":
        monto = float(input("Monto de la venta: "))

    registro = plataforma.crear_registro(tipo, mascota, persona, monto)
    print(f" Registro creado: {registro.mostrar_registro()}")


def mostrar_animales():
    print("\n--- Animales Disponibles ---")
    disponibles = plataforma.mostrar_animales_disponibles()
    if not disponibles:
        print("No hay animales disponibles actualmente.")
    else:
        for m in disponibles:
            print("•", m)


def girar_ruleta():
    print("\n🎡 --- Ruleta de Descuentos --- 🎡")
    ruleta = RuletaDescuento()
    resultado = ruleta.girar()
    print(resultado)


menu()
