# interface.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainApplication(tk.Tk):
    def __init__(self, data_frame, graph_path):
        super().__init__()
        self.title("Análise de Energia")
        self.geometry("1600x800")

        self.data_frame = data_frame
        self.graph_path = graph_path
        self.create_widgets()

    def create_widgets(self):
        # Frame para a tabela de dados
        data_frame = ttk.Frame(self, padding="10")
        data_frame.pack(side="top", fill="both", expand=True)

        # Adicionar o Treeview (tabela)
        all_columns = list(self.data_frame.columns)
        self.tree = ttk.Treeview(data_frame, columns=all_columns, show="headings")
    
        # Adicionar os cabeçalhos para TODAS as colunas
        for col in all_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center") 
        
        # Inserir os dados na tabela
        for index, row in self.data_frame.iterrows():
            self.tree.insert("", "end", values=list(row))

        self.tree.pack(fill="both", expand=True)

        # Frame para os gráficos
        graph_frame = ttk.Frame(self, padding="10")
        graph_frame.pack(side="bottom", fill="both", expand=True)

        # Adicionar o gráfico Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4))
        img = plt.imread(self.graph_path)
        ax.imshow(img)
        ax.axis('off')  # Desliga os eixos
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)

        self.update_idletasks() # Atualiza a geometria da janela

if __name__ == "__main__":
    # Exemplo de uso
    # Este DataFrame e o caminho do gráfico viriam do seu run_pipeline.py
    
    # Exemplo de DataFrame de resultados
    df_exemplo = pd.DataFrame({
        "Periodo": range(1, 11),
        "Consumo": [100, 120, 110, 95, 105, 130, 125, 140, 115, 100],
        "Producao": [110, 115, 90, 100, 120, 140, 100, 130, 105, 95],
        "Decisao": ["Vender"]*10,
        "Lucro": [5.0, -2.5, 0.0, 3.0, 10.0, 5.0, -10.0, 8.0, 2.5, 0.0]
    })
    
    # Supondo que você tem um gráfico salvo como 'forecast_graph.png'
    # No seu código real, você passaria o caminho para o arquivo salvo
    
    app = MainApplication(df_exemplo, "results/forecast_graph.png")
    app.mainloop()