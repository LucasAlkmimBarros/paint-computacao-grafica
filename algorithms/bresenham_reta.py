def execute_bresenham_reta(p1, p2, draw_pixel_func):
    """
    Algoritmo de Bresenham para traçado de retas.
    
    Parâmetros:
    - p1: Tupla (x, y) do ponto inicial
    - p2: Tupla (x, y) do ponto final
    - draw_pixel_func: Função que desenha um pixel na tela. Uso: draw_pixel_func(x, y)
    """
    xi, yi = int(p1[0]), int(p1[1])
    xf, yf = int(p2[0]), int(p2[1])

    dx = xf - xi
    dy = yf - yi
    
    x = xi
    y = yi
    
    draw_pixel_func(x, y)
    
    if dx >= 0:
        xincr = 1
    else:
        xincr = -1
        dx = -dx
        
    if dy >= 0:
        yincr = 1
    else:
        yincr = -1
        dy = -dy
        
    if dx > dy:
        p = 2 * dy - dx
        c1 = 2 * dy
        c2 = 2 * (dy - dx)
        for _ in range(dx):
            x += xincr
            if p < 0:
                p += c1
            else:
                p += c2
                y += yincr
            draw_pixel_func(x, y)
    else:
        p = 2 * dx - dy
        c1 = 2 * dx
        c2 = 2 * (dx - dy)
        for _ in range(dy):
            y += yincr
            if p < 0:
                p += c1
            else:
                p += c2
                x += xincr
            draw_pixel_func(x, y)