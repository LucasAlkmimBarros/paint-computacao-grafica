# ── Códigos de Região (bitmask) ────────────────────────────────────────────
INSIDE = 0   # 0000 — dentro da janela
LEFT   = 1   # 0001 — à esquerda  (x < xmin)
RIGHT  = 2   # 0010 — à direita   (x > xmax)
ABOVE  = 4   # 0100 — acima       (y < ymin, em coordenadas de tela)
BELOW  = 8   # 1000 — abaixo      (y > ymax, em coordenadas de tela)


def _compute_code(x, y, xmin, ymin, xmax, ymax):
    """Calcula o código de região de um ponto em relação à janela de recorte."""
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= ABOVE   # y menor = acima na tela
    elif y > ymax:
        code |= BELOW   # y maior = abaixo na tela
    return code


def execute_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax, draw_pixel_func=None):
    """
    Algoritmo de Cohen-Sutherland para recorte de segmentos de reta.
    Método: regiões codificadas (bitmask).

    Parâmetros:
    - p1, p2       : Tuplas (x, y) dos extremos do segmento
    - xmin, ymin   : Canto superior-esquerdo da janela (coords de tela)
    - xmax, ymax   : Canto inferior-direito da janela  (coords de tela)
    - draw_pixel_func: Não utilizado — mantido para compatibilidade de assinatura

    Retorna:
    - ((x1', y1'), (x2', y2')) com o segmento recortado, ou
    - None se o segmento estiver completamente fora da janela
    """
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])

    code1 = _compute_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = _compute_code(x2, y2, xmin, ymin, xmax, ymax)

    while True:
        if not (code1 | code2):
            # Trivialmente aceito: ambos os pontos dentro da janela
            return (
                (int(round(x1)), int(round(y1))),
                (int(round(x2)), int(round(y2)))
            )

        if code1 & code2:
            # Trivialmente rejeitado: ambos do mesmo lado externo
            return None

        # Escolhe o ponto que está fora da janela
        code_out = code1 if code1 else code2

        # Calcula a interseção com a fronteira correspondente
        if code_out & BELOW:
            # Interseção com fronteira inferior: y = ymax
            if y2 != y1:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            else:
                x = x1
            y = ymax
        elif code_out & ABOVE:
            # Interseção com fronteira superior: y = ymin
            if y2 != y1:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            else:
                x = x1
            y = ymin
        elif code_out & RIGHT:
            # Interseção com fronteira direita: x = xmax
            if x2 != x1:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            else:
                y = y1
            x = xmax
        else:  # LEFT
            # Interseção com fronteira esquerda: x = xmin
            if x2 != x1:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            else:
                y = y1
            x = xmin

        # Substitui o ponto externo pelo ponto de interseção
        if code_out == code1:
            x1, y1 = x, y
            code1 = _compute_code(x1, y1, xmin, ymin, xmax, ymax)
        else:
            x2, y2 = x, y
            code2 = _compute_code(x2, y2, xmin, ymin, xmax, ymax)
