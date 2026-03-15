# IC-RNA-agricultura

## Objetivos

O objetivo deste projeto de pesquisa é identificar e comparar métodos de interpolação espacial aplicados à Agricultura de Precisão, visando a otimização da análise de dados de campo.

Como objetivos especificos desta analise:
[x] Buscar dados referentes a agricultura de precissão para identificar testar os algoritmos. 
[x] Implementar e treinar modelos de Redes Neurais Artificiais (RNA) e Krigagem para testar a eficiência de predição.
[] Comparar o desempenho dos algoritmos com base em métricas estatísticas (RMSE, MAE e $R^2$).

## Tecnologias usadas
- *Linguagem*: python;
- *Bibliotecas*: pykiger, keras, seaborn, pandas;

## Resultados esperados
Com a conclusão deste estudo, espera-se:
<ol>
    <li>
        Mapeamento de Variabilidade: Gerar mapas de calor que representem fielmente a distribuição espacial dos nutrientes ou atributos do solo na área estudada.
    </li>
    <li>
        Desempenho Preditivo: Avaliar se a Rede Neural Artificial (RNA) consegue superar a Krigagem em cenários de alta complexidade e não-linearidade dos dados.
    </li>
    <li>
        Análise de Erro: Identificar qual algoritmo apresenta o menor RMSE (Raiz do Erro Quadrático Médio), indicando maior precisão para a tomada de decisão no campo.
    </li>
    <li>
        Eficiência Computacional: Comparar o tempo de processamento e a facilidade de ajuste de hiperparâmetros entre as duas abordagens.
    </li>

</ol>

## Instalação das dependencias

<code>pip install --upgrade pip</code><br>
<code>pip install pandas seaborn matplotlib pykrige tensorflow</code>