# TP1 - Paint App (Computação Gráfica)
**Aluno:** Lucas Alkmim

Trabalho prático da disciplina de Computação Gráfica. Esta é uma aplicação interativa que implementa os principais algoritmos de rasterização, recorte e transformações geométricas 2D (Unidade 1), sem usar as bibliotecas nativas de desenho ou cálculos internos equivalentes das *gui frameworks*.

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

## 🚀 Como Rodar (Avaliação)

### No Windows (Opção Principal via Instalador/Executável)

Foi preparado um script `.bat` compatível com os requisitos de entrega (atuando como instalador de bibliotecas e inicializador do software sem complexidade).

1. Extraia a pasta do projeto (`TP1_CG_Lucas_Alkmim`).
2. Acesse a pasta e dê **dois cliques no arquivo `executar.bat`**.
3. O script irá automaticamente verificar sua versão do Python, instalar em segundo plano as dependências necessárias de interface (`customtkinter`) e rodar a aplicação.

> **Importante:** É necessário que você tenha o **Python 3.x** instalado em sua máquina com a caixa "Add Python to PATH" marcada. O instalador faz a verificação automatizada.

### No MacOS / Linux

1. Abra um terminal na raiz desta pasta e instale a dependência de layout via `pip`:
```bash
pip install customtkinter
```
*(Nota para usuários macOS/Linux mais recentes: caso ocorra alerta de proteção do pip, utilize a flag extra `pip install customtkinter --break-system-packages`)*

2. Em seguida, execute primariamente com:
```bash
python3 main.py
```

## 📹 Vídeo de Testes e Apresentação

Junto com os arquivos-fonte nesta mesma pasta, foi adicionado um vídeo (arquivo `.mov`) com captura de tela contendo o uso explicativo em áudio de todos os algoritmos avaliados (teste de rasterização, área de recorte comportamental e processamento de geometria e cálculos).

## 🖱 Modos de Uso Gerais da Interface

Toda a interação é concebida inteiramente via uso de cliques na interface (sem necessidade do console/terminal durante o uso):

1. **Aba de Rasterização:** Clique no canvas para marcar os pontos limitantes (ponto primário e secundário) que invocarão aquele algoritmo, pintando diretamente o traçado resultante do cálculo que ocorre no *backend*.
2. **Aba de Recorte:** Arrastar e demarcar o cursor no *canvas* definirá a "área de Janela". Uma vez definido (ou explicitamente inserido via teclado), é possível testar livremente intersecções visuais que ocultam áreas rejeitadas.
3. **Aba de Transformações:** Aplicar funções aos atributos multiplicará a matriz base dos pontos e transformará a cena visualmente sobre essas atualizações progressivas.
