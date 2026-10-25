# Pontos a confirmar e imprecisões declaradas

Itens que **não** foram comprovados em fonte primária durante a elaboração ou que dependem de conferência humana antes da entrega.

## Dados
1. **Receita da Noruega (FMI):** há uma única fonte (Fiscal Monitor, out/2026, coletada em 24/10/2026). Não há segunda fonte independente. A diferença em relação ao trabalho anterior (WEO, out/2024) tem causa **não verificada**.
2. **Dados municipais da Noruega (SSB):** não foram coletados. A comparação com o país é apenas institucional e limitada ao agregado do governo geral.
3. **IPCA de 2024 e 2025:** vêm do arquivo oficial do IBGE baixado em 24/10/2026; as taxas de dez/dez de 2016 a 2023 conferem com as oficiais conhecidas, mas as de 2024 (4,83%) e 2025 (4,26%) não foram conferidas com outra fonte.
4. **População:** é a informada nos arquivos do Siconfi. O IBGE confirma que as estimativas de 2024 incorporam o Censo 2022; a causa exata da queda de 4,6% (Ananindeua) e 5,7% (Marabá) em 2024 não foi analisada.
5. **2025:** incluído na janela de análise (2015 a 2025), mas os arquivos trazem 132 dos 144 municípios paraenses; não se sabe se os demais enviaram a declaração depois, e os dados podem ser retificados.
5b. **Resultado de Marabá em 2025 (R$ 482,8 milhões):** decorre de alta das receitas correntes e de queda de urbanismo e investimentos em relação a 2024 (ano de eleição municipal). O artigo apenas registra o padrão e o descreve como compatível com um ciclo eleitoral, sem testá-lo; os dados de 2025 podem ser retificados.
6. **Receitas de 2015 a 2018:** o rótulo "Total Receitas" inclui as receitas intraorçamentárias (verificado: a diferença é igual à conta 7.0.0.0).

## Bibliometria
7. **Versão do Biblioshiny:** o artigo diz "versão 5", conforme a tela inicial. Confirmar com `packageVersion("bibliometrix")` no RStudio.
8. **Porcentagens de 32,4%, 43,9% e 24,2%:** vêm de classificação por palavras definida pela autora do estudo (script `02_bibliometria_complementar.py`); são aproximadas.
9. **Mapa temático:** a leitura de "alta centralidade e densidade intermediária" é visual (o gráfico não tem escala numérica).
10. **Contagens do Biblioshiny** (558 periódicos, 2.721 autores, palavras-chave) diferem de recontagens diretas do `.bib` por normalização do próprio programa.

## Referências
11. **Acentos nos nomes de autores:** a Web of Science exporta os nomes sem acento, e a conferência foi feita autor a autor nas páginas dos periódicos e dos repositórios. **Aplicado:** Guillamón (Policy Studies, 2022), Håkonsen, Løyland, Rattsø e Sandsør. **Confirmado sem acento no registro do periódico:** Aragon (National Tax Journal, 2013) e Rios (Local Government Studies, 2022). **Não confirmado e mantido como veio da base** (conferir pelo DOI de cada referência): Cárdenas (uma citação de terceiros em espanhol grafa com acento, mas o registro do periódico não foi visto), Caamaño-Alegre, López-Iglesias, Gómez Monge, Vivar Mercadillo, Yüksel, Kjærgaard, Majdzińska, Żołtaszek, Wójtowicz, Araújo (Rego de Araujo; Leitão Araújo) e Sáenz (Saens).
12. **Referência do IBGE (2024):** o ano está entre colchetes por não constar de forma explícita no trecho consultado.
13. **Seleção das 96 referências:** 91 vieram do corpus pelo critério restrito, após leitura dos resumos; 5 estudos sobre a Noruega foram incluídos por busca dirigida. Os resumos foram lidos total ou parcialmente; as descrições se limitam ao que o trecho lido dizia.
14. **Tese de Ferreira (2021):** consultada em seu resumo, em sua introdução e em seu primeiro estudo (capítulo 2); os capítulos 3 e 4 foram conhecidos apenas pelo resumo e pela introdução, e o capítulo 5 não foi lido. A cifra de 65,9% (IBGE, 2018) citada na tese aparece sem a base de cálculo no trecho lido.

## Texto
15. **Afirmações de conhecimento geral sem fonte no artigo:** Ananindeua pertence à região metropolitana de Belém; Marabá fica no sudeste do Pará; Pará tem 144 municípios; a Noruega é um Estado unitário.
16. **Formatação:** o PDF foi gerado com a fonte Liberation Sans (equivalente à Arial). No Word, a fonte é a Arial.
17. **Arquivos do Siconfi no repositório:** são recortes (linhas de Ananindeua, Marabá e Belém), e não os arquivos completos. Os 144 municípios aparecem apenas na tabela de cobertura. Para auditar outro município, é preciso baixar os arquivos completos do Siconfi.
18. **Imagem da rede de co-ocorrência:** a versão do repositório é a usada no artigo (recortada e reduzida a 3.200 pixels de largura); a exportação original do Biblioshiny, de 6.025 pixels, não foi incluída.
