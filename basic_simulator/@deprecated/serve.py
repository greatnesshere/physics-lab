from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os.path
from shutil import which

from json import load
with open(os.path.join(os.path.dirname(__file__),"basic.json"),encoding="utf-8") as config:
    opt=load(config)
    PORT=opt["HTTP"]["PORT"]


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,directory=None,**kwargs):
        if directory is None:
            directory=os.path.join(
                os.path.dirname(__file__),
                "www"
            )
        super().__init__(*args,directory=directory,**kwargs)
def main():
    # TODO: integrate with render process.py
    with TCPServer(("localhost",PORT),MyHTTPRequestHandler) as httpd:
        osascript=which(cmd="osascript")
        if osascript is not None:
            import subprocess
            subprocess.run([osascript,"-e",f'open location "http://localhost:{PORT}"'],check=True)
        # Implement your Windows open website script here
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()

if __name__=="__main__":
    main()
