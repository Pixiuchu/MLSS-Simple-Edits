import os
import io
import tkinter as Tk
from tkinter import ttk
from tkinter import filedialog
import math
import shutil
import csv
import random

colors = [
    "Red",
    "Green",
    "Blue",
    "Yellow",
    "Orange",
    "Pink",
    "Purple",
    "Azure",
    "Black",
    "White",
    "Silhouette",
    "Random"
    #"Chaos",
    #"TrueChaos"
]

cpants = [
    "Vanilla",
    "Red",
    "Green",
    "Blue",
    "Yellow",
    "Orange",
    "Pink",
    "Purple",
    "Azure",
    "Black",
    "White",
    "Random"
    #"Chaos"
]

mainWindow = Tk.Tk()
mainWindow.title("MLSS Color Patcher")
mainWindow.resizable(False, False)
mainWindow.iconbitmap()

if not os.path.exists("Output"):
    os.makedirs("Output")
    print("Creating \"Output\" folder...")

if os.path.exists("Temporary MLSS Modified Colors.gba"):
    os.remove("Temporary MLSS Modified Colors.gba")

def hide_me(widget):
    widget.pack_forget()

def show_me(widget):
    widget.pack(fill="both", expand=True, padx=10, pady=10)


def askfile():
    romfilename = filedialog.askopenfilename(filetypes=[("GBA ROM", ".gba")])
    if romfilename == "":
        print("No file loaded, exiting program...\n")
        exit(1)
    else:
        with open(romfilename, mode="rb") as f:
            filesize = os.stat(romfilename).st_size
            print(filesize)
            if filesize != 16777216:
                print("Not a MLSS ROM! (Wrong filesize)")
                exit(1)
            f.seek(0xA0)
            gamename = f.read(0xD)
            print(gamename)
            if gamename != b'MARIO&LUIGIUA':
                print("Not a MLSS ROM!")
                exit(1)
        hide_me(frameMain)
        show_me(frameSettings)
        shutil.copyfile(romfilename, "output/MLSS Modified Colors.gba")


def patchall():
    with open("output/MLSS Modified Colors.gba", mode="r+b") as f:
        def patchColor(bro, part, mainwidget):
            BroColor = mainwidget.get()
            if BroColor == "Random" and part == "colors":
                while BroColor == "Random" or BroColor == "Silhouette":
                    BroColor = random.choice(colors)
            elif BroColor == "Random" and part == "pants":
                while BroColor == "Random":
                    BroColor = random.choice(cpants)

            print(bro)
            print(part)
            print(BroColor)
            colorimport = getattr(__import__("%s.%s" % (part, BroColor), fromlist=[BroColor]), BroColor)
            print(colorimport[0][0])
            size = len(colorimport[:])
            x = 0
            while x < size:
                colormhat = colorimport[x]
                if bro == "Mario" and colormhat[3] == 1:
                    x += 1
                    continue
                if bro == "Luigi" and colormhat[3] == 0:
                    x += 1
                    continue
                f.seek(colormhat[0])
                newvalue_bytes = int(colormhat[1]).to_bytes(1)
                f.write(newvalue_bytes)
                newvalue_bytesb = int(colormhat[2]).to_bytes(1)
                f.write(newvalue_bytesb)
                x += 1

        patchColor("Mario", "pants", comboMarioPantsColor)
        patchColor("Luigi", "pants", comboLuigiPantsColor)
        patchColor("Mario", "colors", comboMarioHatColor)
        patchColor("Luigi", "colors", comboLuigiHatColor)

        RandomizeMusicOption = ckboxMusicRandomizeVar.get()
        DisableMusicOption = ckboxDisableMusicVar.get()

        if RandomizeMusicOption == 1:
            songs = []
            f.seek(0x21CB74)
            for _ in range(50):
                if f.tell() == 0x21CBD8:
                    f.seek(4, 1)
                    continue
                temp = f.read(4)
                songs.append(temp)

            random.shuffle(songs)
            f.seek(0x21CB74)
            for _ in range(50):
                if f.tell() == 0x21CBD8:
                    f.seek(4, 1)
                    continue
                f.write(songs.pop())

        if DisableMusicOption == 1:
            f.seek(0x19B118)
            f.write(bytes([0x0, 0x25]))



frameMain = Tk.Frame(mainWindow)
frameMain.pack(padx=10, pady=10)
button = Tk.Button(frameMain, text="Load MLSS USA ROM", width=30, height=6, command=askfile)
button.grid(row=0, column=0)

frameSettings = Tk.Frame(mainWindow)

comboMarioHatLabel = Tk.Label(frameSettings, text="Mario Hat")
comboMarioHatLabel.grid(row=0, column=0, sticky=Tk.W, pady=(3,3))
comboMarioHatColor = ttk.Combobox(frameSettings, state="readonly", values=colors, width=10)
comboMarioHatColor.current(0)
comboMarioHatColor.place(x=70, y=3)

comboMarioPantsLabel = Tk.Label(frameSettings, text="Mario Pants")
comboMarioPantsLabel.grid(row=1, column=0, sticky=Tk.W, pady=(3,3))
comboMarioPantsColor = ttk.Combobox(frameSettings, state="readonly", values=cpants, width=10)
comboMarioPantsColor.current(0)
comboMarioPantsColor.place(x=70, y=30)

comboLuigiHatLabel = Tk.Label(frameSettings, text="Luigi Hat")
comboLuigiHatLabel.place(x=173, y=3)
comboLuigiHatColor = ttk.Combobox(frameSettings, state="readonly", values=colors, width=10)
comboLuigiHatColor.current(1)
comboLuigiHatColor.place(x=240, y=3)

comboLuigiPantsLabel = Tk.Label(frameSettings, text="Luigi Pants")
comboLuigiPantsLabel.place(x=173, y=30)
comboLuigiPantsColor = ttk.Combobox(frameSettings, state="readonly", values=cpants, width=10)
comboLuigiPantsColor.current(0)
comboLuigiPantsColor.place(x=240, y=30)

ckboxMusicRandomizeVar = Tk.IntVar()
ckboxMusicRandomize = Tk.Checkbutton(frameSettings, text="Randomize Music?", variable=ckboxMusicRandomizeVar)
ckboxMusicRandomize.grid(row=2, column=0, sticky=Tk.W, pady=3)

ckboxDisableMusicVar = Tk.IntVar()
ckboxDisableMusic = Tk.Checkbutton(frameSettings, text="Disable Music?", variable=ckboxDisableMusicVar)
ckboxDisableMusic.grid(row=3, column=0, sticky=Tk.W, pady=3)
btnPatchAll = Tk.Button(frameSettings, text="Patch Mario & Luigi: Superstar Saga", width=50, height=6, command=patchall)
btnPatchAll.grid(row=6, column=0, pady=(37,0))

# ckGiantBossDrops
# ck

mainWindow.mainloop()