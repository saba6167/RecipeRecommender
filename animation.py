import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

def load_frames(path):
    frames = []
    with Image.open(path) as img:
        for frame in ImageSequence.Iterator(img):
            frames.append(ImageTk.PhotoImage(frame))
    return frames

def play(frames, label, idx=0, delay=100):
    label.config(image=frames[idx])
    idx = (idx + 1) % len(frames)
    label.after(delay, play, frames, label, idx)

# def stop(label):
#     label.after_cancel(label.cancel)

root = tk.Tk()
frames = load_frames('animation.gif')
label = tk.Label(root)
label.pack()
label.cancel = label.after(0, play, frames, label)
root.mainloop()
