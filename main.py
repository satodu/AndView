#!/usr/bin/env python3
"""
AndView - Interface Gráfica para scrcpy e ADB
Ponto de entrada da aplicação
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.ui import MainWindow


def main():
    """Função principal"""
    # Cria a aplicação
    app = QApplication(sys.argv)
    
    # Define estilo
    app.setStyle('Fusion')
    
    # Define o ícone da aplicação no QApplication (para Wayland)
    logo_path = os.path.join(os.path.dirname(__file__), 'src', 'ui', 'resources', 'logo.png')
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
        print(f"DEBUG APP: Ícone definido no QApplication: {logo_path}")
    
    # Cria e mostra a janela principal
    window = MainWindow()
    window.show()
    
    # Inicia o loop de eventos
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

