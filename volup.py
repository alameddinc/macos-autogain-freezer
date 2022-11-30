import threading
import time
import tkinter

import applescript


class VolUP:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.closing = False
        self.tk.title("Microphone Input Volume Stabilizer")
        self.tk.resizable(False, False)
        self.tk.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.volume = 100
        self.is_active = False
        self.loop = threading.Thread(target=self.loop_volume)
        self.loop.start()
        self.volume_label = tkinter.Label(self.tk, text="Volume: 100")
        self.volume_label.grid(row=0, column=0, columnspan=2)
        self.volume_up_button = tkinter.Button(self.tk, text="Volume Up", command=self.volume_up)
        self.volume_up_button.grid(row=1, column=0)
        self.volume_up_25_button = tkinter.Button(self.tk, text="Volume Up 25", command=self.volume_up_25)
        self.volume_up_25_button.grid(row=2, column=0)
        self.volume_down_button = tkinter.Button(self.tk, text="Volume Down", command=self.volume_down)
        self.volume_down_button.grid(row=1, column=1)
        self.volume_down_25_button = tkinter.Button(self.tk, text="Volume Down 25", command=self.volume_down_25)
        self.volume_down_25_button.grid(row=2, column=1)
        self.is_active_button = tkinter.Button(self.tk, text="Start", command=self.activation_toggle)
        self.is_active_button.grid(row=3, column=0, columnspan=2)
        self.tk.mainloop()
    def volume_up(self):
        self.volume += 1
        self.volume_validations()
        self.set_volume()
        self.volume_label.config(text="Volume: " + str(self.volume))
    def volume_down(self):
        self.volume -= 1
        self.volume_validations()
        self.set_volume()
        self.volume_label.config(text="Volume: " + str(self.volume))
    def volume_up_25(self):
        self.volume += 25
        self.volume_validations()
        self.set_volume()
        self.volume_label.config(text="Volume: " + str(self.volume))
    def volume_down_25(self):
        self.volume -= 25
        self.volume_validations()
        self.set_volume()
        self.volume_label.config(text="Volume: " + str(self.volume))
    def volume_validations(self):
        if self.volume <= 0:
            self.volume = 0
            self.volume_down_button.config(state="disabled")
            self.volume_down_25_button.config(state="disabled")
        elif self.volume_up_button["state"] == "disabled":
            self.volume_up_button.config(state="normal")
            self.volume_up_25_button.config(state="normal")

        if self.volume >= 100:
            self.volume = 100
            self.volume_up_button.config(state="disabled")
            self.volume_up_25_button.config(state="disabled")
        elif self.volume_down_button["state"] == "disabled":
            self.volume_down_button.config(state="normal")
            self.volume_down_25_button.config(state="normal")
    def loop_volume(self):
        while True:
            if self.closing:
                break
            if self.is_active:
                applescript.run("set volume input volume " + str(self.volume))
            time.sleep(2.5)
    def on_closing(self):
        self.closing = True
        self.tk.destroy()
    def activation_toggle(self):
        if self.is_active == True:
            self.is_active = False
            self.is_active_button.config(text="Start")
        else:
            self.is_active = True
            self.is_active_button.config(text="Stop")
    def set_volume(self):
        applescript.run("set volume input volume " + str(self.volume))
        pass
