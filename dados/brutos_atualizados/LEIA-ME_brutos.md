# Dados brutos atualizados

## Arquivos do Siconfi (Finbra / DCA)
Os 33 arquivos `finbra_*` são **recortes** dos arquivos baixados do Siconfi (https://siconfi.tesouro.gov.br) em 24/10/2026: anexo I-C (receitas orçamentárias), I-D (despesas orçamentárias) e I-E (despesas por função), de 2015 a 2025.

- **O que foi mantido:** as quatro primeiras linhas de cada arquivo (metadados e cabeçalho das colunas) e **todas as linhas** de três instituições: Ananindeua (código IBGE 1500800), Marabá (1504208) e Belém (1501402).
- **O que foi retirado:** as linhas dos demais municípios do Pará. Nenhum valor foi alterado, e o texto de cada linha foi mantido exatamente como no arquivo original.
- **Por que Belém:** é a evidência do erro do trabalho anterior, em que a série atribuída a Marabá era a de Belém (receita líquida de R$ 4.886,8 milhões em 2023).
- **Por que o recorte:** os arquivos completos somam cerca de 108 MB e trazem os 144 municípios do Pará, o que não cabe no envio pelo navegador ao GitHub. O número de municípios de cada arquivo original está em `../documentacao/cobertura_municipios_por_ano.csv`.
- **Nome dos arquivos:** mantidos como baixados. Em 2022, o arquivo de despesas orçamentárias (I-D) correto é o de sufixo `_csv_1`.

## Demais arquivos
- `ipca_202609SerieHist.xls`: série histórica do IPCA (número-índice), IBGE, completa.
- `fmi_fiscal_monitor_noruega_receita_pib_2014_2026.csv`: receita do governo geral da Noruega em % do PIB (Fiscal Monitor, outubro de 2026, indicador GGR_G01_GDP_PT), coletada em 24/10/2026.

Os resultados do artigo se reproduzem com estes arquivos: `python scripts/01_tratamento_painel_municipal.py dados/brutos_atualizados dados/tratados` gera o mesmo painel entregue em `dados/tratados`.
