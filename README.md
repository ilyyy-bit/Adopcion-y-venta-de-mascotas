
# Adopet — Prototipo solo Python + TXT

Prototipo de escritorio sin DB ni APIs. Persistencia en `.txt` con JSON Lines. Incluye dataclasses, herencia, polimorfismo y GUI con pestañas: Personas, Mascotas, Registros, Banners y Alianzas.

## Requisitos
- Python 3.10+
- Opcional: Pillow para mejores imágenes
  ```bash
  pip install pillow
  ```

## Estructura
- `app/domain`: entidades del dominio
- `app/persistence`: lectura/escritura JSONL
- `app/repositories`: CRUD basado en archivos
- `app/services`: reglas de negocio (Plataforma)
- `app/ui/tk`: interfaz Tkinter
- `data/*.txt`: almacenamiento

## Ejecutar
CLI mínima:
```bash
python -m app.main
```
GUI:
```bash
python -m app.main_gui
```

## Flujo en la GUI
1. Personas: crea una persona.
2. Mascotas: registra adopción o venta; adjunta ruta de imagen si quieres preview.
3. Registros: selecciona persona y mascota; en venta se exige monto y se prellena si la mascota tiene precio.
4. Banners: crea promocionales o de animal. Si es ANIMAL y no seleccionas imagen, usa la imagen de la mascota destacada.
5. Alianzas: crea, actualiza y elimina con tipo y % de comisión.

## Actualización automática
- Al crear una **mascota** se refrescan los combos en **Registros** y **Banners**.
- Al crear un **registro** se actualizan: lista de mascotas, combos de Registros y Banners.
- Al crear una **persona** se refrescan los combos en **Registros**.

## Eliminaciones
- Banners y Alianzas incluyen botones de **Eliminar**. Internamente se reescribe el archivo JSONL dejando fuera el elemento.

## Notas de imágenes
- Con Pillow: JPG/JPEG/PNG/WEBP/BMP/GIF con reescalado de alta calidad.
- Sin Pillow: usa PNG/GIF o instala Pillow.

## Windows
- Ejecuta desde la carpeta del proyecto:
  ```bat
  python -m app.main_gui
  ```
- Si Tk no carga fuentes, cambia a Arial dentro de `_apply_theme`.

## Formato de datos
Una entidad por línea en `data/*`. Ejemplo:
```json
{"type":"Persona","id":"...","nombre":"Ana","identificacion":"123"}
```

## Licencia
Uso educativo y prototipos.
