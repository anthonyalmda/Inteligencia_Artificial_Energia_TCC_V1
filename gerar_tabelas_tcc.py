#!/usr/bin/env python3
"""Gera tabelas formatadas para o TCC em LaTeX e Markdown."""
import pandas as pd
from pathlib import Path
import re

tcc_results = Path("results/tcc_coleta_completa")

# Carregar métricas comparativas
df_metricas = pd.read_csv(tcc_results / "metricas_comparativas.csv")

# Mapear nomes de cenários para nomes mais legíveis
nome_cenarios = {
    '01_baseline': 'Baseline',
    '02_sao_paulo_pvgis': 'São Paulo PVGIS',
    '03_horizon_7': 'Horizonte 7 dias',
    '04_horizon_30': 'Horizonte 30 dias',
    '05_regiao_ne': 'Região NE',
    '06_rio_de_janeiro_pvgis': 'Rio de Janeiro PVGIS',
    '07_brasilia_pvgis': 'Brasília PVGIS',
    '08_treino_curto': 'Treino Curto',
    '09_treino_longo': 'Treino Longo'
}

def extrair_metricas_validacao(cenario_dir):
    """Extrai métricas de validação do arquivo execucao_output.txt"""
    output_path = cenario_dir / "execucao_output.txt"
    if not output_path.exists():
        return None
    
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metricas = {}
    
    # Buscar métricas de consumo
    consumo_match = re.search(r'Consumo - MAE: ([\d.]+) kWh, RMSE: ([\d.]+) kWh', content)
    if consumo_match:
        metricas['consumo_mae'] = float(consumo_match.group(1))
        metricas['consumo_rmse'] = float(consumo_match.group(2))
    
    consumo_mape = re.search(r'Consumo - MAPE: ([\d.]+)%, R²: ([\d.-]+)', content)
    if consumo_mape:
        metricas['consumo_mape'] = float(consumo_mape.group(1))
        metricas['consumo_r2'] = float(consumo_mape.group(2))
    
    # Buscar métricas de produção
    prod_match = re.search(r'Producao - MAE: ([\d.]+) kWh, RMSE: ([\d.]+) kWh', content)
    if prod_match:
        metricas['producao_mae'] = float(prod_match.group(1))
        metricas['producao_rmse'] = float(prod_match.group(2))
    
    prod_mape = re.search(r'Producao - MAPE: ([\d.]+)%, R²: ([\d.-]+)', content)
    if prod_mape:
        metricas['producao_mape'] = float(prod_mape.group(1))
        metricas['producao_r2'] = float(prod_mape.group(2))
    
    return metricas if metricas else None

def extrair_estatisticas_descritivas(cenario_dir):
    """Extrai estatísticas descritivas do output"""
    output_path = cenario_dir / "execucao_output.txt"
    if not output_path.exists():
        return None
    
    with open(output_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    stats = {}
    in_stats = False
    
    for i, line in enumerate(lines):
        if 'Estatisticas dos dados historicos:' in line:
            in_stats = True
            continue
        
        if in_stats and 'count' in line.lower():
            # Processar linhas de estatísticas
            for j in range(i, min(i+8, len(lines))):
                stat_line = lines[j].strip()
                if stat_line and not stat_line.startswith('='):
                    parts = stat_line.split()
                    if len(parts) >= 3:
                        stat_name = parts[0]
                        consumo_val = parts[1]
                        producao_val = parts[2]
                        
                        if stat_name == 'count':
                            stats['count'] = (float(consumo_val), float(producao_val))
                        elif stat_name == 'mean':
                            stats['mean'] = (float(consumo_val), float(producao_val))
                        elif stat_name == 'std':
                            stats['std'] = (float(consumo_val), float(producao_val))
                        elif stat_name == 'min':
                            stats['min'] = (float(consumo_val), float(producao_val))
                        elif stat_name == '25%':
                            stats['q25'] = (float(consumo_val), float(producao_val))
                        elif stat_name == '50%':
                            stats['q50'] = (float(consumo_val), float(producao_val))
                        elif stat_name == '75%':
                            stats['q75'] = (float(consumo_val), float(producao_val))
                        elif stat_name == 'max':
                            stats['max'] = (float(consumo_val), float(producao_val))
                            break
            break
    
    return stats if stats else None

# Coletar métricas de validação de todos os cenários
validacoes = {}
for cenario in nome_cenarios.keys():
    cenario_dir = tcc_results / cenario
    if cenario_dir.exists():
        metricas = extrair_metricas_validacao(cenario_dir)
        if metricas:
            validacoes[cenario] = metricas

# Coletar estatísticas descritivas do baseline
estatisticas_descritivas = extrair_estatisticas_descritivas(tcc_results / "01_baseline")

# Criar diretório de saída
output_dir = tcc_results / "tabelas_tcc"
output_dir.mkdir(exist_ok=True)

print("=" * 70)
print("GERANDO TABELAS PARA TCC")
print("=" * 70)

# ============================================================================
# TABELA 1: Métricas de Qualidade dos Modelos
# ============================================================================
print("\n[1/6] Gerando Tabela 1: Métricas de Qualidade dos Modelos...")

rows = []
for cenario, nome in nome_cenarios.items():
    if cenario in validacoes:
        m = validacoes[cenario]
        rows.append({
            'Cenário': nome,
            'Consumo MAE (kWh)': f"{m['consumo_mae']:.2f}",
            'Consumo RMSE (kWh)': f"{m['consumo_rmse']:.2f}",
            'Consumo MAPE (%)': f"{m['consumo_mape']:.2f}",
            'Consumo R²': f"{m['consumo_r2']:.3f}",
            'Produção MAE (kWh)': f"{m['producao_mae']:.2f}",
            'Produção RMSE (kWh)': f"{m['producao_rmse']:.2f}",
            'Produção MAPE (%)': f"{m['producao_mape']:.2f}",
            'Produção R²': f"{m['producao_r2']:.3f}"
        })

df_t1 = pd.DataFrame(rows)

# LaTeX
latex_t1 = df_t1.to_latex(index=False, escape=False, float_format='%.3f')
with open(output_dir / "tabela1_metricas_qualidade.tex", 'w', encoding='utf-8') as f:
    f.write("% Tabela 1: Métricas de Qualidade dos Modelos\n")
    f.write("% Fonte: Arquivos execucao_output.txt de cada cenário\n\n")
    f.write(latex_t1)

# Markdown (sem tabulate)
def df_to_markdown(df):
    """Converte DataFrame para markdown simples"""
    lines = []
    # Cabeçalho
    headers = '| ' + ' | '.join(df.columns) + ' |'
    lines.append(headers)
    # Separador
    lines.append('|' + '|'.join(['---'] * len(df.columns)) + '|')
    # Dados
    for _, row in df.iterrows():
        lines.append('| ' + ' | '.join([str(val) for val in row.values]) + ' |')
    return '\n'.join(lines)

md_t1 = df_to_markdown(df_t1)
with open(output_dir / "tabela1_metricas_qualidade.md", 'w', encoding='utf-8') as f:
    f.write("# Tabela 1: Métricas de Qualidade dos Modelos\n\n")
    f.write("*Fonte: Arquivos execucao_output.txt de cada cenário*\n\n")
    f.write(md_t1)

print(f"[OK] Tabela 1 salva: {output_dir / 'tabela1_metricas_qualidade.tex'}")

# ============================================================================
# TABELA 2: Estatísticas Descritivas dos Dados Históricos
# ============================================================================
print("\n[2/6] Gerando Tabela 2: Estatísticas Descritivas...")

if estatisticas_descritivas:
    rows_t2 = [
        {'Estatística': 'Contagem', 'Consumo (kWh)': f"{estatisticas_descritivas['count'][0]:.0f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['count'][1]:.0f}"},
        {'Estatística': 'Média', 'Consumo (kWh)': f"{estatisticas_descritivas['mean'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['mean'][1]:.2f}"},
        {'Estatística': 'Desvio Padrão', 'Consumo (kWh)': f"{estatisticas_descritivas['std'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['std'][1]:.2f}"},
        {'Estatística': 'Mínimo', 'Consumo (kWh)': f"{estatisticas_descritivas['min'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['min'][1]:.2f}"},
        {'Estatística': 'Quartil 25%', 'Consumo (kWh)': f"{estatisticas_descritivas['q25'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['q25'][1]:.2f}"},
        {'Estatística': 'Mediana (50%)', 'Consumo (kWh)': f"{estatisticas_descritivas['q50'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['q50'][1]:.2f}"},
        {'Estatística': 'Quartil 75%', 'Consumo (kWh)': f"{estatisticas_descritivas['q75'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['q75'][1]:.2f}"},
        {'Estatística': 'Máximo', 'Consumo (kWh)': f"{estatisticas_descritivas['max'][0]:.2f}", 
         'Produção (kWh)': f"{estatisticas_descritivas['max'][1]:.2f}"}
    ]
    
    df_t2 = pd.DataFrame(rows_t2)
    
    # LaTeX
    latex_t2 = df_t2.to_latex(index=False, escape=False)
    with open(output_dir / "tabela2_estatisticas_descritivas.tex", 'w', encoding='utf-8') as f:
        f.write("% Tabela 2: Estatísticas Descritivas dos Dados Históricos\n")
        f.write("% Fonte: Cenário Baseline - execucao_output.txt\n\n")
        f.write(latex_t2)
    
    # Markdown
    md_t2 = df_to_markdown(df_t2)
    with open(output_dir / "tabela2_estatisticas_descritivas.md", 'w', encoding='utf-8') as f:
        f.write("# Tabela 2: Estatísticas Descritivas dos Dados Históricos\n\n")
        f.write("*Fonte: Cenário Baseline - execucao_output.txt*\n\n")
        f.write(md_t2)
    
    print(f"[OK] Tabela 2 salva: {output_dir / 'tabela2_estatisticas_descritivas.tex'}")

# ============================================================================
# TABELA 3: Resultados Financeiros Comparativos
# ============================================================================
print("\n[3/6] Gerando Tabela 3: Resultados Financeiros...")

df_t3 = df_metricas[['cenario', 'lucro_liquido_total_brl', 'receita_total_vendas_brl', 
                     'custo_total_compras_brl', 'lucro_medio_por_periodo_brl', 
                     'roi_percentual']].copy()
df_t3['Cenário'] = df_t3['cenario'].map(nome_cenarios)
df_t3['Lucro Total (R$)'] = df_t3['lucro_liquido_total_brl'].apply(lambda x: f"{x:.2f}")
df_t3['Receita Total (R$)'] = df_t3['receita_total_vendas_brl'].apply(lambda x: f"{x:.2f}")
df_t3['Custo Total (R$)'] = df_t3['custo_total_compras_brl'].apply(lambda x: f"{x:.2f}")
df_t3['Lucro Médio/Período (R$)'] = df_t3['lucro_medio_por_periodo_brl'].apply(lambda x: f"{x:.2f}")
df_t3['ROI (%)'] = df_t3['roi_percentual'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")

df_t3_final = df_t3[['Cenário', 'Lucro Total (R$)', 'Receita Total (R$)', 
                     'Custo Total (R$)', 'Lucro Médio/Período (R$)', 'ROI (%)']]

# LaTeX
latex_t3 = df_t3_final.to_latex(index=False, escape=False)
with open(output_dir / "tabela3_resultados_financeiros.tex", 'w', encoding='utf-8') as f:
    f.write("% Tabela 3: Resultados Financeiros Comparativos entre Cenários\n")
    f.write("% Fonte: metricas_comparativas.csv\n\n")
    f.write(latex_t3)

# Markdown
md_t3 = df_to_markdown(df_t3_final)
with open(output_dir / "tabela3_resultados_financeiros.md", 'w', encoding='utf-8') as f:
    f.write("# Tabela 3: Resultados Financeiros Comparativos\n\n")
    f.write("*Fonte: metricas_comparativas.csv*\n\n")
    f.write(md_t3)

print(f"[OK] Tabela 3 salva: {output_dir / 'tabela3_resultados_financeiros.tex'}")

# ============================================================================
# TABELA 4: Impacto do Período de Treinamento
# ============================================================================
print("\n[4/6] Gerando Tabela 4: Impacto do Período de Treinamento...")

df_t4 = df_metricas[df_metricas['cenario'].isin(['08_treino_curto', '09_treino_longo'])].copy()
df_t4['Cenário'] = df_t4['cenario'].map(nome_cenarios)
df_t4['Período Treino'] = df_t4['cenario'].map({'08_treino_curto': '30 dias', '09_treino_longo': '180 dias'})
df_t4['Lucro Total (R$)'] = df_t4['lucro_liquido_total_brl'].apply(lambda x: f"{x:.2f}")
df_t4['Lucro Médio (R$)'] = df_t4['lucro_medio_por_periodo_brl'].apply(lambda x: f"{x:.2f}")
df_t4['Excedente (kWh)'] = df_t4['excedente_total_kwh'].apply(lambda x: f"{x:.2f}")
df_t4['Déficit (kWh)'] = df_t4['deficit_total_kwh'].apply(lambda x: f"{x:.2f}")

df_t4_final = df_t4[['Período Treino', 'Lucro Total (R$)', 'Lucro Médio (R$)', 
                     'Excedente (kWh)', 'Déficit (kWh)']]

# LaTeX
latex_t4 = df_t4_final.to_latex(index=False, escape=False)
with open(output_dir / "tabela4_impacto_treinamento.tex", 'w', encoding='utf-8') as f:
    f.write("% Tabela 4: Impacto do Período de Treinamento nos Resultados\n")
    f.write("% Fonte: metricas_comparativas.csv\n\n")
    f.write(latex_t4)

# Markdown
md_t4 = df_to_markdown(df_t4_final)
with open(output_dir / "tabela4_impacto_treinamento.md", 'w', encoding='utf-8') as f:
    f.write("# Tabela 4: Impacto do Período de Treinamento\n\n")
    f.write("*Fonte: metricas_comparativas.csv*\n\n")
    f.write(md_t4)

print(f"[OK] Tabela 4 salva: {output_dir / 'tabela4_impacto_treinamento.tex'}")

# ============================================================================
# TABELA 5: Indicadores Energéticos
# ============================================================================
print("\n[5/6] Gerando Tabela 5: Indicadores Energéticos...")

df_t5 = df_metricas[['cenario', 'excedente_total_kwh', 'deficit_total_kwh',
                     'consumo_medio_kwh', 'producao_media_kwh']].copy()
df_t5['Cenário'] = df_t5['cenario'].map(nome_cenarios)

# Calcular eficiência energética
df_t5['Eficiência (%)'] = ((df_t5['producao_media_kwh'] / df_t5['consumo_medio_kwh']) * 100).apply(lambda x: f"{x:.1f}")

df_t5['Excedente Total (kWh)'] = df_t5['excedente_total_kwh'].apply(lambda x: f"{x:.2f}")
df_t5['Déficit Total (kWh)'] = df_t5['deficit_total_kwh'].apply(lambda x: f"{x:.2f}")
df_t5['Consumo Médio (kWh/dia)'] = df_t5['consumo_medio_kwh'].apply(lambda x: f"{x:.2f}")
df_t5['Produção Média (kWh/dia)'] = df_t5['producao_media_kwh'].apply(lambda x: f"{x:.2f}")

df_t5_final = df_t5[['Cenário', 'Excedente Total (kWh)', 'Déficit Total (kWh)',
                     'Consumo Médio (kWh/dia)', 'Produção Média (kWh/dia)', 'Eficiência (%)']]

# LaTeX
latex_t5 = df_t5_final.to_latex(index=False, escape=False)
with open(output_dir / "tabela5_indicadores_energeticos.tex", 'w', encoding='utf-8') as f:
    f.write("% Tabela 5: Indicadores Energéticos por Cenário\n")
    f.write("% Fonte: metricas_comparativas.csv\n\n")
    f.write(latex_t5)

# Markdown
md_t5 = df_to_markdown(df_t5_final)
with open(output_dir / "tabela5_indicadores_energeticos.md", 'w', encoding='utf-8') as f:
    f.write("# Tabela 5: Indicadores Energéticos\n\n")
    f.write("*Fonte: metricas_comparativas.csv*\n\n")
    f.write(md_t5)

print(f"[OK] Tabela 5 salva: {output_dir / 'tabela5_indicadores_energeticos.tex'}")

# ============================================================================
# TABELA 6: Distribuição de Decisões
# ============================================================================
print("\n[6/6] Gerando Tabela 6: Distribuição de Decisões...")

df_t6 = df_metricas[['cenario', 'decisoes_vender', 'decisoes_comprar', 'decisoes_neutro',
                     'percentual_vender', 'percentual_comprar', 'percentual_neutro']].copy()
df_t6['Cenário'] = df_t6['cenario'].map(nome_cenarios)
df_t6['Vender (absoluto)'] = df_t6['decisoes_vender']
df_t6['Comprar (absoluto)'] = df_t6['decisoes_comprar']
df_t6['Neutro (absoluto)'] = df_t6['decisoes_neutro']
df_t6['Vender (%)'] = df_t6['percentual_vender'].apply(lambda x: f"{x:.1f}")
df_t6['Comprar (%)'] = df_t6['percentual_comprar'].apply(lambda x: f"{x:.1f}")
df_t6['Neutro (%)'] = df_t6['percentual_neutro'].apply(lambda x: f"{x:.1f}")

df_t6_final = df_t6[['Cenário', 'Vender (absoluto)', 'Vender (%)', 
                     'Comprar (absoluto)', 'Comprar (%)', 
                     'Neutro (absoluto)', 'Neutro (%)']]

# LaTeX
latex_t6 = df_t6_final.to_latex(index=False, escape=False)
with open(output_dir / "tabela6_distribuicao_decisoes.tex", 'w', encoding='utf-8') as f:
    f.write("% Tabela 6: Distribuição de Decisões por Cenário\n")
    f.write("% Fonte: metricas_comparativas.csv\n\n")
    f.write(latex_t6)

# Markdown
md_t6 = df_to_markdown(df_t6_final)
with open(output_dir / "tabela6_distribuicao_decisoes.md", 'w', encoding='utf-8') as f:
    f.write("# Tabela 6: Distribuição de Decisões\n\n")
    f.write("*Fonte: metricas_comparativas.csv*\n\n")
    f.write(md_t6)

print(f"[OK] Tabela 6 salva: {output_dir / 'tabela6_distribuicao_decisoes.tex'}")

# ============================================================================
# RESUMO
# ============================================================================
print("\n" + "=" * 70)
print("TABELAS GERADAS COM SUCESSO!")
print("=" * 70)
print(f"\nLocalização: {output_dir}")
print("\nArquivos gerados:")
print("  - Tabela 1: Métricas de Qualidade (.tex e .md)")
print("  - Tabela 2: Estatísticas Descritivas (.tex e .md)")
print("  - Tabela 3: Resultados Financeiros (.tex e .md)")
print("  - Tabela 4: Impacto do Treinamento (.tex e .md)")
print("  - Tabela 5: Indicadores Energéticos (.tex e .md)")
print("  - Tabela 6: Distribuição de Decisões (.tex e .md)")
print("\nFormato LaTeX pode ser inserido diretamente no documento.")
print("Formato Markdown para visualização rápida.")

