"""
Widget de lista de dispositivos
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtCore import Signal, Qt
from typing import List
from ...adb_manager import ADBDevice


class DeviceListWidget(QWidget):
    """Widget para exibir a lista de dispositivos Android conectados"""
    
    device_selected = Signal(ADBDevice)
    refresh_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.devices: List[ADBDevice] = []
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do widget"""
        layout = QVBoxLayout(self)
        
        # Cabeçalho
        header_layout = QHBoxLayout()
        header_label = QLabel("<b>Dispositivos Conectados</b>")
        header_layout.addWidget(header_label)
        
        # Botão de atualizar
        self.refresh_btn = QPushButton("🔄 Atualizar")
        self.refresh_btn.setMaximumWidth(120)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Lista de dispositivos
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        layout.addWidget(self.list_widget)
        
        # Label de status
        self.status_label = QLabel("Nenhum dispositivo encontrado")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #7a7a7a;
            font-style: italic;
            padding: 20px;
        """)
        layout.addWidget(self.status_label)
        
    def update_devices(self, devices: List[ADBDevice]):
        """Atualiza a lista de dispositivos"""
        self.devices = devices
        self.list_widget.clear()
        
        if not devices:
            self.status_label.setText("Nenhum dispositivo encontrado")
            self.status_label.show()
            return
        
        self.status_label.hide()
        
        for device in devices:
            # Cria o texto do item
            if device.state == "device":
                if device.model:
                    text = f"📱 {device.manufacturer} {device.model}"
                    if device.android_version:
                        text += f" (Android {device.android_version})"
                    if device.battery_level:
                        text += f" - 🔋 {device.battery_level}"
                else:
                    text = f"📱 {device.serial}"
            else:
                text = f"⚠️ {device.serial} - {device.state}"
            
            # Adiciona à lista
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, device)
            
            # Define a cor baseado no estado
            if device.state == "device":
                item.setForeground(Qt.black)
            else:
                item.setForeground(Qt.darkGray)
            
            self.list_widget.addItem(item)
        
        # Seleciona o primeiro item automaticamente
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)
            first_item = self.list_widget.item(0)
            device = first_item.data(Qt.UserRole)
            if device.state == "device":
                self.device_selected.emit(device)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Manipula o clique em um item da lista"""
        device = item.data(Qt.UserRole)
        if device.state == "device":
            self.device_selected.emit(device)
    
    def get_selected_device(self) -> ADBDevice:
        """Retorna o dispositivo selecionado"""
        current_item = self.list_widget.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
    
    def set_refreshing(self, refreshing: bool):
        """Define o estado de atualização"""
        self.refresh_btn.setEnabled(not refreshing)
        if refreshing:
            self.refresh_btn.setText("⏳ Atualizando...")
        else:
            self.refresh_btn.setText("🔄 Atualizar")

