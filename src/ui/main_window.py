"""
Janela principal da aplicação
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QStatusBar, QMenuBar, QMessageBox,
    QFileDialog, QLabel, QApplication, QProgressDialog, QTabWidget
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPalette, QColor, QAction
import os
from datetime import datetime

from .widgets.device_list import DeviceListWidget
from .widgets.control_panel import ControlPanelWidget
from .widgets.wifi_connection import WiFiConnectionWidget
from ..adb_manager import ADBManager, ADBDevice
from ..scrcpy_manager import ScrcpyManager, ScrcpyOptions


class MainWindow(QMainWindow):
    """Janela principal do AndView"""
    
    def __init__(self):
        super().__init__()
        
        # Gerenciadores
        self.adb_manager = ADBManager()
        self.scrcpy_manager = ScrcpyManager()
        
        # Estado
        self.current_device: ADBDevice = None
        
        # Configuração da janela
        self.setWindowTitle("AndView - Gerenciador de Dispositivos Android")
        self.setGeometry(100, 100, 1200, 700)
        
        # Define o ícone da aplicação
        logo_path = os.path.join(os.path.dirname(__file__), 'resources', 'logo.png')
        print(f"DEBUG: Tentando carregar ícone de: {logo_path}")
        print(f"DEBUG: Arquivo existe? {os.path.exists(logo_path)}")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
            print("DEBUG: Ícone definido com sucesso!")
        
        # Verifica dependências
        self._check_dependencies()
        
        # Aplica tema escuro
        self._apply_dark_theme()
        
        # Configura UI
        self._setup_ui()
        self._setup_menu_bar()
        self._setup_status_bar()
        
        # Timer para atualização automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._auto_refresh_devices)
        self.update_timer.start(5000)  # Atualiza a cada 5 segundos
        
        # Carrega dispositivos inicial
        self._refresh_devices()
    
    def _apply_dark_theme(self):
        """Aplica tema dark moderno estilo GNOME"""
        app = QApplication.instance()
        
        # Caminhos para recursos
        resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
        check_icon_path = os.path.join(resources_dir, 'check.svg')
        arrow_down_path = os.path.join(resources_dir, 'arrow-down.svg')
        arrow_up_path = os.path.join(resources_dir, 'arrow-up.svg')
        spinbox_arrows_path = os.path.join(resources_dir, 'spinbox-arrows.svg')
        
        # Paleta de cores dark moderna (inspirada no GNOME/Adwaita)
        dark_palette = QPalette()
        
        # Cores principais
        dark_palette.setColor(QPalette.Window, QColor(36, 36, 36))           # Fundo principal
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))    # Texto principal
        dark_palette.setColor(QPalette.Base, QColor(28, 28, 28))             # Fundo de inputs
        dark_palette.setColor(QPalette.AlternateBase, QColor(42, 42, 42))    # Alternado
        dark_palette.setColor(QPalette.ToolTipBase, QColor(48, 48, 48))      # Tooltip fundo
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))   # Tooltip texto
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))          # Texto em inputs
        dark_palette.setColor(QPalette.Button, QColor(48, 48, 48))           # Botões
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))    # Texto botões
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))        # Texto brilhante
        dark_palette.setColor(QPalette.Link, QColor(99, 162, 255))           # Links
        dark_palette.setColor(QPalette.Highlight, QColor(53, 132, 228))      # Seleção (azul GNOME)
        dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))  # Texto selecionado
        
        # Cores desabilitadas
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        
        app.setPalette(dark_palette)
        
        # Stylesheet complementar para elementos específicos
        app.setStyleSheet(f"""
            QMainWindow {{
                background-color: #242424;
            }}
            
            QWidget {{
                font-family: 'Mulish', 'Cantarell', 'Inter', 'SF Pro Display', -apple-system, sans-serif;
                font-size: 10pt;
            }}
            
            QGroupBox {{
                background-color: #303030;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                font-weight: 600;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                color: #ffffff;
            }}
            
            QPushButton {{
                background-color: #3a3a3a;
                border: 1px solid #4a4a4a;
                border-radius: 6px;
                padding: 8px 16px;
                color: #ffffff;
                font-weight: 500;
            }}
            
            QPushButton:hover {{
                background-color: #454545;
                border-color: #5a5a5a;
            }}
            
            QPushButton:pressed {{
                background-color: #2a2a2a;
            }}
            
            QPushButton:disabled {{
                background-color: #2a2a2a;
                color: #7a7a7a;
                border-color: #3a3a3a;
            }}
            
            QLineEdit, QTextEdit, QSpinBox, QComboBox {{
                background-color: #1c1c1c;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px;
                color: #ffffff;
                selection-background-color: #3584e4;
            }}
            
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
                border-color: #3584e4;
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 28px;
                border-left: 1px solid #4a4a4a;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            
            QComboBox::down-arrow {{
                image: url({arrow_down_path});
                width: 12px;
                height: 8px;
            }}
            
            QSpinBox {{
                padding-right: 25px;
            }}
            
            QSpinBox::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 24px;
                height: 14px;
                background-color: #3a3a3a;
                border: none;
                border-top-right-radius: 5px;
                border-bottom: 1px solid #2a2a2a;
                padding-bottom: 5px;
            }}
            
            QSpinBox::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 24px;
                height: 14px;
                background-color: #3a3a3a;
                border: none;
                border-bottom-right-radius: 5px;
                margin-top: -6px;
                padding-top: 5px;
            }}
            
            QSpinBox::up-button:hover {{
                background-color: #454545;
            }}
            
            QSpinBox::down-button:hover {{
                background-color: #454545;
            }}
            
            QSpinBox::up-button:pressed {{
                background-color: #3584e4;
            }}
            
            QSpinBox::down-button:pressed {{
                background-color: #3584e4;
            }}
            
            QSpinBox::up-arrow {{
                image: url({arrow_up_path});
                width: 10px;
                height: 6px;
            }}
            
            QSpinBox::down-arrow {{
                image: url({arrow_down_path});
                width: 10px;
                height: 6px;
            }}
            
            QListWidget {{
                background-color: #1c1c1c;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 4px;
                outline: none;
            }}
            
            QListWidget::item {{
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
            }}
            
            QListWidget::item:selected {{
                background-color: #3584e4;
                color: #ffffff;
            }}
            
            QListWidget::item:hover {{
                background-color: #2a2a2a;
            }}
            
            QTabWidget::pane {{
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                background-color: #242424;
                top: -1px;
            }}
            
            QTabBar::tab {{
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 16px;
                margin-right: 2px;
                color: #b0b0b0;
            }}
            
            QTabBar::tab:selected {{
                background-color: #242424;
                border-color: #3a3a3a;
                color: #ffffff;
            }}
            
            QTabBar::tab:hover {{
                background-color: #353535;
                color: #ffffff;
            }}
            
            QCheckBox {{
                spacing: 8px;
                color: #ffffff;
            }}
            
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #5a5a5a;
                background-color: #1c1c1c;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: #3584e4;
                border-color: #3584e4;
                image: url({check_icon_path});
            }}
            
            QCheckBox::indicator:hover {{
                border-color: #3584e4;
            }}
            
            QCheckBox::indicator:disabled {{
                background-color: #2a2a2a;
                border-color: #3a3a3a;
            }}
            
            QStatusBar {{
                background-color: #2a2a2a;
                color: #b0b0b0;
                border-top: 1px solid #3a3a3a;
            }}
            
            QMenuBar {{
                background-color: #2a2a2a;
                color: #ffffff;
                border-bottom: 1px solid #3a3a3a;
            }}
            
            QMenuBar::item:selected {{
                background-color: #3584e4;
            }}
            
            QMenu {{
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 4px;
            }}
            
            QMenu::item {{
                padding: 6px 24px 6px 12px;
                border-radius: 4px;
            }}
            
            QMenu::item:selected {{
                background-color: #3584e4;
                color: #ffffff;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                selection-background-color: #3584e4;
                selection-color: #ffffff;
                outline: none;
                padding: 4px;
            }}
            
            QComboBox QAbstractItemView::item {{
                padding: 6px 12px;
                border-radius: 4px;
                min-height: 24px;
            }}
            
            QComboBox QAbstractItemView::item:selected {{
                background-color: #3584e4;
                color: #ffffff;
            }}
            
            QComboBox QAbstractItemView::item:hover {{
                background-color: #3a3a3a;
            }}
            
            QScrollBar:vertical {{
                background-color: #1c1c1c;
                width: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: #4a4a4a;
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: #5a5a5a;
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: #1c1c1c;
                height: 12px;
                border-radius: 6px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: #4a4a4a;
                border-radius: 6px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: #5a5a5a;
            }}
        """)
    
    def _check_dependencies(self):
        """Verifica se ADB e scrcpy estão instalados"""
        # Verificação silenciosa - não mostra popup no início
        self.adb_available = self.adb_manager.check_adb_available()
        self.scrcpy_available = self.scrcpy_manager.check_scrcpy_available()
    
    def _setup_ui(self):
        """Configura a interface do usuário"""
        # Aplica tema dark moderno
        self._apply_dark_theme()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Splitter para dividir a tela
        splitter = QSplitter(Qt.Horizontal)
        
        # Container para widgets do lado esquerdo com tabs
        left_container = QWidget()
        left_layout = QVBoxLayout()
        
        # Tab widget
        self.left_tabs = QTabWidget()
        self.left_tabs.setTabPosition(QTabWidget.North)
        
        # Tab 1: Dispositivos
        self.device_list = DeviceListWidget()
        self.device_list.device_selected.connect(self._on_device_selected)
        self.device_list.refresh_requested.connect(self._refresh_devices)
        self.left_tabs.addTab(self.device_list, "📱 Dispositivos")
        
        # Tab 2: Conexão WiFi
        self.wifi_widget = WiFiConnectionWidget(self.adb_manager)
        self.left_tabs.addTab(self.wifi_widget, "🔗 WiFi")
        
        left_layout.addWidget(self.left_tabs)
        left_container.setLayout(left_layout)
        left_container.setMinimumWidth(400)
        left_container.setMaximumWidth(700)
        splitter.addWidget(left_container)
        
        # Painel de controle (lado direito)
        self.control_panel = ControlPanelWidget()
        self.control_panel.start_mirroring.connect(self._on_start_mirroring)
        self.control_panel.stop_mirroring.connect(self._on_stop_mirroring)
        self.control_panel.install_apk.connect(self._on_install_apk)
        self.control_panel.take_screenshot.connect(self._on_take_screenshot)
        self.control_panel.execute_command.connect(self._on_execute_command)
        splitter.addWidget(self.control_panel)
        
        # Define proporções do splitter
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
    
    def _setup_menu_bar(self):
        """Configura a barra de menu"""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("&Arquivo")
        
        refresh_action = QAction("🔄 Atualizar Dispositivos", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._refresh_devices)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("❌ Sair", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("&Ferramentas")
        
        apk_action = QAction("📦 Instalar APK", self)
        apk_action.triggered.connect(self._quick_install_apk)
        tools_menu.addAction(apk_action)
        
        screenshot_action = QAction("📸 Screenshot", self)
        screenshot_action.setShortcut("Ctrl+S")
        screenshot_action.triggered.connect(self._on_take_screenshot)
        tools_menu.addAction(screenshot_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("&Ajuda")
        
        about_action = QAction("ℹ️ Sobre", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        info_action = QAction("ℹ️ Informações", self)
        info_action.triggered.connect(self._show_versions)
        help_menu.addAction(info_action)
    
    def _setup_status_bar(self):
        """Configura a barra de status"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_bar.showMessage("Pronto")
    
    def _refresh_devices(self):
        """Atualiza a lista de dispositivos"""
        self.device_list.set_refreshing(True)
        self.status_bar.showMessage("Atualizando lista de dispositivos...")
        
        devices = self.adb_manager.list_devices()
        self.device_list.update_devices(devices)
        
        self.device_list.set_refreshing(False)
        self.status_bar.showMessage(f"Encontrado(s) {len(devices)} dispositivo(s)")
    
    def _auto_refresh_devices(self):
        """Atualização automática de dispositivos (silenciosa)"""
        devices = self.adb_manager.list_devices()
        self.device_list.update_devices(devices)
    
    def _on_device_selected(self, device: ADBDevice):
        """Manipula seleção de dispositivo"""
        self.current_device = device
        self.control_panel.set_device(device)
        
        # Atualiza informações detalhadas
        details = self.adb_manager.get_device_info(device.serial)
        self.control_panel.set_device_details(details)
        
        self.status_bar.showMessage(f"Dispositivo selecionado: {device.manufacturer} {device.model}")
    
    def _on_start_mirroring(self, options: ScrcpyOptions):
        """Inicia o espelhamento"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        self.status_bar.showMessage("Iniciando scrcpy...")
        
        success, message = self.scrcpy_manager.start_mirroring(
            self.current_device.serial,
            options
        )
        
        if success:
            self.control_panel.set_mirroring_state(True)
            self.status_bar.showMessage("scrcpy iniciado com sucesso")
            
            # Timer para verificar se o processo ainda está rodando
            QTimer.singleShot(1000, self._check_scrcpy_status)
        else:
            QMessageBox.critical(self, "Erro", f"Falha ao iniciar scrcpy:\n{message}")
            self.status_bar.showMessage("Falha ao iniciar scrcpy")
    
    def _on_stop_mirroring(self):
        """Para o espelhamento"""
        success, message = self.scrcpy_manager.stop_mirroring()
        
        if success:
            self.control_panel.set_mirroring_state(False)
            self.status_bar.showMessage("scrcpy finalizado")
        else:
            QMessageBox.warning(self, "Aviso", message)
    
    def _check_scrcpy_status(self):
        """Verifica o status do scrcpy periodicamente"""
        if self.scrcpy_manager.is_running():
            # Verifica novamente em 2 segundos
            QTimer.singleShot(2000, self._check_scrcpy_status)
        else:
            # scrcpy foi fechado
            self.control_panel.set_mirroring_state(False)
            self.status_bar.showMessage("scrcpy finalizado")
    
    def _on_install_apk(self, apk_path: str):
        """Instala um APK"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        self.status_bar.showMessage(f"Instalando {os.path.basename(apk_path)}...")
        
        # Importa QProgressDialog
        from PySide6.QtWidgets import QProgressDialog
        
        # Mostra diálogo de progresso com cancelamento
        progress = QProgressDialog(
            f"Instalando {os.path.basename(apk_path)}...\n\nAguarde ou aceite no dispositivo.",
            "Cancelar",
            0, 0,
            self
        )
        progress.setWindowTitle("Instalando APK")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        
        # Processa eventos para atualizar a interface
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        
        try:
            success, message = self.adb_manager.install_apk(
                self.current_device.serial,
                apk_path
            )
        except Exception as e:
            success = False
            message = str(e)
        finally:
            # Garante que o progresso seja fechado
            progress.close()
            progress.deleteLater()
        
        if success:
            QMessageBox.information(self, "Sucesso", message)
            self.status_bar.showMessage("APK instalado com sucesso")
        else:
            QMessageBox.critical(self, "Erro", f"Falha ao instalar APK:\n{message}")
            self.status_bar.showMessage("Falha ao instalar APK")
    
    def _quick_install_apk(self):
        """Instalação rápida de APK via menu"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Selecione um dispositivo primeiro!")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar APK",
            os.path.expanduser("~"),
            "APK Files (*.apk)"
        )
        
        if file_path:
            self._on_install_apk(file_path)
    
    def _on_take_screenshot(self):
        """Captura uma screenshot"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        # Gera nome do arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"screenshot_{timestamp}.png"
        
        # Pede local para salvar
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Screenshot",
            os.path.join(os.path.expanduser("~"), default_name),
            "PNG Files (*.png)"
        )
        
        if not file_path:
            return
        
        self.status_bar.showMessage("Capturando screenshot...")
        
        success, message = self.adb_manager.take_screenshot(
            self.current_device.serial,
            file_path
        )
        
        if success:
            QMessageBox.information(self, "Sucesso", message)
            self.status_bar.showMessage("Screenshot capturada com sucesso")
        else:
            QMessageBox.critical(self, "Erro", f"Falha ao capturar screenshot:\n{message}")
            self.status_bar.showMessage("Falha ao capturar screenshot")
    
    def _on_execute_command(self, command: str):
        """Executa um comando shell"""
        if not self.current_device:
            return
        
        self.status_bar.showMessage(f"Executando: {command}")
        
        success, output = self.adb_manager.execute_command(
            self.current_device.serial,
            command
        )
        
        # Adiciona saída ao painel
        self.control_panel.append_command_output(f"$ {command}\n{output}\n")
        
        if success:
            self.status_bar.showMessage("Comando executado com sucesso")
        else:
            self.status_bar.showMessage("Erro ao executar comando")
    
    def _show_about(self):
        """Mostra diálogo sobre"""
        about_text = """
        <h2>AndView</h2>
        <p><b>Gerenciador de Dispositivos Android</b></p>
        <p>Versão 0.0.1-alpha</p>
        <p>Uma ferramenta moderna e intuitiva para gerenciar dispositivos Android.</p>
        <p><b>Características:</b></p>
        <ul>
            <li>Detecção automática de dispositivos</li>
            <li>Espelhamento de tela</li>
            <li>Instalação de APKs</li>
            <li>Captura de screenshots</li>
            <li>Execução de comandos shell</li>
        </ul>
        <br>
        <p><b>Desenvolvido por:</b> Eduardo Sato</p>
        <p><b>GitHub:</b> <a href="https://github.com/satodu">@satodu</a></p>
        <p><b>Website:</b> <a href="https://panda.papoinformal.com.br/">panda.papoinformal.com.br</a></p>
        <br>
        <p>Interface desenvolvida com PySide6 e tema inspirado no GNOME Adwaita.</p>
        <p>Desenvolvido com ❤️ usando Python e PySide6</p>
        """
        
        QMessageBox.about(self, "Sobre AndView", about_text)
    
    def _show_versions(self):
        """Mostra versões das ferramentas"""
        version_text = f"""
        <h3>Informações do Sistema</h3>
        <p><b>AndView:</b> 0.0.1-alpha</p>
        <p><b>Python:</b> {self._get_python_version()}</p>
        <p><b>PySide6:</b> {self._get_pyside_version()}</p>
        """
        
        QMessageBox.information(self, "Sobre", version_text)
    
    def _get_python_version(self) -> str:
        """Retorna a versão do Python"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    def _get_pyside_version(self) -> str:
        """Retorna a versão do PySide6"""
        from PySide6 import __version__
        return __version__
    
    def closeEvent(self, event):
        """Manipula o fechamento da janela"""
        # Para o scrcpy se estiver rodando
        if self.scrcpy_manager.is_running():
            self.scrcpy_manager.stop_mirroring()
        
        event.accept()

