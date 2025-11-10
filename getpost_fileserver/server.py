from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import signal
import threading

def main():
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            filename = self.headers.get('X-Filename', 'default_uploaded_file')
            filename = os.path.basename(filename)
            length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(length)
            with open(filename, "wb") as f:
                f.write(post_data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        def do_GET(self):
            try:
                entries = os.listdir('.')
                listing = "\n".join(entries).encode()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Directory listing:\n")
                self.wfile.write(listing)
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}\n".encode())

    def runCode():
        try:
            port = int(sys.argv[1])
        except (IndexError, ValueError):
            print(help()); return

        server = HTTPServer(('0.0.0.0', port), Handler)

        def _graceful(signum, frame):
            print("\nShutting down...")
            threading.Thread(target=server.shutdown, daemon=True).start()

        signal.signal(signal.SIGINT, _graceful)
        signal.signal(signal.SIGTERM, _graceful)

        try:
            print(f"Listening on port {port}...")
            server.serve_forever(poll_interval=0.2)
        finally:
            server.server_close()
            print("Server stopped.")
            print("https://github.com/kaledaljebur/getpost-fileserver.")
    
    def help():
        characters="="*50
        outText = f"""
    {characters}
    ++REQUIRED FORMAT:++
    Windows format: .\\{os.path.basename(sys.argv[0])} <port number>
    Linux format: ./{os.path.basename(sys.argv[0])} <port number>
    Example for Windows: .\\{os.path.basename(sys.argv[0])} 5555
    https://github.com/kaledaljebur/getpost-fileserver
    {characters}
    """
        return outText

    if len(sys.argv) == 2:
        runCode()
    else:
        print(help())        

if __name__ == "__main__":
    main()