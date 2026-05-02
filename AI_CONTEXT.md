# Contexto do Projeto para IA

## Resumo
Este projeto investiga metodos de interpolacao espacial para Agricultura de Precisao, com foco em comparar:
- Krigagem (`pykrige`)
- Rede Neural Artificial (Keras/TensorFlow)
- SVR (em etapa adicional no notebook)

Os experimentos agora estao divididos em notebooks por metodo:
- [krigagem.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/krigagem.ipynb)
- [mlp.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/mlp.ipynb)
- [svr.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/svr.ipynb)

O [main.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/main.ipynb) permanece como historico/legado.

## Objetivo de Pesquisa
Comparar desempenho de modelos na predicao espacial de atributos de campo (inicialmente altitude), usando metricas como:
- RMSE
- MAE
- R2
- IDE/ISI (Indice de Dependencia Espacial)

## Estrutura do Repositorio
- [README.md](C:/Users/Erik/Projetos/IC-RNA-agricultura/README.md): descricao geral do estudo e dependencias.
- `data/`: CSVs de entrada.
- [krigagem.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/krigagem.ipynb): fluxo de krigagem.
- [mlp.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/mlp.ipynb): fluxo de MLP (RNA).
- [svr.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/svr.ipynb): fluxo de SVR.
- [main.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/main.ipynb): notebook original consolidado.
- `models/`: pasta prevista para persistencia dos modelos (atualmente sem arquivos).

## Dados Disponiveis
Arquivos encontrados:
- `data/Altitude_2025-10-14T20_07_43.980Z.csv`
- `data/Altitude_2025-10-14T20_15_03.183Z.csv`
- `data/Boundaries_Tasca_WGS84_UTM22s_2025-10-14T20_15_36.737Z.csv`

Esquema observado:
- Arquivos de altitude: colunas `x`, `y`, `Altitude`
- Arquivo de limites: colunas `x`, `y`

Observacao importante:
- As coordenadas de altitude parecem estar em lon/lat (graus decimais, valores negativos).
- O arquivo de limites parece estar em UTM (valores grandes positivos).
- Antes de analises espaciais finais, confirmar se todos os dados estao no mesmo sistema de referencia.

## Fluxo Atual
Sequencia recomendada:
1. Executar `src/krigagem.ipynb` para resultados de krigagem.
2. Executar `src/mlp.ipynb` para resultados de MLP.
3. Executar `src/svr.ipynb` para resultados de SVR.
4. Consolidar metricas em tabela unica.

Sinais no notebook:
- Aviso de TensorFlow sobre indisponibilidade de GPU nativa no Windows para versoes recentes.
- Avisos do `sklearn` sobre `X does not have valid feature names` no uso de SVR.

## Dependencias (conforme projeto)
Bibliotecas citadas no repositorio/notebook:
- pandas
- numpy
- seaborn
- matplotlib
- scikit-learn
- pykrige
- keras / tensorflow

Modulo auxiliar local:
- `src/spatial_metrics.py` para calculo de IDE/ISI.

## Estado Atual do Projeto
- Pipeline experimental implementado no notebook.
- Comparacao entre metodos em andamento.
- Persistencia de modelos ainda nao consolidada na pasta `models/`.
- Nao ha pacote Python estruturado (o notebook e o ponto de entrada principal).

## Como Rodar Rapido
1. Ativar ambiente virtual (`.venv`).
2. Instalar dependencias.
3. Executar os notebooks por metodo:
   - [krigagem.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/krigagem.ipynb)
   - [mlp.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/mlp.ipynb)
   - [svr.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/svr.ipynb)

## Pendencias Tecnicas Recomendadas
1. Padronizar encoding de textos (`README.md` mostra caracteres acentuados quebrados).
2. Definir CRS unico para todos os dados espaciais.
3. Estruturar saidas de avaliacao (tabela consolidada com RMSE/MAE/R2 por modelo e por dataset).
4. Incluir IDE/ISI para os modelos geoestatisticos baseados em variograma.
5. Salvar modelos e artefatos com nomenclatura reprodutivel em `models/`.
6. Migrar funcoes principais do notebook para scripts/modulos em `src/` para facilitar reproducao por IA e automacao.

## Guia para Outra IA Trabalhar Neste Projeto
Se voce (IA) for continuar este trabalho, siga esta ordem:
1. Ler [README.md](C:/Users/Erik/Projetos/IC-RNA-agricultura/README.md) e este arquivo.
2. Inspecionar colunas e CRS dos CSVs em `data/`.
3. Executar [krigagem.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/krigagem.ipynb), [mlp.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/mlp.ipynb) e [svr.ipynb](C:/Users/Erik/Projetos/IC-RNA-agricultura/src/svr.ipynb), registrando metricas por modelo.
4. Calcular IDE/ISI dos parametros de variograma com `src/spatial_metrics.py`.
5. Corrigir warnings de entrada no SVR (manter nomes de features consistentes entre treino e predicao).
6. Exportar resultados finais em formato tabular (CSV/Markdown) para comparacao objetiva.

## Suposicoes deste Documento
- Este documento foi gerado com base na estrutura e conteudo atuais do repositorio.
- Se o notebook mudar, atualize este arquivo para manter o contexto sincronizado.
