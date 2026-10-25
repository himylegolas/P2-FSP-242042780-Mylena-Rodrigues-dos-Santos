"""
01_tratamento_painel_municipal.py
Constrói o painel tratado de Ananindeua (1500800) e Marabá (1504208), 2015-2025,
a partir dos arquivos brutos do Siconfi/Finbra (DCA) e do IPCA (IBGE).

USO:  python 01_tratamento_painel_municipal.py <pasta_dos_brutos> <pasta_de_saida>
Os brutos esperados (nomes como baixados do Siconfi):
  finbra_receitas_I-C_<ano>_csv.csv | finbra_despesas_funcao_I-E_<ano>_csv.csv |
  finbra_despesas_orcamentarias_I-D_<ano>_csv.csv | ipca_202609SerieHist.xls

DECISÕES (registradas em docs/registro_alteracoes.md):
- Receita líquida = (receitas correntes + receitas de capital, exceto intraorçamentárias)
  - deduções FUNDEB - outras deduções.
- Despesa = despesa LIQUIDADA exceto intraorçamentárias (DCA I-E). Categorias econômicas: DCA I-D.
- Valores reais: deflator = razão entre a MÉDIA ANUAL do número-índice do IPCA do ano-base (2024)
  e a do ano da observação. Nenhum dado ausente é substituído por zero.
- População: a informada nos próprios arquivos do Siconfi (estimativas do IBGE); há quebra de série
  em 2024 (revisão após o Censo 2022) e repetição de valores em alguns anos.
"""
import sys, io, re
from pathlib import Path
import pandas as pd

BR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dados/brutos_atualizados")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dados/tratados")
OUT.mkdir(parents=True, exist_ok=True)
ENTES = {"1500800": "Ananindeua", "1504208": "Marabá"}
ANOS = range(2015, 2026)
BASE = 2024

def ler_finbra(path):
    linhas = Path(path).read_bytes().decode("latin-1").splitlines()
    ano = int(linhas[0].split(":")[1]); tabela = linhas[2].split(":", 1)[1].strip()
    d = pd.read_csv(io.StringIO("\n".join(linhas[3:])), sep=";", dtype=str)
    d["Valor"] = d["Valor"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
    d["ano"], d["tabela"] = ano, tabela
    return d[d["Cod.IBGE"].isin(ENTES)].assign(municipio=lambda x: x["Cod.IBGE"].map(ENTES))

def achar(prefixo, ano, tabela):
    """Escolhe, entre os arquivos do ano (inclusive duplicados), o que de fato traz a tabela esperada
    (verifica o cabeçalho 'Tabela: ...' na 3ª linha), para evitar usar um arquivo baixado por engano."""
    for f in sorted(BR.glob(f"{prefixo}_{ano}_csv*.csv")):
        linhas = f.read_bytes().decode("latin-1").splitlines()
        if len(linhas) > 2 and tabela in linhas[2] and str(ano) in linhas[0]:
            return f
    return None

def val(g, coluna, mascara):
    s = g[(g.Coluna == coluna) & mascara]
    return s.Valor.iloc[0] if len(s) else float("nan")

# ---- IPCA
ip = pd.read_excel(BR / "ipca_202609SerieHist.xls", header=None, skiprows=8, usecols=[0, 1, 2])
ip.columns = ["ano", "mes", "indice"]
ip["ano"] = pd.to_numeric(ip.ano, errors="coerce").ffill()
ip = ip[ip.mes.astype(str).str.len() == 3].copy()
ip["indice"] = pd.to_numeric(ip.indice, errors="coerce"); ip = ip.dropna(subset=["indice"]); ip["ano"] = ip.ano.astype(int)
media = ip[ip.ano.between(2014, 2025)].groupby("ano").indice.mean()
defl = (media[BASE] / media).rename("deflator_base2024")

linhas = []
for a in ANOS:
    r = achar("finbra_receitas_I-C", a, "Receitas Orçamentárias"); e = achar("finbra_despesas_funcao_I-E", a, "Despesas por Função"); o = achar("finbra_despesas_orcamentarias_I-D", a, "Despesas Orçamentárias")
    for rotulo, arq in (("Receitas (I-C)", r), ("Despesas por Função (I-E)", e), ("Despesas Orçamentárias (I-D)", o)):
        if arq is None:
            print(f"AVISO: não há, na pasta dos brutos, arquivo da tabela {rotulo} para {a} com o título correto; as colunas correspondentes ficarão ausentes (NA). "
                  "Confira se os arquivos reenviados (sufixo _csv_1) estão na pasta.")
    R = ler_finbra(r) if r else None; E = ler_finbra(e) if e else None; O = ler_finbra(o) if o else None
    for cod, mun in ENTES.items():
        L = {"ano": a, "cod_ibge": int(cod), "municipio": mun}
        if R is not None:
            g = R[R["Cod.IBGE"] == cod]; B = "Receitas Brutas Realizadas"
            m = lambda p: g.Conta.str.match(p)
            L["populacao"] = int(g.População.iloc[0])
            L["receitas_correntes"] = val(g, B, m(r"^1\.0\.0\.0\.00")); L["receitas_capital"] = val(g, B, m(r"^2\.0\.0\.0\.00"))
            L["impostos_taxas"] = val(g, B, m(r"^1\.1\.0\.0\.00")); L["transferencias_correntes"] = val(g, B, m(r"^1\.7\.0\.0\.00"))
            L["operacoes_credito"] = val(g, B, m(r"^2\.1\.0\.0\.00"))
            tot = g.Conta.str.match(r"^(Total Receitas|RECEITAS \(EXCETO)")
            L["deducoes_fundeb"] = val(g, "Deduções - FUNDEB", tot); L["outras_deducoes"] = val(g, "Outras Deduções da Receita", tot)
        if E is not None:
            g = E[E["Cod.IBGE"] == cod]; Q = "Despesas Liquidadas"
            tot = g.Conta.str.match(r"^Despesas \(?Exceto")
            L["despesa_liquidada_exceto_intra"] = val(g, Q, tot)
            for nome, cd in {"saude": "10", "educacao": "12", "administracao": "04", "urbanismo": "15", "assistencia": "08", "previdencia": "09", "seguranca": "06", "transporte": "26"}.items():
                L[f"desp_{nome}"] = val(g, Q, g.Conta.str.match(rf"^{cd} - "))
        if O is not None:
            g = O[O["Cod.IBGE"] == cod]; Q = "Despesas Liquidadas"
            for nome, p in {"pessoal": r"^3\.1\.00\.00\.00", "juros": r"^3\.2\.00\.00\.00", "investimentos": r"^4\.4\.00\.00\.00", "total_geral_incl_intra": r"^Total Geral"}.items():
                L[f"cat_{nome}"] = val(g, Q, g.Conta.str.match(p))
        linhas.append(L)
P = pd.DataFrame(linhas)
P["receita_bruta"] = P.receitas_correntes + P.receitas_capital
P["receita_liquida"] = P.receita_bruta - P.deducoes_fundeb.fillna(0) - P.outras_deducoes.fillna(0)
P["deflator_base2024"] = P.ano.map(defl)
for c in ["receita_liquida", "receitas_correntes", "impostos_taxas", "transferencias_correntes", "operacoes_credito", "despesa_liquidada_exceto_intra", "desp_saude", "desp_educacao", "desp_urbanismo", "desp_administracao", "cat_pessoal", "cat_investimentos", "cat_juros"]:
    if c in P: P[c + "_real2024"] = P[c] * P.deflator_base2024
P["receita_liquida_real_pc"] = P.receita_liquida_real2024 / P.populacao
P["despesa_real_pc"] = P.despesa_liquidada_exceto_intra_real2024 / P.populacao
P["pct_transferencias_na_receita_bruta"] = 100 * P.transferencias_correntes / P.receita_bruta
P["pct_tributos_proprios_na_receita_bruta"] = 100 * P.impostos_taxas / P.receita_bruta
P["pct_credito_na_receita_bruta"] = 100 * P.operacoes_credito.fillna(0) / P.receita_bruta
P["resultado_orcamentario_real2024"] = P.receita_liquida_real2024 - P.despesa_liquidada_exceto_intra_real2024
P["janela"] = "2015-2025"
P.to_csv(OUT / "painel_municipal_2015_2025.csv", index=False)
defl.round(6).to_csv(OUT / "deflator_ipca_base2024.csv")
print(P.shape, "-> salvo em", OUT)
