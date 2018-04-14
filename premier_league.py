import tkinter as tk                
from tkinter import font  as tkfont 
import json
import api
import webbrowser
from PIL import Image, ImageTk


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        

        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.attributes('-fullscreen', True)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageThree_1, PageThree_2, PageThree_3):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("StartPage")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller

        label1 = tk.Label(self, bg="lightgrey", text="Premier League Database", relief='ridge', borderwidth=5, font=controller.title_font)
        label1.pack(side="top", fill="x", ipady=1)
        
        labelMenu = tk.Label(self, bg='lightgrey', height=5, width=100)
        logoFrame = tk.Frame(labelMenu, bg='lightgrey', relief='ridge', borderwidth=5)
        
        image = Image.open("premier-league.png")
        photo = ImageTk.PhotoImage(image)
        
        label = tk.Label(logoFrame, image=photo)
        label.image = photo # keep a reference!
        label.pack(fill='both', expand=True)
        
        
        logoFrame.pack(side="left", fill="both", expand=True)       
        
        btnFrame = tk.Frame(labelMenu, bg="grey", relief='ridge', borderwidth=5)
        button1 = tk.Button(btnFrame, text="Update Result", height=5, width=20, relief='ridge', borderwidth=5,
                            command=api.call_func)
        button2 = tk.Button(btnFrame, text="Player Statistics", height=5, width=20, relief='ridge', borderwidth=5,
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(btnFrame, text="View Table", height=5, width=20, relief='ridge', borderwidth=5,
                            command=lambda: controller.show_frame("PageThree"))
        button4 = tk.Button(btnFrame, text="Exit", height=5, width=20, relief='ridge', borderwidth=5,
                            command=lambda: controller.destroy())
        button1.grid(row=0, column=0,  padx=10, pady=20)
        button2.grid(row=2, column=0,  padx=10, pady=20)
        button3.grid(row=3, column=0,  padx=10, pady=20)
        button4.grid(row=4, column=0,  padx=10, pady=20)
        btnFrame.pack(side="right", fill="y", padx=1, pady=1)
        labelMenu.pack(fill="both", expand=True)
        


class PageOne(tk.Frame): #ADD RESULT

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,bg="lightgrey", text="Add Results", relief='ridge', borderwidth=5, font=controller.title_font)
        label.pack(side="top", fill="x")
        
        labelMenu = tk.Label(self, bg="lightgrey")
        frameBtn = tk.Frame(labelMenu, bg="grey", relief='ridge', borderwidth=5,)
        
        button = tk.Button(frameBtn, text="Back to Menu", height=5, width=20, relief='ridge', borderwidth=5,
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, padx=10, pady=20)
        
        button = tk.Button(frameBtn, text="Update Table", height=5, width=20, relief='ridge', borderwidth=5,
                           command=None)
        button.grid(row=1, column=0, padx=10, pady=20)
        
              
        frameBtn.pack(side="right", fill="y")

        frameDisplay = tk.Label(labelMenu, bg="lightcyan")
        addResult = ["Winning Team","Losing Team","Goal WT","Goal LT",
                     "GConceded WT","GConceded LT","RCard WT","RCard LT",
                     "YCard WT",'YCard LT','Goals Scorer WT','Goal Scorer LT']
        for i in range(12):
            #tk.Label(frameDisplay, text=addResult[i], width=11, height=2, relief='ridge', borderwidth=3).grid(row=0, column=i, ipadx=1, ipady=1, padx=1, pady=1)
            for _ in range(20):
                tk.Label(frameDisplay, text=addResult[i], width=10, height=1,relief='ridge', borderwidth=3).grid(row=_, column=i, ipadx=2, ipady=2, padx=2, pady=2)
        frameDisplay.pack(fill='both', expand=True)
        labelMenu.pack(expand=True, fill="both")


class PageTwo(tk.Frame): #PLAYER STATISTIC

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='lightgrey')
        self.controller = controller
        label = tk.Label(self, text="Player Statistic", bg="lightgrey", relief="ridge", borderwidth=5,
                         font=controller.title_font)
        label.pack(side="top", fill="x")
        
        mainLabel = tk.Label(self, bg="black")
        with open("api/player_statistic.json", "r") as file:
            data = json.load(file)
       
        scrollLabel = tk.Label(mainLabel, bg="lightgrey", width=0, relief="ridge", borderwidth=5)
        
        s = tk.Scrollbar(scrollLabel)
        c = tk.Canvas(scrollLabel, yscrollcommand=s.set, width=100)
        s.config(command=c.yview)
        s.pack(side='right', fill='y')
        f = tk.Frame(c)
        c.pack(side='left', fill='both', expand=True)
        c.create_window(0,0, window=f, anchor='nw')
        # put your code here
        l = tk.Label(f, text='Rank', bg='grey', fg='white', width=18, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=0, ipadx=5, padx=1, pady=5)
        l = tk.Label(f, text='Player', bg='grey', fg='white', width=30, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=1, ipadx=5, padx=1, pady=5)
        l = tk.Label(f, text='Team', bg='grey', fg='white', width=30, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=2, ipadx=5, padx=1, pady=5)
        l = tk.Label(f, text='GPlayed', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=3, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='GScored', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=4, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='Mins Played', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=5, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='Goals', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=6, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='Assist', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=7, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='Shots', bg='grey', fg='white', font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=8, ipadx=10, padx=1, pady=5)
        l = tk.Label(f, text='Shots on Goal', bg='grey', fg='white', width=15, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=9, ipadx=10, padx=1, pady=5)
       
        
        
        
        for i in range(len(data)):
            
            z = tk.Label(f, text=data['rank_'+str(i+1)]['rank'], font=("Courier", 9))
            z.grid(row=i+1, column=0, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['name'],  font=("Courier", 9))
            z.grid(row=i+1, column=1, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['team'], font=("Courier", 9))
            z.grid(row=i+1, column=2, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['gp'], font=("Courier", 9))
            z.grid(row=i+1, column=3, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['gs'],  font=("Courier", 9))
            z.grid(row=i+1, column=4, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['mins'],  font=("Courier", 9))
            z.grid(row=i+1, column=5, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['g'],  font=("Courier", 9))
            z.grid(row=i+1, column=6, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['asst'],  font=("Courier", 9))
            z.grid(row=i+1, column=7, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['shots'],  font=("Courier", 9))
            z.grid(row=i+1, column=8, padx=5, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['sog'],  font=("Courier", 9))
            z.grid(row=i+1, column=9, padx=5, pady=5)
        #-------------#
        
        self.update()
        c.config(scrollregion=c.bbox('all'))
        scrollLabel.pack(side='right', fill="both", expand=True)
       
        mainLabel.pack(fill="both", expand=True)
        
        bottomLabel = tk.Label(self, bg="lightgrey", relief="ridge", borderwidth=5)
        seperator = tk.Label(bottomLabel, width=70, bg="lightgrey")
        seperator.grid(row=0, column=0)
        entry = tk.Entry(bottomLabel)
        entry.grid(row=0, column=1)
        submit = tk.Button(bottomLabel, text="Search Player", command=lambda : webbrowser.open_new("https://www.whoscored.com/Search/?t="+entry.get()))
        submit.grid(row=0, column=2)
        seperator = tk.Label(bottomLabel, width=50, bg="lightgrey")
        seperator.grid(row=0, column=3)
        button3 = tk.Button(bottomLabel, text="Back to Menu", width=20, height=5, relief='ridge', borderwidth=3,
                           command=lambda: controller.show_frame("StartPage"))
        button3.grid(row=0, column=4)
        bottomLabel.pack(side="right", fill="both", expand=True)

class PageThree(tk.Frame): #VIEW TABLE

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self,bg="lightgrey", text="Current Premier League", relief='ridge', borderwidth=5, font=controller.title_font)
        label.pack(side="top", fill="x")
        
        labelMenu = tk.Label(self, bg="black")
        frameBtn = tk.Frame(labelMenu, bg="lightgrey", relief="ridge", borderwidth=2)
        
        button = tk.Button(frameBtn, text="Back to Menu", height=5, width=20, relief="ridge", borderwidth=5,
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, padx=10, pady=20)
        button = tk.Button(frameBtn, text="Goal Difference Table", height=5, width=20, relief="ridge", borderwidth=5,
                           command=lambda: controller.show_frame("PageThree_1"))
        button.grid(row=1, column=0, padx=10, pady=20)
        button = tk.Button(frameBtn, text="View Red and Yellow Cards", height=5, width=20, relief="ridge", borderwidth=5,
                           command=lambda: controller.show_frame("PageThree_2"))
        button.grid(row=2, column=0, padx=10, pady=20)
        button = tk.Button(frameBtn, text="Team Fouls Table", height=5, width=20, relief="ridge", borderwidth=5,
                           command=lambda: controller.show_frame("PageThree_3"))
        button.grid(row=3, column=0, padx=10, pady=20)
        frameBtn.pack(side="right", fill="y")

        frameDisplay = tk.Frame(labelMenu, bg="white",  relief='ridge', borderwidth=3)
        # Display of current premier league table stored
        with open('api/premier_matches.json', 'r') as load_file:
            data = json.load(load_file)
        
        
        scrollLabel = tk.Label(frameDisplay, bg="lightgrey", width=0, relief="ridge", borderwidth=5)
        
        s = tk.Scrollbar(scrollLabel)
        c = tk.Canvas(scrollLabel, yscrollcommand=s.set, width=100)
        s.config(command=c.yview)
        s.pack(side='right', fill='y')
        f = tk.Frame(c)
        c.pack(side='left', fill='both', expand=True)
        c.create_window(0,0, window=f, anchor='nw')
        # put your code here
        l = tk.Label(f, text='Date', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=0, padx=5, pady=5)
        l = tk.Label(f, text='Team A', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=1, padx=5, pady=5)
        l = tk.Label(f, text='Score Team A', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=2, padx=5, pady=5)
        l = tk.Label(f, text='Score Team B', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=3, padx=5, pady=5)
        l = tk.Label(f, text='Team B', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=4, padx=5, pady=5)
        for i in range(len(data)):
            z = tk.Label(f, text=data['key_'+str(i)]['date'], width=15, font=("Courier", 12))
            z.grid(row=i+1, column=0, padx=5, pady=5)
            z = tk.Label(f, text=data['key_'+str(i)]['team_a'],  font=("Courier", 10))
            z.grid(row=i+1, column=1, padx=5, pady=5)
            z = tk.Label(f, text=data['key_'+str(i)]['score_a'], width=15, font=("Courier", 15))
            z.grid(row=i+1, column=2, padx=5, pady=5)
            z = tk.Label(f, text=data['key_'+str(i)]['score_b'], width=15, font=("Courier", 15))
            z.grid(row=i+1, column=3, padx=5, pady=5)
            z = tk.Label(f, text=data['key_'+str(i)]['team_b'],  font=("Courier", 10))
            z.grid(row=i+1, column=4, padx=5, pady=5)
        #-------------#
        self.update()
        c.config(scrollregion=c.bbox('all'))
        scrollLabel.pack(side='right', fill="both", expand=True)
        
        frameDisplay.pack(side="left", fill='both', expand=True)
        labelMenu.pack(expand=True, fill="both")

class PageThree_1(tk.Frame): #Goal Differences

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='lightgrey')
        self.controller = controller
        label = tk.Label(self, text="Goal Differences", bg="lightgrey", relief="ridge", borderwidth=5,
                         font=controller.title_font)
        label.pack(side="top", fill="x")
        
        mainLabel = tk.Label(self, bg="black")
        playerData = tk.Label(mainLabel, bg='lightcyan', relief='ridge', borderwidth=5)
        with open('api/goals_deff_dics.json', 'r') as load_file: 
            data = json.load(load_file)

        scrollLabel = tk.Label(playerData, bg="lightgrey", width=0, relief="ridge", borderwidth=5)
        
        
        
        s = tk.Scrollbar(scrollLabel)
        c = tk.Canvas(scrollLabel, yscrollcommand=s.set, width=100)
        s.config(command=c.yview)
        s.pack(side='right', fill='y')
        f = tk.Frame(c)
        c.pack(side='left', fill='both', expand=True)
        c.create_window(0,0, window=f, anchor='nw')
        # put your code here
        l = tk.Label(f, text='Rank', bg='grey', fg='white', width=10, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=0, padx=1, pady=3)
        l = tk.Label(f, text='Team', bg='grey', fg='white', width=18, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=1, padx=1, pady=3)
        l = tk.Label(f, text='Matches Played', bg='grey', fg='white', width=18, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=2, padx=1, pady=3)
        l = tk.Label(f, text='Won', bg='grey', fg='white', width=10, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=3, padx=1, pady=3)
        l = tk.Label(f, text='Drawn', bg='grey', fg='white', width=10, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=4, padx=1, pady=3)
        l = tk.Label(f, text='Loss', bg='grey', fg='white', width=10, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=5, padx=1, pady=3)
        l = tk.Label(f, text='Goals For', bg='grey', fg='white', width=10, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=6, padx=1, pady=3)
        l = tk.Label(f, text='Goals Againts', bg='grey', fg='white', width=18, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=7, padx=1, pady=3)
        l = tk.Label(f, text='Goals Difference', bg='grey', fg='white', width=18, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=8, padx=1, pady=3)
        l = tk.Label(f, text='Points', bg='grey', fg='white', width=15, font=("Courier", 9), relief='ridge')
        l.grid(row=0, column=9, padx=1, pady=3)
        
        for i in range(20):
            z = tk.Label(f, text=data['rank_'+str(i+1)]['rank'], width=15, font=("Courier", 11))
            z.grid(row=i+1, column=0, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['team'],  font=("Courier", 11))
            z.grid(row=i+1, column=1, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['mp'], width=15, font=("Courier", 9))
            z.grid(row=i+1, column=2, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['won'], width=15, font=("Courier", 9))
            z.grid(row=i+1, column=3, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['drawn'],  font=("Courier", 9))
            z.grid(row=i+1, column=4, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['loss'],  font=("Courier", 9))
            z.grid(row=i+1, column=5, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['goals_for'],  font=("Courier", 9))
            z.grid(row=i+1, column=6, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['goals_againts'],  font=("Courier", 9))
            z.grid(row=i+1, column=7, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['goals_diff'],  font=("Courier", 9))
            z.grid(row=i+1, column=8, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['points'],  font=("Courier", 9))
            z.grid(row=i+1, column=9, padx=1, pady=5)
            

        #-------------#
        self.update()
        c.config(scrollregion=c.bbox('all'))
        scrollLabel.pack(side='right', fill="both", expand=True)


        
        playerData.pack(side="left", expand=True, fill="both")
        mainLabel.pack(fill="both", expand=True)
        
        bottomLabel = tk.Label(self, bg="lightgrey", relief="ridge", borderwidth=5)
        seperator = tk.Label(bottomLabel, width=70, bg="lightgrey")
        seperator.grid(row=0, column=0)      
        seperator = tk.Label(bottomLabel, width=50, bg="lightgrey")
        seperator.grid(row=0, column=3)
        button3 = tk.Button(bottomLabel, text="Back to Table  ", width=20, height=5, relief='ridge', borderwidth=3,
                           command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=0, column=4)
        bottomLabel.pack(side="right", fill="both", expand=True)
        
class PageThree_2(tk.Frame): #Red and Yellow Card Table

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='lightgrey')
        self.controller = controller
        label = tk.Label(self, text="Red and Yellow Card Table", bg="lightgrey", relief="ridge", borderwidth=5,
                         font=controller.title_font)
        label.pack(side="top", fill="x")
        
        mainLabel = tk.Label(self, bg="black")
        playerData = tk.Label(mainLabel, bg='lightcyan', relief='ridge', borderwidth=5)
        playerData.pack(side="left", expand=True, fill="both")
        #scrollBar = tk.Label(mainLabel, bg="lightgrey", width=50, relief="ridge", borderwidth=5)
        
        with open('api/cards.json','r') as file:
            data = json.load(file)
            
        scrollLabel = tk.Label(playerData, bg="lightgrey", width=0, relief="ridge", borderwidth=5)
        
        
        
        s = tk.Scrollbar(scrollLabel)
        c = tk.Canvas(scrollLabel, yscrollcommand=s.set, width=100)
        s.config(command=c.yview)
        s.pack(side='right', fill='y')
        f = tk.Frame(c)
        c.pack(side='left', fill='both', expand=True)
        c.create_window(0,0, window=f, anchor='nw')
        # put your code here
        l = tk.Label(f, text='Rank', bg='grey', fg='white', width=18, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=0, padx=10, pady=3)
        l = tk.Label(f, text='Team', bg='grey', fg='white', width=18, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=1, padx=10, pady=3)
        l = tk.Label(f, text='Yellow Cards', bg='grey', fg='white', width=18, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=2, padx=10, pady=3)
        l = tk.Label(f, text='Red Cards', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=3, padx=10, pady=3)
        l = tk.Label(f, text='Points', bg='grey', fg='white', width=15, font=("Courier", 15), relief='ridge')
        l.grid(row=0, column=4, padx=10, pady=3)
        
        
        for i in range(1,21):
            z = tk.Label(f, text=i, width=15, font=("Courier", 11))
            z.grid(row=i+1, column=0, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i)]['club'],  font=("Courier", 11))
            z.grid(row=i+1, column=1, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i)]['yc'], width=15, font=("Courier", 9))
            z.grid(row=i+1, column=2, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i)]['rc'], width=15, font=("Courier", 9))
            z.grid(row=i+1, column=3, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i)]['points'], width=15, font=("Courier", 9))
            z.grid(row=i+1, column=4, padx=1, pady=5)
           

        #-------------#
        self.update()
        c.config(scrollregion=c.bbox('all'))
        scrollLabel.pack(side='right', fill="both", expand=True)


        
        
        #scrollBar.pack(side='right', fill="y")
        mainLabel.pack(fill="both", expand=True)
        
        bottomLabel = tk.Label(self, bg="lightgrey", relief="ridge", borderwidth=5)
        seperator = tk.Label(bottomLabel, width=70, bg="lightgrey")
        seperator.grid(row=0, column=0)
        seperator = tk.Label(bottomLabel, width=50, bg="lightgrey")
        seperator.grid(row=0, column=3)
        button3 = tk.Button(bottomLabel, text="Back to Table  ", width=20, height=5, relief='ridge', borderwidth=3,
                           command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=0, column=4)
        bottomLabel.pack(side="right", fill="both", expand=True)
        
class PageThree_3(tk.Frame): #Team Foul

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='lightgrey')
        self.controller = controller
        label = tk.Label(self, text="Team Fouls   ", bg="lightgrey", relief="ridge", borderwidth=5,
                         font=controller.title_font)
        label.pack(side="top", fill="x")
        
        mainLabel = tk.Label(self, bg="black")
        playerData = tk.Label(mainLabel, bg='lightcyan', relief='ridge', borderwidth=5)
        
        with open("api/teamfoul.json",'r') as file:
            data = json.load(file)
        
        scrollLabel = tk.Label(playerData, bg="lightgrey", width=0, relief="ridge", borderwidth=5)
        
        
        
        s = tk.Scrollbar(scrollLabel)
        c = tk.Canvas(scrollLabel, yscrollcommand=s.set, width=100)
        s.config(command=c.yview)
        s.pack(side='right', fill='y')
        f = tk.Frame(c)
        c.pack(side='left', fill='both', expand=True)
        c.create_window(0,0, window=f, anchor='nw')
        # put your code here
        l = tk.Label(f, text='Rank', bg='grey', fg='white', width=10, height=1, font=("Courier", 9, "bold"), relief='ridge')
        l.grid(row=0, column=0, padx=0, pady=3)
        l = tk.Label(f, text='Player Name', bg='grey', fg='white', width=30, height=1, font=("Courier", 9, 'bold'), relief='ridge')
        l.grid(row=0, column=1, padx=1, pady=3)
        l = tk.Label(f, text='Team Name', bg='grey', fg='white', width=30, height=1, font=("Courier", 11, "bold"), relief='ridge')
        l.grid(row=0, column=2, padx=1, pady=3)
        l = tk.Label(f, text='Games Played', bg='grey', fg='white',  height=1, font=("Courier", 11, "bold"), relief='ridge')
        l.grid(row=0, column=3, padx=1, pady=3)
        l = tk.Label(f, text='Yellow Card', bg='grey', fg='white', height=1, font=("Courier", 11, "bold"), relief='ridge')
        l.grid(row=0, column=4, padx=1, pady=3)
        l = tk.Label(f, text='Red Card', bg='grey', fg='white', width=10, height=1, font=("Courier", 11, "bold"), relief='ridge')
        l.grid(row=0, column=5, padx=1, pady=3)
        l = tk.Label(f, text='Fouls Commited', bg='grey', fg='white', width=15, height=1, font=("Courier", 10, "bold"), relief='ridge')
        l.grid(row=0, column=6, padx=1, pady=3)
        
        
        
        for i in range(len(data)):
            z = tk.Label(f, text=data['rank_'+str(i+1)]['rank'], width=10, font=("Courier", 11))
            z.grid(row=i+1, column=0, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['name'], font=("Courier", 11))
            z.grid(row=i+1, column=1, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['team'], font=("Courier", 9))
            z.grid(row=i+1, column=2, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['gp'], width=10, font=("Courier", 9))
            z.grid(row=i+1, column=3, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['yc'],  font=("Courier", 9))
            z.grid(row=i+1, column=4, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['rc'],  font=("Courier", 9))
            z.grid(row=i+1, column=5, padx=1, pady=5)
            z = tk.Label(f, text=data['rank_'+str(i+1)]['fc'],  font=("Courier", 9))
            z.grid(row=i+1, column=6, padx=1, pady=5)
            
        #-------------#
        self.update()
        c.config(scrollregion=c.bbox('all'))
        scrollLabel.pack(side='right', fill="both", expand=True)        
        playerData.pack(side="left", expand=True, fill="both")
        
        mainLabel.pack(fill="both", expand=True)
        
        bottomLabel = tk.Label(self, bg="lightgrey", relief="ridge", borderwidth=5)
        seperator = tk.Label(bottomLabel, width=70, bg="lightgrey")
        seperator.grid(row=0, column=0)
        seperator = tk.Label(bottomLabel, width=50, bg="lightgrey")
        seperator.grid(row=0, column=3)
        button3 = tk.Button(bottomLabel, text="Back to Table  ", width=20, height=5, relief='ridge', borderwidth=3,
                           command=lambda: controller.show_frame("PageThree"))
        button3.grid(row=0, column=4)
        bottomLabel.pack(side="right", fill="both", expand=True)
        


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
