from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from synthlogic.algorithms.Synth import Synth
import threading
from PIL import Image, ImageTk

from synthlogic.gui.Section import Section
from synthlogic.gui.Slider2D import Slider2D
from synthlogic.gui.SliderGroup import SliderGroup

# === basic window configuration
master = Tk()
master.title("EARDRUM BLASTER")
master.resizable(width=False, height=False)
winWidth = 430
winHeight = 650
windowSize = str(winHeight)+'x'+str(winHeight)
master.geometry(windowSize)
# window spawn in center of screen
screenWidth = master.winfo_screenwidth()
screenHeight = master.winfo_screenheight()
startX = int((screenWidth/2) - (winWidth/2))
startY = int((screenHeight/2) - (winHeight/2))
master.geometry('{}x{}+{}+{}'.format(winWidth, winHeight, startX, startY))
# synthesizer
synth = Synth()


def updatePlot():
    global axis, canvas
    axis.cla()
    axis.set_xticks([], [])
    axis.set_yticks([], [])
    axis.spines['top'].set_visible(False)
    axis.spines['right'].set_visible(False)
    axis.spines['bottom'].set_visible(False)
    axis.spines['left'].set_visible(False)

    axis.plot(synth.x, synth.y)
    fig.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.9)

    canvas.draw()
    # every 10ms; raise, to improve performance
    master.after(1000, updatePlot)


def updateBtnText():
    #playBtn.configure(text=synth.status)
    pass

WIDTH_IMG = 50
WIDTH_RB = WIDTH_IMG
HEIGHT_RB = WIDTH_RB

FIRST = 0
SECOND = FIRST + 1
THIRD = SECOND + 1
FOURTH = THIRD + 1
FIFTH = FOURTH + 1
SIXTH = FIFTH + 1
SEVENTH = SIXTH + 1
EIGHTH = SEVENTH + 1

PAD_X = 10
PAD_Y = 10
PAD_X_W = 5
PAD_Y_W = 5

background_image = ImageTk.PhotoImage(file='../scratch.jpg')
#background_image = PhotoImage(file='../background#2.gif')
touchpad_bg = PhotoImage(file='../touchpad.gif')

#Photo by mohammad alizade on Unsplash
#Photo by Paweł Czerwiński on Unsplash
background_label = Label(image=background_image)
background_label.image = background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
master.configure(background='#CFB53B')

#LABELFRAME_BG = '#053E7E'
#LABELFRAME_BG = '#A60000'
LABELFRAME_BG = '#444'
LABELFRAME_FG = 'white'

# default selection
group = StringVar()
group.set(1)

sineIcon = PhotoImage(file="../icons_new/Sine.png")
triangleIcon = PhotoImage(file="../icons_new/Triangle.png")
sawtoothIcon = PhotoImage(file="../icons_new/Sawtooth.png")
squareIcon = PhotoImage(file="../icons_new/Square.png")

# === oscillator section
sectionOsc = Section(master, "OSCILLATOR", LABELFRAME_FG, LABELFRAME_BG)
sectionOsc.setPosition(FIRST, FIRST, 2, 1, PAD_X, PAD_Y)
oscillator = SliderGroup(sectionOsc.getSection())
oscillator.createIcons([sineIcon, triangleIcon, sawtoothIcon, squareIcon])
oscillator.createSlider([synth.valueSine, synth.valueTriangle, synth.valueSawtooth, synth.valueSquare])

# === style options
monoIcon = PhotoImage(file="../icons/mono.png")
duoIcon = PhotoImage(file="../icons/duo.png")
trioIcon = PhotoImage(file="../icons/trio.png")
quattroIcon = PhotoImage(file="../icons/quattro.png")

sectionStyle = Section(master, "STYLE", LABELFRAME_FG, LABELFRAME_BG)
sectionStyle.setPosition(THIRD, FIRST, 1, 1, PAD_X, (0, PAD_Y))
Radiobutton(sectionStyle.getSection(), variable=group, image=monoIcon, value=1, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(1)]).grid(row=FIRST,column=FIRST, padx=(6,0), pady=(PAD_Y_W, 0))
Radiobutton(sectionStyle.getSection(), variable=group, image=duoIcon, value=2, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(2)]).grid(row=FIRST,column=SECOND, padx=(5,0), pady=(PAD_Y_W, 0))
Radiobutton(sectionStyle.getSection(), variable=group, image=trioIcon, value=3, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(3)]).grid(row=FIRST,column=THIRD, padx=(5,0), pady=PAD_Y_W)
Radiobutton(sectionStyle.getSection(), variable=group, image=quattroIcon, value=4, indicatoron=0, width=WIDTH_IMG, height=HEIGHT_RB, command=lambda: [synth.setStyle(4)]).grid(row=FIRST,column=FOURTH, padx=(5,7), pady=PAD_Y_W)

# === frequency
#w = Scale(frameFreq, from_=0, to=1000, length=200, orient=HORIZONTAL, resolution=1, command=lambda x: [synth.setFrequency(x)]).grid(row=SECOND, column=FIRST, columnspan=3, sticky=E+W)
#playBtn = Button(frameFreq, text=synth.status, command=lambda: [synth.toggle(), updateBtnText()])
#playBtn.grid(row=THIRD, column=FIRST, columnspan=3, sticky=E+W, padx=PAD_X_W, pady=PAD_Y_W)

# === chunk section
sectionChunk = Section(master, "CHUNK", LABELFRAME_FG, LABELFRAME_BG)
sectionChunk.setPosition(FOURTH, FIRST, 1, 1, PAD_X, (0, PAD_Y))
fig = Figure(figsize=(2.6, 1), facecolor='#F0F0F0')
axis = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=sectionChunk.getSection())
canvas._tkcanvas.grid(row=FIRST, column=FIRST, sticky=E+W)
t = threading.Thread(target=updatePlot())
t.start()

# === touchpad section
sectionTouchpad = Section(master, "TOUCH ME", LABELFRAME_FG, LABELFRAME_BG)
sectionTouchpad.setPosition(FIFTH, FIRST, 2, 1, PAD_X, (0, PAD_Y))
slider2D = Slider2D(sectionTouchpad.getSection(), 260, 195, synth)

# === envelope section
sectionEnv = Section(master, "ENVELOPE", LABELFRAME_FG, LABELFRAME_BG)
sectionEnv.setPosition(FIRST, SECOND, 1, 1, (0, PAD_X), PAD_Y)
effects = SliderGroup(sectionEnv.getSection())
effects.createSlider([synth.valueAttack])
effects.createLabels(["Attack"])

# === filter section
sectionFilter = Section(master, "FILTER", LABELFRAME_FG, LABELFRAME_BG)
sectionFilter.setPosition(THIRD, SECOND, 2, 2, (0, PAD_X), 0)
effects = SliderGroup(sectionFilter.getSection())
effects.createSlider([synth.valueReverb, synth.valueCutoff])
effects.createLabels(["Reverb", "Cutoff"])

mainloop()
