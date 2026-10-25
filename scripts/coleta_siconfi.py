"""
Coleta Siconfi (Tesouro Nacional) para Ananindeua e Maraba, 2014-2026.

PRINCIPIOS
- NAO altera nem apaga nenhum arquivo em data/original/.
- Grava tudo o que baixar em data/raw_2026/ com data_coleta e fonte.
- Gera data/raw_2026/comparacao_sobreposicao.csv comparando, para os anos que
  existem nos dois lados, o valor original e o valor novo (para voce verificar).
- 2026 vem PARCIAL (so os bimestres ja publicados); nao entra na janela de 10 anos.

COMO USAR (no seu computador, com internet)
    pip install requests pandas
    python coleta_siconfi.py

Fonte: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/  (docs: /docs/siconfi/)
Testar antes de confiar: nomes de parametros e de anexos podem mudar.
"""
import time
import datetime as dt
from pathlib import Path

import pandas as pd
import requests

BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"
ENTES = {"Ananindeua": 1500800, "Maraba": 1504208}   # codigos IBGE
ANOS = range(2014, 2027)
HOJE = dt.date.today().isoformat()

ORIG = Path("data/original")
RAW = Path("data/raw_2026")
RAW.mkdir(parents=True, exist_ok=True)


def get_all(endpoint, params, tentativas=5):
    """Percorre a paginacao ORDS (hasMore/offset). Devolve DataFrame."""
    linhas, offset = [], 0
    while True:
        p = dict(params, offset=offset)
        for i in range(tentativas):
            try:
                r = requests.get(f"{BASE}/{endpoint}", params=p, timeout=60)
                r.raise_for_status()
                break
            except requests.RequestException as e:
                if i == tentativas - 1:
                    print("  FALHOU:", endpoint, params, e)
                    return pd.DataFrame(linhas)
                time.sleep(3 * (i + 1))
        j = r.json()
        linhas += j.get("items", [])
        if not j.get("hasMore"):
            break
        offset += j.get("limit", 5000)
    return pd.DataFrame(linhas)


def rreo(anexo, nome_saida):
    """Mesma estrutura do arquivo original (RREO, bimestre 6)."""
    quadros = []
    for mun, ibge in ENTES.items():
        for ano in ANOS:
            # 2026: tenta bimestres 1..6 e guarda o que existir
            periodos = range(1, 7) if ano == 2026 else [6]
            for per in periodos:
                df = get_all("rreo", {
                    "an_exercicio": ano, "nr_periodo": per,
                    "co_tipo_demonstrativo": "RREO",
                    "no_anexo": anexo, "co_esfera": "M", "id_ente": ibge})
                if len(df):
                    df["municipio"] = mun
                    quadros.append(df)
                print(f"RREO {anexo} {mun} {ano} bim{per}: {len(df)} linhas")
    out = pd.concat(quadros, ignore_index=True) if quadros else pd.DataFrame()
    out["fonte"] = "Siconfi API (apidatalake.tesouro.gov.br)"
    out["data_coleta"] = HOJE
    out.to_csv(RAW / nome_saida, index=False)
    return out


def rgf(anexo, nome_saida):
    quadros = []
    for mun, ibge in ENTES.items():
        for ano in ANOS:
            for per in (1, 2, 3):
                df = get_all("rgf", {
                    "an_exercicio": ano, "in_periodicidade": "Q", "nr_periodo": per,
                    "co_tipo_demonstrativo": "RGF", "no_anexo": anexo,
                    "co_esfera": "M", "co_poder": "E", "id_ente": ibge})
                if len(df):
                    df["municipio"] = mun
                    quadros.append(df)
                print(f"RGF {anexo} {mun} {ano} q{per}: {len(df)} linhas")
    out = pd.concat(quadros, ignore_index=True) if quadros else pd.DataFrame()
    out["fonte"] = "Siconfi API (apidatalake.tesouro.gov.br)"
    out["data_coleta"] = HOJE
    out.to_csv(RAW / nome_saida, index=False)
    return out


def dca(nome_saida):
    """DCA = contas anuais consolidadas (base recomendada para a serie decenal).
    Baixa TODOS os anexos; depois confira em no_anexo quais usar
    (receitas orcamentarias e despesas por funcao)."""
    quadros = []
    for mun, ibge in ENTES.items():
        for ano in range(2014, 2026):          # DCA 2026 ainda nao existe
            df = get_all("dca", {"an_exercicio": ano, "id_ente": ibge})
            if len(df):
                df["municipio"] = mun
                quadros.append(df)
            print(f"DCA {mun} {ano}: {len(df)} linhas")
    out = pd.concat(quadros, ignore_index=True) if quadros else pd.DataFrame()
    out["fonte"] = "Siconfi API (apidatalake.tesouro.gov.br)"
    out["data_coleta"] = HOJE
    out.to_csv(RAW / nome_saida, index=False)
    if len(out):
        print("\nAnexos DCA encontrados:\n", out["anexo"].value_counts().head(30))
    return out


def comparar(orig_csv, novo_df, chaves):
    """Compara original x novo nos anos em comum. Nada e sobrescrito."""
    f = ORIG / orig_csv
    if not f.exists() or novo_df.empty:
        print("sem comparacao para", orig_csv)
        return
    a = pd.read_csv(f)
    n = novo_df.copy()
    n["valor"] = pd.to_numeric(n["valor"], errors="coerce")
    comum = sorted(set(a["exercicio"]) & set(n["exercicio"].astype(int)))
    n["exercicio"] = n["exercicio"].astype(int)
    m = a[a.exercicio.isin(comum)].merge(
        n[n.exercicio.isin(comum)], on=chaves, how="outer",
        suffixes=("_original", "_novo"), indicator=True)
    m["diferenca"] = m["valor_novo"] - m["valor_original"]
    m.to_csv(RAW / f"comparacao_{orig_csv}", index=False)
    print(f"{orig_csv}: {len(m)} linhas comparadas, anos {comum}; "
          f"{(m.diferenca.abs() > 0.5).sum()} com diferenca")


if __name__ == "__main__":
    chaves = ["exercicio", "municipio", "anexo", "coluna", "cod_conta", "conta"]
    r1 = rreo("RREO-Anexo 01", "siconfi_receitas_orcamentarias_atualizado.csv")
    r2 = rreo("RREO-Anexo 02", "siconfi_despesas_funcao_atualizado.csv")
    r6 = rreo("RREO-Anexo 06", "siconfi_resultado_primario_atualizado.csv")
    g1 = rgf("RGF-Anexo 01", "siconfi_rcl_atualizado.csv")
    dca("siconfi_dca_2014_2025.csv")
    comparar("siconfi_receitas_orcamentarias_2014_2023.csv", r1, chaves)
    comparar("siconfi_despesas_funcao_2014_2023.csv", r2, chaves)
    print("\nPronto. Envie a pasta data/raw_2026/ para eu verificar antes de qualquer fusao.")
