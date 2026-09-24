from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from .core import answer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404)
            return
        content = Path(__file__).with_name('index.html').read_bytes()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if self.path != '/api/ask':
            self.send_error(404)
            return
        origin = self.headers.get('Origin')
        if origin and origin not in ('http://127.0.0.1:8765','http://localhost:8765'):
            self.send_error(403)
            return
        try:
            length = int(self.headers.get('Content-Length','0'))
            if not 0 < length <= 16000:
                raise ValueError('Solicitud demasiado extensa o vacía.')
            data = json.loads(self.rfile.read(length))
            history = data.get('history',[])
            if not isinstance(history,list) or any(not isinstance(h,dict) or not isinstance(h.get('question'),str) for h in history):
                raise ValueError('Historial inválido.')
            result = answer(data.get('question'),history,data.get('mode','documental'))
            self.send_response(200)
        except ValueError as exc:
            self.send_response(400)
            result = {'error':str(exc)}
        except Exception:
            self.send_response(503)
            result = {'error':'No se pudo completar la consulta. Verifica Ollama y los modelos o utiliza la consulta documental.'}
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result,ensure_ascii=False).encode())

    def log_message(self,*args):
        pass

def serve():
    print('Nexo disponible en http://127.0.0.1:8765',flush=True)
    HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
