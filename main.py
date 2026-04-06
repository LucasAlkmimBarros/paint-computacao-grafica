#!/usr/bin/env python3
import customtkinter as ctk
import tkinter as tk

# Importa os algoritmos de traçado da pasta "algorithms"
from algorithms.dda import execute_dda
from algorithms.bresenham_reta import execute_bresenham_reta
from algorithms.bresenham_circulo import execute_bresenham_circulo

# Configurações globais do tema
ctk.set_appearance_mode("dark")  # Modo dark por padrão
ctk.set_default_color_theme("blue")  # Tema de cores azulado

class PaintApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal
        self.title("Desenho CG - Algoritmos de Traçado")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        # Variáveis de Estado
        self.points = []
        self.algorithms = ["DDA", "Bresenham (Reta)", "Bresenham (Círculo)"]
        self.selected_algo_idx = tk.IntVar(value=0) # Index do algoritmo atual
        
        self.selected_algo_idx = tk.IntVar(value=0) # Index do algoritmo atual
        
        # Cores (Paleta Moderna)
        self.bg_color = "#1E1E1E"          # Fundo escuro do canvas
        self.grid_color = "#333333"        # Cor das linhas de grade
        self.marker_color = "#E06C75"      # Vermelho pastel para os pontos de marcação
        self.line_color = "#61AFEF"        # Azul para as retas desenhadas
        
        self.setup_ui()
        self.draw_grid()

    def setup_ui(self):
        """Configura o layout principal da aplicação usando Grid"""
        # Configurar proporções das linhas e colunas
        self.grid_rowconfigure(0, weight=1)       # Linha 0 expande (área de desenho)
        self.grid_rowconfigure(1, weight=0)       # Linha 1 fixa (status bar)
        self.grid_columnconfigure(0, weight=0)    # Col 0 fixa (sidebar)
        self.grid_columnconfigure(1, weight=1)    # Col 1 expande (canvas)
        
        # --- SIDEBAR (Barra Lateral Esquerda) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Ferramentas", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botões de Algoritmos
        self.algo_buttons = []
        for i, algo in enumerate(self.algorithms):
            btn = ctk.CTkRadioButton(
                self.sidebar_frame, text=algo, value=i, variable=self.selected_algo_idx,
                font=ctk.CTkFont(size=14), command=self.on_algo_change
            )
            
            # Deixa os botões que não são DDA desabilitados
            if algo not in ["DDA", "Bresenham (Reta)"]:
                btn.configure(state="disabled")
                
            btn.grid(row=i+1, column=0, pady=10, padx=20, sticky="w")
            self.algo_buttons.append(btn)
            
        # Espaçador entre algoritmos e inputs manuais
        self.sidebar_frame.grid_rowconfigure(len(self.algorithms) + 1, weight=1)
        
        # --- INPUTS MANUAIS ---
        self.input_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.input_frame.grid(row=len(self.algorithms) + 2, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=1)
        
        # Ponto 1
        ctk.CTkLabel(self.input_frame, text="Ponto 1:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.entry_x1 = ctk.CTkEntry(self.input_frame, placeholder_text="X1", width=60)
        self.entry_x1.grid(row=1, column=0, padx=(0, 5), pady=(0, 10))
        self.entry_y1 = ctk.CTkEntry(self.input_frame, placeholder_text="Y1", width=60)
        self.entry_y1.grid(row=1, column=1, padx=(5, 0), pady=(0, 10))

        # Ponto 2
        ctk.CTkLabel(self.input_frame, text="Ponto 2:", font=ctk.CTkFont(size=12, weight="bold")).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.entry_x2 = ctk.CTkEntry(self.input_frame, placeholder_text="X2", width=60)
        self.entry_x2.grid(row=3, column=0, padx=(0, 5), pady=(0, 10))
        self.entry_y2 = ctk.CTkEntry(self.input_frame, placeholder_text="Y2", width=60)
        self.entry_y2.grid(row=3, column=1, padx=(5, 0), pady=(0, 10))

        self.btn_draw_manual = ctk.CTkButton(
            self.sidebar_frame, text="Traçar Manual", 
            command=self.on_manual_draw, font=ctk.CTkFont(weight="bold")
        )
        self.btn_draw_manual.grid(row=len(self.algorithms) + 3, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Botão Limpar
        self.clear_btn = ctk.CTkButton(
            self.sidebar_frame, text="Limpar Tela", fg_color="#C23B22", hover_color="#8F2A19",
            command=self.clear_canvas, font=ctk.CTkFont(weight="bold")
        )
        self.clear_btn.grid(row=len(self.algorithms) + 4, column=0, padx=20, pady=20, sticky="ew")

        # --- CANVAS AREA (Centro) ---
        # Container para o Canvas (para ter a borda arredondada do CTK)
        self.canvas_container = ctk.CTkFrame(self, corner_radius=10)
        self.canvas_container.grid(row=0, column=1, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.canvas_container.pack_propagate(False)
        
        # O Canvas nativo do Tkinter (necessário para desenhar livremente)
        self.canvas = tk.Canvas(
            self.canvas_container, bg=self.bg_color, highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Bindings do Canvas (Eventos de mouse)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # --- STATUS BAR (Rodapé) ---
        self.status_frame = ctk.CTkFrame(self, height=30, corner_radius=5)
        self.status_frame.grid(row=1, column=1, padx=(20, 20), pady=(0, 20), sticky="ew")
        self.status_frame.grid_propagate(False)
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        # Removido status_msg a pedido do usuário
        # self.status_msg = ctk.CTkLabel(self.status_frame, text="Bem-vindo! Selecione dois pontos para traçar.", text_color="gray70")
        # self.status_msg.grid(row=0, column=0, padx=10, sticky="w")
        
        self.coord_lbl = ctk.CTkLabel(self.status_frame, text="X: 000 | Y: 000", text_color="gray50")
        self.coord_lbl.grid(row=0, column=1, padx=10, sticky="e")

    def set_status(self, msg):
        # Desativado a pedido do usuário
        pass

    def draw_grid(self, spacing=20):
        """Desenha uma malha de grid sutil no fundo"""
        self.canvas.delete("grid_line")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1: return
        
        for x in range(0, width, spacing):
            self.canvas.create_line([(x, 0), (x, height)], tag="grid_line", fill=self.grid_color)
        for y in range(0, height, spacing):
            self.canvas.create_line([(0, y), (width, y)], tag="grid_line", fill=self.grid_color)
            
        self.canvas.tag_lower("grid_line") # Joga o grid para o fundo

    def on_canvas_resize(self, event):
        """Garante que o grid se redesenhe se a janela for maximizada"""
        self.draw_grid()

    def clear_canvas(self):
        """Limpa toda a cena."""
        self.canvas.delete("all")
        self.points.clear()
        
        self.draw_grid()
        
        self.entry_x1.delete(0, 'end')
        self.entry_y1.delete(0, 'end')
        self.entry_x2.delete(0, 'end')
        self.entry_y2.delete(0, 'end')
        
        self.set_status("Tela limpa.")

    def on_algo_change(self):
        """Trocar de algoritmo limpa o estado de desenho atual."""
        algo = self.algorithms[self.selected_algo_idx.get()]
        self.points.clear()
        self.canvas.delete("temp_marker")
        self.set_status(f"Ferramenta selecionada: {algo}")

    def on_mouse_move(self, event):
        """Atualiza barra de coordenadas do rodapé com a posição X/Y do Mouse"""
        self.coord_lbl.configure(text=f"X: {event.x:03d} | Y: {event.y:03d}")

    def proxy_draw_pixel(self, x, y, color=None):
        """Callback pra Computação Gráfica. Transforma lógica em um rect nativo"""
        if color is None: color = self.line_color
        size = 2 # Tamanho visual prático de um pixel se o grid tem scale 1:1 nativo
        self.canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline=color, tags="drawing")
        
    def proxy_draw_native_line(self, x1, y1, x2, y2, dash=None):
        """Callback pra ajudar nos placeholders"""
        kwargs = {"fill": self.line_color, "width": 2}
        if dash: kwargs["dash"] = dash
        self.canvas.create_line(x1, y1, x2, y2, tags="drawing", **kwargs)
        
    def proxy_draw_native_oval(self, x1, y1, x2, y2):
        """Callback pra placeholders"""
        self.canvas.create_oval(x1, y1, x2, y2, outline=self.line_color, width=2, tags="drawing")

    def on_canvas_click(self, event):
        """Lida com cliques na tela de desenho para montar as retas/círculos"""
        x, y = event.x, event.y
        
        if len(self.points) == 0:
            # Primeiro clique: Inicializando traçado
            self.canvas.delete("drawing")
            self.canvas.delete("temp_marker")
            
            # Limpa e preenche
            self.entry_x1.delete(0, 'end')
            self.entry_x1.insert(0, str(x))
            self.entry_y1.delete(0, 'end')
            self.entry_y1.insert(0, str(y))
            
            self.entry_x2.delete(0, 'end')
            self.entry_y2.delete(0, 'end')
            
            self.points.append((x, y))
            r = 3
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.marker_color, outline="", tags="temp_marker")
            
        elif len(self.points) == 1:
            # Segundo clique
            self.entry_x2.delete(0, 'end')
            self.entry_x2.insert(0, str(x))
            self.entry_y2.delete(0, 'end')
            self.entry_y2.insert(0, str(y))
            
            self.points.append((x, y))
            r = 3
            self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self.marker_color, outline="", tags="temp_marker")
            self.process_drawing()

    def on_manual_draw(self):
        """Lê as coordenadas manuais dos Entry e realiza o desenho"""
        try:
            x1 = int(self.entry_x1.get())
            y1 = int(self.entry_y1.get())
            x2 = int(self.entry_x2.get())
            y2 = int(self.entry_y2.get())
            
            # Limpa o canvas de desenhos anteriores
            self.canvas.delete("drawing")
            self.canvas.delete("temp_marker")
            
            r = 3
            # Pinta marcadores
            self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill=self.marker_color, outline="", tags="temp_marker")
            self.canvas.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill=self.marker_color, outline="", tags="temp_marker")
            
            self.points = [(x1, y1), (x2, y2)]
            self.process_drawing()
        except ValueError:
            self.set_status("Erro: Por favor, insira valores inteiros válidos nos inputs X e Y.")
            
    def process_drawing(self):
        """Roteia o par de pontos para o algoritmo adequado e finaliza o estado"""
        if len(self.points) != 2: return
        
        p1, p2 = self.points[0], self.points[1]
        algo = self.algorithms[self.selected_algo_idx.get()]
        self.set_status(f"Traçado finalizado com {algo} (P1:{p1} → P2:{p2}).")
        
        # Chama a função específica do Controller externo e passa os callbacks de desenho 
        if algo == "DDA":
            execute_dda(p1, p2, self.proxy_draw_pixel, self.proxy_draw_native_line)
        elif algo == "Bresenham (Reta)":
            execute_bresenham_reta(p1, p2, self.proxy_draw_pixel)
        elif algo == "Bresenham (Círculo)":
            execute_bresenham_circulo(p1, p2, self.proxy_draw_pixel)
            
        self.points.clear()
        self.canvas.delete("temp_marker") # Remove marcações antes do desenho final

if __name__ == "__main__":
    app = PaintApp()
    app.mainloop()
