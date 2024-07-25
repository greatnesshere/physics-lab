import pygame,numpy as np
import asyncio
from websockets.server import serve
import os.path
import subprocess
from sys import executable

from json import load
with open(os.path.join(os.path.dirname(__file__),"basic.json"),encoding="utf-8") as config:
    opt=load(config)
    WS_URI=f"ws://localhost:{opt["TK_MAIN"]["WS_PORT"]}"
    WS_PORT=opt["RENDER_PROCESS"]["WS_PORT"]
    SIG1=opt["TK_MAIN"]["SIG1"]

class Point:
    def __init__(self,rad,pos,vel):
        self.rad=rad
        self.ppos=pos-vel
        self.pos=pos
    def update(self,dt):
        vel=self.pos-self.ppos
        self.pos+=vel*dt
        self.ppos=self.pos-vel
class System:
    def __init__(self,dimensions):
        self.width,self.height=dimensions
        self.nodes=[]
        self.links=[]
    def add(self,node):
        self.nodes.append(node)
    def update(self,dt):
        self.update_motion(dt)
    def update_motion(self,dt):
        # TODO: raycast each node
        for node in self.nodes:
            node.update(dt)
WIDTH,HEIGHT=1280,720
sys=System((WIDTH,HEIGHT))
PARTICLE_VELOCITY=.1
p=Point(10,np.array([0.,100.]),np.array([PARTICLE_VELOCITY,0.]))
sys.add(p)

async def handler(client):
    await client.send("Welcome!")
    async for msg in client:
        print(msg)

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
from time import time
clock=pygame.time.Clock()
running=True
dt=0

btn=pygame.font.SysFont(None,16).render("edit velocity...",True,"white","blue")
mouse_down_in_btn=False
edit_widget=None

async def openWidget():
    return subprocess.Popen([
        executable,
        os.path.join(
            os.path.dirname(__file__),
            "widget.py"
        )
    ])

async def render(wsd):
    global screen,clock,running,btn,mouse_down_in_btn,edit_widget,PARTICLE_VELOCITY
    current_time=0
    while running:
        last_time, current_time=current_time,time()
        dt=current_time-last_time
        screen.fill("black")
        for node in sys.nodes:
            pygame.draw.circle(screen,"white",node.pos,node.rad)
        rendered_btn=screen.blit(btn,(4,4))
        sys.update(dt)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==pygame.BUTTON_LEFT:
                pos=pygame.mouse.get_pos()
                if rendered_btn.collidepoint(pos):
                    mouse_down_in_btn=True
            elif event.type==pygame.MOUSEBUTTONUP and event.button==pygame.BUTTON_LEFT and mouse_down_in_btn:
                pos=pygame.mouse.get_pos()
                if rendered_btn.collidepoint(pos):
                    edit_widget=await openWidget()
                    mouse_down_in_btn=False
        if edit_widget is not None:
            print("got here")
            poll=edit_widget.poll()
            if poll is not None:
                try:
                    stdout,stderr=edit_widget.communicate(timeout=15)
                except TimeoutError:
                    edit_widget.kill()
                    stdout,stderr= edit_widget.communicate()
                PARTICLE_VELOCITY=int(stdout)
                p.ppos=p.pos-np.array([PARTICLE_VELOCITY,0.])
                edit_widget=None
        pygame.display.flip()
        # await asyncio.sleep(.1) # required to not block the event loop
        await asyncio.sleep(1 / 60 - (current_time - last_time))
    pygame.quit()
    wsd.close()

async def main():
    # async with websockets.client.connect(WS_URI) as client:
    async with serve(handler,"localhost",WS_PORT) as wsd:
        try:
            await asyncio.gather(wsd.serve_forever(),render(wsd))
        except asyncio.CancelledError:
            pass
if __name__=="__main__":
    asyncio.run(main())
