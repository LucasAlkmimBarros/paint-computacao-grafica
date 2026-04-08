
def region_code(x, y, xmin, ymin, xmax, ymax):
    """
    função region_code(x, y)
    Calcula o código de região binário de um ponto em relação à janela de recorte.

    Bits:
      bit 0 (valor 1) — esquerda : x < xmin
      bit 1 (valor 2) — direita  : x > xmax
      bit 2 (valor 4) — baixo    : y < ymin
      bit 3 (valor 8) — cima     : y > ymax
    """
    codigo = 0

    # esquerda - bit 0
    if x < xmin:
        codigo = codigo + 1

    # direita - bit 1
    if x > xmax:
        codigo = codigo + 2

    # baixo - bit 2
    if y < ymin:
        codigo = codigo + 4

    # cima - bit 3
    if y > ymax:
        codigo = codigo + 8

    return codigo


def execute_cohen_sutherland(p1, p2, xmin, ymin, xmax, ymax, draw_pixel_func=None):
    """
    procedimento Cohen-Sutherland (x1, y1, x2, y2)
    Algoritmo de recorte de segmentos de reta de Cohen-Sutherland.

    Parâmetros:
    - p1, p2         : Tuplas (x, y) dos extremos do segmento
    - xmin, ymin     : Canto inferior-esquerdo da janela
    - xmax, ymax     : Canto superior-direito da janela
    - draw_pixel_func: Não utilizado — mantido para compatibilidade de assinatura

    Retorna:
    - ((x1', y1'), (x2', y2')) com o segmento recortado, ou
    - None se o segmento estiver completamente fora da janela
    """
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])

    aceite = False
    feito = False

    while not feito:
        c1 = region_code(x1, y1, xmin, ymin, xmax, ymax)
        c2 = region_code(x2, y2, xmin, ymin, xmax, ymax)

        if (c1 == 0) and (c2 == 0):
            # segmento completamente dentro
            aceite = True
            feito = True

        elif (c1 & c2) != 0:
            # segmento completamente fora
            feito = True

        else:
            # determina um ponto exterior
            if c1 != 0:
                cfora = c1
            else:
                cfora = c2

            # bit 0 — limite esquerdo
            if (cfora & 1) == 1:
                xint = xmin
                yint = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1) if x2 != x1 else y1

            # bit 1 — limite direito
            elif (cfora & 2) == 2:
                xint = xmax
                yint = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1) if x2 != x1 else y1

            # bit 2 — limite abaixo (ymin)
            elif (cfora & 4) == 4:
                yint = ymin
                xint = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1) if y2 != y1 else x1

            # bit 3 — limite acima (ymax)
            elif (cfora & 8) == 8:
                yint = ymax
                xint = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1) if y2 != y1 else x1

            if c1 == cfora:
                x1 = xint
                y1 = yint
            else:
                x2 = xint
                y2 = yint

    if aceite:
        return (
            (int(round(x1)), int(round(y1))),
            (int(round(x2)), int(round(y2)))
        )

    return None
