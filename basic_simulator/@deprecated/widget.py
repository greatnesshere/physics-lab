import tkinter as tk
def submit():
    try:
        print(int(val.get()))
    except ValueError:
        return
    root.destroy()
root=tk.Tk()
root.title("edit velocity...")
val=tk.StringVar(root)
ent=tk.Entry(root,textvariable=val)
ent.pack()
sub=tk.Button(root,text="Submit",command=submit)
sub.pack()
root.mainloop()