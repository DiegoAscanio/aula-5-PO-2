<style>
  .cabecalho {
    position: absolute;
    top: 10%;
    margin-left: 5%;
    margin-right: 10%;
    font-size: 48px;
    font-weight: bold;
  }
  .conteudo {
    position: absolute;
    top: 30%;
    margin-left: 5%;
    margin-right: 10%;
    font-size: 28px;
    text-align: justify;
  }
  .small {
    font-size: 20px;
  }
  .tiny {
    font-size: 12px;
  }
  .bold {
    font-weight: bold;
  }
  .center {
    text-align: center;
  }
</style>

![bg opacity](./background.png)
# Pesquisa Operacional II
## Otimização Inteira (Aula 2 - Algoritmo Branch and Bound)

Prof. M.Sc. Diego Ascânio Santos (ascanio@cefetmg.br)

Aula baseada sobre o material do professores Dr. João Fernando Machry Sarubbi (joao@cefetmg.br - DECOM), Fernando Nogueira e vídeoaulas do curso de algoritmos de pesquisa operacional da Universidade Nacional de Taiwan.

Belo Horizonte, 2023.

---
<div class="cabecalho">
Roteiro
</div>

<div class="conteudo">
<ol>
  <li>Introdução</li>
  <li>Algoritmo Branch and Bound</li>
  <li>Solução de problemas de programação inteira usando Branch and Bound</li>
  <li>Modelagem de problemas de programação inteira e solução com algoritmo branch and bound</li>
</ol>
</div>

---
![bg opacity](./background.png)
# Introdução

---
![bg opacity](./background.png)
<div class="cabecalho">
Porque estudar o Algoritmo Branch and Bound.
</div>
<div class="conteudo">
<p>
Porque quase nunca os arredondamentos para numeros das soluções do SIMPLEX para programação inteira produzem soluções factíveis ou ótimas, bem como, pelo custo exponencial \(n^m\) para verificação de soluções pelo algoritmo de força bruta é que precisamos de soluções computacionalmente mais eficientes para resolver problemas de programação inteira.
</p>
<br>
<p>
Destarte, os algoritmos branch-and-bound (particiona e delimita) e de planos de corte são alternativas que oferecem maior eficiência computacional. Na aula de hoje, veremos o algoritmo branch-and-bound.
</p>
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Classificação dos problemas.
</div>
<div class="conteudo">
<p>
Os problemas são classificados de acordo com o tipo de variáveis que possuem:
</p>
<br>
<ul>
  <li>Apenas variáveis inteiras;</li> <!-- programação inteira pura -->
  <li>Variáveis inteiras e contínuas;</li> <!-- programação inteira mista -->
  <li>Variáveis binárias \(0 / 1\);</li> <!-- programação inteira binária -->
  <li>Variáveis inteiras genéricas;</li>
</ul>
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Discussões
</div>

<div class="conteudo"> 
<p>
A priori, é discutível a aplicação prática da restrição de valores a números inteiros. Entretanto, como veremos nesta e nas próximas aulas, esta restrição constitui-se uma ferramenta muito poderosa para a resolução de problemas do mundo real.
</p>
<br>
<p>
Inclusive, grande parte das aplicações práticas da programação inteira são mais restritas ainda, aos problemas de programação binária, que representam (por exemplo) problemas de decisão do tipo comprar / não comprar, alocar / não alocar, vender / não vender, representações diversas, dentre outros.
</p>
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Aplicações
</div>
<div class="conteudo">
  <ul>
    <li>Dimensionamento de lotes de itens a serem produzidos \( 0/1 \)</li>
    <li>Custo fixo de produção \( 0/1 \)</li>
    <li>Localização de plantas de produção / entregas \( 0/1 \)</li>
    <li>Alocação de funcionários em restaurantes de uma cadeia de <i>fastfood</i> \( X \in Z \) </li>
    <li>Seleção de itens para transporte (problema da mochila - PIB, PIP, PIM)</li>
  </ul>
  <br>
  <p>Hoje, o foco da nossa aula encontra-se nos problemas inteiros puros genéricos, como o problema das namoradas, o problema da alocação de funcionários em restaurantes de fastfood, dentre outros.</p>
</div>

---
![bg opacity](./background.png)
# Limitações do uso do SIMPLEX arredondado para solução de PI

---
![bg opacity](./background.png)
# De fato, os problemas de programação inteira podem ser "relaxados" à sua forma linear, serem resolvidos pelo SIMPLEX e serem novamente restritos ao domínio dos inteiros através de arredondamento.

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Arredondamento
</div>

<div class="conteudo">
Mas, funciona em todos os casos?
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Arredondamento
</div>

<div class="conteudo">
Mas, funciona em todos os casos?
<br>
<br>
<span style="font-size: 48px; font-weight: bold;">
DEPENDE

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Arredondamento
</div>

<div class="conteudo">
Mas, funciona em todos os casos?
<br>
<br>
<span style="font-size: 48px; font-weight: bold;">
DEPENDE
</span>
<br>
<br>
Quando o problema envolve grandes magnitudes, o arredondamento não traz grandes impactos.
<ul>
  <li>Produção de carros da GM</li>
  <li>Alocação de passageiros da American Airlines</li>
</ul>
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Programação Inteira - Arredondamento
</div>

<div class="conteudo">
Mas, funciona em todos os casos?
<br>
<br>
<span style="font-size: 48px; font-weight: bold;">
DEPENDE
</span>
<br>
<br>
Entretanto, a mesma realidade não se reproduz em pequenas magnitudes.
<ul>
  <li>Alocação de funcionários para redes de <i>Fastfood</i> (Subway, Tacobell, etc.);</li>
  <li>Quantidade de saídas com suas namoradas;</li>
  <li>Entre outros</li>
</ul>
</div>

---
![bg opacity](./background.png)
<h2 style="text-align: center"> A regra do arredondamento da solução não necessariamente conduz a soluções ótimas em todos os casos, e portanto, não é um procedimento robusto para solucionar problemas de Programação Inteira. </h2>

---
![bg opacity](./background.png)
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6" scoped></script>
<script id="MathJax-script" async src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" scoped></script>
<script>
window.MathJax = {
  loader: {load: ['[tex]/ams']},
  tex: {packages: {'[+]': ['ams']}}
};
</script>
<div class="cabecalho">
Verificação da insuficiência do arredondamento
</div>

<div class="conteudo" style="margin-left: 30%; margin-right: 30%">
Considere:

$$
\begin{equation}
\begin{split}
\text{max}(21x_1 + 11x_2) \\

\text{Sujeito a: } \\

\left\{
    \begin{array}{lr}
        7x_1 + 4x_2 \leq 13\\
        x_1, x_2 \geq 0 \in Z
    \end{array}
\right.

\end{split}
\end{equation}
$$

A solução ótima do problema é:

$$ x_1 = 0, x_2 = 3 $$
<!-- Verificado por meio de força bruta -->
</div>

---
![bg opacity](./background.png)
<iframe src="https://mybinder.org/v2/gh/DiegoAscanio/aula-4-PO-2/master?labpath=simplex_insuficiencias.ipynb" width=100% height=100% ></iframe>
<!--<iframe src="http://localhost:8888/notebooks/simplex_insuficiencias.ipynb" width=100% height=100% ></iframe>-->

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/diegoAscanio/aula-4-po-2/master)

---
![bg opacity](./background.png)
# Como encontrar a solução ótima?
## Solução de problemas de programação inteira - Algoritmo Força Bruta!

---
![bg opacity](./background.png)
<div class="cabecalho">
Algoritmos de Resolução de Programação Inteira - Força Bruta
</div>

<div class="conteudo">
<p>
Força-Bruta é um tipo de algoritmo que consiste em resolver um problema computacional através da força bruta 🤣🤣🤣🤣🤣🤣
</p>
<br>
<p>
Brincadeiras a parte, o algoritmo leva este nome por tentar todas as soluções possíveis para resolver um problema.
</p>
<!-- Por isso, recebe o nome de força bruta -->
<br>
<p>
É garantido que em algum momento o Algoritmo encontrará a solução ótima do problema. Entretanto, quando esta solução será encontrada é que é o problema. Porquê?
</p>
<!-- Porque têm custo exponencial, de ordem n (numero de variáveis) ** m (valores maximos que estas variaveis podem assumir) -->
<!-- Assim, é infactível resolver problemas médios em nosso tempo de vida terrestre -->
</div>

---
![bg opacity](./background.png)
<div class="cabecalho">
Algoritmos de Resolução de Programação Inteira - Força Bruta
</div>

<div class="conteudo small">
<!-- Um algoritmo de força bruta para problemas de programação inteira -->
<p>
Um algoritmo de força bruta pode ser representado pelos seguintes passos:
</p>
<br>
<p>
<ol>
<li>Defina uma variável max (min) como -infinita (infinita)</li>
<li>Defina seu vetor de variáveis candidatas</li>
<li>Delimite o espaço de buscas através das restrições</li>
<li>No espaço de buscas, para cada combinação possível de valores das variáveis que respeite as restrições: </li>
  <ul>
    <li>Aplique a combinação de valores na função objetivo</li>
    <li>Se o valor da combinação de valores aplicada função objetivo for \( \gt \text{max} \) </li>
    <ul>
      <li>Atualize o vetor de variáveis candidatas com a combinação de valores</li>
      <li>Atualize max para o valor da aplicação da combinação de valores na função objetivo</li>
    </ul>
  </ul>
  <li>Ao término do algoritmo é garantido que é encontrado o vetor ótimo de variáveis que maximiza(minimiza) a função objetivo</li>
</ol>
</p>
</div>

---
![bg opacity](./background.png)
# Implementação do Algoritmo de Força Bruta

---
![bg opacity](./background.png)
<iframe src="https://mybinder.org/v2/gh/DiegoAscanio/aula-4-PO-2/master?labpath=forca_bruta.ipynb" width=100% height=100% ></iframe>
<!--<iframe src="http://localhost:8888/notebooks/forca_bruta.ipynb" width=100% height=100% ></iframe>-->

---
![bg opacity](./background.png)
# Resolução do problema das namoradas pelo Algoritmo de Força Bruta

---
![bg opacity](./background.png)
<iframe src="https://mybinder.org/v2/gh/DiegoAscanio/aula-4-PO-2/master?labpath=namoradas_forca_bruta.ipynb" width=100% height=100% ></iframe>
<!--<iframe src="http://localhost:8888/notebooks/namoradas_forca_bruta.ipynb" width=100% height=100% ></iframe>-->

---
![bg opacity](./background.png)
# Próxima aula: Algoritmo Branch and Bound
