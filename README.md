# Paint App - Computação Gráfica

Trabalho prático da disciplina de Computação Gráfica. Esta é uma aplicação interativa que implementa os principais algoritmos de rasterização, recorte e transformações geométricas 2D (Unidade 1), sem usar as bibliotecas nativas de desenho ou cálculos internos equivalentes das <i>gui frameworks</i>.

## Funcionalidades Implementadas

* **Rasterização de Primitivas:**
  * Retas: Algoritmo DDA e Algoritmo de Bresenham.
  * Circunferências: Algoritmo de Bresenham.
  * Polígonos (compostos pelas retas criadas do algoritmo DDA/Bresenham).
* **Recorte de Elementos:**
  * Regiões Codificadas (Cohen-Sutherland).
  * Equação Paramétrica (Liang-Barsky).
* **Transformações Geométricas 2D:**
  * Translação (eixos X e Y).
  * Rotação (ângulos por graus).
  * Escala (crescimento e encolhimento).
  * Reflexão (Eixo X, Eixo Y e Origem).

## Pré-requisitos

Para rodar o projeto, é necessário que você tenha o **Python** instalado em sua máquina.

Além da biblioteca nativa do Python (`tkinter`), a interface projetada requer a instalação da biblioteca `customtkinter`.

Abra o prompt de comando (CMD) ou PowerShell e digite:

```bash
pip install customtkinter
```
*(Nota para usuários macOS/Linux: caso ocorra erro de ambiente gerenciado externamente, utilize `pip install customtkinter --break-system-packages`)*

## Como Rodar

Basta baixar ou extrair o repositório, abrir um terminal na raiz do projeto e executar o script primário:

```bash
python main.py
```

## Modos de Uso Detalhados

Toda a interação é concebida inteiramente via uso de cliques e interação com interface sem uso do console/terminal:

1. **Aba de Rasterização:** Clique no canvas para marcar os pontos limitantes (ponto primário e secundário) que invocarão aquele algoritmo, pintando diretamente o traçado resultante do cálculo que ocorre do *backend*.
2. **Aba de Recorte:** Arrastar e demarcar o cursor no *canvas* definirá a "área de Janela". Uma vez definido ou explicitamente inserido manualmente, é possível testar e visualizar o comportamento dinâmico e correto do comportamento e limite dos fragmentos da cena em tela por intersecções de retas e da limitação na *bounding-box* circular.
3. **Aba de Transformações:** Clique em elementos os selecionará iterativamente, e aplicar funções aos seus atributos modificará a estrutura base dos pontos, transformando a cena real matematicamente, que será redesenhada visualmente sobre essas atualizações.
