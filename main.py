import tkinter as tk
from tkinter import messagebox, ttk

# --- Dados Iniciais de Teste com as Mesas Reais ---
RESERVAS_INICIAIS = [
    {
        "id": 1,
        "time": "19:30",
        "name": "João Silva",
        "pax": 4,
        "table_name": "Sala Fado Maior - Mesa 2",
        "status": "Confirmada",
        "comment": "Cadeira de bebé pedida",
    },
    {
        "id": 2,
        "time": "19:45",
        "name": "Maria Santos",
        "pax": 2,
        "table_name": "Sala Fado Maior - Mesa 4",
        "status": "Confirmada",
        "comment": "Aniversário (trazer sobremesa)",
    },
    {
        "id": 3,
        "time": "20:00",
        "name": "Carlos Pereira",
        "pax": 6,
        "table_name": "Sala Fado Maior - Mesa 21",
        "status": "Pendente",
        "comment": "Mesa próxima do palco",
    },
    {
        "id": 4,
        "time": "20:15",
        "name": "Ana Oliveira",
        "pax": 3,
        "table_name": "Sala Fado Menor - Mesa 31",
        "status": "Confirmada",
        "comment": "Clientes habituais",
    },
    {
        "id": 5,
        "time": "20:30",
        "name": "Rui Costa",
        "pax": 5,
        "table_name": "Sala Fado Menor - Mesa 38",
        "status": "Confirmada",
        "comment": "Alergia severa a marisco",
    },
]


class ZenChefFadoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("ZenChef - Clube de Fado (Gestão de Sala)")

    try:
      self.root.state("zoomed")
    except:
      self.root.geometry("1200x800")

    self.root.configure(bg="#0f172a")
    self.reservas = list(RESERVAS_INICIAIS)

    self.configurar_estilos()
    self.criar_interface()
    self.atualizar_tudo()

  def configurar_estilos(self):
    self.style = ttk.Style()
    self.style.theme_use("clam")
    self.style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 12, "bold"),
        background="#334155",
        foreground="white",
        relief="flat",
    )
    self.style.configure(
        "Treeview",
        font=("Segoe UI", 11),
        rowheight=45,
        background="#1e293b",
        foreground="white",
        fieldbackground="#1e293b",
        relief="flat",
    )
    self.style.map(
        "Treeview",
        background=[("selected", "#3b82f6")],
        foreground=[("selected", "white")],
    )

  def criar_interface(self):
    # --- Cabeçalho ---
    header = tk.Frame(self.root, bg="#1e293b", height=80)
    header.pack(fill="x", padx=15, pady=15)
    header.pack_propagate(False)

    tk.Label(
        header,
        text="🎵 CLUBE DE FADO — GESTÃO OFICIAL",
        font=("Segoe UI", 16, "bold"),
        fg="#f8fafc",
        bg="#1e293b",
    ).pack(side="left", padx=20)

    tk.Button(
        header,
        text="🗑️ Apagar",
        font=("Segoe UI", 10, "bold"),
        bg="#ef4444",
        fg="white",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        command=self.apagar,
    ).pack(side="right", padx=10)

    tk.Button(
        header,
        text="✓ Marcar 'Chegou'",
        font=("Segoe UI", 10, "bold"),
        bg="#10b981",
        fg="white",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        command=self.chegou,
    ).pack(side="right", padx=5)

    tk.Button(
        header,
        text="➕ Adicionar Reserva",
        font=("Segoe UI", 10, "bold"),
        bg="#3b82f6",
        fg="white",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        command=self.adicionar,
    ).pack(side="right", padx=5)

    # --- Abas ---
    self.notebook = ttk.Notebook(self.root)
    self.notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    # Aba 1: Lista de Reservas
    self.tab_lista = tk.Frame(self.notebook, bg="#0f172a")
    self.notebook.add(self.tab_lista, text="   📋 Lista de Reservas   ")

    colunas = ("id", "hora", "nome", "pax", "mesa", "estado", "obs")
    self.tree = ttk.Treeview(
        self.tab_lista, columns=colunas, show="headings", selectmode="browse"
    )

    for col, txt, w in [
        ("id", "ID", 50),
        ("hora", "Hora", 90),
        ("nome", "Cliente", 250),
        ("pax", "Pax", 80),
        ("mesa", "Mesa / Sala", 220),
        ("estado", "Estado", 130),
        ("obs", "Observações", 300),
    ]:
      self.tree.heading(col, text=txt)
      self.tree.column(
          col,
          width=w,
          anchor="center" if col != "nome" and col != "obs" else "w",
      )

    self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    sb = ttk.Scrollbar(
        self.tab_lista, orient="vertical", command=self.tree.yview
    )
    self.tree.configure(yscroll=sb.set)
    sb.pack(side="right", fill="y", pady=10)

    # Aba 2: Mapa das Mesas com as Salas Reais
    self.tab_mapa = tk.Frame(self.notebook, bg="#0f172a")
    self.notebook.add(self.tab_mapa, text="   🗺️ Mapa das Mesas   ")

    mapa_container = tk.Frame(self.tab_mapa, bg="#0f172a")
    mapa_container.pack(fill="both", expand=True, padx=10, pady=10)

    self.f_maior = tk.LabelFrame(
        mapa_container,
        text=" Sala Fado Maior[span_2](start_span)[span_2](end_span) ",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg="#1e293b",
    )
    self.f_maior.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    self.grid_maior = tk.Frame(self.f_maior, bg="#1e293b")
    self.grid_maior.pack(fill="both", expand=True, padx=10, pady=10)

    self.f_menor = tk.LabelFrame(
        mapa_container,
        text=" Sala Fado Menor[span_3](start_span)[span_3](end_span) ",
        font=("Segoe UI", 12, "bold"),
        fg="white",
        bg="#1e293b",
    )
    self.f_menor.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    self.grid_menor = tk.Frame(self.f_menor, bg="#1e293b")
    self.grid_menor.pack(fill="both", expand=True, padx=10, pady=10)

  def atualizar_tudo(self):
    for row in self.tree.get_children():
      self.tree.delete(row)

    for r in self.reservas:
      self.tree.insert(
          "",
          "end",
          values=(
              r["id"],
              r["time"],
              r["name"],
              f"{r['pax']} pax",
              r["table_name"],
              r["status"],
              r["comment"],
          ),
      )

    self.atualizar_mapa()

  def atualizar_mapa(self):
    for w in self.grid_maior.winfo_children():
      w.destroy()
    for w in self.grid_menor.winfo_children():
      w.destroy()

    ocupadas = {}
    for r in self.reservas:
      for m_num in [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          "20-19",
          21,
          24,
          25,
          26,
          28,
          30,
          31,
          32,
          33,
          35,
          36,
          37,
          38,
          39,
          40,
          41,
          42,
          43,
          44,
          45,
          46,
          47,
          48,
          49,
      ]:
        if f"Mesa {m_num}" in r["table_name"]:
          ocupadas[str(m_num)] = {"cli": r["name"], "pax": r["pax"]}

    # Mesas exatas da Sala Fado Maior (conforme a imagem 7)[span_4](start_span)[span_4](end_span)
    mesas_maior = [
        21,
        "20-19",
        24,
        25,
        28,
        18,
        17,
        16,
        26,
        15,
        9,
        14,
        8,
        13,
        7,
        12,
        6,
        11,
        5,
        10,
        4,
        30,
        3,
        2,
        1,
    ]
    for idx, m_num in enumerate(mesas_maior):
      m_id = str(m_num)
      ocupada = m_id in ocupadas
      bg_c = "#1e3a8a" if ocupada else "#0f172a"
      card = tk.Frame(
          self.grid_maior,
          bg=bg_c,
          bd=2,
          relief="solid",
          highlightbackground="#3b82f6" if ocupada else "#334155",
      )
      card.grid(row=idx // 5, column=idx % 5, padx=5, pady=5, sticky="nsew")
      self.grid_maior.rowconfigure(idx // 5, weight=1)
      self.grid_maior.columnconfigure(idx % 5, weight=1)

      tk.Label(
          card, text=f"Mesa {m_id}", font=("Segoe UI", 9, "bold"), fg="white", bg=bg_c
      ).pack(pady=(6, 2))
      txt = (
          f"{ocupadas[m_id]['cli'][:10]}\n({ocupadas[m_id]['pax']}p)"
          if ocupada
          else "Livre"
      )
      tk.Label(
          card,
          text=txt,
          font=("Segoe UI", 8),
          fg="#93c5fd" if ocupada else "#64748b",
          bg=bg_c,
      ).pack(pady=(0, 6))

    # Mesas exatas da Sala Fado Menor (conforme a imagem 8)[span_5](start_span)[span_5](end_span)
    mesas_menor = [
        31,
        32,
        33,
        35,
        37,
        39,
        41,
        43,
        36,
        38,
        40,
        42,
        44,
        49,
        48,
        45,
        46,
        47,
    ]
    for idx, m_num in enumerate(mesas_menor):
      m_id = str(m_num)
      ocupada = m_id in ocupadas
      bg_c = "#1e3a8a" if ocupada else "#0f172a"
      card = tk.Frame(
          self.grid_menor,
          bg=bg_c,
          bd=2,
          relief="solid",
          highlightbackground="#3b82f6" if ocupada else "#334155",
      )
      card.grid(row=idx // 4, column=idx % 4, padx=5, pady=5, sticky="nsew")
      self.grid_menor.rowconfigure(idx // 4, weight=1)
      self.grid_menor.columnconfigure(idx % 4, weight=1)

      tk.Label(
          card, text=f"Mesa {m_id}", font=("Segoe UI", 9, "bold"), fg="white", bg=bg_c
      ).pack(pady=(6, 2))
      txt = (
          f"{ocupadas[m_id]['cli'][:10]}\n({ocupadas[m_id]['pax']}p)"
          if ocupada
          else "Livre"
      )
      tk.Label(
          card,
          text=txt,
          font=("Segoe UI", 8),
          fg="#93c5fd" if ocupada else "#64748b",
          bg=bg_c,
      ).pack(pady=(0, 6))

  def chegou(self):
    sel = self.tree.selection()
    if not sel:
      return messagebox.showwarning("Aviso", "Seleciona uma reserva na lista.")
    rid = int(self.tree.item(sel[0])["values"][0])
    for r in self.reservas:
      if r["id"] == rid:
        r["status"] = "Chegou"
    self.atualizar_tudo()

  def apagar(self):
    sel = self.tree.selection()
    if not sel:
      return messagebox.showwarning("Aviso", "Seleciona uma reserva na lista.")
    rid = int(self.tree.item(sel[0])["values"][0])
    self.reservas = [r for r in self.reservas if r["id"] != rid]
    self.atualizar_tudo()

  def adicionar(self):
    top = tk.Toplevel(self.root)
    top.title("Nova Reserva")
    top.geometry("350x400")
    top.configure(bg="#1e293b")

    tk.Label(top, text="Nome:", fg="white", bg="#1e293b").pack(
        anchor="w", padx=20, pady=(15, 0)
    )
    e_nome = tk.Entry(top, width=30)
    e_nome.pack(padx=20, pady=5)
    e_nome.insert(0, "Novo Cliente")

    tk.Label(
        top, text="Mesa (ex: Sala Fado Maior - Mesa 2):", fg="white", bg="#1e293b"
    ).pack(anchor="w", padx=20, pady=(10, 0))
    e_mesa = tk.Entry(top, width=30)
    e_mesa.pack(padx=20, pady=5)
    e_mesa.insert(0, "Sala Fado Maior - Mesa 2")

    def salvar():
      nid = max([r["id"] for r in self.reservas], default=0) + 1
      self.reservas.append({
          "id": nid,
          "time": "20:00",
          "name": e_nome.get(),
          "pax": 2,
          "table_name": e_mesa.get(),
          "status": "Confirmada",
          "comment": "Adicionada manualmente",
      })
      self.atualizar_tudo()
      top.destroy()

    tk.Button(
        top,
        text="Guardar",
        bg="#10b981",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        command=salvar,
    ).pack(pady=20)


if __name__ == "__main__":
  root = tk.Tk()
  app = ZenChefFadoApp(root)
  root.mainloop()
