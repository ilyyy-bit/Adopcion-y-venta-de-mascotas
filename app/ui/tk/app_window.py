
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from app.services.plataforma import Plataforma
from app.domain.base_types import TipoProceso, TipoAlianza, TipoBanner
from app.domain.mascota_venta import MascotaEnVenta
from app.utils.images import load_image_for_tk
_PAD = 8
def _apply_theme(root: tk.Tk):
    from tkinter import font as tkfont
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    try:
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)
    except Exception:
        pass
    style.configure(".", font=("Segoe UI", 10))
    style.configure("TFrame", padding=_PAD)
    style.configure("TLabel", padding=2)
    style.configure("TButton", padding=6, font=("Segoe UI", 10, "bold"))
    style.configure("TEntry", padding=2)
    style.configure("Treeview", rowheight=24)
    root.configure(bg="#f7f7f7")
class PersonasTab(ttk.Frame):
    def __init__(self, master, plataforma: Plataforma, on_personas_changed=None):
        super().__init__(master)
        self.plataforma = plataforma
        self.on_personas_changed = on_personas_changed
        self._build()
    def _build(self):
        form = ttk.Labelframe(self, text="Registrar Persona")
        form.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, _PAD))
        form.columnconfigure(1, weight=1)
        self.var_nombre = tk.StringVar(); self.var_ident = tk.StringVar()
        self.var_tel = tk.StringVar(); self.var_email = tk.StringVar()
        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew")
        ttk.Label(form, text="Identificación").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_ident).grid(row=0, column=3, sticky="ew")
        ttk.Label(form, text="Teléfono").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_tel).grid(row=1, column=1, sticky="ew")
        ttk.Label(form, text="Email").grid(row=1, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_email).grid(row=1, column=3, sticky="ew")
        ttk.Button(form, text="Registrar", command=self._registrar).grid(row=2, column=0, columnspan=4, sticky="e", pady=6)
        table_frame = ttk.Labelframe(self, text="Personas")
        table_frame.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1); self.rowconfigure(1, weight=1)
        columns = ("id", "nombre", "ident", "tel", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for c, t in zip(columns, ["ID", "Nombre", "Identificación", "Teléfono", "Email"]):
            self.tree.heading(c, text=t); self.tree.column(c, width=140 if c=="id" else 120, anchor="w")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set); self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_frame.columnconfigure(0, weight=1); table_frame.rowconfigure(0, weight=1)
        btns = ttk.Frame(self); btns.grid(row=2, column=0, sticky="e", pady=(6,0))
        ttk.Button(btns, text="Refrescar", command=self._load).grid(row=0, column=0, padx=4)
        self._load()
    def _registrar(self):
        try:
            p = self.plataforma.registrar_persona(self.var_nombre.get().strip(), self.var_ident.get().strip(), self.var_tel.get().strip(), self.var_email.get().strip())
            messagebox.showinfo("OK", f"Persona registrada: {p.nombre}"); self._clear_form(); self._load()
            if self.on_personas_changed: self.on_personas_changed()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _clear_form(self):
        self.var_nombre.set(""); self.var_ident.set(""); self.var_tel.set(""); self.var_email.set("")
    def _load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in self.plataforma.personas.list_all():
            self.tree.insert("", "end", values=(p.id, p.nombre, p.identificacion, p.telefono or "", p.email or ""))
class MascotasTab(ttk.Frame):
    def __init__(self, master, plataforma: Plataforma, on_mascotas_changed=None):
        super().__init__(master)
        self.plataforma = plataforma
        self.on_mascotas_changed = on_mascotas_changed
        self._img_ref = None
        self._build()
    def _build(self):
        form = ttk.Labelframe(self, text="Registrar Mascota")
        form.grid(row=0, column=0, sticky="ew", pady=(0, _PAD))
        for col in range(0, 7): form.columnconfigure(col, weight=1)
        self.var_tipo = tk.StringVar(value="ADOPCION")
        self.var_nombre = tk.StringVar(); self.var_especie = tk.StringVar(); self.var_edad = tk.StringVar()
        self.var_raza = tk.StringVar(); self.var_salud = tk.StringVar(); self.var_precio = tk.StringVar(); self.var_imagen = tk.StringVar()
        ttk.Radiobutton(form, text="Adopción", variable=self.var_tipo, value="ADOPCION", command=self._toggle_precio).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(form, text="Venta",    variable=self.var_tipo, value="VENTA",    command=self._toggle_precio).grid(row=0, column=1, sticky="w")
        ttk.Label(form, text="Nombre").grid(row=1, column=0, sticky="w"); ttk.Entry(form, textvariable=self.var_nombre).grid(row=1, column=1, sticky="ew")
        ttk.Label(form, text="Especie").grid(row=1, column=2, sticky="w"); ttk.Entry(form, textvariable=self.var_especie).grid(row=1, column=3, sticky="ew")
        ttk.Label(form, text="Edad").grid(row=1, column=4, sticky="w"); ttk.Entry(form, textvariable=self.var_edad).grid(row=1, column=5, sticky="ew")
        ttk.Label(form, text="Raza").grid(row=2, column=0, sticky="w"); ttk.Entry(form, textvariable=self.var_raza).grid(row=2, column=1, sticky="ew")
        ttk.Label(form, text="Salud").grid(row=2, column=2, sticky="w"); ttk.Entry(form, textvariable=self.var_salud).grid(row=2, column=3, sticky="ew")
        ttk.Label(form, text="Precio").grid(row=2, column=4, sticky="w"); self.ent_precio = ttk.Entry(form, textvariable=self.var_precio); self.ent_precio.grid(row=2, column=5, sticky="ew")
        ttk.Label(form, text="Imagen (ruta)").grid(row=3, column=0, sticky="w")
        ent_img = ttk.Entry(form, textvariable=self.var_imagen); ent_img.grid(row=3, column=1, columnspan=3, sticky="ew")
        ttk.Button(form, text="Examinar...", command=self._browse_img).grid(row=3, column=4, sticky="w")
        ttk.Button(form, text="Registrar", command=self._registrar).grid(row=3, column=5, sticky="e", pady=6)
        prev = ttk.Labelframe(self, text="Preview"); prev.grid(row=0, column=1, sticky="nsew", padx=(8,0), pady=(0,_PAD))
        self.preview_lbl = ttk.Label(prev, text="(sin imagen)"); self.preview_lbl.pack(fill="both", expand=True, padx=6, pady=6)
        self.columnconfigure(0, weight=3); self.columnconfigure(1, weight=2)
        table = ttk.Labelframe(self, text="Mascotas")
        table.grid(row=1, column=0, columnspan=2, sticky="nsew"); self.rowconfigure(1, weight=1)
        cols = ("id","tipo","nombre","especie","edad","raza","salud","precio")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=10)
        headers = ["ID","Tipo","Nombre","Especie","Edad","Raza","Salud","Precio"]
        for c, t in zip(cols, headers): self.tree.heading(c, text=t); self.tree.column(c, width=120 if c!="id" else 140, anchor="w")
        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); vsb.grid(row=0, column=1, sticky="ns")
        table.columnconfigure(0, weight=1); table.rowconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self._on_select_tree)
        btns = ttk.Frame(self); btns.grid(row=2, column=0, columnspan=2, sticky="e", pady=(6,0))
        ttk.Button(btns, text="Refrescar", command=self._load).grid(row=0, column=0, padx=4)
        self._toggle_precio(); self._load()
    def _browse_img(self):
        path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp"),("Todos","*.*")])
        if path:
            self.var_imagen.set(path); self._update_preview(path)
    def _update_preview(self, path: str | None):
        if not path:
            self.preview_lbl.configure(text="(sin imagen)", image=""); self._img_ref = None; return
        img = load_image_for_tk(path, (360,240))
        if img is None:
            self.preview_lbl.configure(text="(no se pudo cargar la imagen)", image=""); self._img_ref = None
        else:
            self.preview_lbl.configure(image=img, text=""); self._img_ref = img
    def _on_select_tree(self, *_):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0]); mid = item["values"][0]
        m = self.plataforma.mascotas.get(mid)
        self._update_preview(getattr(m, "imagen_path", None))
    def _toggle_precio(self):
        is_venta = self.var_tipo.get() == "VENTA"
        self.ent_precio.configure(state="normal" if is_venta else "disabled")
        if not is_venta: self.var_precio.set("")
    def _registrar(self):
        try:
            if self.var_tipo.get() == "ADOPCION":
                self.plataforma.registrar_mascota_adopcion(self.var_nombre.get(), self.var_especie.get(), int(self.var_edad.get() or 0), self.var_raza.get(), self.var_salud.get(), self.var_imagen.get() or None)
            else:
                self.plataforma.registrar_mascota_venta(self.var_nombre.get(), self.var_especie.get(), int(self.var_edad.get() or 0), self.var_raza.get(), self.var_salud.get(), float(self.var_precio.get()), self.var_imagen.get() or None)
            messagebox.showinfo("OK", "Mascota registrada"); self._clear_form(); self._load(); self._update_preview(None)
            if self.on_mascotas_changed: self.on_mascotas_changed()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _clear_form(self):
        self.var_nombre.set(""); self.var_especie.set(""); self.var_edad.set(""); self.var_raza.set(""); self.var_salud.set(""); self.var_precio.set(""); self.var_imagen.set("")
    def _load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for m in self.plataforma.listar_mascotas_todas():
            tipo = "VENTA" if isinstance(m, MascotaEnVenta) else "ADOPCION"
            precio = f"{getattr(m,'precio',0):,.0f}" if tipo=="VENTA" else ""
            self.tree.insert("", "end", values=(m.id, tipo, m.nombre, m.especie, m.edad, m.raza, m.estado_salud, precio))
class RegistrosTab(ttk.Frame):
    def __init__(self, master, plataforma: Plataforma, on_after_create=None):
        super().__init__(master); self.plataforma = plataforma; self.on_after_create = on_after_create; self._build()
    def _build(self):
        form = ttk.Labelframe(self, text="Crear Registro")
        form.grid(row=0, column=0, sticky="ew", pady=(0, _PAD))
        for c in range(0,6): form.columnconfigure(c, weight=1)
        self.var_tipo = tk.StringVar(value="ADOPCION")
        ttk.Radiobutton(form, text="Adopción", variable=self.var_tipo, value="ADOPCION", command=self._toggle_monto).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(form, text="Venta",    variable=self.var_tipo, value="VENTA",    command=self._toggle_monto).grid(row=0, column=1, sticky="w")
        ttk.Label(form, text="Persona").grid(row=1, column=0, sticky="w"); self.cb_persona = ttk.Combobox(form, state="readonly"); self.cb_persona.grid(row=1, column=1, columnspan=2, sticky="ew")
        ttk.Label(form, text="Mascota").grid(row=1, column=3, sticky="w"); self.cb_mascota = ttk.Combobox(form, state="readonly"); self.cb_mascota.grid(row=1, column=4, columnspan=2, sticky="ew")
        self.cb_mascota.bind("<<ComboboxSelected>>", self._prefill_monto)
        ttk.Label(form, text="Monto").grid(row=2, column=0, sticky="w"); self.var_monto = tk.StringVar(); self.ent_monto = ttk.Entry(form, textvariable=self.var_monto); self.ent_monto.grid(row=2, column=1, sticky="ew")
        ttk.Button(form, text="Crear", command=self._crear).grid(row=2, column=5, sticky="e", pady=6)
        table = ttk.Labelframe(self, text="Registros"); table.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1); self.rowconfigure(1, weight=1)
        cols = ("id","fecha","tipo","persona","mascota","monto")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=10)
        headers = ["ID","Fecha","Tipo","Persona","Mascota","Monto"]
        for c, t in zip(cols, headers): self.tree.heading(c, text=t); self.tree.column(c, width=120 if c not in ("id","monto") else 140, anchor="w")
        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); vsb.grid(row=0, column=1, sticky="ns")
        table.columnconfigure(0, weight=1); table.rowconfigure(0, weight=1)
        btns = ttk.Frame(self); btns.grid(row=2, column=0, sticky="e", pady=(6,0))
        ttk.Button(btns, text="Refrescar", command=self._load).grid(row=0, column=0, padx=4)
        self._reload_combos(); self._toggle_monto(); self._load()
    def _toggle_monto(self):
        is_venta = self.var_tipo.get() == "VENTA"
        self.ent_monto.configure(state="normal" if is_venta else "disabled")
        if not is_venta: self.var_monto.set("")
    def _reload_combos(self):
        self._personas = self.plataforma.personas.list_all()
        self._mascotas = self.plataforma.mascotas.list_disponibles()
        self.cb_persona["values"] = [f"{p.nombre} — {p.identificacion} | {p.id}" for p in self._personas]
        self.cb_mascota["values"] = [f"{m.mostrar_datos()} | {m.id}" for m in self._mascotas]
        if self._personas: self.cb_persona.current(0)
        else: self.cb_persona.set("")
        if self._mascotas: self.cb_mascota.current(0)
        else: self.cb_mascota.set("")
    def _prefill_monto(self, *_):
        try:
            if self.var_tipo.get() != "VENTA": return
            idx = self.cb_mascota.current()
            if idx < 0: return
            from app.domain.mascota_venta import MascotaEnVenta
            m = self._mascotas[idx]
            if isinstance(m, MascotaEnVenta): self.var_monto.set(str(getattr(m, "precio", 0)))
        except Exception: pass
    def _crear(self):
        try:
            if not self._personas or not self._mascotas:
                messagebox.showwarning("Atención", "Debes tener al menos 1 persona y 1 mascota"); return
            p_idx = self.cb_persona.current(); m_idx = self.cb_mascota.current()
            if p_idx < 0 or m_idx < 0: messagebox.showwarning("Atención", "Selecciona persona y mascota"); return
            p = self._personas[p_idx]; m = self._mascotas[m_idx]; tipo = TipoProceso[self.var_tipo.get()]
            monto = float(self.var_monto.get()) if tipo == TipoProceso.VENTA else None
            self.plataforma.crear_registro(tipo, p.id, m.id, monto); messagebox.showinfo("OK", "Registro creado")
            self._reload_combos(); self._load()
            if self.on_after_create: self.on_after_create()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.plataforma.listar_registros():
            self.tree.insert("", "end", values=(r.id, r.fecha, r.tipo.name, r.persona_id, r.mascota_id, r.monto if r.monto is not None else ""))
class BannersTab(ttk.Frame):
    def __init__(self, master, plataforma: Plataforma):
        super().__init__(master); self.plataforma = plataforma; self._img_ref = None; self._build()
    def _build(self):
        form = ttk.Labelframe(self, text="Banners")
        form.grid(row=0, column=0, sticky="ew", pady=(0, _PAD))
        for c in range(0,6): form.columnconfigure(c, weight=1)
        self.var_tipo = tk.StringVar(value="PROMOCIONAL"); self.var_texto = tk.StringVar(); self.var_imagen = tk.StringVar()
        self.var_inicio = tk.StringVar(); self.var_fin = tk.StringVar(); self.var_activo = tk.BooleanVar(value=False)
        ttk.Radiobutton(form, text="Promocional", variable=self.var_tipo, value="PROMOCIONAL", command=self._toggle_mascota).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(form, text="Animal",      variable=self.var_tipo, value="ANIMAL",       command=self._toggle_mascota).grid(row=0, column=1, sticky="w")
        ttk.Label(form, text="Texto").grid(row=1, column=0, sticky="w"); ttk.Entry(form, textvariable=self.var_texto).grid(row=1, column=1, columnspan=4, sticky="ew")
        ttk.Checkbutton(form, text="Activo", variable=self.var_activo).grid(row=1, column=5, sticky="e")
        ttk.Label(form, text="Imagen").grid(row=2, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_imagen).grid(row=2, column=1, columnspan=3, sticky="ew")
        ttk.Button(form, text="Examinar...", command=self._browse_img).grid(row=2, column=4, sticky="w")
        ttk.Label(form, text="Inicio YYYY-MM-DD").grid(row=3, column=0, sticky="w"); ttk.Entry(form, textvariable=self.var_inicio).grid(row=3, column=1, sticky="ew")
        ttk.Label(form, text="Fin YYYY-MM-DD").grid(row=3, column=2, sticky="w"); ttk.Entry(form, textvariable=self.var_fin).grid(row=3, column=3, sticky="ew")
        ttk.Label(form, text="Mascota destacada").grid(row=4, column=0, sticky="w"); self.cb_mascota = ttk.Combobox(form, state="readonly"); self.cb_mascota.grid(row=4, column=1, columnspan=2, sticky="ew")
        ttk.Button(form, text="Crear", command=self._crear).grid(row=4, column=5, sticky="e", pady=6)
        prev = ttk.Labelframe(self, text="Preview"); prev.grid(row=0, column=1, sticky="nsew", padx=(8,0))
        self.preview_lbl = ttk.Label(prev, text="(sin imagen)"); self.preview_lbl.pack(fill="both", expand=True, padx=6, pady=6)
        self.columnconfigure(0, weight=3); self.columnconfigure(1, weight=2)
        table = ttk.Labelframe(self, text="Banners"); table.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.rowconfigure(1, weight=1)
        cols = ("id","tipo","activo","inicio","fin","texto","destacado")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=10)
        headers = ["ID","Tipo","Activo","Inicio","Fin","Texto","Mascota"]
        widths = [140,80,60,100,100,260,140]
        for c, t, w in zip(cols, headers, widths): self.tree.heading(c, text=t); self.tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); vsb.grid(row=0, column=1, sticky="ns")
        table.columnconfigure(0, weight=1); table.rowconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self._on_select_tree)
        btns = ttk.Frame(self); btns.grid(row=2, column=0, columnspan=2, sticky="e", pady=(6,0))
        ttk.Button(btns, text="Refrescar", command=self._load).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Activar", command=lambda: self._set_active(True)).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Desactivar", command=lambda: self._set_active(False)).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Eliminar", command=self._delete).grid(row=0, column=3, padx=4)
        self.reload_sources(); self._toggle_mascota(); self._load()
    def reload_sources(self):
        ms = self.plataforma.mascotas.list_all()
        self._mascotas = ms
        self.cb_mascota["values"] = [f"{m.nombre} • {m.especie} • {m.id}" for m in ms]
        if ms: self.cb_mascota.current(0)
        else: self.cb_mascota.set("")
    def _toggle_mascota(self):
        self.cb_mascota.configure(state=("readonly" if self.var_tipo.get()=="ANIMAL" else "disabled"))
    def _browse_img(self):
        path = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp"),("Todos","*.*")])
        if path: self.var_imagen.set(path); self._update_preview()
    def _update_preview(self):
        path = self.var_imagen.get().strip() or None
        if not path and self.var_tipo.get()=="ANIMAL":
            idx = self.cb_mascota.current()
            if idx >= 0 and idx < len(self._mascotas):
                path = getattr(self._mascotas[idx], "imagen_path", None)
        if not path:
            self.preview_lbl.configure(text="(sin imagen)", image=""); self._img_ref = None; return
        img = load_image_for_tk(path, (360,240))
        if img is None:
            self.preview_lbl.configure(text="(no se pudo cargar)", image=""); self._img_ref = None
        else:
            self.preview_lbl.configure(image=img, text=""); self._img_ref = img
    def _crear(self):
        try:
            tipo = TipoBanner[self.var_tipo.get()]
            texto = self.var_texto.get().strip()
            inicio = self.var_inicio.get().strip() or None
            fin = self.var_fin.get().strip() or None
            activo = bool(self.var_activo.get())
            imagen = self.var_imagen.get().strip() or None
            destacado_id = None
            if tipo.name == "ANIMAL":
                idx = self.cb_mascota.current()
                if idx >= 0 and idx < len(self._mascotas): destacado_id = self._mascotas[idx].id
            self.plataforma.crear_banner(tipo, texto, imagen, inicio, fin, activo, destacado_id)
            messagebox.showinfo("OK", "Banner creado"); self._clear_form(); self._load(); self._update_preview()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _clear_form(self):
        self.var_texto.set(""); self.var_imagen.set(""); self.var_inicio.set(""); self.var_fin.set(""); self.var_activo.set(False); self.var_tipo.set("PROMOCIONAL"); self._toggle_mascota()
    def _on_select_tree(self, *_):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel[0])
        self.var_tipo.set(item["values"][1]); self.var_activo.set(bool(item["values"][2])); self.var_inicio.set(str(item["values"][3] or ""))
        self.var_fin.set(str(item["values"][4] or "")); self.var_texto.set(str(item["values"][5] or ""))
        dest = item["values"][6] or ""
        if self.var_tipo.get()=="ANIMAL" and dest:
            for i, m in enumerate(self._mascotas):
                if m.id == dest: self.cb_mascota.current(i); break
        self._update_preview()
    def _selected_banner_id(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])["values"][0]
    def _set_active(self, state: bool):
        try:
            bid = self._selected_banner_id()
            if not bid: messagebox.showwarning("Atención","Selecciona un banner"); return
            banners = self.plataforma.banners.list_all()
            b = next((x for x in banners if x.id == bid), None)
            if not b: messagebox.showerror("Error","Banner no encontrado"); return
            if state: self.plataforma.activar_banner(b)
            else: self.plataforma.desactivar_banner(b)
            self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _delete(self):
        try:
            bid = self._selected_banner_id()
            if not bid: messagebox.showwarning("Atención","Selecciona un banner"); return
            if messagebox.askyesno("Confirmar","¿Eliminar banner?"):
                self.plataforma.eliminar_banner(bid); self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for b in self.plataforma.banners.list_all():
            self.tree.insert("", "end", values=(b.id, b.tipo.name, b.activo, b.inicio or "", b.fin or "", b.texto or "", b.destacado_mascota_id or ""))
class AlianzasTab(ttk.Frame):
    def __init__(self, master, plataforma: Plataforma):
        super().__init__(master); self.plataforma = plataforma; self._build()
    def _build(self):
        form = ttk.Labelframe(self, text="Alianzas")
        form.grid(row=0, column=0, sticky="ew", pady=(0, _PAD))
        for c in range(0,5): form.columnconfigure(c, weight=1)
        self.var_nombre = tk.StringVar(); self.var_tipo = tk.StringVar(value="CRIADERO"); self.var_comision = tk.StringVar()
        ttk.Label(form, text="Nombre").grid(row=0, column=0, sticky="w"); ttk.Entry(form, textvariable=self.var_nombre).grid(row=0, column=1, sticky="ew")
        ttk.Label(form, text="Tipo").grid(row=0, column=2, sticky="w"); self.cb_tipo = ttk.Combobox(form, state="readonly", values=["CRIADERO","ALBERGUE"], textvariable=self.var_tipo); self.cb_tipo.grid(row=0, column=3, sticky="ew")
        ttk.Label(form, text="Comisión %").grid(row=0, column=4, sticky="w"); ttk.Entry(form, textvariable=self.var_comision).grid(row=0, column=5, sticky="ew")
        ttk.Button(form, text="Crear", command=self._crear).grid(row=0, column=6, sticky="e")
        ttk.Button(form, text="Actualizar", command=self._actualizar).grid(row=0, column=7, sticky="e")
        ttk.Button(form, text="Eliminar", command=self._eliminar).grid(row=0, column=8, sticky="e")
        table = ttk.Labelframe(self, text="Listado"); table.grid(row=1, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1); self.rowconfigure(1, weight=1)
        cols = ("id","nombre","tipo","comision")
        self.tree = ttk.Treeview(table, columns=cols, show="headings", height=10)
        for c, t, w in zip(cols, ["ID","Nombre","Tipo","Comisión %"], [160,200,140,120]):
            self.tree.heading(c, text=t); self.tree.column(c, width=w, anchor="w")
        vsb = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew"); vsb.grid(row=0, column=1, sticky="ns")
        table.columnconfigure(0, weight=1); table.rowconfigure(0, weight=1)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        btns = ttk.Frame(self); btns.grid(row=2, column=0, sticky="e", pady=(6,0))
        ttk.Button(btns, text="Refrescar", command=self._load).grid(row=0, column=0, padx=4)
        self._load()
    def _selected_id(self):
        sel = self.tree.selection()
        if not sel: return None
        return self.tree.item(sel[0])["values"][0]
    def _on_select(self, *_):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0])["values"]
        self.var_nombre.set(v[1])
        self.var_tipo.set(v[2])
        self.var_comision.set(str(v[3]))
    def _crear(self):
        try:
            nombre = self.var_nombre.get().strip()
            from app.domain.base_types import TipoAlianza
            tipo = TipoAlianza[self.var_tipo.get()]
            comision = float(self.var_comision.get())
            self.plataforma.registrar_alianza(nombre, tipo, comision)
            messagebox.showinfo("OK", "Alianza creada"); self._clear(); self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _actualizar(self):
        try:
            id_ = self._selected_id()
            if not id_: messagebox.showwarning("Atención","Selecciona una alianza"); return
            from app.domain.alianza import Alianza
            from app.domain.base_types import TipoAlianza
            a = Alianza(id=id_, nombre=self.var_nombre.get().strip(), tipo=TipoAlianza[self.var_tipo.get()], comision=float(self.var_comision.get()))
            self.plataforma.actualizar_alianza(a)
            messagebox.showinfo("OK", "Alianza actualizada"); self._clear(); self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _eliminar(self):
        try:
            id_ = self._selected_id()
            if not id_: messagebox.showwarning("Atención","Selecciona una alianza"); return
            if messagebox.askyesno("Confirmar","¿Eliminar alianza?"):
                self.plataforma.eliminar_alianza(id_); self._clear(); self._load()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _clear(self):
        self.var_nombre.set(""); self.var_tipo.set("CRIADERO"); self.var_comision.set("")
    def _load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for a in self.plataforma.alianzas.list_all():
            self.tree.insert("", "end", values=(a.id, a.nombre, a.tipo.name, a.comision))
class App(tk.Tk):
    def __init__(self, plataforma: Plataforma):
        super().__init__(); self.title("Adopet • Prototipo (Tkinter)"); self.geometry("1200x720"); _apply_theme(self)
        nb = ttk.Notebook(self); nb.pack(fill="both", expand=True)
        self.registros_tab = RegistrosTab(nb, plataforma, on_after_create=self._on_registro_created)
        self.banners_tab = BannersTab(nb, plataforma)
        self.mascotas_tab = MascotasTab(nb, plataforma, on_mascotas_changed=self._on_mascotas_changed)
        self.personas_tab = PersonasTab(nb, plataforma, on_personas_changed=self._on_personas_changed)
        self.alianzas_tab = AlianzasTab(nb, plataforma)
        nb.add(self.personas_tab, text="Personas")
        nb.add(self.mascotas_tab, text="Mascotas")
        nb.add(self.registros_tab, text="Registros")
        nb.add(self.banners_tab, text="Banners")
        nb.add(self.alianzas_tab, text="Alianzas")
    def _on_mascotas_changed(self):
        self.registros_tab._reload_combos()
        self.banners_tab.reload_sources()
    def _on_personas_changed(self):
        self.registros_tab._reload_combos()
    def _on_registro_created(self):
        self.mascotas_tab._load()
        self.registros_tab._reload_combos()
        self.banners_tab.reload_sources()
def run_gui(plataforma: Plataforma):
    app = App(plataforma); app.mainloop()
