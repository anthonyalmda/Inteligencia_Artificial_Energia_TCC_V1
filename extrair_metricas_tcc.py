#!/usr/bin/env python3
"""Extrai métricas comparativas de todos os cenários coletados."""
import pandas as pd
from pathlib import Path
from datetime import datetime

tcc_results = Path("results/tcc_coleta_completa")
metricas_todos = []
cenarios_sem_dados = []

print("=" * 70)
print("EXTRAINDO MÉTRICAS DE TODOS OS CENÁRIOS")
print("=" * 70)

# Para cada cenário
for cenario_dir in sorted(tcc_results.iterdir()):
    if not cenario_dir.is_dir() or cenario_dir.name.startswith('.') or cenario_dir.name.startswith('__'):
        continue
    
    csv_path = cenario_dir / "forecast_results.csv"
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path)
            
            if len(df) > 0:
                # Ler README para pegar descrição
                descricao = cenario_dir.name
                parametros = ""
                readme_path = cenario_dir / "README.txt"
                if readme_path.exists():
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "Descrição:" in content:
                            descricao = content.split("Descrição:")[1].split("\n")[0].strip()
                        if "Parâmetros:" in content:
                            parametros = content.split("Parâmetros:")[1].split("\n")[0].strip()
                
                metricas = {
                    "cenario": cenario_dir.name,
                    "descricao": descricao,
                    "parametros": parametros,
                    "total_periodos": len(df),
                    "lucro_liquido_total_brl": float(df['net_profit_brl'].sum()),
                    "receita_total_vendas_brl": float(df['sell_revenue_brl'].sum()),
                    "custo_total_compras_brl": float(df['buy_cost_brl'].sum()),
                    "custo_fixo_total_brl": float(df.get('fixed_cost_brl', pd.Series([0])).sum()),
                    "excedente_total_kwh": float(df['surplus_kwh'].sum()),
                    "deficit_total_kwh": float(df['deficit_kwh'].sum()),
                    "lucro_medio_por_periodo_brl": float(df['net_profit_brl'].mean()),
                    "consumo_medio_kwh": float(df['consumption_kwh'].mean()),
                    "producao_media_kwh": float(df['production_kwh'].mean()),
                    "consumo_total_kwh": float(df['consumption_kwh'].sum()),
                    "producao_total_kwh": float(df['production_kwh'].sum()),
                    "decisoes_vender": int((df['decision'] == 'Vender').sum()),
                    "decisoes_comprar": int((df['decision'] == 'Comprar').sum()),
                    "decisoes_neutro": int((df['decision'] == 'Neutro').sum()),
                    "percentual_vender": float((df['decision'] == 'Vender').sum() / len(df) * 100),
                    "percentual_comprar": float((df['decision'] == 'Comprar').sum() / len(df) * 100),
                    "percentual_neutro": float((df['decision'] == 'Neutro').sum() / len(df) * 100)
                }
                
                # Calcular ROI se houver custos
                if metricas["custo_total_compras_brl"] > 0:
                    metricas["roi_percentual"] = float(
                        (metricas["lucro_liquido_total_brl"] / metricas["custo_total_compras_brl"]) * 100
                    )
                else:
                    metricas["roi_percentual"] = None
                
                # Lucro por kWh excedente
                if metricas["excedente_total_kwh"] > 0:
                    metricas["lucro_por_kwh_excedente_brl"] = float(
                        metricas["lucro_liquido_total_brl"] / metricas["excedente_total_kwh"]
                    )
                else:
                    metricas["lucro_por_kwh_excedente_brl"] = None
                
                metricas_todos.append(metricas)
                print(f"[OK] {cenario_dir.name}: {len(df)} períodos")
            else:
                cenarios_sem_dados.append(cenario_dir.name)
                print(f"[AVISO] {cenario_dir.name}: CSV vazio")
        except Exception as e:
            cenarios_sem_dados.append(f"{cenario_dir.name} (erro: {str(e)[:30]})")
            print(f"[ERRO] {cenario_dir.name}: {e}")
    else:
        cenarios_sem_dados.append(cenario_dir.name)
        print(f"[AVISO] {cenario_dir.name}: CSV não encontrado")

# Criar DataFrame comparativo
if metricas_todos:
    df_metricas = pd.DataFrame(metricas_todos)
    
    # Reordenar colunas (mais importantes primeiro)
    colunas_ordenadas = [
        'cenario', 'descricao', 'parametros', 'total_periodos',
        'lucro_liquido_total_brl', 'receita_total_vendas_brl', 'custo_total_compras_brl',
        'excedente_total_kwh', 'deficit_total_kwh',
        'consumo_total_kwh', 'producao_total_kwh',
        'consumo_medio_kwh', 'producao_media_kwh',
        'lucro_medio_por_periodo_brl',
        'decisoes_vender', 'decisoes_comprar', 'decisoes_neutro',
        'percentual_vender', 'percentual_comprar', 'percentual_neutro',
        'roi_percentual', 'lucro_por_kwh_excedente_brl'
    ]
    
    # Garantir que todas as colunas existem
    colunas_finais = [c for c in colunas_ordenadas if c in df_metricas.columns]
    colunas_finais += [c for c in df_metricas.columns if c not in colunas_finais]
    df_metricas = df_metricas[colunas_finais]
    
    # Salvar CSV
    output_csv = tcc_results / "metricas_comparativas.csv"
    df_metricas.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"\n[OK] Métricas CSV salvas: {output_csv}")
    
    # Tentar salvar Excel (se openpyxl estiver instalado)
    try:
        output_excel = tcc_results / "metricas_comparativas.xlsx"
        df_metricas.to_excel(output_excel, index=False, sheet_name='Metricas')
        print(f"[OK] Métricas Excel salvas: {output_excel}")
    except ImportError:
        print("[AVISO] openpyxl não instalado - pulando Excel (instale com: pip install openpyxl)")
    
    # Criar relatório em Markdown
    relatorio_md = tcc_results / "ANALISE_METRICAS.md"
    with open(relatorio_md, 'w', encoding='utf-8') as f:
        f.write("# ANÁLISE DE MÉTRICAS - TODOS OS CENÁRIOS\n\n")
        f.write(f"**Data de Extração**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total de Cenários Analisados**: {len(metricas_todos)}\n\n")
        
        f.write("---\n\n")
        f.write("## 📊 TABELA COMPARATIVA COMPLETA\n\n")
        f.write("| Cenário | Lucro Total (R$) | Excedente (kWh) | Déficit (kWh) | Vender | Comprar | Lucro Médio (R$) |\n")
        f.write("|---------|------------------|-----------------|---------------|--------|---------|-------------------|\n")
        
        for m in metricas_todos:
            nome_curto = m['cenario'].replace('_', ' ').title()
            f.write(f"| {nome_curto} | R$ {m['lucro_liquido_total_brl']:.2f} | "
                   f"{m['excedente_total_kwh']:.2f} | {m['deficit_total_kwh']:.2f} | "
                   f"{m['decisoes_vender']} | {m['decisoes_comprar']} | "
                   f"R$ {m['lucro_medio_por_periodo_brl']:.2f} |\n")
        
        f.write("\n---\n\n")
        f.write("## 📈 RANKINGS\n\n")
        
        # Melhor lucro
        melhor_lucro = max(metricas_todos, key=lambda x: x['lucro_liquido_total_brl'])
        f.write(f"### 🏆 Melhor Lucro Líquido\n")
        f.write(f"- **Cenário**: {melhor_lucro['cenario']}\n")
        f.write(f"- **Lucro**: R$ {melhor_lucro['lucro_liquido_total_brl']:.2f}\n")
        f.write(f"- **Descrição**: {melhor_lucro['descricao']}\n\n")
        
        # Maior excedente
        maior_excedente = max(metricas_todos, key=lambda x: x['excedente_total_kwh'])
        f.write(f"### ⚡ Maior Excedente\n")
        f.write(f"- **Cenário**: {maior_excedente['cenario']}\n")
        f.write(f"- **Excedente**: {maior_excedente['excedente_total_kwh']:.2f} kWh\n\n")
        
        # Mais decisões de venda
        mais_vendas = max(metricas_todos, key=lambda x: x['decisoes_vender'])
        f.write(f"### 💰 Mais Decisões de Venda\n")
        f.write(f"- **Cenário**: {mais_vendas['cenario']}\n")
        f.write(f"- **Decisões de Vender**: {mais_vendas['decisoes_vender']} ({mais_vendas['percentual_vender']:.1f}%)\n\n")
        
        f.write("---\n\n")
        f.write("## 📋 DETALHES POR CENÁRIO\n\n")
        
        for m in metricas_todos:
            f.write(f"### {m['cenario']}\n\n")
            f.write(f"**Descrição**: {m['descricao']}\n\n")
            f.write(f"**Parâmetros**: {m['parametros']}\n\n")
            f.write(f"**Métricas Principais:**\n")
            f.write(f"- Lucro Líquido Total: R$ {m['lucro_liquido_total_brl']:.2f}\n")
            f.write(f"- Receita Total de Vendas: R$ {m['receita_total_vendas_brl']:.2f}\n")
            f.write(f"- Custo Total de Compras: R$ {m['custo_total_compras_brl']:.2f}\n")
            f.write(f"- Excedente Total: {m['excedente_total_kwh']:.2f} kWh\n")
            f.write(f"- Déficit Total: {m['deficit_total_kwh']:.2f} kWh\n")
            f.write(f"- Lucro Médio por Período: R$ {m['lucro_medio_por_periodo_brl']:.2f}\n")
            if m['roi_percentual']:
                f.write(f"- ROI: {m['roi_percentual']:.2f}%\n")
            f.write(f"- Consumo Médio: {m['consumo_medio_kwh']:.2f} kWh\n")
            f.write(f"- Produção Média: {m['producao_media_kwh']:.2f} kWh\n")
            f.write(f"- Decisões: Vender={m['decisoes_vender']} ({m['percentual_vender']:.1f}%), "
                   f"Comprar={m['decisoes_comprar']} ({m['percentual_comprar']:.1f}%), "
                   f"Neutro={m['decisoes_neutro']} ({m['percentual_neutro']:.1f}%)\n\n")
            f.write("---\n\n")
        
        if cenarios_sem_dados:
            f.write("## ⚠️ CENÁRIOS SEM DADOS\n\n")
            for cenario in cenarios_sem_dados:
                f.write(f"- {cenario}\n")
            f.write("\n")
    
    print(f"[OK] Relatório Markdown salvo: {relatorio_md}")
    
    # Mostrar resumo no terminal
    print("\n" + "=" * 70)
    print("RESUMO COMPARATIVO")
    print("=" * 70)
    print("\nCenários com melhor desempenho:\n")
    df_sorted = df_metricas.sort_values('lucro_liquido_total_brl', ascending=False)
    print(df_sorted[['cenario', 'lucro_liquido_total_brl', 'excedente_total_kwh', 
                     'decisoes_vender', 'decisoes_comprar']].head(5).to_string(index=False))
    
else:
    print("[ERRO] Nenhuma métrica extraída. Verifique se os cenários foram executados.")

if cenarios_sem_dados:
    print(f"\n[AVISO] {len(cenarios_sem_dados)} cenários sem dados: {', '.join(cenarios_sem_dados[:5])}")

print("\n" + "=" * 70)
print("[OK] Extração de métricas concluida!")
print("=" * 70)

