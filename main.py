#!/usr/bin/env python3
import customtkinter as ctk
import tkinter as tk

# ── Rasterização ──────────────────────────────────────────────────────────────
from algorithms.dda import execute_dda
from algorithms.bresenham_reta import execute_bresenham_reta
from algorithms.bresenham_circulo import execute_bresenham_circulo

# ── Recorte ───────────────────────────────────────────────────────────────────
from algorithms.cohen_sutherland import execute_cohen_sutherland
from algorithms.liang_barsky import execute_liang_barsky

# ── Transformações ────────────────────────────────────────────────────────────
from transformations.translacao import execute_translacao
from transformations.rotacao import execute_rotacao
from transformations.escala import execute_escala
from transformations.reflexao import execute_reflexao

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Modos do canvas ───────────────────────────────────────────────────────────
MODE_DRAW_LINE    = "draw_line"
MODE_DRAW_CIRCLE  = "draw_circle"
MODE_DRAW_POLYGON = "draw_polygon"
MODE_CLIP_DEFINE  = "clip_define"
MODE_SELECT       = "select"


class PaintApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Desenho CG — Algoritmos de Traçado")
        self.geometry("1100x700")
        self.minsize(950, 620)

        # ── Paleta ────────────────────────────────────────────────────────────
        self.bg_color     = "#1E1E1E"
        self.grid_color   = "#333333"
        self.marker_color = "#E06C75"
        self.line_color   = "#61AFEF"
        self.clip_color   = "#E5C07B"
        self.select_color = "#98C379"
        self.poly_color   = "#C678DD"

        # ── Estado do canvas ──────────────────────────────────────────────────
        self.mode          = MODE_DRAW_LINE
        self.points        = []        # pontos coletados no modo atual
        self.clip_window   = None      # (xmin, ymin, xmax, ymax)
        self.drag_start    = None
        self.drag_rect_id  = None
        self.selected_items = []       # IDs de itens do canvas selecionados

        # ── Cena (modelo de dados) ────────────────────────────────────────────
        # Cada primitivo: {'id', 'type', 'points', 'algo', 'tag', 'color'}
        self.scene    = []
        self._prim_id = 0

        # ── Variáveis de controle ─────────────────────────────────────────────
        self.raster_algo = tk.StringVar(value="DDA")
        self.clip_algo   = tk.StringVar(value="Cohen-Sutherland")
        self.reflex_eixo = tk.StringVar(value="X")

        self.setup_ui()
        self.draw_grid()

    # ══════════════════════════════════════════════════════════════════════════
    # INTERFACE
    # ══════════════════════════════════════════════════════════════════════════

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self._build_sidebar()
        self._build_canvas_area()
        self._build_status_bar()

    def _build_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.sidebar_frame, text="Ferramentas",
            font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10))

        self.tabview = ctk.CTkTabview(
            self.sidebar_frame, width=230,
            command=self._on_tab_change
        )
        self.tabview.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self.tabview.add("Rasterização")
        self.tabview.add("Recorte")
        self.tabview.add("Transformações")

        self._build_tab_rasterizacao()
        self._build_tab_recorte()
        self._build_tab_transformacoes()

        self.clear_btn = ctk.CTkButton(
            self.sidebar_frame, text="Limpar Tela",
            fg_color="#C23B22", hover_color="#8F2A19",
            command=self.clear_canvas, font=ctk.CTkFont(weight="bold")
        )
        self.clear_btn.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="ew")

    # ── Aba Rasterização ──────────────────────────────────────────────────────

    def _build_tab_rasterizacao(self):
        tab = self.tabview.tab("Rasterização")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Algoritmo:", font=ctk.CTkFont(size=13, weight="bold")
                     ).grid(row=0, column=0, sticky="w", pady=(8, 4), padx=4)

        opcoes = [
            ("DDA",                 MODE_DRAW_LINE,    "DDA"),
            ("Bresenham (Reta)",    MODE_DRAW_LINE,    "Bresenham (Reta)"),
            ("Bresenham (Círculo)", MODE_DRAW_CIRCLE,  "Bresenham (Círculo)"),
            ("Polígono",            MODE_DRAW_POLYGON, "Polígono"),
        ]
        self._raster_btns = {}
        for i, (label, mode, val) in enumerate(opcoes):
            btn = ctk.CTkButton(
                tab, text=label,
                font=ctk.CTkFont(size=13),
                fg_color="#2B5BA0" if val == "DDA" else "#2E2E2E",
                hover_color="#1E4A8A",
                border_width=0,
                command=lambda m=mode, v=val: self._on_raster_algo_change(m, v)
            )
            btn.grid(row=i + 1, column=0, sticky="ew", padx=10, pady=3)
            self._raster_btns[val] = btn

        ctk.CTkFrame(tab, height=1, fg_color="#444444").grid(
            row=5, column=0, sticky="ew", padx=6, pady=8)

        self.btn_close_polygon = ctk.CTkButton(
            tab, text="Fechar Polígono", command=self.close_polygon,
            font=ctk.CTkFont(size=12), state="disabled",
            fg_color="#6B3FA0", hover_color="#4A2870"
        )
        self.btn_close_polygon.grid(row=6, column=0, padx=10, pady=(0, 6), sticky="ew")

        ctk.CTkFrame(tab, height=1, fg_color="#444444").grid(
            row=7, column=0, sticky="ew", padx=6, pady=6)

        self.input_frame = ctk.CTkFrame(tab, fg_color="transparent")
        self.input_frame.grid(row=8, column=0, padx=6, pady=0, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.input_frame, text="Ponto 1:",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 3))
        self.entry_x1 = ctk.CTkEntry(self.input_frame, placeholder_text="X1", width=75)
        self.entry_x1.grid(row=1, column=0, padx=(0, 4), pady=(0, 8))
        self.entry_y1 = ctk.CTkEntry(self.input_frame, placeholder_text="Y1", width=75)
        self.entry_y1.grid(row=1, column=1, padx=(4, 0), pady=(0, 8))

        ctk.CTkLabel(self.input_frame, text="Ponto 2:",
                     font=ctk.CTkFont(size=12, weight="bold")
                     ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 3))
        self.entry_x2 = ctk.CTkEntry(self.input_frame, placeholder_text="X2", width=75)
        self.entry_x2.grid(row=3, column=0, padx=(0, 4), pady=(0, 8))
        self.entry_y2 = ctk.CTkEntry(self.input_frame, placeholder_text="Y2", width=75)
        self.entry_y2.grid(row=3, column=1, padx=(4, 0), pady=(0, 8))

        self.btn_draw_manual = ctk.CTkButton(
            tab, text="Traçar Manual", command=self.on_manual_draw,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_draw_manual.grid(row=9, column=0, padx=10, pady=(2, 10), sticky="ew")

    # ── Aba Recorte ───────────────────────────────────────────────────────────

    def _build_tab_recorte(self):
        tab = self.tabview.tab("Recorte")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="Algoritmo:", font=ctk.CTkFont(size=13, weight="bold")
                     ).grid(row=0, column=0, sticky="w", padx=4, pady=(8, 4))
        self.seg_clip_algo = ctk.CTkSegmentedButton(
            tab,
            values=["Cohen-Sutherland", "Liang-Barsky"],
            variable=self.clip_algo,
            font=ctk.CTkFont(size=12),
            selected_color="#1A5276",
            selected_hover_color="#154360",
            unselected_color="#2E2E2E",
            unselected_hover_color="#3A3A3A",
        )
        self.seg_clip_algo.grid(row=1, column=0, padx=10, pady=(4, 8), sticky="ew")

        ctk.CTkFrame(tab, height=1, fg_color="#444444").grid(
            row=3, column=0, sticky="ew", padx=6, pady=8)

        ctk.CTkLabel(tab, text="Janela de Recorte:",
                     font=ctk.CTkFont(size=13, weight="bold")
                     ).grid(row=4, column=0, sticky="w", padx=4, pady=(0, 6))

        grid = ctk.CTkFrame(tab, fg_color="transparent")
        grid.grid(row=5, column=0, padx=6, sticky="ew")
        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)

        for col, lbl in enumerate(["Xmín", "Ymín"]):
            ctk.CTkLabel(grid, text=lbl, font=ctk.CTkFont(size=11),
                         text_color="gray60").grid(row=0, column=col, pady=(0, 2))
        self.entry_clip_xmin = ctk.CTkEntry(grid, placeholder_text="0", width=75)
        self.entry_clip_xmin.grid(row=1, column=0, padx=(0, 4), pady=(0, 8))
        self.entry_clip_ymin = ctk.CTkEntry(grid, placeholder_text="0", width=75)
        self.entry_clip_ymin.grid(row=1, column=1, padx=(4, 0), pady=(0, 8))

        for col, lbl in enumerate(["Xmáx", "Ymáx"]):
            ctk.CTkLabel(grid, text=lbl, font=ctk.CTkFont(size=11),
                         text_color="gray60").grid(row=2, column=col, pady=(0, 2))
        self.entry_clip_xmax = ctk.CTkEntry(grid, placeholder_text="400", width=75)
        self.entry_clip_xmax.grid(row=3, column=0, padx=(0, 4), pady=(0, 8))
        self.entry_clip_ymax = ctk.CTkEntry(grid, placeholder_text="300", width=75)
        self.entry_clip_ymax.grid(row=3, column=1, padx=(4, 0), pady=(0, 8))

        ctk.CTkButton(tab, text="Mostrar Janela Manualmente",
                      command=self.draw_clip_window, font=ctk.CTkFont(size=12),
                      fg_color="#3A4A2A", hover_color="#28361E"
                      ).grid(row=6, column=0, padx=10, pady=(2, 4), sticky="ew")

        ctk.CTkFrame(tab, height=1, fg_color="#555555").grid(
            row=7, column=0, sticky="ew", padx=6, pady=4)

        ctk.CTkButton(tab, text="Definir no Canvas",
                      command=self.on_define_clip_mode, font=ctk.CTkFont(size=12),
                      fg_color="#5A5A00", hover_color="#3A3A00"
                      ).grid(row=8, column=0, padx=10, pady=(4, 5), sticky="ew")

        ctk.CTkFrame(tab, height=1, fg_color="#444444").grid(
            row=9, column=0, sticky="ew", padx=6, pady=8)

        ctk.CTkButton(tab, text="Aplicar Recorte",
                      command=self.on_apply_clip, font=ctk.CTkFont(weight="bold"),
                      fg_color="#1A5276", hover_color="#154360"
                      ).grid(row=10, column=0, padx=10, pady=(0, 5), sticky="ew")

        ctk.CTkButton(tab, text="Remover Janela",
                      command=self.on_remove_clip, font=ctk.CTkFont(size=12),
                      fg_color="#5C3317", hover_color="#3D2210"
                      ).grid(row=11, column=0, padx=10, pady=(0, 10), sticky="ew")

    # ── Aba Transformações ────────────────────────────────────────────────────

    def _build_tab_transformacoes(self):
        tab = self.tabview.tab("Transformações")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(tab, text="Modo Seleção", command=self.on_select_mode,
                      font=ctk.CTkFont(size=12),
                      fg_color="#2E4A2E", hover_color="#1C301C"
                      ).grid(row=0, column=0, padx=10, pady=(10, 4), sticky="ew")

        self.lbl_selection = ctk.CTkLabel(
            tab, text="Nenhum objeto selecionado",
            font=ctk.CTkFont(size=11), text_color="gray50")
        self.lbl_selection.grid(row=1, column=0, padx=10, pady=(0, 6))

        # Translação
        self._section_header(tab, row=2, text="Translação")
        tr = ctk.CTkFrame(tab, fg_color="transparent")
        tr.grid(row=3, column=0, padx=10, pady=(2, 0), sticky="ew")
        tr.grid_columnconfigure(0, weight=1)
        tr.grid_columnconfigure(1, weight=1)
        for col, lbl in enumerate(["dx", "dy"]):
            ctk.CTkLabel(tr, text=lbl, font=ctk.CTkFont(size=11),
                         text_color="gray60").grid(row=0, column=col)
        self.entry_tr_dx = ctk.CTkEntry(tr, placeholder_text="0", width=75)
        self.entry_tr_dx.grid(row=1, column=0, padx=(0, 4), pady=(2, 6))
        self.entry_tr_dy = ctk.CTkEntry(tr, placeholder_text="0", width=75)
        self.entry_tr_dy.grid(row=1, column=1, padx=(4, 0), pady=(2, 6))
        ctk.CTkButton(tab, text="Aplicar Translação",
                      command=self.on_apply_translacao, font=ctk.CTkFont(size=12)
                      ).grid(row=4, column=0, padx=10, pady=(0, 6), sticky="ew")

        # Rotação
        self._section_header(tab, row=5, text="Rotação")
        ro = ctk.CTkFrame(tab, fg_color="transparent")
        ro.grid(row=6, column=0, padx=10, pady=(2, 0), sticky="ew")
        ro.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(ro, text="Ângulo (°)", font=ctk.CTkFont(size=11),
                     text_color="gray60").grid(row=0, column=0)
        self.entry_ro_angle = ctk.CTkEntry(ro, placeholder_text="0.0", width=75)
        self.entry_ro_angle.grid(row=1, column=0, pady=(2, 6))
        ctk.CTkButton(tab, text="Aplicar Rotação",
                      command=self.on_apply_rotacao, font=ctk.CTkFont(size=12)
                      ).grid(row=7, column=0, padx=10, pady=(0, 6), sticky="ew")

        # Escala
        self._section_header(tab, row=8, text="Escala")
        sc = ctk.CTkFrame(tab, fg_color="transparent")
        sc.grid(row=9, column=0, padx=10, pady=(2, 0), sticky="ew")
        sc.grid_columnconfigure(0, weight=1)
        sc.grid_columnconfigure(1, weight=1)
        for col, lbl in enumerate(["Sx", "Sy"]):
            ctk.CTkLabel(sc, text=lbl, font=ctk.CTkFont(size=11),
                         text_color="gray60").grid(row=0, column=col)
        self.entry_sc_sx = ctk.CTkEntry(sc, placeholder_text="1.0", width=75)
        self.entry_sc_sx.grid(row=1, column=0, padx=(0, 4), pady=(2, 6))
        self.entry_sc_sy = ctk.CTkEntry(sc, placeholder_text="1.0", width=75)
        self.entry_sc_sy.grid(row=1, column=1, padx=(4, 0), pady=(2, 6))
        ctk.CTkButton(tab, text="Aplicar Escala",
                      command=self.on_apply_escala, font=ctk.CTkFont(size=12)
                      ).grid(row=10, column=0, padx=10, pady=(0, 6), sticky="ew")

        # Reflexão
        self._section_header(tab, row=11, text="Reflexão")
        self.seg_reflex_eixo = ctk.CTkSegmentedButton(
            tab,
            values=["Eixo X", "Eixo Y", "Eixo XY"],
            font=ctk.CTkFont(size=12),
            selected_color="#1A5276",
            selected_hover_color="#154360",
            unselected_color="#2E2E2E",
            unselected_hover_color="#3A3A3A",
            command=lambda v: self.reflex_eixo.set(v.replace("Eixo ", ""))
        )
        self.seg_reflex_eixo.set("Eixo X")
        self.seg_reflex_eixo.grid(row=12, column=0, padx=10, pady=(4, 6), sticky="ew")
        ctk.CTkButton(tab, text="Aplicar Reflexão",
                      command=self.on_apply_reflexao, font=ctk.CTkFont(size=12)
                      ).grid(row=13, column=0, padx=10, pady=(0, 10), sticky="ew")

    def _section_header(self, parent, row, text):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=0, sticky="ew", padx=4, pady=(6, 0))
        f.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=text, font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#61AFEF").grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(f, height=1, fg_color="#3A3A3A").grid(
            row=1, column=0, sticky="ew", pady=(2, 4))

    def _build_canvas_area(self):
        self.canvas_container = ctk.CTkFrame(self, corner_radius=10)
        self.canvas_container.grid(row=0, column=1, padx=(16, 16),
                                   pady=(16, 8), sticky="nsew")
        self.canvas_container.pack_propagate(False)

        self.canvas = tk.Canvas(self.canvas_container, bg=self.bg_color,
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        self.canvas.bind("<Motion>",          self.on_mouse_move)
        self.canvas.bind("<Button-1>",        self.on_canvas_click)
        self.canvas.bind("<B1-Motion>",       self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Configure>",       self.on_canvas_resize)

    def _build_status_bar(self):
        self.status_frame = ctk.CTkFrame(self, height=30, corner_radius=5)
        self.status_frame.grid(row=1, column=1, padx=(16, 16),
                               pady=(0, 16), sticky="ew")
        self.status_frame.grid_propagate(False)
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_columnconfigure(1, weight=0)

        self.status_msg_lbl = ctk.CTkLabel(
            self.status_frame,
            text="Selecione um algoritmo e clique no canvas.",
            text_color="gray60", font=ctk.CTkFont(size=11))
        self.status_msg_lbl.grid(row=0, column=0, padx=10, sticky="w")

        self.coord_lbl = ctk.CTkLabel(self.status_frame, text="X: 000 | Y: 000",
                                      text_color="gray50", font=ctk.CTkFont(size=11))
        self.coord_lbl.grid(row=0, column=1, padx=10, sticky="e")

    # ══════════════════════════════════════════════════════════════════════════
    # CENA (modelo de dados)
    # ══════════════════════════════════════════════════════════════════════════

    def _next_prim_id(self):
        self._prim_id += 1
        return self._prim_id

    def _add_to_scene(self, ptype, points, algo, color=None):
        """Cria um primitivo e adiciona à cena. Retorna o primitivo."""
        pid = self._next_prim_id()
        prim = {
            'id':     pid,
            'type':   ptype,           # 'line' | 'circle' | 'polygon'
            'points': list(points),    # lista de (x, y)
            'algo':   algo,
            'tag':    f"prim_{pid}",   # tag única no canvas
            'color':  color or self.line_color,
        }
        self.scene.append(prim)
        return prim

    def _redraw_primitive(self, prim):
        """Apaga itens antigos do canvas e re-rasteriza o primitivo."""
        self.canvas.delete(prim['tag'])
        tag   = prim['tag']
        color = prim['color']
        pts   = prim['points']
        algo  = prim['algo']

        # Funções de desenho com a tag do primitivo embutida
        def draw_px(x, y, c=None):
            s = 2
            fc = c or color
            self.canvas.create_rectangle(
                x, y, x + s, y + s, fill=fc, outline=fc,
                tags=("drawing", tag))

        def draw_ln(x1, y1, x2, y2, dash=None, color=None, tag=tag):
            fc = color or prim['color']
            kw = {"fill": fc, "width": 2, "tags": ("drawing", tag)}
            if dash:
                kw["dash"] = dash
            self.canvas.create_line(x1, y1, x2, y2, **kw)

        def draw_ov(x1, y1, x2, y2):
            self.canvas.create_oval(
                x1, y1, x2, y2, outline=color, width=2,
                tags=("drawing", tag))

        if prim['type'] == 'line':
            if algo == 'DDA':
                execute_dda(pts[0], pts[1], draw_px, draw_ln)
            elif algo == 'Bresenham (Reta)':
                execute_bresenham_reta(pts[0], pts[1], draw_px)

        elif prim['type'] == 'circle':
            execute_bresenham_circulo(pts[0], pts[1], draw_px, draw_ov)

        elif prim['type'] == 'polygon':
            n = len(pts)
            for i in range(n):
                ps, pe = pts[i], pts[(i + 1) % n]
                draw_ln(ps[0], ps[1], pe[0], pe[1])

    def _get_selected_primitives(self):
        """Retorna os primitivos que possuem itens dentro da seleção atual."""
        selected_set = set(self.selected_items)
        result = []
        for prim in self.scene:
            prim_items = set(self.canvas.find_withtag(prim['tag']))
            if prim_items & selected_set:
                result.append(prim)
        return result

    def _centroid_of_prim(self, prim):
        """Calcula o centroide de um único primitivo."""
        pts = prim['points']
        if not pts:
            return 0.0, 0.0
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        return cx, cy

    # ══════════════════════════════════════════════════════════════════════════
    # HELPERS DO CANVAS
    # ══════════════════════════════════════════════════════════════════════════

    def set_status(self, msg):
        self.status_msg_lbl.configure(text=msg)

    def draw_grid(self, spacing=20):
        self.canvas.delete("grid_line")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
        for x in range(0, w, spacing):
            self.canvas.create_line(x, 0, x, h, tag="grid_line", fill=self.grid_color)
        for y in range(0, h, spacing):
            self.canvas.create_line(0, y, w, y, tag="grid_line", fill=self.grid_color)
        self.canvas.tag_lower("grid_line")

    def on_canvas_resize(self, event):
        self.draw_grid()

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        self.scene.clear()
        self.clip_window    = None
        self.drag_start     = None
        self.drag_rect_id   = None
        self.selected_items = []
        self.draw_grid()

        for entry in (self.entry_x1, self.entry_y1, self.entry_x2, self.entry_y2):
            entry.delete(0, "end")

        self.btn_close_polygon.configure(state="disabled")
        self.lbl_selection.configure(text="Nenhum objeto selecionado")
        self.set_status("Tela limpa.")

    def _draw_marker(self, x, y, color=None, tag="temp_marker"):
        c = color or self.marker_color
        r = 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                fill=c, outline="", tags=tag)

    # ══════════════════════════════════════════════════════════════════════════
    # EVENTOS DO CANVAS
    # ══════════════════════════════════════════════════════════════════════════

    def on_mouse_move(self, event):
        self.coord_lbl.configure(text=f"X: {event.x:03d} | Y: {event.y:03d}")

    def on_canvas_click(self, event):
        x, y = event.x, event.y

        if self.mode in (MODE_SELECT, MODE_CLIP_DEFINE):
            self.drag_start = (x, y)
            return

        if self.mode == MODE_DRAW_POLYGON:
            self._handle_polygon_click(x, y)
            return

        # ── 2 pontos (reta ou círculo) ────────────────────────────────────────
        if len(self.points) == 0:
            self.canvas.delete("temp_marker")
            self.entry_x1.delete(0, "end"); self.entry_x1.insert(0, str(x))
            self.entry_y1.delete(0, "end"); self.entry_y1.insert(0, str(y))
            self.entry_x2.delete(0, "end")
            self.entry_y2.delete(0, "end")
            self.points.append((x, y))
            self._draw_marker(x, y)
            self.set_status(f"Ponto 1 ({x},{y}) registrado. Clique para o Ponto 2.")

        elif len(self.points) == 1:
            self.entry_x2.delete(0, "end"); self.entry_x2.insert(0, str(x))
            self.entry_y2.delete(0, "end"); self.entry_y2.insert(0, str(y))
            self.points.append((x, y))
            self._draw_marker(x, y)
            self.process_drawing()

    def on_canvas_drag(self, event):
        if self.drag_start is None:
            return
        x0, y0 = self.drag_start
        if self.drag_rect_id:
            self.canvas.delete(self.drag_rect_id)
        color = self.select_color if self.mode == MODE_SELECT else self.clip_color
        self.drag_rect_id = self.canvas.create_rectangle(
            x0, y0, event.x, event.y,
            outline=color, dash=(4, 4), width=2, tags="temp_drag")

    def on_canvas_release(self, event):
        if self.drag_start is None:
            return
        x0, y0 = self.drag_start
        x1, y1 = event.x, event.y

        if self.mode == MODE_CLIP_DEFINE:
            self._finish_clip_define(x0, y0, x1, y1)
        elif self.mode == MODE_SELECT:
            self._finish_selection(x0, y0, x1, y1)

        self.drag_start = None
        if self.drag_rect_id:
            self.canvas.delete(self.drag_rect_id)
            self.drag_rect_id = None

    # ══════════════════════════════════════════════════════════════════════════
    # LÓGICA DOS MODOS
    # ══════════════════════════════════════════════════════════════════════════

    def _handle_polygon_click(self, x, y):
        self.points.append((x, y))
        self._draw_marker(x, y, color=self.poly_color)
        if len(self.points) >= 2:
            prev = self.points[-2]
            self.canvas.create_line(
                prev[0], prev[1], x, y,
                fill=self.poly_color, width=2, tags=("polygon_temp",))
            self.btn_close_polygon.configure(state="normal")
        n = len(self.points)
        self.set_status(f"Polígono: {n} vértice(s). "
                        f"{'Clique para adicionar ou feche.' if n < 3 else 'Pronto para fechar.'}")

    def close_polygon(self):
        if len(self.points) < 3:
            self.set_status("São necessários ao menos 3 vértices para fechar.")
            return

        # Registra na cena e redesenha com tag própria
        prim = self._add_to_scene('polygon', self.points.copy(),
                                  'Polígono', color=self.poly_color)
        self.canvas.delete("polygon_temp")
        self._redraw_primitive(prim)

        self.set_status(f"Polígono fechado com {len(self.points)} vértices.")
        self.points.clear()
        self.canvas.delete("temp_marker")
        self.btn_close_polygon.configure(state="disabled")

    def _finish_clip_define(self, x0, y0, x1, y1):
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])
        self.clip_window = (xmin, ymin, xmax, ymax)

        for entry, val in zip(
            [self.entry_clip_xmin, self.entry_clip_ymin,
             self.entry_clip_xmax, self.entry_clip_ymax],
            [xmin, ymin, xmax, ymax]
        ):
            entry.delete(0, "end")
            entry.insert(0, str(val))

        self.draw_clip_window()
        self.set_status(f"Janela de recorte: ({xmin},{ymin}) \u2192 ({xmax},{ymax}) — arraste para redefinir.")

    def draw_clip_window(self):
        try:
            xmin = int(self.entry_clip_xmin.get())
            ymin = int(self.entry_clip_ymin.get())
            xmax = int(self.entry_clip_xmax.get())
            ymax = int(self.entry_clip_ymax.get())
        except ValueError:
            self.set_status("Erro: preencha os 4 campos da janela de recorte.")
            return
        self.clip_window = (xmin, ymin, xmax, ymax)
        self.canvas.delete("clip_rect")
        self.canvas.create_rectangle(
            xmin, ymin, xmax, ymax,
            outline=self.clip_color, dash=(6, 3), width=2, tags="clip_rect")
        self.set_status(f"Janela mostrada: ({xmin},{ymin}) → ({xmax},{ymax})")

    def _finish_selection(self, x0, y0, x1, y1):
        xmin, xmax = sorted([x0, x1])
        ymin, ymax = sorted([y0, y1])

        all_items = self.canvas.find_enclosed(xmin, ymin, xmax, ymax)
        self.selected_items = [
            i for i in all_items
            if any(t in self.canvas.gettags(i) for t in ("drawing",))
        ]

        # Destaque visual temporário
        self.canvas.delete("selection_highlight")
        prims = self._get_selected_primitives()
        for prim in prims:
            pts = prim['points']
            if pts:
                cx = sum(p[0] for p in pts) / len(pts)
                cy = sum(p[1] for p in pts) / len(pts)
                r = 8
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    outline=self.select_color, width=2,
                    tags="selection_highlight")

        n = len(prims)
        txt = f"{n} objeto(s) selecionado(s)" if n else "Nenhum objeto selecionado"
        self.lbl_selection.configure(text=txt)
        self.set_status(f"Seleção: {n} objeto(s).")

    # ══════════════════════════════════════════════════════════════════════════
    # CALLBACKS
    # ══════════════════════════════════════════════════════════════════════════

    def _on_raster_algo_change(self, mode, algo_name):
        self.mode = mode
        self.raster_algo.set(algo_name)
        self.points.clear()
        self.canvas.delete("temp_marker")
        self.btn_close_polygon.configure(
            state="normal" if mode == MODE_DRAW_POLYGON else "disabled")
        # Atualiza visual dos botões toggle
        for val, btn in self._raster_btns.items():
            btn.configure(fg_color="#2B5BA0" if val == algo_name else "#2E2E2E")
        self.set_status(f"Ferramenta: {algo_name}")

    def on_define_clip_mode(self):
        self.mode = MODE_CLIP_DEFINE
        self.set_status("Modo Recorte: arraste no canvas para definir a janela.")

    def on_select_mode(self):
        self.mode = MODE_SELECT
        self.set_status("Modo Seleção: arraste para selecionar objetos.")

    def _on_tab_change(self):
        """Ajusta o modo do canvas ao trocar de aba."""
        tab = self.tabview.get()
        if tab == "Rasterização":
            algo = self.raster_algo.get()
            mode_map = {
                "DDA":                 MODE_DRAW_LINE,
                "Bresenham (Reta)":    MODE_DRAW_LINE,
                "Bresenham (Círculo)": MODE_DRAW_CIRCLE,
                "Polígono":            MODE_DRAW_POLYGON,
            }
            self.mode = mode_map.get(algo, MODE_DRAW_LINE)
            self.set_status(f"Ferramenta: {algo}")
        elif tab == "Recorte":
            self.mode = MODE_CLIP_DEFINE
            self.set_status("Modo Recorte: arraste no canvas para definir a janela.")
        elif tab == "Transformações":
            self.mode = MODE_SELECT
            self.set_status("Modo Seleção: arraste para selecionar objetos.")

    # ── Traçar Manual ─────────────────────────────────────────────────────────

    def on_manual_draw(self):
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
        except ValueError:
            self.set_status("Erro: insira valores inteiros válidos nos campos X e Y.")
            return
        self.canvas.delete("temp_marker")
        self._draw_marker(x1, y1)
        self._draw_marker(x2, y2)
        self.points = [(x1, y1), (x2, y2)]
        self.process_drawing()

    # ── Processo de Desenho ───────────────────────────────────────────────────

    def process_drawing(self):
        if len(self.points) != 2:
            return
        p1, p2 = self.points
        algo = self.raster_algo.get()

        ptype = 'circle' if algo == 'Bresenham (Círculo)' else 'line'
        prim = self._add_to_scene(ptype, [p1, p2], algo)
        self._redraw_primitive(prim)

        self.set_status(f"Traçado: {algo} | P1{p1} → P2{p2}")
        self.points.clear()
        self.canvas.delete("temp_marker")

    # ── Recorte ───────────────────────────────────────────────────────────────

    def on_apply_clip(self):
        try:
            xmin = int(self.entry_clip_xmin.get())
            ymin = int(self.entry_clip_ymin.get())
            xmax = int(self.entry_clip_xmax.get())
            ymax = int(self.entry_clip_ymax.get())
        except ValueError:
            self.set_status("Erro: preencha os 4 campos da janela de recorte.")
            return

        algo    = self.clip_algo.get()
        clip_fn = (execute_cohen_sutherland if algo == "Cohen-Sutherland"
                   else execute_liang_barsky)

        DIM_COLOR = "#5A5A5A"   # cor dos segmentos fora da janela (cinza médio)

        # ── Limpa overlays e redesenhos anteriores ────────────────────────────
        self.canvas.delete("clip_overlay")
        self.canvas.delete("clip_clipped")

        # ── Redesenha cada primitivo: segmento fora=dim, dentro=original ──────
        for prim in self.scene:
            color_in  = prim['color']
            color_out = DIM_COLOR
            pts       = prim['points']
            tag       = prim['tag']

            if prim['type'] == 'line':
                p1, p2  = pts[0], pts[1]
                clipped = clip_fn(p1, p2, xmin, ymin, xmax, ymax)
                self.canvas.delete(tag)
                # redesenha linha inteira em dim
                self.canvas.create_line(
                    p1[0], p1[1], p2[0], p2[1],
                    fill=color_out, width=2,
                    tags=("clip_clipped", tag))
                # sobrepõe o trecho visível em cor original
                if clipped:
                    cp1, cp2 = clipped
                    self.canvas.create_line(
                        cp1[0], cp1[1], cp2[0], cp2[1],
                        fill=color_in, width=2,
                        tags=("clip_clipped", tag))

            elif prim['type'] == 'polygon':
                n = len(pts)
                self.canvas.delete(tag)
                for i in range(n):
                    ps, pe  = pts[i], pts[(i + 1) % n]
                    clipped = clip_fn(ps, pe, xmin, ymin, xmax, ymax)
                    self.canvas.create_line(
                        ps[0], ps[1], pe[0], pe[1],
                        fill=color_out, width=2,
                        tags=("clip_clipped", tag))
                    if clipped:
                        cp1, cp2 = clipped
                        self.canvas.create_line(
                            cp1[0], cp1[1], cp2[0], cp2[1],
                            fill=color_in, width=2,
                            tags=("clip_clipped", tag))

            elif prim['type'] == 'circle':
                import math as _math
                center = pts[0]; edge = pts[1]
                r  = _math.sqrt((edge[0]-center[0])**2 + (edge[1]-center[1])**2)
                cx, cy = center
                inside = (cx + r >= xmin and cx - r <= xmax and
                          cy + r >= ymin and cy - r <= ymax)
                self.canvas.delete(tag)
                self.canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    outline=(color_in if inside else color_out), width=2,
                    tags=("clip_clipped", tag))

        # ── Z-order: borda da janela por cima de tudo ────────────────────────
        self.canvas.tag_raise("clip_rect")

        self.set_status(
            f"Recorte ({algo}): área interna destacada "
            f"({xmin},{ymin}) \u2192 ({xmax},{ymax})")

    def on_remove_clip(self):
        """Remove o overlay de recorte e restaura os desenhos originais."""
        self.canvas.delete("clip_overlay")
        self.canvas.delete("clip_clipped")
        self.canvas.delete("clip_rect")
        self.clip_window = None
        # Restaura todos os primitivos com suas cores originais
        for prim in self.scene:
            self._redraw_primitive(prim)
        self.set_status("Janela de recorte removida. Desenhos restaurados.")

    # ── Transformações ────────────────────────────────────────────────────────

    def _apply_transform(self, fn, *args, label="Transformação"):
        """Helper genérico: aplica fn(pontos, *args) a cada primitivo selecionado."""
        prims = self._get_selected_primitives()
        if not prims:
            self.set_status("Selecione objetos antes de aplicar a transformação.")
            return
        for prim in prims:
            prim['points'] = fn(prim['points'], *args)
            self._redraw_primitive(prim)
        self.canvas.delete("selection_highlight")
        self.set_status(f"{label} aplicada a {len(prims)} objeto(s).")

    def on_apply_translacao(self):
        try:
            dx = float(self.entry_tr_dx.get())
            dy = float(self.entry_tr_dy.get())
        except ValueError:
            self.set_status("Erro: insira valores numéricos para dx e dy.")
            return
        self._apply_transform(execute_translacao, dx, dy,
                              label=f"Translação (dx={dx}, dy={dy})")

    def on_apply_rotacao(self):
        try:
            angulo = float(self.entry_ro_angle.get())
        except ValueError:
            self.set_status("Erro: insira um ângulo numérico.")
            return
        prims = self._get_selected_primitives()
        if not prims:
            self.set_status("Selecione objetos antes de aplicar a rotação.")
            return
        for prim in prims:
            cx, cy = self._centroid_of_prim(prim)
            prim['points'] = execute_rotacao(prim['points'], angulo, cx, cy)
            self._redraw_primitive(prim)
        self.canvas.delete("selection_highlight")
        self.set_status(f"Rotação ({angulo}°) aplicada a {len(prims)} objeto(s).")

    def on_apply_escala(self):
        try:
            sx = float(self.entry_sc_sx.get())
            sy = float(self.entry_sc_sy.get())
        except ValueError:
            self.set_status("Erro: insira valores numéricos para Sx e Sy.")
            return
        prims = self._get_selected_primitives()
        if not prims:
            self.set_status("Selecione objetos antes de aplicar a escala.")
            return
        for prim in prims:
            cx, cy = self._centroid_of_prim(prim)
            prim['points'] = execute_escala(prim['points'], sx, sy, cx, cy)
            self._redraw_primitive(prim)
        self.canvas.delete("selection_highlight")
        self.set_status(f"Escala (Sx={sx}, Sy={sy}) aplicada a {len(prims)} objeto(s).")

    def on_apply_reflexao(self):
        eixo = self.reflex_eixo.get()
        prims = self._get_selected_primitives()
        if not prims:
            self.set_status("Selecione objetos antes de aplicar a reflexão.")
            return
        for prim in prims:
            cx, cy = self._centroid_of_prim(prim)
            prim['points'] = execute_reflexao(prim['points'], eixo, cx, cy)
            self._redraw_primitive(prim)
        self.canvas.delete("selection_highlight")
        self.set_status(f"Reflexão (Eixo {eixo}) aplicada a {len(prims)} objeto(s).")


# ── Ponto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PaintApp()
    app.mainloop()
