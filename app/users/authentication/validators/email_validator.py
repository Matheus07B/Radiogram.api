import os
import re
import smtplib
import dns.resolver
from dotenv import load_dotenv
from typing import Dict

# Configurações do seu e-mail
load_dotenv()

class EmailValidator:
    def __init__(self):
      self.allowed_tlds = os.getenv('ALLOWED_TLDS', 'com,net,org,edu,gov,io,br,info').split(',')
      self.blocked_domains = os.getenv('BLOCKED_EMAIL_DOMAINS', 'tempmail.com,mailinator.com').split(',')
      self.smtp_timeout = int(os.getenv('SMTP_TIMEOUT', 10))
      self.helo_domain = os.getenv('HELO_DOMAIN')
      self.test_email = os.getenv('EMAIL_SENDER')  # Usando seu e-mail como remetente de teste

    def validate_email(self, email: str) -> Dict[str, any]:
      """Validação completa do e-mail com 3 camadas"""
      if not isinstance(email, str):
        return self._error_result(email, "Tipo inválido (deve ser string)")

      resultado = {
        "email": email,
        "valid": False,
        "reason": "",
        "confidence": "low"
      }

      # 1ª Camada: Validação Regex
      if not self._check_format(email):
        resultado["reason"] = "Formato inválido ou domínio proibido"
        return resultado

      dominio = email.split('@')[-1]

      # 2ª Camada: Validação DNS MX
      if not self._check_mx_records(dominio, resultado):
        return resultado

      # 3ª Camada: Verificação SMTP
      self._smtp_validation(email, dominio, resultado)
      
      return resultado

    def _error_result(self, email: str, reason: str) -> Dict[str, any]:
      """Helper para criar resultado de erro"""
      return {
        "email": email,
        "valid": False,
        "reason": reason,
        "confidence": "low"
      }

    def _check_format(self, email: str) -> bool:
      """Regex avançada com bloqueio de domínios descartáveis"""
      tld_pattern = '|'.join(map(re.escape, self.allowed_tlds))
      blocked_pattern = '|'.join(map(re.escape, self.blocked_domains))
      
      # Usando f-strings para evitar problemas com format()
      pattern = (
        r'^(?!.*\.{2})'  # Não permite dois pontos consecutivos
        r'(?!.*@(?:{blocked})$)'  # Bloqueia domínios proibidos
        r'[a-zA-Z0-9._%+-]+'  # Parte local
        r'@' 
        r'[a-zA-Z0-9.-]+'  # Domínio
        r'\.(?:{tlds})$'  # TLDs permitidos
      ).replace('{blocked}', blocked_pattern).replace('{tlds}', tld_pattern)
      
      return bool(re.fullmatch(pattern, email))

    def _check_mx_records(self, dominio: str, resultado: Dict) -> bool:
      """Consulta registros MX com tratamento de erros"""
      try:
        answers = dns.resolver.resolve(dominio, 'MX')
        if not answers:
            resultado["reason"] = "Domínio sem registros MX"
            return False
        return True
      except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        resultado["reason"] = "Domínio não existe ou não aceita e-mails"
        return False
      except Exception as e:
        resultado["reason"] = f"Erro na consulta DNS: {str(e)}"
        return False

    def _smtp_validation(self, email: str, dominio: str, resultado: Dict):
      """Verificação SMTP sem enviar e-mail"""
      try:
        answers = dns.resolver.resolve(dominio, 'MX')
        mx_record = str(answers[0].exchange).rstrip('.')
        
        with smtplib.SMTP(mx_record, timeout=self.smtp_timeout) as server:
          server.helo(self.helo_domain)
          server.mail(self.test_email)
          code, _ = server.rcpt(email)
            
          if code in (250, 251):
            resultado.update({
              "valid": True,
              "reason": "E-mail verificado com sucesso",
              "confidence": "high"
            })
          else:
            resultado["reason"] = f"Servidor recusou o e-mail (código {code})"
      except smtplib.SMTPConnectError:
        resultado["reason"] = "Não foi possível conectar ao servidor de e-mail"
      except Exception as e:
        resultado["reason"] = f"Falha na verificação SMTP: {str(e)}"

# Instância global para reutilização
email_validator = EmailValidator()

def validar_email_completo(email: str) -> dict:
  """Interface simplificada para o validador"""
  return email_validator.validate_email(email)