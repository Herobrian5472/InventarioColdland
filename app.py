import os
import json
import shutil
import datetime
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

DB_FILE = "compras_db.json"
BACKUP_DIR = "backups"
HTML_FILE = "index.html"

# Datos por defecto si no existe la base
DEFAULT_DATA = {
    "users": [
        {"username": "admin", "password": "admin123", "nombre": "Administrador", "role": "admin", "email": "admin@coldland.com"},
        {"username": "comprador", "password": "comprador123", "nombre": "Comprador", "role": "comprador", "email": "comprador@coldland.com"},
        {"username": "externo", "password": "externo123", "nombre": "Externo", "role": "externo", "email": "externo@coldland.com"}
    ],
    "proveedores": [
        { "id": "P1001", "razon_social": "FERRONIER SRL", "cuit": "30-68675578-5", "localidad": "Zárate", "email": "" },
        { "id": "P1002", "razon_social": "SYMBAR S.A.", "cuit": "30-69437933-4", "localidad": "Ricardo Rojas", "email": "" },
        { "id": "P1003", "razon_social": "MUNDO STRETCH SRL", "cuit": "30-71567574-5", "localidad": "Buenos Aires", "email": "" },
        { "id": "P1004", "razon_social": "MORE CLEAN SRL", "cuit": "30-71627693-3", "localidad": "Buenos Aires", "email": "" }
    ],
    "materiales": [],
    "maquinarias": [],
    "ubicaciones": [],
    "centrosCosto": [
        "Administración", "Operaciones", "Oficina Operaciones", "Aduana", 
        "Portería", "Mantenimiento", "Sala de Máquinas", "Limpieza Oficinas", "Limpieza Operaciones"
    ],
    "solicitudes": [],
    "cotizaciones": [],
    "ordenes": [],
    "migos": [], 
    "movimientos122": [],
    "miros": [],  
    "stockPanol": [],
    "consumos": []
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_DATA

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    create_backup()

def create_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.json")
    try:
        shutil.copy(DB_FILE, backup_file)
        backups = sorted([os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR)])
        if len(backups) > 15:
            os.remove(backups[0])
    except:
        pass

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            try:
                with open(HTML_FILE, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            except FileNotFoundError:
                self.wfile.write("<h1>Error: Archivo index.html no encontrado.</h1>".encode('utf-8'))
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = load_db()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        elif self.path.endswith('.png') or self.path.endswith('.jpg'):
            try:
                filename = os.path.basename(self.path).replace('%20', ' ')
                with open(filename, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    self.wfile.write(f.read())
            except:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/data':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            save_db(data)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
        else:
            self.send_error(404)
            
    def log_message(self, format, *args):
        pass

def run_server():
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("=====================================================")
    print("🚀 SISTEMA COLDLAND INICIADO CORRECTAMENTE")
    print("👉 Abre tu navegador e ingresa a esta direccion: http://127.0.0.1:8080")
    print("   Para apagar el sistema, presiona Ctrl+C en esta consola")
    print("=====================================================")
    httpd.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    webbrowser.open('http://127.0.0.1:8080')
    try:
        # Mantiene el proceso vivo
        while True:
            pass
    except KeyboardInterrupt:
        print("Cerrando el servidor...")
