import subprocess, json, sys
import tkinter as tk

try:
    layout = json.load(open(sys.argv[1]))
except:
    print('no layout file supplied', file=sys.stderr)
    exit()

buttons = {}

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master,
                          width=layout['width'],
                          height=layout['height'])
        self['bg'] = '#1D1F21'
        self.pack()
        self.create_widgets()
        proc = subprocess.Popen(['xinput', 'test-xi2', '--root'],
                        stdout=subprocess.PIPE)

        inkeypressevent = False
        inkeyrelevent = False

        while True:
            line = proc.stdout.readline()
            if line != '':
                if line == b'EVENT type 2 (KeyPress)\n':
                    inkeypressevent = True
                elif line == b'EVENT type 3 (KeyRelease)\n':
                    inkeyrelevent = True
                elif line.startswith(b'    detail:'):
                    if inkeypressevent or inkeyrelevent:
                        code = int(line.split()[1])
                        try:
                            if inkeypressevent == True:
                                buttons[code]['bg'] = '#198844'
                            elif inkeyrelevent == True:
                                buttons[code]['bg'] = '#969896'
                        except KeyError:
                            pass
                    inkeypressevent = False
                    inkeyrelevent = False
            self.update()


    def create_widgets(self):
        timesran = 0
        for button in layout['buttons']:
            btn = tk.Label(text=button['text'])
            btn.place(width=button['width'], height=button['height'],
                      x=button['x'], y=button['y'])
            btn['bg'] = '#969896'
            btn['font'] = (None, 12)
            buttons[button['keycode']] = btn
            timesran += 1
        self.winfo_toplevel().title("Keyboard inputs")


root = tk.Tk()
app = Application(master=root)
