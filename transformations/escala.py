def execute_escala(pontos, sx, sy, cx, cy):
    """
    Aplica escala 2D a uma lista de pontos em relação a um ponto de referência (cx, cy).

    Fórmula (escala em torno do pivô):
        x' = cx + sx * (x - cx)
        y' = cy + sy * (y - cy)

    Parâmetros:
    - pontos : Lista de tuplas [(x, y), ...] do objeto a ser transformado
    - sx, sy : Fatores de escala nos eixos X e Y (1.0 = sem alteração)
    - cx, cy : Coordenadas do ponto de referência (centro da escala / pivô)

    Retorna:
    - Lista de tuplas [(x', y'), ...] com os pontos transformados
    """
    resultado = []
    for x, y in pontos:
        x_new = cx + sx * (x - cx)
        y_new = cy + sy * (y - cy)
        resultado.append((int(round(x_new)), int(round(y_new))))

    return resultado
