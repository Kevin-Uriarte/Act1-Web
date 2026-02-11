from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse


class WebRequestHandler(BaseHTTPRequestHandler):
    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        response = self.get_response()

        if response is None:
            self.send_response(404)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina no encontrada</h1>")

        else:    
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(self.get_response().encode("utf-8"))

    def get_response(self):
        ruta = self.url().path
        query = self.query_data()

        if ruta.startswith("/proyecto/"):
            proyecto = ruta.split("/")[-1]
            autor = query.get("autor","desconocido")

            return f"<h1>Proyecto: {proyecto} Autor: {autor}</h1>"
        # home page
        if ruta == "/":
            with open ("home.html","r",encoding="utf-8") as archivo:
                return archivo.read()
        return None
    pass     


if __name__ == "__main__":
    print("Starting server")
    #el servidor escucha en el puerto 8000
    puerto = 8000
    print(f"Servidor eschuchando en puerto: {puerto}")
    server = HTTPServer(("localhost", puerto), WebRequestHandler)
    server.serve_forever()
