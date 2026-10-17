import tkinter as tk
def show_window():
    root = tk.Tk()
    root.geometry("300x100")
    root.resizable(False, False)
    root.title("controls for niko hat factory")

    text = tk.Label(root,
                    text="WASD to move the camera\n1 to spawn a belt\n2 to spawn a collector\n3 to spawn a niko hatgenerator\nE and Q to rotate objects\nany mouse button to delete an object")
    text.pack()

    root.mainloop()