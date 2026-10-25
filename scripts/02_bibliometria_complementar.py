"""
02_bibliometria_complementar.py
Reproduz, a partir de bibliometria/wos_completo.bib (Web of Science, 24/10/2026), os números da
seção "Mapeamento bibliométrico da literatura" que NÃO saem diretamente do Biblioshiny:
  (a) Tabela 1 (artigos por periódico e período);
  (b) parcelas aproximadas de estudos do "núcleo do tema" e "ambientais" por período;
  (c) conjunto de artigos elegíveis para o referencial (critério restrito) e a lista de candidatas.
Os totais do Biblioshiny (documentos, periódicos, autores, etc.) NÃO são recalculados aqui.
USO:  python scripts/02_bibliometria_complementar.py bibliometria/wos_completo.bib resultados/tabelas
"""
import re, sys
from pathlib import Path
import pandas as pd

BIB = Path(sys.argv[1] if len(sys.argv) > 1 else "bibliometria/wos_completo.bib")
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "resultados/tabelas"); OUT.mkdir(parents=True, exist_ok=True)

def parse(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    pos = [(m.start(), m.group(1), m.group(2).strip()) for m in re.finditer(r"(?m)^@(\w+)\{\s*([^,]*),", t)] + [(len(t), None, None)]
    out = []
    for (s, ty, key), (e, _, _) in zip(pos[:-1], pos[1:]):
        body = t[s:e]; rec = {"_type": ty, "_key": key}; j = body.find(",") + 1
        while True:
            m = re.compile(r"\s*([A-Za-z\-]+)\s*=\s*\{").match(body, j)
            if not m: break
            k = m.group(1).lower(); j = m.end(); depth = 1; st = j
            while depth and j < len(body):
                depth += (body[j] == "{") - (body[j] == "}"); j += 1
            rec[k] = re.sub(r"\s+", " ", body[st:j - 1]).strip()
            mm = re.compile(r"\s*,").match(body, j); j = mm.end() if mm else j
        out.append(rec)
    return pd.DataFrame(out)

df = parse(BIB); df["year"] = pd.to_numeric(df.year, errors="coerce"); df["tc"] = pd.to_numeric(df["times-cited"], errors="coerce")
print("registros:", len(df))
art = df[(df._type == "article") & df.journal.notna()].copy()
print("artigos com periódico:", len(art))

# (a) Tabela 1
art["periodo"] = pd.cut(art.year, [1982, 1999, 2009, 2019, 2026], labels=["1983-1999", "2000-2009", "2010-2019", "2020-2026"])
top = art.journal.value_counts().head(10).index
T = pd.crosstab(art.journal, art.periodo).loc[top]; T["Total"] = T.sum(axis=1)
T.to_csv(OUT / "bib_periodicos_por_periodo.csv"); print(T)

# (b) parcelas aproximadas (título + resumo + palavras-chave dos autores)
txt = (art.title.fillna("") + " " + art.abstract.fillna("") + " " + art.keywords.fillna("")).str.lower()
CORE = r"flypaper|fiscal illusion|veil of oates|intergovernmental (?:transfer|grant)|grants?[- ]in[- ]aid|fiscal transfer|lump-sum|unconditional grant"
ENV = r"carbon|emission|pollution|green|environment|energy|climate|sustainab"
art["nucleo"] = txt.str.contains(CORE, regex=True); art["ambiental"] = txt.str.contains(ENV, regex=True)
P = art.groupby("periodo", observed=True).agg(artigos=("title", "size"), nucleo_tematico=("nucleo", "sum"), ambiental=("ambiental", "sum"))
P["%_nucleo"] = (100 * P.nucleo_tematico / P.artigos).round(1); P["%_ambiental"] = (100 * P.ambiental / P.artigos).round(1)
P.to_csv(OUT / "bib_nucleo_tematico_por_periodo.csv"); print(P)

# (c) critério restrito para o referencial
a = df[(df._type == "article") & df.journal.notna()].copy(); a["tn"] = a.title.str.lower().str.replace(r"[^a-z0-9]", "", regex=True); a = a.drop_duplicates("tn")
a = a[a.doi.notna() & a.abstract.notna()].copy()
ta = (a.title.fillna("") + " " + a.abstract.fillna("")).str.lower()
CORE2 = r"flypaper|fiscal illusion|veil of oates|intergovernmental (?:transfer|grant)|grants?[- ]in[- ]aid|fiscal transfer|equali[sz]ation|lump-sum|unconditional grant|tax effort|own[- ]source revenue|local tax"
OFF = r"pollution|carbon|emission|social work|energy|climate|tourism|covid|pandemic|health care|hospital|school achievement|education quality"
LOC = r"municipal|local government|local authorit|subnational|sub-national|city|cities|county|counties"
loc_txt = (a.title.fillna("") + " " + a.abstract.fillna("") + " " + a.keywords.fillna("") + " " + a["keywords-plus"].fillna("")).str.lower()
a["hits"] = ta.str.count(CORE2)
a["off"] = ta.str.contains(OFF, regex=True) & ~ta.str.contains(r"flypaper|fiscal illusion", regex=True)
a["loc"] = loc_txt.str.contains(LOC, regex=True)
elig = a[(a.hits >= 2) & a["loc"] & ~a.off]
print("artigos elegíveis (critério restrito):", len(elig))
elig[["_key", "author", "year", "title", "journal", "doi", "hits"]].to_csv(OUT / "bib_elegiveis_criterio_restrito.csv", index=False)

# (d) idioma e nomes de autores (para a seção de limitações)
lang = df.language.value_counts()
print("\nidiomas:", lang.head(4).to_dict(), "| % inglês:", round(100 * lang.get("English", 0) / len(df), 1))
nomes = set()
for s in df.author.dropna(): nomes.update(x.strip().lower() for x in s.split(" and "))
print("nomes completos distintos no arquivo:", len(nomes), "(o bibliometrix contou 2.721 autores com nomes abreviados por sobrenome e iniciais)")
