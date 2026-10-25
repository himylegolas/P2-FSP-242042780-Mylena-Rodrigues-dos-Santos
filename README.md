# Dependência de transferências e composição fiscal em Ananindeua e Marabá (PA), 2015 a 2025

**Autora:** Mylena Rodrigues  
**Matrícula:** 242042780  
**Disciplina:** Finanças do Setor Público (CCA0169), Universidade de Brasília, 2026.2

> ### Comece por aqui
> **[Ler o artigo em PDF](artigo/artigo_242042780.pdf)** (versão em Word: [artigo_242042780.docx](artigo/artigo_242042780.docx))

## Do que trata o trabalho

Este trabalho atualiza o estudo anterior da disciplina, que comparava a Noruega com os municípios paraenses de Ananindeua e Marabá. A base foi refeita a partir de fontes oficiais (Siconfi, IBGE e FMI), os erros do trabalho anterior foram corrigidos e as séries foram estendidas até 2025, em valores reais de 2024.

**A pergunta:** em que medida a composição das receitas (transferências e arrecadação própria) e das despesas difere entre os dois municípios, e o que isso sugere sobre dependência fiscal à luz da literatura sobre o efeito flypaper e a ilusão fiscal, tendo a Noruega como referência institucional? O desenho é descritivo: **não** se estimam efeitos causais.

## Principais resultados

- As transferências correntes respondem por **61% a 77%** da receita bruta de Ananindeua e por **62% a 72%** da de Marabá.
- A receita líquida real por habitante de Marabá equivale a **2,3 vezes** a de Ananindeua em 2015 e a **2,2 vezes** em 2025.
- **Correção importante:** no trabalho anterior, a série atribuída a Marabá era, na verdade, a de **Belém**, e o deflator superestimava os valores reais de Ananindeua entre 3,3% e 7,9%.
- Em Ananindeua, o recurso ao crédito cresce a partir de 2021, e o perfil da despesa muda em 2022 e 2023, com mais investimento e juros. Os dados mostram a coincidência, mas não permitem atribuir causa.

## O que há em cada pasta

| Pasta | Conteúdo |
|---|---|
| [`artigo/`](artigo) | O artigo completo (PDF e Word), com lista de siglas, sumário, mapeamento bibliométrico, referencial teórico, metodologia, resultados e conclusão |
| [`dados/originais/`](dados/originais) | Os 5 arquivos do trabalho anterior, **sem alteração** |
| [`dados/brutos_atualizados/`](dados/brutos_atualizados) | Dados das fontes coletados em 24/10/2026: recortes dos arquivos do Siconfi (linhas de Ananindeua, Marabá e Belém, sem nenhum valor alterado), IPCA e série do FMI. Explicação em `LEIA-ME_brutos.md` |
| [`dados/tratados/`](dados/tratados) | Painel municipal tratado, em valores reais de 2024 e per capita, e as séries usadas no artigo |
| [`dados/documentacao/`](dados/documentacao) | Dicionário de variáveis, registro de alterações em relação ao trabalho anterior, pendências declaradas e cobertura do Siconfi por ano |
| [`scripts/`](scripts) | Códigos que refazem o painel e as tabelas bibliométricas a partir dos dados brutos |
| [`resultados/`](resultados) | Gráficos e tabelas do artigo |
| [`bibliografia/`](bibliografia) | Candidatas a referência (com metadados da Web of Science) e as referências da seção bibliométrica |
| [`bibliometria/`](bibliometria) | Dados de entrada do bibliometrix (1.547 artigos da Web of Science) e as saídas do Biblioshiny |

## Como reproduzir

1. Instale as bibliotecas: `pip install pandas xlrd matplotlib`.
2. Refaça o painel tratado: `python scripts/01_tratamento_painel_municipal.py dados/brutos_atualizados dados/tratados`.
3. Refaça a Tabela 1 da bibliometria e o conjunto de 219 artigos elegíveis: `python scripts/02_bibliometria_complementar.py bibliometria/wos_completo.bib resultados/tabelas`.
4. Para repetir a análise no bibliometrix, abra o RStudio e rode `install.packages("bibliometrix")`, `library(bibliometrix)` e `biblioshiny()`, e importe `bibliometria/wos_completo.bib` (ou use `scripts/analise_bibliometrix.R`).

Para refazer a partir dos arquivos completos do Siconfi (anexos I-C, I-D e I-E da DCA), baixe-os em https://siconfi.tesouro.gov.br e coloque-os em `dados/brutos_atualizados/`, inclusive os reenviados com sufixo `_csv_1` (em 2022, o arquivo correto das despesas orçamentárias I-D é o `_csv_1`). O script escolhe o arquivo com o título certo e avisa se faltar algum.

## Decisões metodológicas

- **Receita líquida:** receitas correntes mais receitas de capital, exceto intraorçamentárias, menos as deduções.
- **Despesa:** liquidada, exceto intraorçamentárias.
- **Valores reais:** média anual do IPCA, com 2024 como ano-base.
- **Janela de análise:** 2015 a 2025 (onze exercícios).

## Fontes

- Siconfi / Tesouro Nacional: https://siconfi.tesouro.gov.br
- IBGE, IPCA: https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9256-indice-nacional-de-precos-ao-consumidor-amplo.html
- FMI, Fiscal Monitor (outubro de 2026): https://www.imf.org/external/datamapper
- Web of Science Core Collection, acessada pelo Portal de Periódicos da CAPES (busca de 24/10/2026, 1.547 artigos)

O detalhamento por variável está em [`dados/documentacao/dicionario_variaveis.csv`](dados/documentacao/dicionario_variaveis.csv).

## Limitações conhecidas

- Os dados de 2025 do Siconfi são os mais recentes e podem ser retificados (os arquivos trazem 132 dos 144 municípios paraenses). A estimativa de população muda em 2024, com a incorporação do Censo 2022.
- A receita da Noruega do FMI difere dos valores do trabalho anterior, por causa não verificada. **Os dados municipais da Noruega não foram coletados:** a Noruega entra apenas pelo agregado fiscal do FMI, e a despesa e o saldo não foram coletados.
- Com dois municípios e onze anos, não há inferência causal: os resultados são descritivos.
- A base da Web of Science mistura a literatura de federalismo fiscal com a de descentralização e meio ambiente na China, e por isso a lista de referências usa um recorte mais estrito.
- O artigo discute 96 estudos de periódicos, além de 5 trabalhos citados na seção bibliométrica. Nomes de autores e de periódicos podem ter perdido acentos na exportação da base e devem ser conferidos.
- A tese de Ferreira (2021), indicada como referência de partida, foi consultada em seu resumo, introdução e primeiro estudo, e não integralmente.

A lista completa de pendências está em [`dados/documentacao/pontos_a_confirmar.md`](dados/documentacao/pontos_a_confirmar.md).
