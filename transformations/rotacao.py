import math


def execute_rotacao(pontos, angulo, cx, cy):
    """
    Aplica rotação 2D a uma lista de pontos em torno de um ponto pivô (cx, cy).

    Fórmula (rotação em torno do pivô):
        x' = cx + (x - cx)*cos(θ) - (y - cy)*sin(θ)
        y' = cy + (x - cx)*sin(θ) + (y - cy)*cos(θ)

    Nota: em coordenadas de tela (y cresce para baixo), ângulos positivos
    correspondem a rotação no sentido horário visualmente.

    Parâmetros:
    - pontos : Lista de tuplas [(x, y), ...] do objeto a ser transformado
    - angulo : Ângulo de rotação em graus
    - cx, cy : Coordenadas do ponto de pivô (centro de rotação)

    Retorna:
    - Lista de tuplas [(x', y'), ...] com os pontos transformados
    """
    rad = math.radians(angulo)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    resultado = []
    for x, y in pontos:
        x_rel = x - cx
        y_rel = y - cy
        x_rot = x_rel * cos_a - y_rel * sin_a
        y_rot = x_rel * sin_a + y_rel * cos_a
        resultado.append((int(round(cx + x_rot)), int(round(cy + y_rot))))

    return resultado
