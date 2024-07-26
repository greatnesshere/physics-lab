from http.server import ThreadingHTTPServer
from server import MyHTTPRequestHandler
from threading import Thread
from queue import Queue
from websockets.sync.server import serve
from json import loads,dumps

from matter import *
import pygame
from sys import argv
# import argparse
# parser=argparse.ArgumentParser()
# parser.add_argument(

WS_PORT,HTTP_PORT=8032,8080

data=Queue()

def serve_web():
    httpd=ThreadingHTTPServer(('',HTTP_PORT),MyHTTPRequestHandler)
    def serve_forever(httpd):
        if '--open' in argv:
            import webbrowser
            webbrowser.open(f"localhost:{HTTP_PORT}")
        httpd.serve_forever()
    Thread(target=serve_forever,args=(httpd,)).start()
    return httpd

CLIENTS=set()

def serve_ws():
    def handler(connection):
        CLIENTS.add(connection)
        connection.send(dumps({
            "type":"measure_velocity",
            "value":PARTICLE_VELOCITY
        }))
        for msg in connection:
            payload=loads(msg)
            if payload['type']=='push':
                p.ppos[0]=p.pos[0]-payload['value']
    server=serve(handler,'',WS_PORT)
    def serve_forever(server):
        server.serve_forever()
    Thread(target=serve_forever,args=(server,)).start()
    return server

WIDTH,HEIGHT=1280,720
PARTICLE_VELOCITY=1.
p=Node(
    # A one-dimensional node would have no radius
    10,
    np.array([0.,100.]),
    np.array([PARTICLE_VELOCITY,0.])
)
sys=System()
sys.add(p)
def main():
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()
    running=True
    dt=0
    time=0
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        screen.fill("black")
        for node in sys.nodes:
            pygame.draw.circle(screen,"white",node.pos,node.rad)
        data.put_nowait({
            "type":"data",
            "value":{
                "time":time,
                "x":p.pos[0],
                "accel":0, # TODO: change in velocity
                "vel":(p.pos-p.ppos)[0]
            }
        })
        sys.update(dt)
        pygame.display.flip()
        dt=clock.tick(60)/1000
        time+=dt
    pygame.quit()
httpd=serve_web()
ws=serve_ws()
main()
# May have to close browser tab first FIXME
httpd.server_close()
httpd.shutdown()

ws.shutdown()
