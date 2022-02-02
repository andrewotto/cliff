#UI
from tkinter import *
import tkinter

#sound
import winsound  #sorry everyone

#threading
import threading

#yeah
MAX_STEPS=16
BEATS_PER_MINUTE = 120
SECONDS_PER_MINUTE = 60
BEATS_PER_MEASURE = 4
STEPS_PER_MEASURE = 16

#FIXME add channel

#step
class Step:
    def __init__(self, id, button):
        self.id=id
        self.active=False 
        self.button=button
        self.button.grid(row=1, column=id)
        self.currentBackColor='#000000'

    def toggle(self):        
        if self.active:
            self.active=False
            self.currentBackColor='#000000'
        else:
            self.active=True
            self.currentBackColor='red'
                        
    #FIXME here we enumerate through our channels
    #and play each active channel's sound. rn beep
    def play(self):
        # print("calling play on " , self.id, " : ", self.active)
        if self.active:
            self.button.configure(background='red')
            self.playMe()
    def playMe(self):
        winsound.Beep(440,10) #FIXME duration should be BPM / minute, not 250
    def active():
        return self.active
    def highlight(self):
        self.button.configure(background='orange')
    def unhighlight(self):
        self.button.configure(background=self.currentBackColor)

#song
class Song:
    def __init__(self):
        self.steps=[]
        self.currentStep=0
    def toggle(self, stepIndex):
        print("In Song: Toggle: ", stepIndex)
        self.steps[stepIndex].toggle()
    def append(self, step):
        self.steps.append(step)
    def highlightActiveStep(self):
        for s in self.steps:
            s.unhighlight()
    def advance(self):
        self.highlightActiveStep()
        self.steps[self.currentStep].play()
        if self.currentStep + 1 == MAX_STEPS:
            self.currentStep=0
        else:
            self.currentStep = self.currentStep + 1
        self.steps[self.currentStep].highlight()
        
MainApp = tkinter.Tk()
MainApp.title('Cliff - A Sequencer')

#callback for clicking a step button
def select(value, song):
    song.toggle(value-1)
    
#scrap main
#make 16 step buttons at bottom of window

mySong=Song()
for n in range(1, MAX_STEPS+1):
    command = lambda x=n: select(x, mySong)
    mySong.append(Step(n, tkinter.Button(MainApp, text=str(n), width=5, bg="#000000", fg="#FFFFFF",
                   activebackground="#ff00ff", activeforeground="#00ff00", relief="raised", padx=12,
                   pady=4, bd=4, command=command)))

#how often to transition to a step
transition_sec=((BEATS_PER_MINUTE / SECONDS_PER_MINUTE) / (STEPS_PER_MEASURE))
print("Transition Sec: ", transition_sec)

def loopMe(song):    
    threading.Timer(transition_sec, loopMe, (song, )).start()
    song.advance()

loopMe(mySong)

#the tkinter main windows loop
MainApp.mainloop()