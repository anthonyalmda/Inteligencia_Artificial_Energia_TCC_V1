"""Interface gráfica Tkinter para visualização de resultados."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pathlib import Path
from typing import Optional
import numpy as np

from .plots import plot_forecast_comparison, plot_surplus_deficit, plot_cumulative_profit

class MainApplication(tk.Tk):
    """Interface principal da aplicação."""
    
    def __init__(self, data_frame: pd.DataFrame, output_dir: Path):
        """
        Args:
            data_frame: DataFrame com resultados da análise
            output_dir: Diretório com gráficos salvos
        """
        super().__init__()
        
        self.data_frame = data_frame
        self.output_dir = Path(output_dir)
        self.filtered_df = data_frame.copy()
        
        self.title("Análise de Energia - TCC")
        self.geometry("1600x900")
        
        # Criar widgets
        self.create_widgets()
        
        # Carregar gráficos
        self.load_plots()
    
    def create_widgets(self):
        """Cria todos os widgets da interface."""
        # Frame principal com notebook (abas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Aba 1: Tabela de dados
        self.create_data_tab(notebook)
        
        # Aba 2: Gráficos
        self.create_plots_tab(notebook)
        
        # Aba 3: Resumo
        self.create_summary_tab(notebook)
        
        # Barra de status
        self.status_bar = ttk.Label(
            self,
            text=f"Total de registros: {len(self.data_frame)}",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_data_tab(self, notebook):
        """Cria aba com tabela de dados."""
        data_frame = ttk.Frame(notebook, padding="10")
        notebook.add(data_frame, text="📊 Dados")
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(data_frame, text="Filtros", padding="10")
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Filtro por decisão
        ttk.Label(filter_frame, text="Decisão:").grid(row=0, column=0, sticky="w", padx=5)
        self.decision_filter = ttk.Combobox(
            filter_frame,
            values=["Todos"] + list(self.data_frame['decision'].unique()),
            state="readonly",
            width=15
        )
        self.decision_filter.set("Todos")
        self.decision_filter.grid(row=0, column=1, padx=5)
        self.decision_filter.bind("<<ComboboxSelected>>", self.apply_filters)
        
        # Botão de reset
        ttk.Button(
            filter_frame,
            text="Limpar Filtros",
            command=self.reset_filters
        ).grid(row=0, column=2, padx=10)
        
        # Botão de exportar
        ttk.Button(
            filter_frame,
            text="Exportar CSV",
            command=self.export_csv
        ).grid(row=0, column=3, padx=10)
        
        # Frame para tabela com scroll
        table_frame = ttk.Frame(data_frame)
        table_frame.pack(fill="both", expand=True)
        
        # Treeview (tabela)
        columns = list(self.data_frame.columns)
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configurar colunas
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, anchor="center", width=120)
        
        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Preencher tabela
        self.populate_table()
    
    def create_plots_tab(self, notebook):
        """Cria aba com gráficos."""
        plots_frame = ttk.Frame(notebook, padding="10")
        notebook.add(plots_frame, text="📈 Gráficos")
        
        # Notebook para múltiplos gráficos
        plots_notebook = ttk.Notebook(plots_frame)
        plots_notebook.pack(fill="both", expand=True)
        
        # Gráfico 1: Previsão
        self.create_plot_subtab(
            plots_notebook,
            "Previsão",
            self.output_dir / "forecast_comparison.png"
        )
        
        # Gráfico 2: Excedente/Déficit
        self.create_plot_subtab(
            plots_notebook,
            "Excedente/Déficit",
            self.output_dir / "surplus_deficit.png"
        )
        
        # Gráfico 3: Lucro Acumulado
        self.create_plot_subtab(
            plots_notebook,
            "Lucro Acumulado",
            self.output_dir / "cumulative_profit.png"
        )
        
        # Gráfico dinâmico
        self.create_dynamic_plot_tab(plots_notebook)
    
    def create_plot_subtab(self, parent, title, image_path):
        """Cria subtab com gráfico estático."""
        frame = ttk.Frame(parent, padding="10")
        parent.add(frame, text=title)
        
        if image_path.exists():
            fig, ax = plt.subplots(figsize=(10, 5))
            img = plt.imread(image_path)
            ax.imshow(img)
            ax.axis('off')
            
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        else:
            ttk.Label(
                frame,
                text=f"Gráfico não encontrado: {image_path}",
                font=("Arial", 12)
            ).pack(expand=True)
    
    def create_dynamic_plot_tab(self, parent):
        """Cria subtab com gráfico gerado dinamicamente."""
        frame = ttk.Frame(parent, padding="10")
        parent.add(frame, text="Gráfico Dinâmico")
        
        # Opções de gráfico
        options_frame = ttk.Frame(frame)
        options_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(options_frame, text="Tipo:").pack(side=tk.LEFT, padx=5)
        self.plot_type = ttk.Combobox(
            options_frame,
            values=["Lucro Acumulado", "Excedente/Déficit", "Receitas/Custos"],
            state="readonly",
            width=20
        )
        self.plot_type.set("Lucro Acumulado")
        self.plot_type.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            options_frame,
            text="Atualizar",
            command=self.update_dynamic_plot
        ).pack(side=tk.LEFT, padx=10)
        
        # Frame para o gráfico
        self.plot_frame = ttk.Frame(frame)
        self.plot_frame.pack(fill="both", expand=True)
        
        # Gerar gráfico inicial
        self.update_dynamic_plot()
    
    def create_summary_tab(self, notebook):
        """Cria aba com resumo estatístico."""
        summary_frame = ttk.Frame(notebook, padding="20")
        notebook.add(summary_frame, text="📋 Resumo")
        
        # Criar texto de resumo
        summary_text = self.generate_summary()
        
        text_widget = tk.Text(
            summary_frame,
            wrap=tk.WORD,
            font=("Courier", 11),
            padx=10,
            pady=10
        )
        text_widget.insert("1.0", summary_text)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(summary_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
    
    def generate_summary(self) -> str:
        """Gera texto de resumo estatístico."""
        df = self.filtered_df
        
        summary = "=" * 70 + "\n"
        summary += " RESUMO ESTATÍSTICO\n"
        summary += "=" * 70 + "\n\n"
        
        summary += f"Total de Períodos: {len(df)}\n\n"
        
        summary += "--- CONSUMO E PRODUÇÃO ---\n"
        summary += f"Consumo Médio: {df['consumption_kwh'].mean():.2f} kWh\n"
        summary += f"Produção Média: {df['production_kwh'].mean():.2f} kWh\n"
        summary += f"Excedente Total: {df['surplus_kwh'].sum():.2f} kWh\n"
        summary += f"Déficit Total: {df['deficit_kwh'].sum():.2f} kWh\n\n"
        
        summary += "--- FINANCEIRO ---\n"
        summary += f"Receita Total de Vendas: R$ {df['sell_revenue_brl'].sum():.2f}\n"
        summary += f"Custo Total de Compras: R$ {df['buy_cost_brl'].sum():.2f}\n"
        summary += f"Custo Fixo Total: R$ {df.get('fixed_cost_brl', pd.Series([0])).sum():.2f}\n"
        summary += f"Lucro Líquido Total: R$ {df['net_profit_brl'].sum():.2f}\n\n"
        
        summary += "--- DECISÕES ---\n"
        decisions = df['decision'].value_counts()
        for decision, count in decisions.items():
            pct = (count / len(df)) * 100
            summary += f"{decision}: {count} períodos ({pct:.1f}%)\n"
        
        summary += "\n" + "=" * 70 + "\n"
        
        return summary
    
    def populate_table(self):
        """Preenche a tabela com dados."""
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Inserir dados filtrados
        for index, row in self.filtered_df.iterrows():
            values = [str(row[col]) for col in self.data_frame.columns]
            self.tree.insert("", "end", values=values)
        
        self.status_bar.config(text=f"Registros exibidos: {len(self.filtered_df)} / {len(self.data_frame)}")
    
    def apply_filters(self, event=None):
        """Aplica filtros selecionados."""
        self.filtered_df = self.data_frame.copy()
        
        # Filtro por decisão
        decision = self.decision_filter.get()
        if decision != "Todos":
            self.filtered_df = self.filtered_df[self.filtered_df['decision'] == decision]
        
        self.populate_table()
    
    def reset_filters(self):
        """Reseta todos os filtros."""
        self.decision_filter.set("Todos")
        self.filtered_df = self.data_frame.copy()
        self.populate_table()
    
    def sort_column(self, col):
        """Ordena coluna quando clicada."""
        # Alternar ordem
        if not hasattr(self, 'sort_reverse') or col != getattr(self, 'sort_col', None):
            self.sort_reverse = False
        else:
            self.sort_reverse = not self.sort_reverse
        
        self.sort_col = col
        
        # Ordenar DataFrame
        self.filtered_df = self.filtered_df.sort_values(
            by=col,
            ascending=not self.sort_reverse
        )
        self.populate_table()
    
    def export_csv(self):
        """Exporta DataFrame filtrado para CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.filtered_df.to_csv(file_path, index=False)
            messagebox.showinfo("Sucesso", f"Arquivo salvo em: {file_path}")
    
    def update_dynamic_plot(self):
        """Atualiza gráfico dinâmico."""
        # Limpar frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        plot_type = self.plot_type.get()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if plot_type == "Lucro Acumulado":
            plot_cumulative_profit(self.filtered_df)
            fig = plt.gcf()
        elif plot_type == "Excedente/Déficit":
            plot_surplus_deficit(self.filtered_df)
            fig = plt.gcf()
        elif plot_type == "Receitas/Custos":
            periods = range(len(self.filtered_df))
            ax.bar(periods, self.filtered_df['sell_revenue_brl'], 
                   label="Receitas (Venda)", color='green', alpha=0.7)
            ax.bar(periods, -self.filtered_df['buy_cost_brl'], 
                   label="Custos (Compra)", color='red', alpha=0.7)
            ax.set_xlabel("Período")
            ax.set_ylabel("Valor (R$)")
            ax.set_title("Receitas vs Custos")
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def load_plots(self):
        """Carrega gráficos salvos (já criados na aba de gráficos)."""
        pass  # Gráficos já são carregados na criação das abas

if __name__ == "__main__":
    # Exemplo de uso
    df_exemplo = pd.DataFrame({
        "timestamp": pd.date_range(start="2024-01-01", periods=10, freq="D"),
        "consumption_kwh": np.random.uniform(80, 120, 10),
        "production_kwh": np.random.uniform(90, 130, 10),
        "surplus_kwh": np.maximum(0, np.random.uniform(-10, 30, 10)),
        "deficit_kwh": np.maximum(0, np.random.uniform(-10, 20, 10)),
        "sell_revenue_brl": np.random.uniform(0, 50, 10),
        "buy_cost_brl": np.random.uniform(0, 30, 10),
        "net_profit_brl": np.random.uniform(-20, 40, 10),
        "decision": np.random.choice(["Vender", "Comprar", "Neutro"], 10)
    })
    
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    
    app = MainApplication(df_exemplo, output_dir)
    app.mainloop()

