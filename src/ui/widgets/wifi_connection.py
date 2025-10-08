"""
Widget para conexão WiFi de dispositivos Android
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QGroupBox, QMessageBox,
    QSpinBox, QProgressDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import re


class WiFiConnectionWorker(QThread):
    """Worker thread para operações WiFi"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, adb_manager, operation, **kwargs):
        super().__init__()
        self.adb_manager = adb_manager
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.operation == "connect":
                success, message = self.adb_manager.connect_wifi_device(
                    self.kwargs["ip"], self.kwargs["port"]
                )
            elif self.operation == "enable":
                success, message = self.adb_manager.enable_wifi_mode(
                    self.kwargs["device_id"], self.kwargs["port"]
                )
            elif self.operation == "get_ip":
                ip = self.adb_manager.get_device_ip(self.kwargs["device_id"])
                success, message = bool(ip), ip if ip else "IP não encontrado"
            else:
                success, message = False, "Operação inválida"
            
            self.finished.emit(success, message)
        except Exception as e:
            self.finished.emit(False, f"Erro: {str(e)}")


class WiFiConnectionWidget(QGroupBox):
    """Widget para gerenciar conexões WiFi"""
    
    def __init__(self, adb_manager):
        super().__init__()
        self.adb_manager = adb_manager
        self.worker = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura a interface do widget"""
        # self.setTitle("Conexão WiFi")  # Título removido
        self.setMinimumHeight(600)
        self.setMaximumHeight(750)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # BLOCO 1: Ativar modo WiFi (requer USB)
        usb_group = QGroupBox("1. Ativar modo WiFi (USB conectado)")
        usb_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                padding-bottom: 15px;
                padding-left: 15px;
                padding-right: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        usb_layout = QVBoxLayout()
        usb_layout.setSpacing(20)
        usb_layout.setContentsMargins(10, 20, 10, 20)
        
        # Linha com porta
        port_layout = QHBoxLayout()
        port_label = QLabel("Porta:")
        port_label.setStyleSheet("font-size: 11px; padding: 3px;")
        port_layout.addWidget(port_label)
        port_layout.addSpacing(15)
        
        self.wifi_port_spin = QSpinBox()
        self.wifi_port_spin.setRange(1024, 65535)
        self.wifi_port_spin.setValue(5555)
        self.wifi_port_spin.setFixedWidth(100)
        self.wifi_port_spin.setFixedHeight(32)
        port_layout.addWidget(self.wifi_port_spin)
        port_layout.addStretch()
        
        usb_layout.addLayout(port_layout)
        
        # Espaçamento antes do botão
        usb_layout.addSpacing(10)
        
        # Botão ativar WiFi (largura total)
        self.enable_wifi_btn = QPushButton("Ativar WiFi")
        self.enable_wifi_btn.clicked.connect(self._enable_wifi_mode)
        self.enable_wifi_btn.setFixedHeight(35)
        self.enable_wifi_btn.setStyleSheet("font-size: 11px;")
        usb_layout.addWidget(self.enable_wifi_btn)
        
        usb_group.setLayout(usb_layout)
        layout.addWidget(usb_group)
        
        # BLOCO 2: Conectar via IP
        ip_group = QGroupBox("2. Conectar via IP")
        ip_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                padding-bottom: 25px;
                padding-left: 15px;
                padding-right: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        ip_layout = QVBoxLayout()
        ip_layout.setSpacing(20)
        ip_layout.setContentsMargins(10, 20, 10, 30)
        
        # Linha 1: IP (igual ao passo 1)
        ip_line_layout = QHBoxLayout()
        ip_label = QLabel("IP:")
        ip_label.setStyleSheet("font-size: 11px; padding: 5px; min-height: 20px;")
        ip_line_layout.addWidget(ip_label)
        ip_line_layout.addSpacing(15)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        self.ip_input.textChanged.connect(self._validate_ip)
        self.ip_input.setFixedHeight(32)
        self.ip_input.setStyleSheet("font-size: 11px;")
        ip_line_layout.addWidget(self.ip_input)
        ip_line_layout.addSpacing(15)
        
        self.get_ip_btn = QPushButton("Obter IP")
        self.get_ip_btn.clicked.connect(self._get_device_ip)
        self.get_ip_btn.setFixedWidth(100)
        self.get_ip_btn.setFixedHeight(32)
        self.get_ip_btn.setStyleSheet("font-size: 11px;")
        ip_line_layout.addWidget(self.get_ip_btn)
        ip_line_layout.addStretch()
        
        ip_layout.addLayout(ip_line_layout)
        
        # Espaçamento entre IP e Porta
        ip_layout.addSpacing(20)
        
        # Linha 2: Porta (igual ao passo 1)
        port_line_layout = QHBoxLayout()
        port_label2 = QLabel("Porta:")
        port_label2.setStyleSheet("font-size: 11px; padding: 5px; min-height: 20px;")
        port_line_layout.addWidget(port_label2)
        port_line_layout.addSpacing(15)
        
        self.connect_port_spin = QSpinBox()
        self.connect_port_spin.setRange(1024, 65535)
        self.connect_port_spin.setValue(5555)
        self.connect_port_spin.setFixedWidth(100)
        self.connect_port_spin.setFixedHeight(32)
        port_line_layout.addWidget(self.connect_port_spin)
        port_line_layout.addStretch()
        
        ip_layout.addLayout(port_line_layout)
        
        # Espaçamento entre Porta e Conectar
        ip_layout.addSpacing(20)
        
        # Linha 3: Conectar (igual ao passo 1)
        self.connect_btn = QPushButton("Conectar")
        self.connect_btn.clicked.connect(self._connect_wifi)
        self.connect_btn.setEnabled(False)
        self.connect_btn.setFixedHeight(35)
        self.connect_btn.setStyleSheet("font-size: 11px;")
        ip_layout.addWidget(self.connect_btn)
        
        ip_group.setLayout(ip_layout)
        layout.addWidget(ip_group)
        
        # Seção: IP detectado
        self.ip_display = QLabel("IP não detectado")
        self.ip_display.setStyleSheet("color: #3584e4; font-weight: bold; font-size: 11px; padding: 8px;")
        self.ip_display.setWordWrap(True)
        layout.addWidget(self.ip_display)
        
        # Seção: Informações
        info_section = QVBoxLayout()
        info_section.setSpacing(8)
        info_label = QLabel("💡 Conecte via USB → Obtenha o IP → Ative WiFi → Conecte via IP")
        info_label.setStyleSheet("color: #888888; font-size: 11px; padding: 10px; background-color: #2a2a2a; border-radius: 6px;")
        info_label.setWordWrap(True)
        info_section.addWidget(info_label)
        
        # Seção: Status da conexão
        self.status_label = QLabel("Status: Aguardando conexão...")
        self.status_label.setStyleSheet("color: #888888; font-size: 10px; padding: 5px;")
        info_section.addWidget(self.status_label)
        
        layout.addLayout(info_section)
        
        self.setLayout(layout)
        
        # Tenta obter IP automaticamente ao inicializar
        self._auto_detect_ip()
    
    def _validate_ip(self, text):
        """Valida o formato do IP"""
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        is_valid = bool(re.match(ip_pattern, text)) and text != ""
        self.connect_btn.setEnabled(is_valid)
    
    def _auto_detect_ip(self):
        """Tenta detectar automaticamente o IP do dispositivo"""
        try:
            devices = self.adb_manager.list_devices()
            usb_devices = [d for d in devices if d.state == "device" and not ":" in d.serial]
            
            if usb_devices:
                device = usb_devices[0]
                ip = self.adb_manager.get_device_ip(device.serial)
                if ip:
                    self.ip_display.setText(f"📱 IP detectado: {ip}")
                    self.ip_input.setText(ip)
                    self.get_ip_btn.setText("🔄 Atualizar")
                else:
                    self.ip_display.setText("📱 Conectado via USB - clique 'Obter IP'")
            else:
                self.ip_display.setText("📱 Nenhum dispositivo USB conectado")
        except Exception as e:
            self.ip_display.setText(f"❌ Erro: {str(e)}")
    
    def _get_device_ip(self):
        """Obtém o IP do dispositivo conectado via USB"""
        try:
            devices = self.adb_manager.list_devices()
            usb_devices = [d for d in devices if d.state == "device" and not ":" in d.serial]
            
            if not usb_devices:
                QMessageBox.warning(
                    self, 
                    "Nenhum dispositivo USB", 
                    "Conecte um dispositivo via USB primeiro!"
                )
                return
            
            device = usb_devices[0]
            self.ip_display.setText("🔍 Detectando IP...")
            
            # Executa em thread separada
            self.worker = WiFiConnectionWorker(
                self.adb_manager, 
                "get_ip", 
                device_id=device.serial
            )
            self.worker.finished.connect(self._on_ip_detected)
            self.worker.start()
            
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao obter IP: {str(e)}")
    
    def _on_ip_detected(self, success, message):
        """Callback quando IP é detectado"""
        if success and message and message != "Erro: Operação inválida":
            ip = message.strip()
            self.ip_display.setText(f"📱 IP detectado: {ip}")
            self.ip_input.setText(ip)
            self.get_ip_btn.setText("🔄 Atualizar")
            QMessageBox.information(self, "IP Detectado", f"IP encontrado: {ip}")
        else:
            self.ip_display.setText("❌ Não foi possível detectar o IP")
            QMessageBox.warning(
                self, 
                "IP não detectado", 
                "Não foi possível obter o IP automaticamente.\n"
                "Verifique se o dispositivo está conectado via USB\n"
                "e se está na mesma rede WiFi."
            )
    
    def _enable_wifi_mode(self):
        """Ativa o modo WiFi no dispositivo"""
        devices = self.adb_manager.list_devices()
        usb_devices = [d for d in devices if d.state == "device" and not ":" in d.serial]
        
        if not usb_devices:
            QMessageBox.warning(
                self, 
                "Nenhum dispositivo USB", 
                "Conecte um dispositivo via USB primeiro!"
            )
            return
        
        device = usb_devices[0]  # Usa o primeiro dispositivo USB
        port = self.wifi_port_spin.value()
        
        # Mostra progress dialog
        progress = QProgressDialog("Ativando modo WiFi...", "Cancelar", 0, 0)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        # Executa em thread separada
        self.worker = WiFiConnectionWorker(
            self.adb_manager, 
            "enable", 
            device_id=device.serial, 
            port=port
        )
        self.worker.finished.connect(lambda success, msg: self._on_wifi_enabled(success, msg, progress))
        self.worker.start()
    
    def _on_wifi_enabled(self, success, message, progress):
        """Callback quando modo WiFi é ativado"""
        progress.close()
        
        if success:
            QMessageBox.information(self, "Sucesso", message)
        else:
            QMessageBox.warning(self, "Erro", message)
    
    def _connect_wifi(self):
        """Conecta a um dispositivo via WiFi"""
        ip = self.ip_input.text().strip()
        port = self.connect_port_spin.value()
        
        if not ip:
            QMessageBox.warning(self, "IP inválido", "Digite um endereço IP válido!")
            return
        
        # Mostra progress dialog
        progress = QProgressDialog("Conectando via WiFi...", "Cancelar", 0, 0)
        progress.setWindowModality(Qt.WindowModal)
        progress.show()
        
        # Executa em thread separada
        self.worker = WiFiConnectionWorker(
            self.adb_manager, 
            "connect", 
            ip=ip, 
            port=port
        )
        self.worker.finished.connect(lambda success, msg: self._on_wifi_connected(success, msg, progress))
        self.worker.start()
    
    def _on_wifi_connected(self, success, message, progress):
        """Callback quando conexão WiFi é estabelecida"""
        progress.close()
        
        if success:
            QMessageBox.information(self, "Conectado!", message)
            # Limpa o campo IP após sucesso
            self.ip_input.clear()
        else:
            QMessageBox.warning(self, "Erro na conexão", message)
