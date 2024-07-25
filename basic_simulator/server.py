from http.server import SimpleHTTPRequestHandler
import os.path
class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self,*args,directory=None,**kwargs):
        if directory is None:
            directory=os.path.join(
                os.path.dirname(__file__),
                "www"
            )
        super().__init__(*args,directory=directory,**kwargs)