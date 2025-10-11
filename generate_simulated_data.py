# generate_simulated_data.py

"""
Gera dados simulados de consumo e produção e salva em CSV.
Uso:
    python generate_simulated_data.py --out raw --days 120
"""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_simulated(dias=100, seed=42, start_date="2024-01-01"):
    np.random.seed(seed)
    start = datetime.fromisoformat(start_date)
    dates = [start + timedelta(days=i) for i in range(dias)]
    consumo = 80 + 20 * np.sin(np.linspace(0, 6.28, dias)) + np.random.normal(0, 5, size=dias)
    producao = 70 + 25 * np.cos(np.linspace(0, 6.28, dias)) + np.random.normal(0, 7, size=dias)
    df_consumo = pd.DataFrame({"date": [d.strftime("%Y-%m-%d") for d in dates], "consumption": consumo.round(2)})
    df_producao = pd.DataFrame({"date": [d.strftime("%Y-%m-%d") for d in dates], "production": producao.round(2)})
    return df_consumo, df_producao

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", choices=["raw", "simulation"], default="raw",
                        help="Salvar em src/data/raw ou src/data/simulation")
    parser.add_argument("--days", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start", type=str, default="2024-01-01")
    args = parser.parse_args()

    df_c, df_p = generate_simulated(dias=args.days, seed=args.seed, start_date=args.start)

    base = Path(__file__).resolve().parents[2] / "src" / "data"
    out_dir = base / args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    c_path = out_dir / "consumption.csv"
    p_path = out_dir / "production.csv"

    df_c.to_csv(c_path, index=False)
    df_p.to_csv(p_path, index=False)

    print(f"Arquivos gerados em: {out_dir}")
    print(f"- {c_path.name}  ({len(df_c)} linhas)")
    print(f"- {p_path.name}  ({len(df_p)} linhas)")

if __name__ == "__main__":
    main()
