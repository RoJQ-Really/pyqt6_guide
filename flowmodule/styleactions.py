def relative_change_color(color: str|list[int], matrix: list[float], out_type = 'RGB') -> str | None:
    if isinstance(color, str) and color.startswith("#"):
        color = [int(color[-2:], 16), int(color[-4:-2], 16), int(color[-6:-4], 16), int(color[-8:-6], 16)]
    if not isinstance(color, list):
        return None
    elif len(matrix) < len(color):
        return None
    
    for i, v in enumerate(matrix):
        color[i] = int(color[i] * v)
        if color[i] > 255:
            color[i] = 255
        elif color[i] < 0:
            color[i] = 0 
            
    if out_type == 'RGB':
        return "#" + "".join([hex(i)[2:] for i in color[:3]])
    elif out_type == 'RGBA':
        return "#" + "".join([hex(i)[2:] for i in color[:4]])