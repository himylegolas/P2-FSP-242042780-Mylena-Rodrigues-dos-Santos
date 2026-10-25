# Análise bibliométrica (bibliometrix) - P2 Finanças do Setor Público
# Base: Web of Science Core Collection via Portal CAPES (UnB), busca em 24/10/2026, 1.547 artigos.
# Rodar no RStudio, com o diretório de trabalho na pasta do projeto (P2-FSP-242042780).

# install.packages("bibliometrix")   # só na primeira vez
library(bibliometrix)

files <- if (file.exists("bibliometria/wos_completo.bib")) "bibliometria/wos_completo.bib" else list.files("bibliometria", pattern = "\\.bib$", full.names = TRUE)  # usa o arquivo único, para não importar registros em duplicidade
print(files)                          # deve listar os 4 arquivos

M <- convert2df(file = files, dbsource = "wos", format = "bibtex")
cat("Documentos importados:", nrow(M), "\n")   # esperado: 1547 (ou pouco menos, se houver duplicatas)

results <- biblioAnalysis(M, sep = ";")
S <- summary(object = results, k = 10, pause = FALSE)

# Salva as tabelas e os gráficos para o repositório
dir.create("resultados/tabelas", recursive = TRUE, showWarnings = FALSE)
dir.create("resultados/graficos", recursive = TRUE, showWarnings = FALSE)
write.csv(S$MainInformationDF,        "resultados/tabelas/bibliometrix_informacoes_principais.csv", row.names = FALSE)
write.csv(S$AnnualProduction,         "resultados/tabelas/bibliometrix_producao_anual.csv",         row.names = FALSE)
write.csv(S$MostProdAuthors,          "resultados/tabelas/bibliometrix_autores_mais_produtivos.csv", row.names = FALSE)
write.csv(S$MostCitedPapers,          "resultados/tabelas/bibliometrix_artigos_mais_citados.csv",    row.names = FALSE)
write.csv(S$MostProdCountries,        "resultados/tabelas/bibliometrix_paises_mais_produtivos.csv",  row.names = FALSE)
write.csv(S$MostRelSources,           "resultados/tabelas/bibliometrix_periodicos_principais.csv",   row.names = FALSE)
write.csv(S$MostRelKeywords,          "resultados/tabelas/bibliometrix_palavras_chave.csv",          row.names = FALSE)

png("resultados/graficos/bibliometrix_resumo.png", width = 1600, height = 1200, res = 150)
plot(x = results, k = 10, pause = FALSE)
dev.off()

# Interface gráfica (Biblioshiny): em Data > Import or Load > Load bibliometrix file,
# ou importe de novo os arquivos .bib em "Import raw file" > Web of Science > BibTeX.
biblioshiny()
