def execute_liang_barsky(p1, p2, xmin, ymin, xmax, ymax, draw_pixel_func=None):
    """
    Algoritmo de Liang-Barsky para recorte de segmentos de reta.
    Método: equação paramétrica — P(t) = P1 + t*(P2 - P1), 0 ≤ t ≤ 1.

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

    dx = x2 - x1
    dy = y2 - y1

    # Parâmetros p e q para cada uma das 4 fronteiras:
    # p < 0 → direção de entrada; p > 0 → direção de saída; p = 0 → paralelo
    p = [-dx, dx, -dy, dy]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

    t_enter = 0.0   # parâmetro de entrada máximo
    t_leave = 1.0   # parâmetro de saída mínimo

    for pi, qi in zip(p, q):
        if pi == 0:
            # Segmento paralelo à fronteira
            if qi < 0:
                # Completamente fora desta fronteira
                return None
            # Senão, totalmente dentro nesta direção → sem restrição
        elif pi < 0:
            # Direção de entrada: atualiza t_enter
            t = qi / pi
            if t > t_leave:
                return None   # Segmento rejeitado
            t_enter = max(t_enter, t)
        else:
            # Direção de saída: atualiza t_leave
            t = qi / pi
            if t < t_enter:
                return None   # Segmento rejeitado
            t_leave = min(t_leave, t)

    # Calcula os pontos recortados usando os parâmetros t_enter e t_leave
    x1_clip = int(round(x1 + t_enter * dx))
    y1_clip = int(round(y1 + t_enter * dy))
    x2_clip = int(round(x1 + t_leave * dx))
    y2_clip = int(round(y1 + t_leave * dy))

    return (x1_clip, y1_clip), (x2_clip, y2_clip)
