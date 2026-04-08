def cliptest(p, q, u1, u2):
    """
    função cliptest(p, q, u1, u2)
    Testa uma fronteira e atualiza os parâmetros paramétricos u1 e u2.

    Parâmetros:
    - p, q : coeficientes da fronteira
    - u1   : parâmetro de entrada (t mínimo)
    - u2   : parâmetro de saída  (t máximo)

    Retorna (result, u1, u2):
    - result=False → segmento rejeitado por esta fronteira
    - result=True  → segmento aceito, u1/u2 possivelmente atualizados
    """
    result = True

    if p < 0.0:                  # fora para dentro
        r = q / p
        if r > u2:
            result = False
        elif r > u1:
            u1 = r

    elif p > 0.0:                # dentro para fora
        r = q / p
        if r < u1:
            result = False
        elif r < u2:
            u2 = r

    elif q < 0.0:                # paralelo e fora da fronteira
        result = False

    return result, u1, u2


def execute_liang_barsky(p1, p2, xmin, ymin, xmax, ymax):
    """
    procedimento Liang-Barski (x1, y1, x2, y2)
    Algoritmo de recorte paramétrico de Liang-Barsky.

    Parâmetros:
    - p1, p2     : Tuplas (x, y) dos extremos do segmento
    - xmin, ymin : Canto superior-esquerdo da janela (coords de tela)
    - xmax, ymax : Canto inferior-direito da janela  (coords de tela)

    Retorna:
    - ((x1', y1'), (x2', y2')) com o segmento recortado, ou
    - None se o segmento estiver completamente fora da janela
    """
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])

    u1 = 0.0
    u2 = 1.0
    dx = x2 - x1
    dy = y2 - y1

    result, u1, u2 = cliptest(-dx, x1 - xmin, u1, u2)
    if result:
        result, u1, u2 = cliptest(dx, xmax - x1, u1, u2)
        if result:
            result, u1, u2 = cliptest(-dy, y1 - ymin, u1, u2)
            if result:
                result, u1, u2 = cliptest(dy, ymax - y1, u1, u2)
                if result:
                    if u2 < 1.0:
                        x2 = x1 + u2 * dx
                        y2 = y1 + u2 * dy
                    if u1 > 0.0:
                        x1 = x1 + u1 * dx
                        y1 = y1 + u1 * dy
                    return (
                        (int(round(x1)), int(round(y1))),
                        (int(round(x2)), int(round(y2)))
                    )

    return None
