"""
Módulo para gerenciamento de comandos ADB
"""

import subprocess
import re
from typing import List, Dict, Optional, Tuple


class ADBDevice:
    """Representa um dispositivo Android conectado"""
    
    def __init__(self, serial: str, state: str):
        self.serial = serial
        self.state = state
        self.model = ""
        self.manufacturer = ""
        self.android_version = ""
        self.battery_level = ""
        
    def __repr__(self):
        return f"ADBDevice(serial={self.serial}, state={self.state}, model={self.model})"


class ADBManager:
    """Gerenciador de comandos ADB"""
    
    def __init__(self):
        self.adb_path = "adb"
        
    def check_adb_available(self) -> bool:
        """Verifica se o ADB está instalado e disponível"""
        try:
            result = subprocess.run(
                [self.adb_path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_adb_version(self) -> Optional[str]:
        """Retorna a versão do ADB instalado"""
        try:
            result = subprocess.run(
                [self.adb_path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Extrai a versão da primeira linha
                match = re.search(r'version ([\d.]+)', result.stdout)
                if match:
                    return match.group(1)
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
    
    def list_devices(self) -> List[ADBDevice]:
        """Lista todos os dispositivos conectados"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices", "-l"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return []
            
            devices = []
            lines = result.stdout.strip().split('\n')[1:]  # Pula a primeira linha "List of devices attached"
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    state = parts[1]
                    
                    device = ADBDevice(serial, state)
                    
                    # Tenta extrair informações adicionais
                    if state == "device":
                        self._populate_device_info(device)
                    
                    devices.append(device)
            
            return devices
            
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []
    
    def _populate_device_info(self, device: ADBDevice):
        """Popula informações adicionais do dispositivo"""
        # Modelo
        device.model = self._get_device_property(device.serial, "ro.product.model")
        
        # Fabricante
        device.manufacturer = self._get_device_property(device.serial, "ro.product.manufacturer")
        
        # Versão do Android
        device.android_version = self._get_device_property(device.serial, "ro.build.version.release")
        
        # Nível da bateria
        device.battery_level = self._get_battery_level(device.serial)
    
    def _get_device_property(self, serial: str, property_name: str) -> str:
        """Obtém uma propriedade do dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "shell", "getprop", property_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return ""
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return ""
    
    def _get_battery_level(self, serial: str) -> str:
        """Obtém o nível da bateria do dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "shell", "dumpsys", "battery"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                match = re.search(r'level: (\d+)', result.stdout)
                if match:
                    return f"{match.group(1)}%"
            return ""
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return ""
    
    def install_apk(self, serial: str, apk_path: str) -> Tuple[bool, str]:
        """Instala um APK no dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "install", "-r", apk_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0 and "Success" in result.stdout:
                return True, "APK instalado com sucesso!"
            else:
                return False, result.stdout + result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao instalar APK"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def take_screenshot(self, serial: str, output_path: str) -> Tuple[bool, str]:
        """Captura uma screenshot do dispositivo"""
        try:
            # Primeiro, captura a screenshot no dispositivo
            device_path = "/sdcard/screenshot.png"
            
            result = subprocess.run(
                [self.adb_path, "-s", serial, "shell", "screencap", "-p", device_path],
                capture_output=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return False, "Falha ao capturar screenshot"
            
            # Depois, puxa a screenshot para o computador
            result = subprocess.run(
                [self.adb_path, "-s", serial, "pull", device_path, output_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Remove a screenshot do dispositivo
                subprocess.run(
                    [self.adb_path, "-s", serial, "shell", "rm", device_path],
                    capture_output=True,
                    timeout=5
                )
                return True, f"Screenshot salva em: {output_path}"
            else:
                return False, "Falha ao transferir screenshot"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao capturar screenshot"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def push_file(self, serial: str, local_path: str, remote_path: str) -> Tuple[bool, str]:
        """Envia um arquivo para o dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "push", local_path, remote_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, f"Arquivo enviado para: {remote_path}"
            else:
                return False, result.stdout + result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao enviar arquivo"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def pull_file(self, serial: str, remote_path: str, local_path: str) -> Tuple[bool, str]:
        """Baixa um arquivo do dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "pull", remote_path, local_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, f"Arquivo baixado para: {local_path}"
            else:
                return False, result.stdout + result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao baixar arquivo"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def execute_command(self, serial: str, command: str) -> Tuple[bool, str]:
        """Executa um comando shell no dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "-s", serial, "shell", command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            return result.returncode == 0, output
            
        except subprocess.TimeoutExpired:
            return False, "Timeout ao executar comando"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def reboot_device(self, serial: str, mode: str = "system") -> Tuple[bool, str]:
        """Reinicia o dispositivo (system, recovery, bootloader)"""
        try:
            if mode == "system":
                result = subprocess.run(
                    [self.adb_path, "-s", serial, "reboot"],
                    capture_output=True,
                    timeout=10
                )
            else:
                result = subprocess.run(
                    [self.adb_path, "-s", serial, "reboot", mode],
                    capture_output=True,
                    timeout=10
                )
            
            if result.returncode == 0:
                return True, f"Dispositivo reiniciando em modo {mode}"
            else:
                return False, "Falha ao reiniciar dispositivo"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao reiniciar dispositivo"
        except FileNotFoundError:
            return False, "ADB não encontrado"
    
    def get_device_info(self, serial: str) -> Dict[str, str]:
        """Obtém informações detalhadas do dispositivo"""
        info = {}
        
        properties = {
            "Modelo": "ro.product.model",
            "Fabricante": "ro.product.manufacturer",
            "Android": "ro.build.version.release",
            "SDK": "ro.build.version.sdk",
            "CPU": "ro.product.cpu.abi",
            "Serial": "ro.serialno",
        }
        
        for label, prop in properties.items():
            info[label] = self._get_device_property(serial, prop)
        
        info["Bateria"] = self._get_battery_level(serial)
        
        return info
    
    def connect_wifi_device(self, ip_address: str, port: int = 5555) -> Tuple[bool, str]:
        """Conecta a um dispositivo Android via WiFi"""
        try:
            print(f"Tentando conectar ao dispositivo WiFi: {ip_address}:{port}")
            
            # Conecta via WiFi
            result = subprocess.run(
                [self.adb_path, "connect", f"{ip_address}:{port}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"Dispositivo conectado via WiFi: {ip_address}:{port}")
                return True, f"Conectado via WiFi: {ip_address}:{port}"
            else:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                print(f"Erro ao conectar via WiFi: {error_msg}")
                return False, f"Erro: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao conectar via WiFi"
        except Exception as e:
            print(f"Erro ao conectar dispositivo WiFi: {e}")
            return False, f"Erro: {str(e)}"
    
    def disconnect_device(self, device_id: str) -> Tuple[bool, str]:
        """Desconecta um dispositivo"""
        try:
            result = subprocess.run(
                [self.adb_path, "disconnect", device_id],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True, f"Dispositivo {device_id} desconectado"
            else:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                return False, f"Erro ao desconectar: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao desconectar dispositivo"
        except Exception as e:
            print(f"Erro ao desconectar dispositivo: {e}")
            return False, f"Erro: {str(e)}"
    
    def enable_wifi_mode(self, device_id: str, port: int = 5555) -> Tuple[bool, str]:
        """Ativa o modo WiFi no dispositivo (requer USB conectado)"""
        try:
            # Ativa o modo tcpip na porta especificada
            result = subprocess.run(
                [self.adb_path, "-s", device_id, "tcpip", str(port)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"Modo WiFi ativado no dispositivo {device_id} na porta {port}")
                return True, f"Modo WiFi ativado na porta {port}"
            else:
                error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
                print(f"Erro ao ativar modo WiFi: {error_msg}")
                return False, f"Erro ao ativar modo WiFi: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout ao ativar modo WiFi"
        except Exception as e:
            print(f"Erro ao ativar modo WiFi: {e}")
            return False, f"Erro: {str(e)}"
    
    def get_device_ip(self, device_id: str) -> str:
        """Obtém o IP do dispositivo via WiFi"""
        try:
            print(f"DEBUG: Tentando obter IP do dispositivo {device_id}")
            
            # Método 1: Usando getprop para diferentes interfaces WiFi
            wifi_props = [
                "dhcp.wlan0.ipaddress",
                "dhcp.wifi.ipaddress", 
                "dhcp.wlan1.ipaddress",
                "dhcp.eth0.ipaddress"
            ]
            
            for prop in wifi_props:
                result = subprocess.run(
                    [self.adb_path, "-s", device_id, "shell", "getprop", prop],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    ip = result.stdout.strip()
                    print(f"DEBUG: Propriedade {prop} retornou: {ip}")
                    if ip and '.' in ip and ip.count('.') == 3:
                        # Verifica se não é IP de loopback ou gateway comum
                        if not ip.startswith('127.') and ip != '192.168.0.1' and ip != '192.168.1.1' and ip != '10.0.0.1':
                            print(f"DEBUG: IP válido encontrado: {ip}")
                            return ip
            
            # Método 2: Usando ip addr show com parsing melhorado
            result = subprocess.run(
                [self.adb_path, "-s", device_id, "shell", "ip", "addr", "show"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"DEBUG: Saída do ip addr show:\n{result.stdout}")
                lines = result.stdout.strip().split('\n')
                
                for i, line in enumerate(lines):
                    # Procura por interfaces de rede
                    if any(keyword in line.lower() for keyword in ['wlan', 'wifi', 'wl', 'eth']):
                        # Procura nas próximas linhas por 'inet'
                        for j in range(i+1, min(i+5, len(lines))):
                            inet_line = lines[j]
                            if 'inet ' in inet_line and '/' in inet_line:
                                # Extrai o IP (formato: inet 192.168.1.100/24)
                                parts = inet_line.split()
                                for part in parts:
                                    if '.' in part and part.count('.') == 3 and '/' in part:
                                        ip = part.split('/')[0]
                                        # Verifica se não é IP de loopback ou gateway comum
                                        if not ip.startswith('127.') and ip != '192.168.0.1' and ip != '192.168.1.1' and ip != '10.0.0.1':
                                            print(f"DEBUG: IP encontrado via ip addr: {ip}")
                                            return ip
            
            # Método 3: Usando ifconfig (fallback)
            result = subprocess.run(
                [self.adb_path, "-s", device_id, "shell", "ifconfig", "wlan0"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"DEBUG: Saída do ifconfig:\n{result.stdout}")
                import re
                ip_match = re.search(r'inet addr:(\d+\.\d+\.\d+\.\d+)', result.stdout)
                if ip_match:
                    ip = ip_match.group(1)
                    if ip != '192.168.0.1' and ip != '192.168.1.1' and ip != '10.0.0.1':
                        print(f"DEBUG: IP encontrado via ifconfig: {ip}")
                        return ip
            
            print("DEBUG: Nenhum IP válido encontrado")
            return ""
            
        except (subprocess.TimeoutExpired, Exception) as e:
            print(f"DEBUG: Erro ao obter IP: {e}")
            return ""

