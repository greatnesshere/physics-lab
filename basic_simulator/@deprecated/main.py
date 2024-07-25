#!/usr/bin/env python
import subprocess,tkinter as tk,sys,os.path,asyncio

from functools import partial
from websockets.server import serve

from json import load
# Quick fix due to Python interpreter running in outer workspace
with open(os.path.join(os.path.dirname(__file__),"basic.json"),encoding="utf-8") as config:
    opt=load(config)
    WS_PORT=opt["TK_MAIN"]["WS_PORT"]
    SIG1=opt["TK_MAIN"]["SIG1"]

# 49152–65535	suggested by RFC 6335 and the Internet Assigned Numbers Authority (IANA) for dynamic or private ports.[2][3] FreeBSD has used the IANA port range since release 4.6. Windows Vista, Windows 7, and Server 2008 use the IANA range by default.[4]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("task mgr")
        self.child_procs=(
            subprocess.Popen([
                sys.executable,
                os.path.join(
                    os.path.dirname(__file__),
                    "render.py"
                )
            ]),
            subprocess.Popen([
                sys.executable,
                os.path.join(
                    os.path.dirname(__file__),
                    "serve.py"
                )
            ]),
        )
        self.stat_indicators=tuple(
            tk.Checkbutton(self,text=" ".join(map(os.path.basename,proc.args)),command=partial(self.ask_term_child,idx))
            for idx,proc in enumerate(self.child_procs)
        )
        for idx,wid in enumerate(self.stat_indicators):
            wid.grid(row=idx,sticky=tk.W)
            wid.select()
        self.protocol("WM_DELETE_WINDOW",self.exit)
        self.check_children()
    def check_children(self):
        self.update_idletasks()
        exited_processes=0
        for idx,proc in enumerate(self.child_procs):
            ret=proc.poll()
            if ret is not None:
                self.stat_indicators[idx].config(state=tk.DISABLED)
                self.stat_indicators[idx].deselect()
                self.stat_indicators[idx].config(text=" ".join(map(os.path.basename,proc.args))+f" (returned code {proc.returncode})")
                exited_processes+=1
        if exited_processes==len(self.child_procs):
            self.destroy()
        self.after(0,self.check_children)
    def exit(self):
        for proc in self.child_procs:
            proc.terminate()
        if self.winfo_exists():
            self.destroy()
    def ask_term_child(self,idx):
        self.stat_indicators[idx].config(state=tk.DISABLED)
        self.stat_indicators[idx].select()
        self.child_procs[idx].terminate()
