import tkinter as tk
from tkinter import ttk
import math

class Professor:
    """Representa um professor no mapa"""
    def __init__(self, id, name, areas, x, y, bio, skills):
        self.id = id
        self.name = name
        self.areas = areas  # lista de áreas
        self.x = x
        self.y = y
        self.bio = bio
        self.skills = skills
        self.canvas_id = None

class Transition:
    """Ligação entre professores baseada em áreas comuns"""
    def __init__(self, from_id, to_id, shared_areas):
        self.from_id = from_id
        self.to_id = to_id
        self.shared_areas = shared_areas  # número de áreas em comum
        self.line_id = None

class ProfessorMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa de Professores e Áreas de Pesquisa")
        self.root.geometry("1400x800")

        # Professores (exemplo)
        self.professors = {
            1: Professor(
                1, "Prof. Ana", ["IA", "Aprendizado de Máquina"], 
                150, 200, 
                "Pesquisadora na área de Inteligência Artificial aplicada.",
                ["Python", "TensorFlow", "Machine Learning"]
            ),
            2: Professor(
                2, "Prof. Marcos", ["Visão Computacional", "IA"],
                450, 350,
                "Trabalha com reconhecimento de padrões e visão computacional.",
                ["OpenCV", "CNNs", "Deep Learning"]
            ),
            3: Professor(
                3, "Prof. Júlia", ["Aprendizado de Máquina", "Dados"],
                750, 200,
                "Focada em modelagem estatística e predição.",
                ["Python", "Pandas", "Modelos Estatísticos"]
            ),
            4: Professor(
                4, "Prof. Roberto", ["Redes Neurais", "Visão Computacional"],
                450, 80,
                "Especialista em arquiteturas neurais profundas.",
                ["PyTorch", "GANs", "Deep Learning"]
            )
        }

        # Criar transições automaticamente
        self.transitions = self.generate_transitions()

        self.selected_prof = None
        self.hovered_prof = None

        # Para arrastar o mapa
        self.dragging = False
        self.last_drag_pos = (0, 0)

        # Zoom
        self.scale = 1.0

        self.setup_ui()
        self.auto_layout()
        self.draw_map()

    def generate_transitions(self):
        """Cria ligações entre professores que compartilham áreas"""
        transitions = []
        profs = list(self.professors.values())

        for i in range(len(profs)):
            for j in range(i+1, len(profs)):
                shared = set(profs[i].areas) & set(profs[j].areas)
                if shared:
                    transitions.append(
                        Transition(profs[i].id, profs[j].id, len(shared))
                    )
        return transitions

    # ============================================
    # AUTO-LAYOUT (organização automática circular)
    # ============================================
    def auto_layout(self):
        cx, cy = 600, 350     # centro
        radius = 250
        profs = list(self.professors.values())
        n = len(profs)

        for i, p in enumerate(profs):
            angle = 2 * math.pi * i / n
            p.x = cx + radius * math.cos(angle)
            p.y = cy + radius * math.sin(angle)

    # ============================================
    # SETUP UI
    # ============================================
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#f8fafc")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título
        tk.Label(main_frame, text="Mapa de Professores e Pesquisas",
                 font=("Arial", 20, "bold"), bg="#f8fafc", fg="#1e293b"
        ).pack(anchor="w")

        content = tk.Frame(main_frame, bg="#f8fafc")
        content.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(content, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scroll + Zoom
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        # Arrastar com botão direito
        self.canvas.bind("<ButtonPress-3>", self.start_drag)
        self.canvas.bind("<B3-Motion>", self.drag_map)
        self.canvas.bind("<ButtonRelease-3>", self.stop_drag)

        # Painel lateral
        self.details = tk.Frame(content, bg="white", width=320)
        self.details.pack(side=tk.RIGHT, fill=tk.Y)
        self.details.pack_propagate(False)

        self.details_msg = tk.Label(self.details, text="Selecione um professor",
                                    font=("Arial", 12), bg="white")
        self.details_msg.pack(expand=True)

        # Eventos de clique e hover
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)

    # ============================================
    # DESENHO DO MAPA
    # ============================================
    def draw_map(self):
        self.canvas.delete("all")

        # Linhas
        for t in self.transitions:
            self.draw_transition(t)

        # Nós
        for p in self.professors.values():
            self.draw_prof(p)

    def draw_transition(self, t):
        p1 = self.professors[t.from_id]
        p2 = self.professors[t.to_id]

        line = self.canvas.create_line(
            p1.x, p1.y, p2.x, p2.y,
            width=2, fill="#94a3b8"
        )
        t.line_id = line

    def draw_prof(self, prof):
        rect = self.canvas.create_rectangle(
            prof.x - 80, prof.y - 30, prof.x + 80, prof.y + 30,
            fill="#e0f2fe",
            outline="#0284c7",
            width=2,
            tags=("prof", f"prof_{prof.id}")
        )

        self.canvas.create_text(
            prof.x, prof.y - 5,
            text=prof.name, font=("Arial", 11, "bold"),
            tags=("prof", f"prof_{prof.id}")
        )

        self.canvas.create_text(
            prof.x, prof.y + 20,
            text=", ".join(prof.areas),
            font=("Arial", 9),
            fill="#0369a1",
            tags=("prof", f"prof_{prof.id}")
        )

        prof.canvas_id = rect

    # ============================================
    # ZOOM
    # ============================================
    def on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= factor
        self.canvas.scale("all", event.x, event.y, factor, factor)

    # ============================================
    # ARRASTAR MAPA
    # ============================================
    def start_drag(self, event):
        self.dragging = True
        self.last_drag_pos = (event.x, event.y)

    def drag_map(self, event):
        if not self.dragging:
            return

        dx = event.x - self.last_drag_pos[0]
        dy = event.y - self.last_drag_pos[1]

        self.canvas.move("all", dx, dy)
        self.last_drag_pos = (event.x, event.y)

    def stop_drag(self, event):
        self.dragging = False

    # ============================================
    # INTERAÇÃO (selecionar professor)
    # ============================================
    def on_click(self, event):
        item = self.canvas.find_withtag("current")
        if not item:
            return
        
        tags = self.canvas.gettags(item)
        for t in tags:
            if t.startswith("prof_"):
                id = int(t.split("_")[1])
                self.selected_prof = self.professors[id]
                self.show_details()
                break

    def on_hover(self, event):
        pass  # pode adicionar highlight depois

    def show_details(self):
        for w in self.details.winfo_children():
            w.destroy()

        p = self.selected_prof

        tk.Label(self.details, text=p.name,
                 font=("Arial", 16, "bold"), bg="white").pack(anchor="w", padx=15, pady=10)

        tk.Label(self.details, text="Áreas de Pesquisa:",
                 font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=15)

        for a in p.areas:
            tk.Label(self.details, text=f"• {a}", bg="white",
                     font=("Arial", 10)).pack(anchor="w", padx=25)

        tk.Label(self.details, text="\nSobre:",
                 font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=15)

        tk.Label(self.details, text=p.bio, wraplength=280,
                 bg="white", font=("Arial", 10)).pack(anchor="w", padx=15, pady=5)

        tk.Label(self.details, text="Habilidades:",
                 font=("Arial", 12, "bold"), bg="white").pack(anchor="w", padx=15)

        for s in p.skills:
            tk.Label(self.details, text=f"✓ {s}", bg="white",
                     font=("Arial", 10)).pack(anchor="w", padx=25)


# Executar
if __name__ == "__main__":
    root = tk.Tk()
    app = ProfessorMapApp(root)
    root.mainloop()
