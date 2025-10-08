"""
Estilo customizado para checkboxes com ícone
"""

import base64

# SVG do ícone de check (✓)
CHECK_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
    <path fill="white" d="M13.5 2.5L6 10L2.5 6.5L3.5 5.5L6 8L12.5 1.5z"/>
</svg>
"""

def get_checkbox_check_icon():
    """Retorna o ícone de check em base64 para usar no CSS"""
    svg_bytes = CHECK_SVG.encode('utf-8')
    b64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

