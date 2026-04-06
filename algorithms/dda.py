def execute_dda(p1, p2, draw_pixel_func, canvas_line_func):
    """
    Algoritmo DDA para traçado de retas.
    
    Parâmetros:
    - p1: Tupla (x, y) do ponto inicial
    - p2: Tupla (x, y) do ponto final
    - draw_pixel_func: Função que desenha um pixel na tela. Uso: draw_pixel_func(x, y, cor)
    - canvas_line_func: Função nativa que desenha uma linha. Útil como placeholder provisório.
    """
    
    xi, yi = p1
    xf, yf = p2
    
    x = float(xi)
    y = float(yi)
    dy = float(yf - yi)
    dx = float(xf - xi)
    
    draw_pixel_func(round(x), round(y))
    
    if abs(dx) > abs(dy):
        passos = int(abs(dx))
    else:
        passos = int(abs(dy))
        
    if passos == 0:
        return
        
    xincr = dx / passos
    yincr = dy / passos
    
    for i in range(passos):
        x += xincr
        y += yincr
        draw_pixel_func(round(x), round(y))
