"""
Widget do painel de controle
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox,
    QLabel, QComboBox, QSpinBox, QCheckBox, QLineEdit,
    QFileDialog, QMessageBox, QTextEdit, QTabWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from ...adb_manager import ADBDevice
from ...scrcpy_manager import ScrcpyOptions


class ControlPanelWidget(QWidget):
    """Widget do painel de controle do scrcpy e ADB"""
    
    start_mirroring = pyqtSignal(ScrcpyOptions)
    stop_mirroring = pyqtSignal()
    install_apk = pyqtSignal(str)
    take_screenshot = pyqtSignal()
    execute_command = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_device: ADBDevice = None
        self.is_mirroring = False
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Abas
        self.tabs = QTabWidget()
        
        # Aba de espelhamento
        mirror_tab = self._create_mirror_tab()
        self.tabs.addTab(mirror_tab, "📺 Espelhamento")
        
        # Aba de ferramentas
        tools_tab = self._create_tools_tab()
        self.tabs.addTab(tools_tab, "🛠️ Ferramentas")
        
        # Aba de comandos
        commands_tab = self._create_commands_tab()
        self.tabs.addTab(commands_tab, "⌨️ Comandos")
        
        layout.addWidget(self.tabs)
        
    def _create_mirror_tab(self) -> QWidget:
        """Cria a aba de espelhamento"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Grupo de qualidade
        quality_group = QGroupBox("Configurações de Qualidade")
        quality_layout = QVBoxLayout()
        
        # Preset
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Padrão",
            "Alta Qualidade",
            "Performance",
            "Baixa Latência",
            "Gravação"
        ])
        self.preset_combo.currentIndexChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        quality_layout.addLayout(preset_layout)
        
        # Resolução
        resolution_layout = QHBoxLayout()
        resolution_layout.addWidget(QLabel("Resolução Máx:"))
        self.resolution_spin = QSpinBox()
        self.resolution_spin.setRange(0, 2560)
        self.resolution_spin.setValue(0)
        self.resolution_spin.setSuffix(" px (0 = original)")
        self.resolution_spin.setSpecialValueText("Original")
        resolution_layout.addWidget(self.resolution_spin)
        quality_layout.addLayout(resolution_layout)
        
        # Bitrate
        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel("Bitrate:"))
        self.bitrate_combo = QComboBox()
        self.bitrate_combo.addItems(["2M", "4M", "8M", "12M", "16M", "20M"])
        self.bitrate_combo.setCurrentText("8M")
        bitrate_layout.addWidget(self.bitrate_combo)
        quality_layout.addLayout(bitrate_layout)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel("FPS Máximo:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(0, 120)
        self.fps_spin.setValue(0)
        self.fps_spin.setSpecialValueText("Padrão")
        fps_layout.addWidget(self.fps_spin)
        quality_layout.addLayout(fps_layout)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Grupo de opções de exibição
        display_group = QGroupBox("Opções de Exibição")
        display_layout = QVBoxLayout()
        
        self.fullscreen_check = QCheckBox("Tela Cheia")
        display_layout.addWidget(self.fullscreen_check)
        
        self.always_on_top_check = QCheckBox("Sempre no Topo")
        display_layout.addWidget(self.always_on_top_check)
        
        self.borderless_check = QCheckBox("Sem Bordas")
        display_layout.addWidget(self.borderless_check)
        
        # Orientação
        orientation_layout = QHBoxLayout()
        orientation_layout.addWidget(QLabel("Orientação:"))
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems([
            "Automática",
            "Retrato",
            "Paisagem", 
            "Retrato Invertido",
            "Paisagem Invertida"
        ])
        orientation_layout.addWidget(self.orientation_combo)
        display_layout.addLayout(orientation_layout)
        
        display_group.setLayout(display_layout)
        layout.addWidget(display_group)
        
        # Grupo de opções do dispositivo
        device_group = QGroupBox("Opções do Dispositivo")
        device_layout = QVBoxLayout()
        
        self.stay_awake_check = QCheckBox("Manter Tela Ligada")
        self.stay_awake_check.setChecked(True)
        device_layout.addWidget(self.stay_awake_check)
        
        self.show_touches_check = QCheckBox("Mostrar Toques")
        device_layout.addWidget(self.show_touches_check)
        
        self.turn_screen_off_check = QCheckBox("Desligar Tela do Dispositivo")
        device_layout.addWidget(self.turn_screen_off_check)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Botões de controle
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Iniciar Espelhamento")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #3584e4;
                color: white;
                padding: 10px 20px;
                font-weight: 600;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1c71d8;
            }
            QPushButton:pressed {
                background-color: #1a5fb4;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #7a7a7a;
            }
        """)
        self.start_btn.clicked.connect(self._on_start_mirroring)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Parar")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e01b24;
                color: white;
                padding: 10px 20px;
                font-weight: 600;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c01c28;
            }
            QPushButton:pressed {
                background-color: #a51d2d;
            }
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #7a7a7a;
            }
        """)
        self.stop_btn.clicked.connect(self._on_stop_mirroring)
        buttons_layout.addWidget(self.stop_btn)
        
        layout.addLayout(buttons_layout)
        
        layout.addStretch()
        
        return widget
    
    def _create_tools_tab(self) -> QWidget:
        """Cria a aba de ferramentas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Instalar APK
        apk_group = QGroupBox("Instalação de APK")
        apk_layout = QVBoxLayout()
        
        apk_btn_layout = QHBoxLayout()
        self.apk_path_edit = QLineEdit()
        self.apk_path_edit.setPlaceholderText("Selecione um arquivo APK...")
        self.apk_path_edit.setReadOnly(True)
        apk_btn_layout.addWidget(self.apk_path_edit)
        
        browse_apk_btn = QPushButton("📁 Procurar")
        browse_apk_btn.clicked.connect(self._browse_apk)
        apk_btn_layout.addWidget(browse_apk_btn)
        
        apk_layout.addLayout(apk_btn_layout)
        
        install_apk_btn = QPushButton("📦 Instalar APK")
        install_apk_btn.clicked.connect(self._on_install_apk)
        apk_layout.addWidget(install_apk_btn)
        
        apk_group.setLayout(apk_layout)
        layout.addWidget(apk_group)
        
        # Screenshot
        screenshot_group = QGroupBox("Screenshot")
        screenshot_layout = QVBoxLayout()
        
        screenshot_btn = QPushButton("📸 Capturar Screenshot")
        screenshot_btn.clicked.connect(self._on_take_screenshot)
        screenshot_layout.addWidget(screenshot_btn)
        
        screenshot_group.setLayout(screenshot_layout)
        layout.addWidget(screenshot_group)
        
        # Informações do dispositivo
        info_group = QGroupBox("Informações do Dispositivo")
        info_layout = QVBoxLayout()
        
        self.device_details = QTextEdit()
        self.device_details.setReadOnly(True)
        self.device_details.setMaximumHeight(150)
        info_layout.addWidget(self.device_details)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_commands_tab(self) -> QWidget:
        """Cria a aba de comandos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Comando shell
        shell_group = QGroupBox("Executar Comando ADB Shell")
        shell_layout = QVBoxLayout()
        
        cmd_layout = QHBoxLayout()
        self.command_edit = QLineEdit()
        self.command_edit.setPlaceholderText("Digite um comando shell...")
        self.command_edit.returnPressed.connect(self._on_execute_command)
        cmd_layout.addWidget(self.command_edit)
        
        execute_btn = QPushButton("▶️ Executar")
        execute_btn.clicked.connect(self._on_execute_command)
        cmd_layout.addWidget(execute_btn)
        
        shell_layout.addLayout(cmd_layout)
        
        self.command_output = QTextEdit()
        self.command_output.setReadOnly(True)
        self.command_output.setPlaceholderText("A saída dos comandos aparecerá aqui...")
        shell_layout.addWidget(self.command_output)
        
        clear_btn = QPushButton("🗑️ Limpar Saída")
        clear_btn.clicked.connect(self.command_output.clear)
        shell_layout.addWidget(clear_btn)
        
        shell_group.setLayout(shell_layout)
        layout.addWidget(shell_group)
        
        return widget
    
    def _on_preset_changed(self, index: int):
        """Manipula mudança de preset"""
        presets = {
            0: {"resolution": 0, "bitrate": "8M", "fps": 0},  # Padrão
            1: {"resolution": 0, "bitrate": "16M", "fps": 60},  # Alta Qualidade
            2: {"resolution": 720, "bitrate": "4M", "fps": 30},  # Performance
            3: {"resolution": 1024, "bitrate": "8M", "fps": 60},  # Baixa Latência
            4: {"resolution": 0, "bitrate": "16M", "fps": 60},  # Gravação
        }
        
        if index in presets:
            preset = presets[index]
            self.resolution_spin.setValue(preset["resolution"])
            self.bitrate_combo.setCurrentText(preset["bitrate"])
            self.fps_spin.setValue(preset["fps"])
    
    def _on_start_mirroring(self):
        """Manipula início do espelhamento"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        # Cria opções baseadas nas configurações
        options = ScrcpyOptions()
        
        if self.resolution_spin.value() > 0:
            options.max_size = self.resolution_spin.value()
        
        options.bit_rate = self.bitrate_combo.currentText()
        
        if self.fps_spin.value() > 0:
            options.max_fps = self.fps_spin.value()
        
        options.fullscreen = self.fullscreen_check.isChecked()
        options.always_on_top = self.always_on_top_check.isChecked()
        options.borderless = self.borderless_check.isChecked()
        options.stay_awake = self.stay_awake_check.isChecked()
        options.show_touches = self.show_touches_check.isChecked()
        options.turn_screen_off = self.turn_screen_off_check.isChecked()
        
        # Orientação
        orientation_index = self.orientation_combo.currentIndex()
        # Debug: vamos ver o valor
        print(f"DEBUG: Orientação selecionada - Index: {orientation_index}")
        
        if orientation_index > 0:  # 0 é "Automática"
            # scrcpy 3.2+ usa graus diretos: 0, 90, 180, 270
            orientation_map = {
                1: 0,    # Retrato -> 0°
                2: 90,   # Paisagem -> 90°
                3: 180,  # Retrato Invertido -> 180°
                4: 270   # Paisagem Invertida -> 270°
            }
            options.lock_orientation = orientation_map.get(orientation_index)
            print(f"DEBUG: Valor enviado ao scrcpy (em graus): {options.lock_orientation}")
        
        # Emite sinal
        self.start_mirroring.emit(options)
    
    def _on_stop_mirroring(self):
        """Manipula parada do espelhamento"""
        self.stop_mirroring.emit()
    
    def _browse_apk(self):
        """Abre diálogo para selecionar APK"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar APK",
            "",
            "APK Files (*.apk)"
        )
        
        if file_path:
            self.apk_path_edit.setText(file_path)
    
    def _on_install_apk(self):
        """Manipula instalação de APK"""
        apk_path = self.apk_path_edit.text()
        
        if not apk_path:
            QMessageBox.warning(self, "Aviso", "Selecione um arquivo APK!")
            return
        
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        self.install_apk.emit(apk_path)
    
    def _on_take_screenshot(self):
        """Manipula captura de screenshot"""
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        self.take_screenshot.emit()
    
    def _on_execute_command(self):
        """Manipula execução de comando"""
        command = self.command_edit.text().strip()
        
        if not command:
            return
        
        if not self.current_device:
            QMessageBox.warning(self, "Aviso", "Nenhum dispositivo selecionado!")
            return
        
        self.execute_command.emit(command)
        self.command_edit.clear()
    
    def set_device(self, device: ADBDevice):
        """Define o dispositivo atual"""
        self.current_device = device
        
        if device:
            self.start_btn.setEnabled(True)
        else:
            self.start_btn.setEnabled(False)
    
    def set_device_details(self, details: dict):
        """Define detalhes do dispositivo"""
        text = ""
        for key, value in details.items():
            text += f"<b>{key}:</b> {value}<br>"
        
        self.device_details.setHtml(text)
    
    def set_mirroring_state(self, is_mirroring: bool):
        """Define o estado do espelhamento"""
        self.is_mirroring = is_mirroring
        self.start_btn.setEnabled(not is_mirroring and self.current_device is not None)
        self.stop_btn.setEnabled(is_mirroring)
    
    def append_command_output(self, output: str):
        """Adiciona saída de comando"""
        self.command_output.append(output)

