import re
import unicodedata
import logging
from typing import List, Tuple, Optional

# Configuração inicial de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(' MessageValidator')

# Compilação de padrões uma vez no início
SAFE_TEXT_PATTERN = re.compile(
    r'^[\w\sáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ,.!?<>=-]+$',
    re.IGNORECASE | re.UNICODE
)

EMOJI_ONLY_PATTERN = re.compile(
    r'^['
    r'\U0001F600-\U0001F64F\U0001F300-\U0001F5FF'
    r'\U0001F680-\U0001F6FF\U0001F700-\U0001F77F'
    r'\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF'
    r'\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F'
    r'\U0001FA70-\U0001FAFF\U00002702-\U000027B0'
    r'\U000024C2-\U0001F251'
    r']+$'
)

THREAT_PATTERNS = {
    'xss': [
        re.compile(r"<\/?[a-z]+\d*", re.IGNORECASE),
        re.compile(r"on\w+=", re.IGNORECASE),
        re.compile(r"javascript:|data:", re.IGNORECASE)
    ],
    'sqli': [
        re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE)\b", re.IGNORECASE),
        re.compile(r"--|#|\/\*|\*\/|' OR '1'='1", re.IGNORECASE)
    ],
    'injection': [
        re.compile(r"[|&;`$]", re.IGNORECASE),
        re.compile(r"\b(exec|system|passthru|shell_exec)\b", re.IGNORECASE)
    ],
    'encoding': [
        re.compile(r"\\[xu]|%[0-9a-fA-F]{2}|&[#x]", re.IGNORECASE)
    ],
    'homoglyphs': [
        re.compile(r"[\u0430-\u044f\u0451\u0401]", re.IGNORECASE)  # Cirílico
    ],
    'control_chars': [
        re.compile(r'[\u0000-\u001F\u007F-\u009F\u200B-\u200F\u2028-\u202F\uFEFF]')
    ]
}

def is_message_safe(message: str) -> bool:
    """
    Verifica se uma mensagem é segura usando múltiplas camadas de validação.
    
    Retorna:
        bool: True se a mensagem for segura, False caso contrário
    """
    # Verificação inicial do tipo
    if not isinstance(message, str):
        logger.warning("Tipo de mensagem inválido recebido")
        return False

    # Normalização e limpeza
    message = unicodedata.normalize("NFKC", message).strip()
    if not message:
        return False

    # Verificação de caracteres de controle
    if THREAT_PATTERNS['control_chars'][0].search(message):
        logger.warning(f"Caracteres de controle detectados: {message[:50]}")
        return False

    # Verificação de homóglifos
    if THREAT_PATTERNS['homoglyphs'][0].search(message):
        logger.warning(f"Homóglifos detectados: {message[:50]}")
        return False

    # Verificação de emojis puros
    if EMOJI_ONLY_PATTERN.fullmatch(message):
        return True

    # Verificação de padrão de texto seguro
    if not SAFE_TEXT_PATTERN.fullmatch(message):
        logger.warning(f"Formato de mensagem inválido: {message[:50]}")
        return False

    # Verificação de ameaças categorizadas
    for threat_type, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(message):
                logger.warning(f"Ameaça {threat_type} detectada: {message[:50]}")
                return False

    # Sanitização final
    clean_message = THREAT_PATTERNS['control_chars'][0].sub('', message)
    clean_message = ' '.join(clean_message.split())
    
    if clean_message != message:
        logger.info(f"Mensagem sanitizada: {message[:50]} -> {clean_message[:50]}")

    return True


# DEIXE COMENTADO, ISSO È APENAS PARA VERIFICAR SE ESTÁ TUDO CERTO.
# test_messages = [
#     "1000 > 999",  # Válido
#     "dinheiro > carro",  # Válido
#     "<script>alert(1)</script>",  # XSS
#     "SELECT * FROM users",  # SQLi
#     "cat /etc/passwd",  # Shell injection
#     "ｅｘａｍｐｌｅ",  # Homóglifos
#     "Olá \u200Bmundo",  # Caractere de controle
#     "😊❤️"  # Apenas emojis
# ]

# for msg in test_messages:
#     result = is_message_safe(msg)
#     print(f"{'✅' if result else '❌'} {msg[:30]:<30}")

# NAO VOU APAGAR POIS POSSO USAR DEPOIS

# not_allowed_texts = [
#     # Tags HTML/XML perigosas
#     "<script", "</script", 
#     "<iframe", "</iframe", 
#     "<object", "</object", 
#     "<embed", "</embed", 
#     "<link", "</link", 
#     "<meta", "</meta", 
#     "<style", "</style", 
#     "<base", "</base", 
#     "<form", "</form", 
#     "<input", 
#     "<textarea", "</textarea", 
#     "<svg", "</svg", 
#     "<math", "</math", 
#     "<applet", "</applet", 
#     "<marquee", "</marquee", 
#     "<frameset", "</frameset", 
#     "<frame", "</frame", 
#     "<img", "<image", 
#     "<body", "</body", 
#     "<html", "</html", 
#     "<head", "</head", 
#     "<title", "</title", 
#     "<video", "</video", 
#     "<audio", "</audio", 
#     "<source", 
#     "<track", 
#     "<xss", 
#     "<!DOCTYPE", 
#     "<!ENTITY", 
#     "<!ELEMENT", 
    
#     # Atributos de eventos
#     "onabort=", "onafterprint=", "onbeforeprint=", 
#     "onbeforeunload=", "onblur=", "oncanplay=", 
#     "oncanplaythrough=", "onchange=", "onclick=", 
#     "oncontextmenu=", "oncopy=", "oncuechange=", 
#     "oncut=", "ondblclick=", "ondrag=", 
#     "ondragend=", "ondragenter=", "ondragleave=", 
#     "ondragover=", "ondragstart=", "ondrop=", 
#     "ondurationchange=", "onemptied=", "onended=", 
#     "onerror=", "onfocus=", "onhashchange=", 
#     "oninput=", "oninvalid=", "onkeydown=", 
#     "onkeypress=", "onkeyup=", "onload=", 
#     "onloadeddata=", "onloadedmetadata=", "onloadstart=", 
#     "onmessage=", "onmousedown=", "onmouseenter=", 
#     "onmouseleave=", "onmousemove=", "onmouseover=", 
#     "onmouseout=", "onmouseup=", "onmousewheel=", 
#     "onoffline=", "ononline=", "onpagehide=", 
#     "onpageshow=", "onpaste=", "onpause=", 
#     "onplay=", "onplaying=", "onpopstate=", 
#     "onprogress=", "onratechange=", "onreset=", 
#     "onresize=", "onscroll=", "onsearch=", 
#     "onseeked=", "onseeking=", "onselect=", 
#     "onshow=", "onstalled=", "onstorage=", 
#     "onsubmit=", "onsuspend=", "ontimeupdate=", 
#     "ontoggle=", "onunload=", "onvolumechange=", 
#     "onwaiting=", "onwheel=",
    
#     # Protocolos perigosos
#     "javascript:", 
#     "vbscript:", 
#     "data:", 
#     "about:", 
#     "jar:", 
#     "ws:", 
#     "wss:", 
#     "feed:", 
#     "tel:", 
#     "callto:", 
#     "file:", 
    
#     # Código server-side
#     "<?php", "<?=", "?>", 
#     "<%", "%>", 
#     "<?", "?>", 
#     "<jsp:", "</jsp:", 
#     "<asp:", "</asp:", 
    
#     # Acesso a DOM/APIs sensíveis
#     "document.cookie", 
#     "window.location", 
#     "document.write", 
#     "document.domain", 
#     "eval(", 
#     "setTimeout(", 
#     "setInterval(", 
#     "Function(", 
#     "alert(", 
#     "confirm(", 
#     "prompt(", 
#     "fetch(", 
#     "XMLHttpRequest", 
#     "WebSocket", 
#     "localStorage", 
#     "sessionStorage", 
#     "indexedDB", 
    
#     # Injeção SQL (padrões comuns)
#     "SELECT ", "INSERT ", "UPDATE ", "DELETE ", 
#     "DROP ", "ALTER ", "CREATE ", "TRUNCATE ", 
#     "UNION ", "JOIN ", "WHERE ", "FROM ", 
#     "--", "#", "/*", "*/", 
#     "' OR '1'='1", "' OR 1=1", 
    
#     # Codificação suspeita
#     "\\x", "\\u", 
#     "%0", "%1", "%2", "%3", 
#     "&#", "&x", 
    
#     # Shell injection
#     "|", "&", ";", "`", "$(", ">", "<", 
#     "\\n", "\\r", 
    
#     # Outros padrões maliciosos
#     "import ", "require(", 
#     "include(", "include_once(", 
#     "exec(", "system(", "passthru(", 
#     "shell_exec(", "proc_open(", 
#     "popen(", "pcntl_exec(", 
#     "assert(", "extract(", 
#     "parse_str(", "putenv(", 
#     "ini_set(", "dl(", 
#     "header(", "setcookie("
# ]