def execute_reflexao(pontos, eixo, cx=None, cy=None):
    """
    Aplica reflexão 2D a uma lista de pontos em relação a um eixo.

    O pivô (cx, cy) é o centro de referência da reflexão.
    Se não fornecido, usa o centroide dos próprios pontos,
    de modo que o objeto seja refletido "no lugar".

    Fórmulas:
        Eixo X  → inverte Y em torno de cy:  x' = x,       y' = 2*cy - y
        Eixo Y  → inverte X em torno de cx:  x' = 2*cx - x, y' = y
        Eixo XY → inverte ambos em torno do pivô:
                                              x' = 2*cx - x, y' = 2*cy - y

    Parâmetros:
    - pontos : Lista de tuplas [(x, y), ...] do objeto a ser transformado
    - eixo   : Eixo de reflexão — "X", "Y" ou "XY"
    - cx, cy : Centro de referência (opcional; usa centroide se None)

    Retorna:
    - Lista de tuplas [(x', y'), ...] com os pontos transformados
    """
    if not pontos:
        return []

    # Calcula o centroide se o pivô não for fornecido
    if cx is None:
        cx = sum(p[0] for p in pontos) / len(pontos)
    if cy is None:
        cy = sum(p[1] for p in pontos) / len(pontos)

    resultado = []
    for x, y in pontos:
        if eixo == "X":
            # Reflexão sobre o eixo X: inverte Y em torno de cy
            resultado.append((x, int(round(2 * cy - y))))
        elif eixo == "Y":
            # Reflexão sobre o eixo Y: inverte X em torno de cx
            resultado.append((int(round(2 * cx - x)), y))
        elif eixo == "XY":
            # Reflexão sobre a origem (ambos os eixos)
            resultado.append((int(round(2 * cx - x)), int(round(2 * cy - y))))
        else:
            resultado.append((x, y))

    return resultado
