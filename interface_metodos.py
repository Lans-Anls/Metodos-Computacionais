"""Interface gráfica para os métodos numéricos do trabalho."""
from __future__ import annotations

import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np

from aplicacao.calculos import calcular
from aplicacao.configuracao import METODOS, OPCOES_ERRO


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos")
        self.geometry("1220x820")
        self.minsize(980, 720)
        self.configure(bg="#F4F1EA")
        self.entradas: dict[str, ttk.Entry | ttk.Combobox] = {}
        self.arquivos: tuple[Path, Path] | None = None
        self._configurar_estilo()
        self._montar_interface()
        self._atualizar_metodos()

    def _configurar_estilo(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#F4F1EA")
        estilo.configure("Title.TLabel", background="#153243", foreground="white",
                         font=("Segoe UI Semibold", 20))
        estilo.configure("Section.TLabel", background="#F4F1EA", foreground="#153243",
                         font=("Segoe UI Semibold", 11))
        estilo.configure("TLabel", background="#F4F1EA", font=("Segoe UI", 10))
        estilo.configure("Accent.TButton", background="#D95D39", foreground="white",
                         font=("Segoe UI Semibold", 10), padding=(14, 8))
        estilo.map("Accent.TButton", background=[("active", "#B94728")])
        estilo.configure("Treeview.Heading", background="#153243", foreground="white",
                         font=("Segoe UI Semibold", 9))

    def _montar_interface(self):
        topo = tk.Frame(self, bg="#153243", height=82)
        topo.pack(fill="x")
        topo.pack_propagate(False)
        ttk.Label(topo, text="Laboratório de Métodos Numéricos",
                  style="Title.TLabel").pack(anchor="w", padx=28, pady=(14, 0))
        tk.Label(topo, text="Explore raízes, sistemas, interpolação e ajuste de curvas.",
                 bg="#153243", fg="#D7E3E8", font=("Segoe UI", 10)).pack(anchor="w", padx=30)

        corpo = ttk.Frame(self, padding=20)
        corpo.pack(fill="both", expand=True)
        corpo.columnconfigure(1, weight=1)
        corpo.rowconfigure(0, weight=1)

        painel_rolavel = ttk.Frame(corpo)
        painel_rolavel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        painel_rolavel.rowconfigure(0, weight=1)
        painel_rolavel.columnconfigure(0, weight=1)
        self.canvas_painel = tk.Canvas(
            painel_rolavel, width=310, background="#F4F1EA",
            highlightthickness=0, borderwidth=0)
        self.canvas_painel.grid(row=0, column=0, sticky="nsew")
        barra_painel = ttk.Scrollbar(
            painel_rolavel, orient="vertical", command=self.canvas_painel.yview)
        barra_painel.grid(row=0, column=1, sticky="ns")
        self.canvas_painel.configure(yscrollcommand=barra_painel.set)

        painel = ttk.Frame(self.canvas_painel)
        self.janela_painel = self.canvas_painel.create_window(
            (0, 0), window=painel, anchor="nw")
        painel.bind("<Configure>", self._ajustar_regiao_painel)
        self.canvas_painel.bind("<Configure>", self._ajustar_largura_painel)
        self.bind_all("<MouseWheel>", self._rolar_painel)

        ttk.Label(painel, text="1. Tipo do problema", style="Section.TLabel").pack(anchor="w")
        self.categoria = tk.StringVar(value="Linear")
        for texto in METODOS:
            ttk.Radiobutton(painel, text=texto, value=texto, variable=self.categoria,
                            command=self._atualizar_metodos).pack(anchor="w", pady=2)

        ttk.Separator(painel).pack(fill="x", pady=12)
        ttk.Label(painel, text="2. Método", style="Section.TLabel").pack(anchor="w")
        self.metodo = tk.StringVar()
        self.combo = ttk.Combobox(painel, textvariable=self.metodo, state="readonly", width=29)
        self.combo.pack(fill="x", pady=(6, 0))
        self.combo.bind("<<ComboboxSelected>>", lambda _: self._montar_campos())
        self.info = ttk.Label(painel, wraplength=285, justify="left")
        self.info.pack(anchor="w", pady=12)
        ttk.Separator(painel).pack(fill="x", pady=(0, 12))
        ttk.Label(painel, text="3. Dados de entrada", style="Section.TLabel").pack(anchor="w")
        self.formulario = ttk.Frame(painel)
        self.formulario.pack(fill="x", pady=5)
        ttk.Button(painel, text="Calcular e gerar arquivos", style="Accent.TButton",
                   command=self._calcular).pack(fill="x", pady=(12, 5))
        self.botao_arquivo = ttk.Button(painel, text="Abrir Excel", state="disabled",
                                        command=lambda: self._abrir(0))
        self.botao_arquivo.pack(fill="x", pady=3)
        self.botao_grafico = ttk.Button(painel, text="Abrir gráfico", state="disabled",
                                        command=lambda: self._abrir(1))
        self.botao_grafico.pack(fill="x", pady=3)

        resultados = ttk.Frame(corpo)
        resultados.grid(row=0, column=1, sticky="nsew")
        resultados.rowconfigure(2, weight=1)
        resultados.columnconfigure(0, weight=1)
        ttk.Label(resultados, text="Resultado", style="Section.TLabel").grid(sticky="w")
        self.resumo = ttk.Label(resultados, text="Aguardando cálculo.", wraplength=680)
        self.resumo.grid(row=1, column=0, sticky="ew", pady=(5, 10))
        tabela_frame = ttk.Frame(resultados)
        tabela_frame.grid(row=2, column=0, sticky="nsew")
        tabela_frame.rowconfigure(0, weight=1)
        tabela_frame.columnconfigure(0, weight=1)
        self.tabela = ttk.Treeview(tabela_frame, show="headings")
        self.tabela.grid(row=0, column=0, sticky="nsew")
        barra_vertical = ttk.Scrollbar(tabela_frame, orient="vertical",
                                        command=self.tabela.yview)
        barra_vertical.grid(row=0, column=1, sticky="ns")
        barra_horizontal = ttk.Scrollbar(tabela_frame, orient="horizontal",
                                          command=self.tabela.xview)
        barra_horizontal.grid(row=1, column=0, sticky="ew")
        self.tabela.configure(yscrollcommand=barra_vertical.set,
                              xscrollcommand=barra_horizontal.set)

    def _ajustar_regiao_painel(self, _evento=None):
        self.canvas_painel.configure(scrollregion=self.canvas_painel.bbox("all"))

    def _ajustar_largura_painel(self, evento):
        self.canvas_painel.itemconfigure(self.janela_painel, width=evento.width)

    def _rolar_painel(self, evento):
        x_mouse = getattr(evento, "x_root", self.winfo_pointerx())
        y_mouse = getattr(evento, "y_root", self.winfo_pointery())
        x_canvas = self.canvas_painel.winfo_rootx()
        y_canvas = self.canvas_painel.winfo_rooty()
        dentro_do_painel = (
            x_canvas <= x_mouse < x_canvas + self.canvas_painel.winfo_width()
            and y_canvas <= y_mouse < y_canvas + self.canvas_painel.winfo_height()
        )
        if not dentro_do_painel:
            return None
        deslocamento = -1 if evento.delta > 0 else 1
        self.canvas_painel.yview_scroll(deslocamento, "units")
        return "break"

    def _atualizar_metodos(self):
        opcoes = list(METODOS[self.categoria.get()])
        self.combo["values"] = opcoes
        self.metodo.set(opcoes[0])
        self._montar_campos()

    def _montar_campos(self):
        for widget in self.formulario.winfo_children():
            widget.destroy()
        self.entradas.clear()
        config = METODOS[self.categoria.get()][self.metodo.get()]
        if self.categoria.get() in ("Linear", "Não linear"):
            dica = ("Sintaxe: use * para multiplicar e ^ para potência. "
                    "Funções: sin, cos, tan, exp, ln, log, sqrt e abs. "
                    "O erro desejado pode ser selecionado ou digitado.")
        elif self.categoria.get() == "Interpolação":
            dica = ("Use ; para separar listas e vírgula ou ponto nos decimais. "
                    "Valor exato e máximo da derivada podem ficar vazios.")
        else:
            dica = ("Use ; para separar listas e vírgula ou ponto nos decimais. "
                    "A estimativa em x pode ficar vazia.")
        self.info.configure(
            text=(f"Parada: {config['criterio']}\n\n"
                  f"{dica}"))
        for linha, (chave, rotulo, padrao) in enumerate(config["campos"]):
            ttk.Label(self.formulario, text=rotulo).grid(row=linha * 2, column=0, sticky="w", pady=(5, 1))
            if chave in OPCOES_ERRO:
                entrada = ttk.Combobox(
                    self.formulario, values=OPCOES_ERRO[chave], state="normal", width=29)
                entrada.set(padrao)
            else:
                entrada = ttk.Entry(self.formulario, width=31)
                entrada.insert(0, padrao)
            entrada.grid(row=linha * 2 + 1, column=0, sticky="ew")
            self.entradas[chave] = entrada
        self.after_idle(self._ajustar_regiao_painel)

    def _calcular(self):
        try:
            dados = {chave: entrada.get() for chave, entrada in self.entradas.items()}
            colunas, linhas, resumo, excel, grafico = calcular(
                self.categoria.get(), self.metodo.get(), dados)
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            messagebox.showerror("Não foi possível calcular", str(exc), parent=self)
            return
        except Exception as exc:
            messagebox.showerror("Erro inesperado", f"Falha ao executar o método:\n{exc}", parent=self)
            return

        self.tabela.delete(*self.tabela.get_children())
        self.tabela["columns"] = colunas
        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna)
            self.tabela.column(coluna, width=105, minwidth=80, anchor="center")
        for linha in linhas:
            valores = []
            for coluna in colunas:
                valor = linha.get(coluna)
                valores.append(f"{valor:.6g}" if isinstance(valor, (float, np.floating)) else valor)
            self.tabela.insert("", "end", values=valores)
        self.resumo.configure(text=f"{resumo}\nExcel: {excel}\nGráfico: {grafico}")
        self.arquivos = (excel, grafico)
        self.botao_arquivo.configure(state="normal")
        self.botao_grafico.configure(state="normal")
        if "A tolerância não foi alcançada" in resumo:
            messagebox.showwarning(
                "Tolerância não alcançada",
                f"{resumo}\n\nA tabela parcial, o Excel e o gráfico foram gerados.",
                parent=self,
            )

    def _abrir(self, indice: int):
        if self.arquivos:
            os.startfile(self.arquivos[indice])


def main():
    Aplicacao().mainloop()


if __name__ == "__main__":
    main()
