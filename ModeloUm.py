import tkinter as tk
from tkinter import ttk, messagebox
import math

class Career:
    """Representa uma carreira no mapa"""
    def __init__(self, id, name, level, area, salary, x, y, skills, description):
        self.id = id
        self.name = name
        self.level = level
        self.area = area
        self.salary = salary
        self.x = x
        self.y = y
        self.skills = skills
        self.description = description
        self.canvas_id = None

class Transition:
    """Representa uma transição entre carreiras"""
    def __init__(self, from_id, to_id, difficulty, months):
        self.from_id = from_id
        self.to_id = to_id
        self.difficulty = difficulty
        self.months = months
        self.line_id = None

class CareerMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa de Carreiras Interativo")
        self.root.geometry("1400x800")
        
        # Dados das carreiras (simulando banco de dados)
        self.careers = {
            1: Career(1, "Desenvolvedor\nJúnior", "Júnior", "Tecnologia", 
                     "R$ 3.000 - R$ 5.000", 100, 250, 
                     ["HTML", "CSS", "JavaScript", "Git"],
                     "Início da carreira em desenvolvimento,\naprendendo fundamentos."),
            
            2: Career(2, "Desenvolvedor\nPleno", "Pleno", "Tecnologia",
                     "R$ 6.000 - R$ 10.000", 300, 250,
                     ["React", "Node.js", "APIs REST", "Banco de Dados"],
                     "Desenvolve features completas\ncom autonomia."),
            
            3: Career(3, "Desenvolvedor\nSênior", "Sênior", "Tecnologia",
                     "R$ 12.000 - R$ 20.000", 500, 250,
                     ["Arquitetura", "Microserviços", "Cloud", "Mentoria"],
                     "Decisões técnicas importantes\ne mentoria do time."),
            
            4: Career(4, "Tech Lead", "Liderança", "Tecnologia",
                     "R$ 15.000 - R$ 25.000", 500, 100,
                     ["Gestão de Pessoas", "Planejamento", "Arquitetura"],
                     "Lidera tecnicamente um time\nde desenvolvimento."),
            
            5: Career(5, "Arquiteto de\nSoftware", "Especialista", "Tecnologia",
                     "R$ 18.000 - R$ 30.000", 700, 250,
                     ["Design Patterns", "Escalabilidade", "Performance"],
                     "Define arquitetura de\nsistemas complexos."),
            
            6: Career(6, "DevOps\nEngineer", "Pleno", "Tecnologia",
                     "R$ 8.000 - R$ 15.000", 300, 400,
                     ["Docker", "Kubernetes", "CI/CD", "AWS/Azure"],
                     "Automatiza deploys e gerencia\ninfraestrutura."),
            
            7: Career(7, "Product\nManager", "Gestão", "Produto",
                     "R$ 10.000 - R$ 18.000", 500, 50,
                     ["Visão de Produto", "Análise", "UX", "Stakeholders"],
                     "Define roadmap e prioridades\ndo produto."),
            
            8: Career(8, "Data\nScientist", "Pleno", "Dados",
                     "R$ 8.000 - R$ 16.000", 100, 100,
                     ["Python", "Machine Learning", "Estatística", "SQL"],
                     "Analisa dados e cria\nmodelos preditivos.")
        }
        
        # Transições entre carreiras
        self.transitions = [
            Transition(1, 2, 2, 18),
            Transition(2, 3, 3, 24),
            Transition(3, 4, 3, 12),
            Transition(3, 5, 4, 18),
            Transition(2, 6, 3, 12),
            Transition(3, 7, 4, 12),
            Transition(1, 8, 4, 24),
        ]
        
        self.selected_career = None
        self.hovered_career = None
        self.current_filter = "Todas"
        self.search_term = ""
        
        self.setup_ui()
        self.draw_map()
        
    def setup_ui(self):
        """Configura a interface"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#f8fafc")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_frame = tk.Frame(main_frame, bg="#f8fafc")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, text="🚀 Mapa de Carreiras", 
                              font=("Arial", 20, "bold"), bg="#f8fafc", fg="#1e293b")
        title_label.pack(side=tk.LEFT)
        
        subtitle = tk.Label(title_frame, text="Explore caminhos profissionais e transições",
                           font=("Arial", 11), bg="#f8fafc", fg="#64748b")
        subtitle.pack(side=tk.LEFT, padx=15)
        
        # Frame de filtros
        filter_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Busca
        tk.Label(filter_frame, text="🔍 Buscar:", font=("Arial", 10), 
                bg="white").pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.apply_filters())
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, 
                               font=("Arial", 10), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Filtros por área
        tk.Label(filter_frame, text="Área:", font=("Arial", 10), 
                bg="white").pack(side=tk.LEFT, padx=(20, 5))
        
        areas = ["Todas", "Tecnologia", "Produto", "Dados"]
        for area in areas:
            btn = tk.Button(filter_frame, text=area, 
                          command=lambda a=area: self.set_filter(a),
                          font=("Arial", 9), relief=tk.FLAT,
                          bg="#e2e8f0" if area != "Todas" else "#3b82f6",
                          fg="black" if area != "Todas" else "white",
                          padx=15, pady=5)
            btn.pack(side=tk.LEFT, padx=2)
            setattr(self, f"btn_{area}", btn)
        
        # Frame de conteúdo
        content_frame = tk.Frame(main_frame, bg="#f8fafc")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para o mapa
        canvas_frame = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Painel de detalhes
        self.details_frame = tk.Frame(content_frame, bg="white", width=300, 
                                     relief=tk.RAISED, bd=1)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_frame.pack_propagate(False)
        
        self.setup_details_panel()
        
        # Legenda
        legend_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, bd=1)
        legend_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(legend_frame, text="● Carreira", font=("Arial", 9), 
                bg="white", fg="#64748b").pack(side=tk.LEFT, padx=10, pady=5)
        tk.Label(legend_frame, text="● Selecionada", font=("Arial", 9), 
                bg="white", fg="#3b82f6").pack(side=tk.LEFT, padx=10)
        tk.Label(legend_frame, text="→ Transição de carreira", font=("Arial", 9),
                bg="white", fg="#64748b").pack(side=tk.LEFT, padx=10)
        
        # Bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        
    def setup_details_panel(self):
        """Configura o painel de detalhes"""
        # Título do painel
        tk.Label(self.details_frame, text="Detalhes da Carreira", 
                font=("Arial", 14, "bold"), bg="white", fg="#1e293b"
                ).pack(pady=15, padx=15, anchor='w')
        
        # Frame de conteúdo scrollable
        self.details_content = tk.Frame(self.details_frame, bg="white")
        self.details_content.pack(fill=tk.BOTH, expand=True, padx=15)
        
        # Mensagem inicial
        self.empty_msg = tk.Label(self.details_content, 
                                 text="👈 Clique em uma carreira\nno mapa para ver detalhes",
                                 font=("Arial", 11), bg="white", fg="#94a3b8",
                                 justify=tk.CENTER)
        self.empty_msg.pack(expand=True)
        
    def draw_map(self):
        """Desenha o mapa de carreiras"""
        self.canvas.delete("all")
        
        # Filtrar carreiras visíveis
        visible_careers = self.get_visible_careers()
        visible_ids = [c.id for c in visible_careers]
        
        # Desenhar transições (linhas)
        for transition in self.transitions:
            if transition.from_id in visible_ids and transition.to_id in visible_ids:
                self.draw_transition(transition)
        
        # Desenhar carreiras (nós)
        for career in visible_careers:
            self.draw_career(career)
    
    def draw_transition(self, transition):
        """Desenha uma transição entre carreiras"""
        from_career = self.careers[transition.from_id]
        to_career = self.careers[transition.to_id]
        
        # Calcular posições
        x1, y1 = from_career.x + 60, from_career.y + 30
        x2, y2 = to_career.x + 60, to_career.y + 30
        
        # Cor da linha
        is_highlighted = (self.hovered_career and 
                         (self.hovered_career == transition.from_id or 
                          self.hovered_career == transition.to_id))
        
        color = "#3b82f6" if is_highlighted else "#cbd5e1"
        width = 3 if is_highlighted else 2
        
        # Desenhar linha
        line = self.canvas.create_line(x1, y1, x2, y2, 
                                      fill=color, width=width, 
                                      arrow=tk.LAST, arrowshape=(10, 12, 5))
        
        # Texto com tempo
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(mid_x, mid_y - 10, 
                               text=f"{transition.months}m",
                               font=("Arial", 9), fill="#64748b")
        
        transition.line_id = line
    
    def draw_career(self, career):
        """Desenha um nó de carreira"""
        # Determinar cor
        if self.selected_career and self.selected_career.id == career.id:
            bg_color = "#3b82f6"
            text_color = "white"
            outline = "#2563eb"
        elif self.hovered_career == career.id or self.is_connected(career.id):
            bg_color = "#60a5fa"
            text_color = "white"
            outline = "#3b82f6"
        else:
            bg_color = "#f1f5f9"
            text_color = "#1e293b"
            outline = "#cbd5e1"
        
        # Desenhar retângulo
        rect = self.canvas.create_rectangle(
            career.x, career.y, 
            career.x + 120, career.y + 60,
            fill=bg_color, outline=outline, width=2,
            tags=("career", f"career_{career.id}")
        )
        
        # Texto do nome
        text1 = self.canvas.create_text(
            career.x + 60, career.y + 22,
            text=career.name, font=("Arial", 10, "bold"),
            fill=text_color, tags=("career", f"career_{career.id}")
        )
        
        # Texto do nível
        text2 = self.canvas.create_text(
            career.x + 60, career.y + 45,
            text=career.level, font=("Arial", 8),
            fill=text_color if bg_color != "#f1f5f9" else "#64748b",
            tags=("career", f"career_{career.id}")
        )
        
        career.canvas_id = rect
    
    def on_canvas_click(self, event):
        """Trata clique no canvas"""
        item = self.canvas.find_withtag(tk.CURRENT)
        if item:
            tags = self.canvas.gettags(item[0])
            for tag in tags:
                if tag.startswith("career_"):
                    career_id = int(tag.split("_")[1])
                    self.select_career(career_id)
                    break
    
    def on_canvas_hover(self, event):
        """Trata hover no canvas"""
        item = self.canvas.find_withtag(tk.CURRENT)
        new_hovered = None
        
        if item:
            tags = self.canvas.gettags(item[0])
            for tag in tags:
                if tag.startswith("career_"):
                    new_hovered = int(tag.split("_")[1])
                    break
        
        if new_hovered != self.hovered_career:
            self.hovered_career = new_hovered
            self.draw_map()
    
    def select_career(self, career_id):
        """Seleciona uma carreira"""
        self.selected_career = self.careers[career_id]
        self.draw_map()
        self.show_career_details()
    
    def show_career_details(self):
        """Mostra detalhes da carreira selecionada"""
        # Limpar painel
        for widget in self.details_content.winfo_children():
            widget.destroy()
        
        career = self.selected_career
        
        # Nome e badges
        name_label = tk.Label(self.details_content, text=career.name.replace('\n', ' '),
                             font=("Arial", 14, "bold"), bg="white", fg="#1e293b")
        name_label.pack(anchor='w', pady=(0, 10))
        
        badges_frame = tk.Frame(self.details_content, bg="white")
        badges_frame.pack(anchor='w', pady=(0, 10))
        
        tk.Label(badges_frame, text=career.level, bg="#dbeafe", fg="#1e40af",
                font=("Arial", 9), padx=8, pady=3).pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(badges_frame, text=career.area, bg="#f3e8ff", fg="#6b21a8",
                font=("Arial", 9), padx=8, pady=3).pack(side=tk.LEFT)
        
        # Descrição
        desc_label = tk.Label(self.details_content, text=career.description,
                             font=("Arial", 10), bg="white", fg="#64748b",
                             justify=tk.LEFT, wraplength=250)
        desc_label.pack(anchor='w', pady=(0, 15))
        
        # Salário
        salary_frame = tk.Frame(self.details_content, bg="white")
        salary_frame.pack(anchor='w', pady=(0, 15))
        tk.Label(salary_frame, text="💰", font=("Arial", 12), bg="white").pack(side=tk.LEFT)
        tk.Label(salary_frame, text=career.salary, font=("Arial", 10, "bold"),
                bg="white", fg="#059669").pack(side=tk.LEFT, padx=5)
        
        # Habilidades
        tk.Label(self.details_content, text="📚 Habilidades Necessárias",
                font=("Arial", 11, "bold"), bg="white", fg="#1e293b").pack(anchor='w', pady=(0, 8))
        
        skills_frame = tk.Frame(self.details_content, bg="white")
        skills_frame.pack(anchor='w', fill=tk.X, pady=(0, 15))
        
        row_frame = None
        for i, skill in enumerate(career.skills):
            if i % 2 == 0:
                row_frame = tk.Frame(skills_frame, bg="white")
                row_frame.pack(anchor='w', pady=2)
            
            tk.Label(row_frame, text=skill, bg="#f1f5f9", fg="#475569",
                    font=("Arial", 8), padx=6, pady=3).pack(side=tk.LEFT, padx=2)
        
        # Próximas transições
        tk.Label(self.details_content, text="⏱️ Próximas Transições",
                font=("Arial", 11, "bold"), bg="white", fg="#1e293b").pack(anchor='w', pady=(0, 8))
        
        next_transitions = [t for t in self.transitions if t.from_id == career.id]
        
        if next_transitions:
            for trans in next_transitions:
                next_career = self.careers[trans.to_id]
                trans_frame = tk.Frame(self.details_content, bg="#f8fafc", 
                                      relief=tk.SOLID, bd=1)
                trans_frame.pack(fill=tk.X, pady=3)
                
                tk.Label(trans_frame, text=next_career.name.replace('\n', ' '),
                        font=("Arial", 10, "bold"), bg="#f8fafc", fg="#1e293b"
                        ).pack(anchor='w', padx=8, pady=(5, 2))
                
                info_text = f"Tempo: {trans.months} meses • Dificuldade: {'⭐' * trans.difficulty}"
                tk.Label(trans_frame, text=info_text, font=("Arial", 8),
                        bg="#f8fafc", fg="#64748b").pack(anchor='w', padx=8, pady=(0, 5))
        else:
            tk.Label(self.details_content, text="Nenhuma transição mapeada",
                    font=("Arial", 9), bg="white", fg="#94a3b8").pack(anchor='w')
    
    def is_connected(self, career_id):
        """Verifica se carreira está conectada à carreira em hover"""
        if not self.hovered_career:
            return False
        
        for trans in self.transitions:
            if ((trans.from_id == self.hovered_career and trans.to_id == career_id) or
                (trans.to_id == self.hovered_career and trans.from_id == career_id)):
                return True
        return False
    
    def get_visible_careers(self):
        """Retorna carreiras visíveis de acordo com filtros"""
        visible = []
        search = self.search_var.get().lower()
        
        for career in self.careers.values():
            # Filtro de busca
            if search and search not in career.name.lower():
                continue
            
            # Filtro de área
            if self.current_filter != "Todas" and career.area != self.current_filter:
                continue
            
            visible.append(career)
        
        return visible
    
    def set_filter(self, area):
        """Define filtro de área"""
        self.current_filter = area
        
        # Atualizar botões
        areas = ["Todas", "Tecnologia", "Produto", "Dados"]
        for a in areas:
            btn = getattr(self, f"btn_{a}")
            if a == area:
                btn.config(bg="#3b82f6", fg="white")
            else:
                btn.config(bg="#e2e8f0", fg="black")
        
        self.apply_filters()
    
    def apply_filters(self):
        """Aplica filtros e redesenha"""
        self.draw_map()

# Executar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = CareerMapApp(root)
    root.mainloop()
