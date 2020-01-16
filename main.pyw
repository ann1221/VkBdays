#-*- coding: utf-8 -*-
import Logic
import MainInfo
import MyErrors
import PIL.ImageTk as ImageTk
from PIL import Image as Image
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

class Application(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        root.bind_all("<Double-Button-1>", lambda e: self.ChangeAppZoomed())
        root.bind_all("<Button-3>", lambda e: self.ChangeAppLocat())
        root.bind_all("<Escape>", lambda e: self.ExitBtnPress())
        root.bind_all("<Key>", self._onKeyRelease, "+")
        
        self.isNormAppSize = True
        self.isCanChangeAppLocat = False
        
        self.CreateBasicVidgs()
        self.PlaceBasicVidgs()

        self.MainBdayInfoLab = None
        self.BdayTop25Labs = []

        self.UpdDataBtnPress()
        
    def CreateBasicVidgs(self):
        self.pad = Canvas(root, bg = "#081528" ) 
        self.bgImage = ImageTk.PhotoImage(file = MainInfo.PATHs['bgPicture'])
        padBgImage = self.pad.create_image( 0,0, image=self.bgImage)
        padBgImageProlongat = self.pad.create_image( 0,600, image=self.bgImage)
        self.littlePad = Frame(self.pad, bg = "#081528", highlightbackground = "white", highlightcolor = "white", highlightthickness = 1)
            
        self.changeUsrBtn = Button(self.pad, bg = "#081528", relief = GROOVE, font = 'courier 12', fg = "white", activebackground = "#081528",
                text = MainInfo.form['Buttons'][0], command = lambda: self.ChangeUsrBtnPress())             
        self.changeUsrBtn.bind("<Enter>", lambda e: self.ChangeUserBtnCover())
        self.changeUsrBtn.bind("<Leave>", lambda e: self.ChangeUserBtnUncover())
        
        self.updDataBtn = Button(self.pad, bg = "#081528", relief = GROOVE, font = 'courier 12', fg = "white", activebackground = "#081528",          
                text = MainInfo.form['Buttons'][1], command = lambda: self.UpdDataBtnPress(True))                   
        self.updDataBtn.bind("<Enter>", lambda e: self.updDataBtnCover())
        self.updDataBtn.bind("<Leave>", lambda e: self.updDataBtnUncover())
        
        self.exitBtn = Button(self.pad, bg = "#081528", relief = GROOVE, font = "courier 12", fg = "white", activebackground = "#081528", 
                text = MainInfo.form['Buttons'][2], command = lambda: self.ExitBtnPress())   
        self.exitBtn.bind("<Enter>", lambda e: self.exitBtnCover())
        self.exitBtn.bind("<Leave>", lambda e: self.exitBtnUncover())
        
        self.howBtn = Button(self.pad, bg = "#081528", relief = GROOVE, font = "courier 12", fg = "white", activebackground = "#081528", 
                text = MainInfo.form['Buttons'][3], command = lambda: self.ChangeTokenBtnPress())   
        self.howBtn.bind("<Enter>", lambda e: self.howBtnCover())
        self.howBtn.bind("<Leave>", lambda e: self.howBtnUncover())
        
        self.topLabel = Label(self.pad,font =  "courier 18", fg = '#d36e70', bg = '#081528', text = MainInfo.form['Labels']['top'])
        self.waitLabel = Label(self.littlePad, font = "courier 8", bg = "#081528", fg = "white", text = MainInfo.form['Labels']['wait'])
                        
    def PlaceBasicVidgs(self):
        self.pad.place(x=0, y=0, relwidth=1, relheight=1)
        self.littlePad.place(x=30, rely = 0.25, width = 280, relheight = 0.5 )
        
        self.changeUsrBtn.place(x = 45, rely = 0.21, width = 250, relheight = 0.04)
        self.updDataBtn.place(x = 45, rely = 0.75, width = 250, relheight = 0.04)
        self.exitBtn.place(x = 50, rely = 0.957, width = 200, relheight = 0.04)
        self.howBtn.place(x = 255, rely = 0.957, width = 25, relheight = 0.04)
        
        self.topLabel.place(x = 520, y = 40)
        self.waitLabel.place(relx = -1, rely = -1)
           
    def _onKeyRelease(self,event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")
        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")
        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>") 
        
    def ChangeAppZoomed(self):
        if self.isNormAppSize:
            root.state('zoomed')
        else:
            root.state('normal')
        self.isNormAppSize = not self.isNormAppSize

    def ChangeAppLocat(self):
        if self.isCanChangeAppLocat:
            root.overrideredirect(1)
            placement = "{0}+{1}".format(str(root.winfo_rootx()), str(root.winfo_rooty()))
            Logic.FileWorker.ChangePosition(placement)
        else:
            root.overrideredirect(0)
        self.isCanChangeAppLocat = not self.isCanChangeAppLocat

    def ChangeUserBtnCover(self):
        self.changeUsrBtn.config(bg = "white", fg="#081528")
    def ChangeUserBtnUncover(self):
        self.changeUsrBtn.config(bg = "#081528", fg = "white")
        
    def updDataBtnCover(self):
        self.updDataBtn.config(bg = "white", fg="#081528")
    def updDataBtnUncover(self):
        self.updDataBtn.config(bg = "#081528", fg = "white")
        
    def exitBtnCover(self):
        self.exitBtn.config(bg = "white", fg="#081528")
    def exitBtnUncover(self):
        self.exitBtn.config(bg = "#081528", fg = "white")
        
    def howBtnCover(self):
        self.howBtn.config(bg = "white", fg="#081528")
    def howBtnUncover(self):
        self.howBtn.config(bg = "#081528", fg = "white")
    
    def InputDataProcessing(self, dataType):
        answer =  simpledialog.askstring(MainInfo.form['Titles'][str(dataType)], MainInfo.form['Descript'][str(dataType)], parent=self.root)
        if answer is None:
            return
        if dataType == 'user':
            result = Logic.FileWorker.ChangeUser(answer)
        else:
            result = Logic.FileWorker.ChangeToken(answer)
        if MyErrors.Error.Search(result) is not None:
            messagebox.showinfo(MainInfo.form['Titles'][str(dataType)], result)  
        else:
            messagebox.showinfo(MainInfo.form['Titles'][str(dataType)],MainInfo.form['Info'][str(dataType)])
    
    def ChangeTokenBtnPress(self):
        self.InputDataProcessing('token')
        
    def ChangeUsrBtnPress(self):
        self.InputDataProcessing('user')
         
    def UpdDataBtnPress(self, isNeedToUpdate = False):
        self.waitLabel.place(relx = 0, rely = 0)
        self.DestrClientVidgs()
        
        userID = Logic.FileWorker.GetUser()
        if MyErrors.Error.Search(userID) is not None:
            messagebox.showinfo(MainInfo.form['Titles']['user'], userID)
            self.waitLabel.place(relx = -1, rely = -1)
            return             
        token = Logic.FileWorker.GetToken()
        if MyErrors.Error.Search(token) is not None:
            messagebox.showinfo(MainInfo.form['Titles']['token'],token)
            self.waitLabel.place(relx = -1, rely = -1)
            return
            
        user = Logic.VkClient(userID, token)
        if isNeedToUpdate:
            frList = user.UpdateFriendsList()
        else:
            frList = user.GetFriendsList()
            
        if MyErrors.Error.Search(frList) is not None:
            messagebox.showinfo(MainInfo.form['Titles']['list'],  MyErrors.Error.Translate(frList))
            self.waitLabel.place(relx = -1, rely = -1)
            return

        self.CreateClientVidgs(user)
        self.waitLabel.place(relx = -1, rely = -1)
           
    def DestrClientVidgs(self): 
        if self.MainBdayInfoLab is not None:
            self.MainBdayInfoLab.destroy()
        for i in range(len(self.BdayTop25Labs)):
            self.BdayTop25Labs[i].destroy()
        self.BdayTop25Labs.clear() 
        root.update() 
        
    def CreateClientVidgs(self, user):
        self.MainBdayInfoLab = Label(self.littlePad, font = "courier 18", bg = "#081528", fg = "#d36e70", text = user.GetSoonestBdayFriend())
        self.MainBdayInfoLab.place(relx = 0.5, rely = 0.5, anchor=CENTER)
        top = user.GetTopSoonestBday()
        for i in range(len(top)):
            self.BdayTop25Labs.append(Label(self.pad, font = "courier 12", bg = "#081528", fg = "white", text = top[i]))
            self.BdayTop25Labs[i].place(x = 450, y = i * 20 + 90 ) 
    
    def ExitBtnPress(self):
        sys.exit()

if __name__ == '__main__':             
    root = Tk()
    root.title(MainInfo.form['Titles']['main'])
    try:
        root.geometry(MainInfo.form['Size'].format(Logic.FileWorker.GetPosition()))
    except:
        print(MyErrors.Error.message['File'])
        root.geometry(MainInfo.form['Size'].format('0+0'))
    try:
        root.iconbitmap(MainInfo.PATHs['icon'])
    except:
        print(MyErrors.Error.message['Icon'])
    root.overrideredirect(1)
    app = Application(root)
    root.mainloop()

