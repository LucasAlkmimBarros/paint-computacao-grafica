import math

def execute_bresenham_circulo(center, edge_point, draw_pixel_func, canvas_oval_func=None):
    """
    Algoritmo de Bresenham para rasterização de circunferências.
    Utiliza simetria de 8 pontos para máxima eficiência.

    Parâmetros:
    - center: Tupla (xc, yc) — centro da circunferência
    - edge_point: Tupla (xe, ye) — ponto na borda (define o raio)
    - draw_pixel_func: Função de desenho de pixel. Uso: draw_pixel_func(x, y)
    - canvas_oval_func: Parâmetro de compatibilidade (não utilizado pelo algoritmo)
    """
    xc, yc = int(center[0]), int(center[1])
    xe, ye = int(edge_point[0]), int(edge_point[1])

    # Raio = distância euclidiana entre centro e ponto de borda
    r = int(round(math.sqrt((xe - xc) ** 2 + (ye - yc) ** 2)))

    if r == 0:
        draw_pixel_func(xc, yc)
        return

    def plot_8_points(x, y):
        """Plota os 8 pontos simétricos da circunferência."""
        draw_pixel_func(xc + x, yc + y)
        draw_pixel_func(xc - x, yc + y)
        draw_pixel_func(xc + x, yc - y)
        draw_pixel_func(xc - x, yc - y)
        draw_pixel_func(xc + y, yc + x)
        draw_pixel_func(xc - y, yc + x)
        draw_pixel_func(xc + y, yc - x)
        draw_pixel_func(xc - y, yc - x)

    x = 0
    y = r
    # Parâmetro de decisão inicial: d = 3 - 2r
    d = 3 - 2 * r

    plot_8_points(x, y)

    while x < y:
        if d < 0:
            # Ponto E (East): somente incrementa x
            d += 4 * x + 6
        else:
            # Ponto SE (South-East): incrementa x, decrementa y
            d += 4 * (x - y) + 10
            y -= 1
        x += 1
        plot_8_points(x, y)
