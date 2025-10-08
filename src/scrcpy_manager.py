"""
Módulo para gerenciamento do scrcpy
"""

import subprocess
import shlex
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class ScrcpyOptions:
    """Opções de configuração para o scrcpy"""
    
    # Resolução
    max_size: Optional[int] = None  # ex: 1024 (largura máxima)
    
    # Taxa de bits
    bit_rate: Optional[str] = "8M"  # ex: "8M", "2M"
    
    # FPS máximo
    max_fps: Optional[int] = None  # ex: 60, 30
    
    # Orientação
    lock_orientation: Optional[int] = None  # 0: natural, 1: 90°, 2: 180°, 3: 270°
    
    # Display
    fullscreen: bool = False
    always_on_top: bool = False
    borderless: bool = False
    
    # Controle
    turn_screen_off: bool = False
    stay_awake: bool = False
    show_touches: bool = False
    disable_screensaver: bool = False
    
    # Gravação
    record_file: Optional[str] = None
    no_display: bool = False  # Apenas gravar sem exibir
    
    # Áudio (scrcpy >= 2.0)
    no_audio: bool = False
    
    # Codec
    video_codec: str = "h264"  # h264, h265, av1
    
    # Outras
    window_title: Optional[str] = None
    window_x: Optional[int] = None
    window_y: Optional[int] = None
    window_width: Optional[int] = None
    window_height: Optional[int] = None
    
    def to_args(self) -> list:
        """Converte as opções para argumentos de linha de comando"""
        args = []
        
        if self.max_size:
            args.extend(["-m", str(self.max_size)])
        
        if self.bit_rate:
            args.extend(["-b", self.bit_rate])
        
        if self.max_fps:
            args.extend(["--max-fps", str(self.max_fps)])
        
        if self.lock_orientation is not None:
            # scrcpy 3.2+ usa: --capture-orientation com valores em graus (0, 90, 180, 270)
            print(f"DEBUG: Adicionando orientação ao comando: --capture-orientation={self.lock_orientation}")
            args.append(f"--capture-orientation={self.lock_orientation}")
        
        if self.fullscreen:
            args.append("-f")
        
        if self.always_on_top:
            args.append("--always-on-top")
        
        if self.borderless:
            args.append("--window-borderless")
        
        if self.turn_screen_off:
            args.append("--turn-screen-off")
        
        if self.stay_awake:
            args.append("--stay-awake")
        
        if self.show_touches:
            args.append("--show-touches")
        
        if self.disable_screensaver:
            args.append("--disable-screensaver")
        
        if self.record_file:
            args.extend(["-r", self.record_file])
        
        if self.no_display:
            args.append("-N")
        
        if self.no_audio:
            args.append("--no-audio")
        
        if self.video_codec:
            args.extend(["--video-codec", self.video_codec])
        
        if self.window_title:
            args.extend(["--window-title", self.window_title])
        
        if self.window_x is not None and self.window_y is not None:
            args.extend(["--window-x", str(self.window_x)])
            args.extend(["--window-y", str(self.window_y)])
        
        if self.window_width is not None and self.window_height is not None:
            args.extend(["--window-width", str(self.window_width)])
            args.extend(["--window-height", str(self.window_height)])
        
        return args


class ScrcpyManager:
    """Gerenciador do scrcpy"""
    
    def __init__(self):
        self.scrcpy_path = "scrcpy"
        self.process: Optional[subprocess.Popen] = None
        
    def check_scrcpy_available(self) -> bool:
        """Verifica se o scrcpy está instalado e disponível"""
        try:
            result = subprocess.run(
                [self.scrcpy_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_scrcpy_version(self) -> Optional[str]:
        """Retorna a versão do scrcpy instalado"""
        try:
            result = subprocess.run(
                [self.scrcpy_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # A primeira linha geralmente contém a versão
                lines = result.stdout.strip().split('\n')
                if lines:
                    return lines[0].replace("scrcpy", "").strip()
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
    
    def start_mirroring(self, serial: Optional[str] = None, options: Optional[ScrcpyOptions] = None) -> tuple[bool, str]:
        """
        Inicia o espelhamento de tela
        
        Args:
            serial: Serial do dispositivo (None para o primeiro dispositivo)
            options: Opções de configuração do scrcpy
        
        Returns:
            Tuple (sucesso, mensagem)
        """
        if self.is_running():
            return False, "scrcpy já está em execução"
        
        try:
            args = [self.scrcpy_path]
            
            # Adiciona o serial se fornecido
            if serial:
                args.extend(["-s", serial])
            
            # Adiciona as opções se fornecidas
            if options:
                args.extend(options.to_args())
            
            # Debug: mostra o comando completo
            print(f"DEBUG SCRCPY: Comando completo: {' '.join(args)}")
            
            # Inicia o processo em background
            self.process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return True, "scrcpy iniciado com sucesso"
            
        except FileNotFoundError:
            return False, "scrcpy não encontrado. Certifique-se de que está instalado."
        except Exception as e:
            return False, f"Erro ao iniciar scrcpy: {str(e)}"
    
    def start_mirroring_wireless(self, ip_address: str, port: int = 5555, options: Optional[ScrcpyOptions] = None) -> tuple[bool, str]:
        """
        Inicia o espelhamento via conexão sem fio
        
        Args:
            ip_address: Endereço IP do dispositivo
            port: Porta TCP (padrão: 5555)
            options: Opções de configuração do scrcpy
        
        Returns:
            Tuple (sucesso, mensagem)
        """
        if self.is_running():
            return False, "scrcpy já está em execução"
        
        try:
            # Primeiro, conecta ao dispositivo via ADB
            connect_result = subprocess.run(
                ["adb", "connect", f"{ip_address}:{port}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "connected" not in connect_result.stdout.lower():
                return False, f"Falha ao conectar ao dispositivo: {connect_result.stdout}"
            
            # Então inicia o scrcpy
            args = [self.scrcpy_path, "-s", f"{ip_address}:{port}"]
            
            if options:
                args.extend(options.to_args())
            
            self.process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return True, f"scrcpy conectado a {ip_address}:{port}"
            
        except FileNotFoundError:
            return False, "scrcpy ou adb não encontrado"
        except subprocess.TimeoutExpired:
            return False, "Timeout ao conectar ao dispositivo"
        except Exception as e:
            return False, f"Erro ao iniciar scrcpy: {str(e)}"
    
    def stop_mirroring(self) -> tuple[bool, str]:
        """Para o espelhamento de tela"""
        if not self.is_running():
            return False, "scrcpy não está em execução"
        
        try:
            self.process.terminate()
            self.process.wait(timeout=5)
            self.process = None
            return True, "scrcpy finalizado"
        except subprocess.TimeoutExpired:
            # Force kill se não terminar normalmente
            self.process.kill()
            self.process = None
            return True, "scrcpy finalizado (forçado)"
        except Exception as e:
            return False, f"Erro ao finalizar scrcpy: {str(e)}"
    
    def is_running(self) -> bool:
        """Verifica se o scrcpy está em execução"""
        if self.process is None:
            return False
        
        # Verifica se o processo ainda está ativo
        return self.process.poll() is None
    
    def get_preset_options(self, preset: str) -> ScrcpyOptions:
        """
        Retorna opções pré-configuradas
        
        Presets disponíveis:
        - quality: Melhor qualidade
        - performance: Melhor performance
        - low_latency: Menor latência
        - record: Para gravação
        """
        if preset == "quality":
            return ScrcpyOptions(
                bit_rate="16M",
                max_fps=60,
                video_codec="h265",
                stay_awake=True,
                disable_screensaver=True
            )
        
        elif preset == "performance":
            return ScrcpyOptions(
                max_size=720,
                bit_rate="4M",
                max_fps=30,
                video_codec="h264",
                stay_awake=True
            )
        
        elif preset == "low_latency":
            return ScrcpyOptions(
                max_size=1024,
                bit_rate="8M",
                max_fps=60,
                video_codec="h264",
                no_audio=True,
                disable_screensaver=True
            )
        
        elif preset == "record":
            return ScrcpyOptions(
                bit_rate="16M",
                max_fps=60,
                video_codec="h265",
                no_display=False,
                stay_awake=True
            )
        
        else:
            # Padrão
            return ScrcpyOptions(
                bit_rate="8M",
                stay_awake=True
            )
    
    def get_process_info(self) -> Optional[Dict[str, Any]]:
        """Retorna informações sobre o processo em execução"""
        if not self.is_running():
            return None
        
        return {
            "pid": self.process.pid,
            "running": True
        }

