#!/usr/bin/env python3
"""Script para coletar resultados de múltiplos cenários para TCC."""
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import sys

# Criar pasta de resultados do TCC dentro de results
tcc_results = Path("results/tcc_coleta_completa")
tcc_results.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("COLETA COMPLETA DE RESULTADOS PARA TCC")
print("=" * 70)
print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Pasta de destino: {tcc_results}")
print("=" * 70)

cenarios = [
    {
        "nome": "01_baseline",
        "comando": ["python", "run_pipeline.py", "--horizon", "14", "--no-gui"],
        "descricao": "Baseline - Dados simulados, horizonte 14 dias, região SE",
        "parametros": "Horizonte: 14 dias | Região: SE | Dados: Simulados"
    },
    {
        "nome": "02_sao_paulo_pvgis",
        "comando": ["python", "run_pipeline.py", "--use-real-data", 
                   "--lat", "-23.5505", "--lon", "-46.6333", 
                   "--horizon", "14", "--no-gui", "--cache"],
        "descricao": "São Paulo com PVGIS - Dados reais de irradiação solar",
        "parametros": "Coordenadas: -23.5505, -46.6333 | API: PVGIS | Horizonte: 14 dias"
    },
    {
        "nome": "03_horizon_7",
        "comando": ["python", "run_pipeline.py", "--horizon", "7", "--no-gui"],
        "descricao": "Horizonte curto - 7 dias de previsão",
        "parametros": "Horizonte: 7 dias | Região: SE | Dados: Simulados"
    },
    {
        "nome": "04_horizon_30",
        "comando": ["python", "run_pipeline.py", "--horizon", "30", "--no-gui"],
        "descricao": "Horizonte longo - 30 dias de previsão",
        "parametros": "Horizonte: 30 dias | Região: SE | Dados: Simulados"
    },
    {
        "nome": "05_regiao_ne",
        "comando": ["python", "run_pipeline.py", "--region", "NE", 
                   "--submercado", "NE", "--horizon", "14", "--no-gui"],
        "descricao": "Região Nordeste - Análise por contexto regional",
        "parametros": "Região: NE | Submercado: NE | Horizonte: 14 dias"
    },
    {
        "nome": "06_rio_de_janeiro_pvgis",
        "comando": ["python", "run_pipeline.py", "--use-real-data", 
                   "--lat", "-22.9068", "--lon", "-43.1729", 
                   "--horizon", "14", "--no-gui", "--cache"],
        "descricao": "Rio de Janeiro com PVGIS - Comparação com São Paulo",
        "parametros": "Coordenadas: -22.9068, -43.1729 | API: PVGIS | Horizonte: 14 dias"
    },
    {
        "nome": "07_brasilia_pvgis",
        "comando": ["python", "run_pipeline.py", "--use-real-data", 
                   "--lat", "-15.7942", "--lon", "-47.8822", 
                   "--horizon", "14", "--no-gui", "--cache"],
        "descricao": "Brasília com PVGIS - Análise para região central",
        "parametros": "Coordenadas: -15.7942, -47.8822 | API: PVGIS | Horizonte: 14 dias"
    },
    {
        "nome": "08_treino_curto",
        "comando": ["python", "run_pipeline.py", 
                   "--train-start", "2024-09-30", 
                   "--train-end", "2024-10-30",
                   "--horizon", "14", "--no-gui"],
        "descricao": "Período de treino curto (30 dias) - Impacto do histórico limitado",
        "parametros": "Treino: 30 dias | Horizonte: 14 dias"
    },
    {
        "nome": "09_treino_longo",
        "comando": ["python", "run_pipeline.py", 
                   "--train-start", "2024-05-01", 
                   "--train-end", "2024-10-30",
                   "--horizon", "14", "--no-gui"],
        "descricao": "Período de treino longo (180 dias) - Mais dados históricos",
        "parametros": "Treino: 180 dias | Horizonte: 14 dias"
    }
]

resultados_coletados = []
erros_ocorridos = []

for i, cenario in enumerate(cenarios, 1):
    print(f"\n[{i}/{len(cenarios)}] Executando: {cenario['nome']}")
    print(f"Descrição: {cenario['descricao']}")
    print(f"Parâmetros: {cenario['parametros']}")
    print("-" * 70)
    
    try:
        # Executar pipeline
        resultado = subprocess.run(
            cenario["comando"],
            capture_output=True,
            text=True,
            check=True,
            timeout=300  # 5 minutos timeout
        )
        
        # Criar pasta para este cenário
        destino = tcc_results / cenario["nome"]
        destino.mkdir(exist_ok=True)
        
        # Copiar resultados
        arquivos_copiados = []
        if Path("results").exists():
            for arquivo in Path("results").glob("*"):
                if arquivo.is_file() and arquivo.suffix in ['.csv', '.parquet', '.png']:
                    shutil.copy2(arquivo, destino / arquivo.name)
                    arquivos_copiados.append(arquivo.name)
        
        # Salvar output do terminal
        output_path = destino / "execucao_output.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"CENÁRIO: {cenario['nome']}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Descrição: {cenario['descricao']}\n")
            f.write(f"Parâmetros: {cenario['parametros']}\n")
            f.write(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("COMANDO EXECUTADO:\n")
            f.write(" ".join(cenario["comando"]) + "\n\n")
            f.write("=" * 70 + "\n")
            f.write("OUTPUT DO PIPELINE:\n")
            f.write("=" * 70 + "\n\n")
            f.write(resultado.stdout)
            if resultado.stderr:
                f.write("\n\nSTDERR:\n" + resultado.stderr)
        
        # Criar README para o cenário
        readme_path = destino / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write(f"CENÁRIO: {cenario['nome']}\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Descrição: {cenario['descricao']}\n\n")
            f.write(f"Parâmetros:\n{cenario['parametros']}\n\n")
            f.write(f"Data de execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Comando executado:\n{' '.join(cenario['comando'])}\n\n")
            f.write(f"Status: Executado com sucesso\n\n")
            f.write(f"Arquivos gerados ({len(arquivos_copiados)}):\n")
            for arquivo in arquivos_copiados:
                f.write(f"  - {arquivo}\n")
            f.write(f"\nOutput completo: execucao_output.txt\n")
        
        resultados_coletados.append({
            "cenario": cenario["nome"],
            "status": "OK",
            "pasta": str(destino),
            "arquivos": len(arquivos_copiados),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        print(f"[OK] Resultados salvos em: {destino}")
        print(f"[OK] Arquivos: {len(arquivos_copiados)}")
        
    except subprocess.TimeoutExpired:
        erro = f"Timeout - execução demorou mais de 5 minutos"
        print(f"[ERRO] {erro}")
        erros_ocorridos.append({
            "cenario": cenario["nome"],
            "erro": erro
        })
        resultados_coletados.append({
            "cenario": cenario["nome"],
            "status": "ERRO - Timeout",
            "pasta": None
        })
    except subprocess.CalledProcessError as e:
        erro = f"Falha ao executar: {e}"
        print(f"[ERRO] {erro}")
        erros_ocorridos.append({
            "cenario": cenario["nome"],
            "erro": erro
        })
        resultados_coletados.append({
            "cenario": cenario["nome"],
            "status": f"ERRO - Falha na execução",
            "pasta": None
        })
    except Exception as e:
        erro = f"Erro inesperado: {str(e)}"
        print(f"[ERRO] {erro}")
        erros_ocorridos.append({
            "cenario": cenario["nome"],
            "erro": erro
        })
        resultados_coletados.append({
            "cenario": cenario["nome"],
            "status": f"ERRO - {str(e)[:50]}",
            "pasta": None
        })

# Criar resumo completo
print("\n" + "=" * 70)
print("GERANDO RESUMO COMPLETO...")
print("=" * 70)

resumo_path = tcc_results / "RESUMO_COMPLETO.md"
with open(resumo_path, 'w', encoding='utf-8') as f:
    f.write("# RESUMO COMPLETO - COLETA DE RESULTADOS PARA TCC\n\n")
    f.write(f"**Data/Hora da Coleta**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"**Total de Cenários**: {len(cenarios)}\n")
    f.write(f"**Cenários Executados com Sucesso**: {sum(1 for r in resultados_coletados if r['status'] == 'OK')}\n")
    f.write(f"**Cenários com Erro**: {sum(1 for r in resultados_coletados if r['status'] != 'OK')}\n\n")
    
    f.write("---\n\n")
    f.write("## 📋 CENÁRIOS EXECUTADOS\n\n")
    
    for i, (cenario, resultado) in enumerate(zip(cenarios, resultados_coletados), 1):
        f.write(f"### {i}. {cenario['nome']}\n\n")
        f.write(f"**Descrição**: {cenario['descricao']}\n\n")
        f.write(f"**Parâmetros**: {cenario['parametros']}\n\n")
        f.write(f"**Status**: {resultado['status']}\n\n")
        if resultado.get('pasta'):
            f.write(f"**Localização**: `{resultado['pasta']}`\n\n")
            if resultado.get('arquivos'):
                f.write(f"**Arquivos gerados**: {resultado['arquivos']}\n\n")
        f.write("---\n\n")
    
    if erros_ocorridos:
        f.write("## ⚠️ ERROS OCORRIDOS\n\n")
        for erro in erros_ocorridos:
            f.write(f"- **{erro['cenario']}**: {erro['erro']}\n\n")
    
    f.write("---\n\n")
    f.write("## 📊 ESTRUTURA DE PASTAS\n\n")
    f.write("```\n")
    f.write("results/tcc_coleta_completa/\n")
    for resultado in resultados_coletados:
        if resultado.get('pasta'):
            nome_curto = Path(resultado['pasta']).name
            f.write(f"├── {nome_curto}/\n")
            f.write(f"│   ├── README.txt (informações do cenário)\n")
            f.write(f"│   ├── execucao_output.txt (output completo)\n")
            f.write(f"│   ├── forecast_results.csv\n")
            f.write(f"│   ├── forecast_results.parquet\n")
            f.write(f"│   ├── forecast_comparison.png\n")
            f.write(f"│   ├── surplus_deficit.png\n")
            f.write(f"│   ├── cumulative_profit.png\n")
            f.write(f"│   └── pld_timeseries.png (se disponível)\n")
    f.write("└── RESUMO_COMPLETO.md (este arquivo)\n")
    f.write("```\n\n")
    
    f.write("---\n\n")
    f.write("## 📈 PRÓXIMOS PASSOS\n\n")
    f.write("1. Analisar resultados em cada pasta de cenário\n")
    f.write("2. Comparar métricas entre cenários\n")
    f.write("3. Usar gráficos PNG nos slides do TCC\n")
    f.write("4. Extrair métricas comparativas (usar script `extrair_metricas_tcc.py`)\n\n")

print(f"[OK] Resumo completo salvo em: {resumo_path}")

# Criar também arquivo TXT simples
resumo_txt_path = tcc_results / "RESUMO_COMPLETO.txt"
with open(resumo_txt_path, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("RESUMO COMPLETO - COLETA DE RESULTADOS PARA TCC\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Data/Hora da Coleta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"Total de Cenários: {len(cenarios)}\n")
    f.write(f"Cenários com Sucesso: {sum(1 for r in resultados_coletados if r['status'] == 'OK')}\n")
    f.write(f"Cenários com Erro: {sum(1 for r in resultados_coletados if r['status'] != 'OK')}\n\n")
    f.write("=" * 70 + "\n")
    f.write("CENÁRIOS EXECUTADOS:\n")
    f.write("=" * 70 + "\n\n")
    
    for resultado in resultados_coletados:
        f.write(f"Cenário: {resultado['cenario']}\n")
        f.write(f"Status: {resultado['status']}\n")
        if resultado.get('pasta'):
            f.write(f"Local: {resultado['pasta']}\n")
        f.write("\n" + "-" * 70 + "\n\n")

print(f"[OK] Resumo TXT salvo em: {resumo_txt_path}")

# Mostrar resumo final
print("\n" + "=" * 70)
print("RESUMO DA COLETA")
print("=" * 70)
print(f"\nCenários executados: {len(resultados_coletados)}")
print(f"Sucesso: {sum(1 for r in resultados_coletados if r['status'] == 'OK')}")
print(f"Erros: {sum(1 for r in resultados_coletados if r['status'] != 'OK')}")

if resultados_coletados:
    print("\nDetalhes:")
    for r in resultados_coletados:
        status_symbol = "[OK]" if r['status'] == 'OK' else "[ERRO]"
        print(f"  {status_symbol} {r['cenario']}")

print(f"\n[OK] Todos os resultados salvos em: {tcc_results}")
print(f"[OK] Leia: {resumo_path}")
print("\n" + "=" * 70)
print("[OK] Coleta concluida!")
print("=" * 70)

