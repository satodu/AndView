"""
Sistema de internacionalização
"""

import json
import locale
import os


class I18n:
    """Gerenciador de traduções"""
    
    def __init__(self):
        self.current_lang = self._detect_system_language()
        self.translations = {}
        self.load_translations()
    
    def _detect_system_language(self) -> str:
        """Detecta a língua do sistema"""
        try:
            # Tenta obter a locale do sistema
            system_locale = locale.getdefaultlocale()[0]
            
            if system_locale:
                # Formata para pt_BR, en_US, etc
                lang_code = system_locale
                
                # Se tiver pt_BR, en_US, etc, mantém
                if '_' in lang_code:
                    return lang_code
                
                # Se for só 'pt', 'en', 'es', adiciona país padrão
                if lang_code.startswith('pt'):
                    return 'pt_BR'
                elif lang_code.startswith('en'):
                    return 'en_US'
                elif lang_code.startswith('es'):
                    return 'es_ES'
                elif lang_code.startswith('fr'):
                    return 'fr_FR'
                elif lang_code.startswith('de'):
                    return 'de_DE'
            
            # Fallback para inglês
            return 'en_US'
            
        except Exception:
            return 'en_US'
    
    def load_translations(self):
        """Carrega o arquivo de traduções"""
        i18n_dir = os.path.dirname(__file__)
        lang_file = os.path.join(i18n_dir, f"{self.current_lang}.json")
        
        # Se não encontrar o arquivo, tenta fallback para pt_BR
        if not os.path.exists(lang_file):
            lang_file = os.path.join(i18n_dir, "pt_BR.json")
        
        # Se ainda não encontrar, usa en_US
        if not os.path.exists(lang_file):
            lang_file = os.path.join(i18n_dir, "en_US.json")
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar traduções: {e}")
            self.translations = {}
    
    def t(self, key: str, **kwargs) -> str:
        """
        Traduz uma chave
        
        Args:
            key: Chave no formato 'menu.file' ou 'devices.title'
            **kwargs: Variáveis para interpolação (ex: count=5)
        
        Returns:
            Texto traduzido
        """
        keys = key.split('.')
        value = self.translations
        
        try:
            for k in keys:
                value = value[k]
            
            # Interpola variáveis se houver
            if kwargs:
                return value.format(**kwargs)
            
            return value
        except (KeyError, TypeError):
            # Se não encontrar, retorna a chave
            return key
    
    def set_language(self, lang_code: str):
        """Muda o idioma"""
        self.current_lang = lang_code
        self.load_translations()


# Instância global
_i18n = None

def get_i18n() -> I18n:
    """Retorna a instância global de I18n"""
    global _i18n
    if _i18n is None:
        _i18n = I18n()
    return _i18n

def t(key: str, **kwargs) -> str:
    """Atalho para traduzir"""
    return get_i18n().t(key, **kwargs)

