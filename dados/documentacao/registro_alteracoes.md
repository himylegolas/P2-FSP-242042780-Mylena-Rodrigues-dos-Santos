# Registro de alterações (trabalho anterior x versão atual)

Trabalho anterior: *Análise de Finanças Públicas Comparada: Noruega, Ananindeua-PA e Marabá-PA* (FSP.PDF, 2025) e os 5 CSVs da issue #2 (`dados/originais`, preservados sem alteração).

| # | O que foi encontrado | Evidência | Providência |
|---|---|---|---|
| 1 | O "Marabá" dos CSVs é Belém (cod_ibge 1501402, "Prefeitura Municipal de Belém - PA", população de ~1,5 mi) | Colunas `cod_ibge`, `instituicao` e `populacao`; a receita "de Marabá" de 2023 (R$ 4.886,8 mi) é igual à receita líquida de Belém na DCA | Marabá recoletada pelo código 1504208. Conclusões do PDF antigo sobre Marabá (p. ex., receita per capita 6,5 vezes a de Ananindeua) descartadas |
| 2 | Valores "reais" do PDF superestimados em 3,3% a 7,9% (média de 6,2% em 2015-2022) para Ananindeua | Fatores do PDF comparados ao IPCA oficial (média anual e dezembro): nenhum reproduz o fator usado | Deflator refeito com o número-índice do IPCA/IBGE; ano-base 2024 |
| 3 | `Norue.xlsx` com decimais removidos e zeros finais perdidos | Valores municipais x100; dígitos ausentes em linhas isoladas | Arquivo não usado; permanece só como evidência. Dados reconstruídos das fontes |
| 4 | Série municipal começa em 2015 (nome dos arquivos diz 2014) | Contagem por exercício | Janela 2015-2025 |
| 5 | Fonte municipal: RREO bimestral | Comparação com a DCA | Passa a ser a DCA/Finbra (anexos I-C, I-D, I-E); em 2015-2023 a receita líquida de Ananindeua coincide com o RREO (diferença máxima de R$ 0,72 mi em 2016) |
| 6 | "Total Receitas" de 2015-2018 inclui receitas intraorçamentárias | Soma de correntes + capital menor que o rótulo | Total recalculado como correntes + capital em todos os anos |
| 7 | Mudança de classificação da receita em 2018 (códigos e nome do grupo 1.1) e dois formatos de código de despesa | Códigos de conta por ano | Seleção por prefixo do código; funções por código de 2 dígitos |
| 8 | Operações de crédito de Ananindeua de 5% a 12% da receita bruta a partir de 2021 | DCA I-C | Receita sem crédito passa a ser considerada nas leituras de capacidade fiscal |
| 9 | Dependência de transferências do PDF ("55% a 75% nos dois municípios") | DCA I-C | Recalculada: Ananindeua 77,2% (2015) a 62,7% (2024); Marabá 69,1% a 61,8% |
| 10 | Quebra da população em 2024 (estimativas após o Censo 2022) e valores repetidos | Coluna `populacao` | Mantida como informada; limitação declarada |
| 11 | Receita da Noruega do FMI atual diverge do PDF antigo | FMI Fiscal Monitor (out/2026) x WEO (out/2024) citado no PDF | Registrada; causa não verificada |
| 12 | Curva de Laffer: coeficiente quadrático positivo indica parábola convexa (vértice = mínimo); regressão receita x PIB com n=10 e séries com tendência | Tabela 5 e 6 do PDF antigo | Análises abandonadas no novo desenho (descritivo comparativo) |
| 13 | Arquivos do Siconfi pesados demais para o envio ao GitHub (cerca de 108 MB, com os 144 municípios do Pará) | Tamanho dos arquivos baixados | Recortes com as linhas de Ananindeua, Marabá e Belém, sem alterar valores; cobertura por ano em `cobertura_municipios_por_ano.csv`; painel refeito a partir dos recortes é idêntico ao entregue |
