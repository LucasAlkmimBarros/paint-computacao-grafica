def execute_translacao(pontos, dx, dy):
    """
    Aplica translação 2D a uma lista de pontos.

    Fórmula:
        x' = x + dx
        y' = y + dy

    Parâmetros:
    - pontos : Lista de tuplas [(x, y), ...] do objeto a ser transformado
    - dx     : Deslocamento no eixo X
    - dy     : Deslocamento no eixo Y

    Retorna:
    - Lista de tuplas [(x', y'), ...] com os pontos transformados
    """
    return [(int(round(x + dx)), int(round(y + dy))) for x, y in pontos]
