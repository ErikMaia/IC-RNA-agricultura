# IC-RNA-agricultura

Projeto de pesquisa para comparar metodos de interpolacao espacial aplicados a Agricultura de Precisao.

## Objetivo

Avaliar o desempenho de tecnicas de predicao espacial para dados de campo, com foco inicial em altitude, comparando:

- Krigagem (`pykrige`)
- Rede Neural Artificial (Keras/TensorFlow)
- SVR (`scikit-learn`, etapa adicional no notebook)

## Pergunta de pesquisa

Qual abordagem apresenta melhor equilibrio entre:

- precisao de predicao
- qualidade da superficie espacial gerada
- custo computacional

## Metricas de avaliacao

- RMSE
- MAE
- R2
- IDE/ISI (Indice de Dependencia Espacial)

## IDE/ISI (dependencia espacial)

Para complementar a comparacao, o projeto passa a considerar tambem a dependencia espacial estimada pelo variograma:

- `IDE (%) = 100 * C1 / (C0 + C1)`
- `ISI (%) = 100 * C0 / (C0 + C1)`

Onde:

- `C0`: nugget (efeito pepita)
- `C1`: variancia estruturada

Interpretacao adotada:

- forte: `IDE >= 75` (equivalente a `ISI <= 25`)
- moderada: `25 <= IDE < 75`
- fraca: `IDE < 25`

Exemplo de uso no notebook:

```python
from src.spatial_metrics import ide_isi_from_pykrige

# params pode ser dict {'nugget': ..., 'sill': ...} ou lista [sill, range, nugget]
ide_info = ide_isi_from_pykrige(params)
print(ide_info)
```

## Estrutura do repositorio

```text
IC-RNA-agricultura/
|- data/
|- models/
|- src/
|  |- main.ipynb
|  |- krigagem.ipynb
|  |- mlp.ipynb
|  |- svr.ipynb
|  `- spatial_metrics.py
|- AI_CONTEXT.md
`- README.md
```

- `src/main.ipynb`: notebook historico/original com o fluxo completo.
- `src/krigagem.ipynb`: funcoes e execucao da krigagem.
- `src/mlp.ipynb`: funcoes e execucao da MLP (RNA).
- `src/svr.ipynb`: funcoes e execucao da SVR.
- `src/spatial_metrics.py`: funcoes para calcular IDE/ISI a partir de parametros do variograma.
- `data/`: dados de entrada em CSV.
- `models/`: pasta reservada para modelos/artefatos salvos.
- `AI_CONTEXT.md`: contexto rapido para onboarding de IA.

## Dados

Arquivos atuais:

- `data/Altitude_2025-10-14T20_07_43.980Z.csv`
- `data/Altitude_2025-10-14T20_15_03.183Z.csv`
- `data/Boundaries_Tasca_WGS84_UTM22s_2025-10-14T20_15_36.737Z.csv`

Colunas observadas:

- Altitude: `x`, `y`, `Altitude`
- Limites: `x`, `y`

Observacao: validar sistema de coordenadas entre os datasets antes da comparacao final dos modelos.

## Ambiente e dependencias

Requisitos:

- Python 3.10+
- `pip`

Instalacao rapida:

```bash
pip install --upgrade pip
pip install pandas numpy seaborn matplotlib pykrige keras tensorflow scikit-learn jupyter
```

## Como executar

1. Ative o ambiente virtual (recomendado).
2. Abra o notebook do metodo desejado em `src/` (`krigagem.ipynb`, `mlp.ipynb` ou `svr.ipynb`).
3. Execute as celulas em ordem.
4. Registre os resultados de cada metodo para comparacao.

## Status do projeto

- [x] Coleta e preparacao inicial dos dados
- [x] Implementacao base de Krigagem
- [x] Implementacao base de RNA
- [ ] Comparacao final consolidada por metricas (RMSE, MAE, R2, IDE/ISI)
- [ ] Persistencia padronizada de modelos em `models/`

## Melhorias planejadas

- padronizar CRS dos dados espaciais
- consolidar resultados em tabela unica (CSV/Markdown)
- reduzir warnings de entrada no SVR
- mover funcoes do notebook para modulos Python em `src/`

## Licenca

Este projeto esta sob a licenca MIT. Consulte o arquivo `LICENSE`.
