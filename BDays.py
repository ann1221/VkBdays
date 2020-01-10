#-*- coding: utf-8 -*-
import VkFriends
import AppInfo
import PIL.ImageTk as ImageTk
from PIL import Image as Image
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
import os

class Application(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        
        self.isNormAppSize = True
        self.isCanChangeAppLocat = False
        root.bind_all("<Double-Button-1>", lambda e: self.ChangeAppZoomed())
        root.bind_all("<Button-3>", lambda e: self.ChangeAppLocat())
        root.bind_all("<Escape>", lambda e: self.Exit())
        
        root.bind_all("<Key>", self._onKeyRelease, "+")
        
        self.CreateBasicVidgs()
        self.PlaceBasicVidgs()

        self.BdayInfoLab = None
        self.BdayTop25Labs = []

        self.LoadDATAFile()
    
    def _onKeyRelease(self,event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")    

    def CreateBasicVidgs(self):
        self.pad = Canvas(root, bg = "#081528" )
        self.bgImage = ImageTk.PhotoImage(file = AppInfo.PATHs['bgPicture'])
        padBgImage = self.pad.create_image( 0,0, image=self.bgImage)
        padBgImageProlongat = self.pad.create_image( 0,600, image=self.bgImage)

        self.littlePad = Frame(self.pad, bg = "#081528", highlightbackground = "white", 
                                highlightcolor = "white", highlightthickness = 1)
            
        self.changeUsrBtn = Button(self.pad, bg = "#081528", text = AppInfo.text['btnName'][0],
                    relief = GROOVE, font = 'courier 12', fg = "white", activebackground = "#081528",
                    command = lambda: self.ChangeUsrBtnPressed())
        self.changeUsrBtn.bind("<Enter>", lambda e: self.ChangeUserBtnCover())
        self.changeUsrBtn.bind("<Leave>", lambda e: self.ChangeUserBtnUncover())
        
        self.updDataBtn = Button(self.pad, bg = "#081528", text = AppInfo.text['btnName'][1],
                        relief = GROOVE, font = 'courier 12', fg = "white", activebackground = "#081528", 
                        activeforeground = "white", command = lambda: self.UpdateData())           
        self.updDataBtn.bind("<Enter>", lambda e: self.updDataBtnCover())
        self.updDataBtn.bind("<Leave>", lambda e: self.updDataBtnUncover())
        
        self.exitBtn = Button(self.pad, bg = "#081528", text = AppInfo.text['btnName'][2],
                    relief = GROOVE, font = "courier 12", fg = "white", activebackground = "#081528", 
                    activeforeground = "white", command = lambda: self.Exit())   
        self.exitBtn.bind("<Enter>", lambda e: self.exitBtnCover())
        self.exitBtn.bind("<Leave>", lambda e: self.exitBtnUncover())
        
        self.howBtn = Button(self.pad, bg = "#081528", text = AppInfo.text['btnName'][3], 
                    relief = GROOVE, font = "courier 12", fg = "white", activebackground = "#081528", 
                    activeforeground = "white", command = lambda: self.FAQ())   
        self.howBtn.bind("<Enter>", lambda e: self.howBtnCover())
        self.howBtn.bind("<Leave>", lambda e: self.howBtnUncover())
        
        self.label = Label(self.pad, text = AppInfo.text['info']['top25'][0], 
                        font =  "courier 18", fg = '#d36e70', bg = '#081528')
        self.waitLab = Label(self.littlePad, font = "courier 8", bg = "#081528", fg = "white", 
                             text = AppInfo.text['info']['wait'])
                        
    def PlaceBasicVidgs(self):
        self.pad.place(x=0, y=0, relwidth=1, relheight=1)
        self.littlePad.place(x=30, rely = 0.25, width = 280, relheight = 0.5 )
        
        self.changeUsrBtn.place(x = 45, rely = 0.21, width = 250, relheight = 0.04)
        self.updDataBtn.place(x = 45, rely = 0.75, width = 250, relheight = 0.04)
        self.exitBtn.place(x = 50, rely = 0.957, width = 200, relheight = 0.04)
        self.howBtn.place(x = 255, rely = 0.957, width = 25, relheight = 0.04)
        
        self.label.place(x = 600, y = 40)
        self.waitLab.place(relx = -1, rely = -1)
 
    def ChangeAppZoomed(self):
        if self.isNormAppSize:
            root.state('zoomed')
        else:
            root.state('normal')
        self.isNormAppSize = not self.isNormAppSize

    def ChangeAppLocat(self):
        if self.isCanChangeAppLocat:
            root.overrideredirect(1)
            self.WriteCoords()
        else:
            root.overrideredirect(0)
        self.isCanChangeAppLocat = not self.isCanChangeAppLocat
            
    def WriteCoords(self):
        writer = open(AppInfo.PATHs['position'], "w")
        writer.write("{0}+{1}".format(str(root.winfo_rootx()), str(root.winfo_rooty())))
        writer.close()
    
    def Exit(self):
        sys.exit()
    
    def CreateToken(self, token):
        writer = open(AppInfo.PATHs['token'], "w")
        writer.write(str(token).strip())
        writer.close() 
    
    def FAQ(self):
        answer = simpledialog.askstring(AppInfo.text['info']['name'],AppInfo.text['info']['FAQ'])
        if answer is None:
            return 
        elif len(answer) < 30:
            messagebox.showinfo(AppInfo.text['error']['name'],AppInfo.text['error']['token'])
            return
        else:
            if not os.path.exists(AppInfo.PATHs['api']):
                os.mkdir(AppInfo.PATHs['api'])
            if not os.path.exists(AppInfo.PATHs['token']):
                self.CreateToken(answer)
                messagebox.showinfo(AppInfo.text['info']['name'],AppInfo.text['info']['token'][2])
            else:
                check = messagebox.askquestion(AppInfo.text['info']['token'][0], AppInfo.text['info']['token'][1])
                if check == 'yes':
                    self.CreateToken(answer)
                    messagebox.showinfo(AppInfo.text['info']['name'],AppInfo.text['info']['token'][2])
                

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
    
    def UpdateData(self):
        self.waitLab.place(relx = 0, rely = 0)
        self.DestrVidgs()
        frListObj = self.CreateNewDATAFile()
        self.DATA = frListObj.GetFList()
        if self.DATA is None:
            messagebox.showinfo(AppInfo.text['error']['name'], AppInfo.text['error']['frList'])
        else:
            self.CreateNewVidgs(frListObj)      
        self.waitLab.place(relx = -1, rely = -1)

    def ChangeUsrBtnPressed(self):
        if self.CreateNewUser():
            self.UpdateData()
        
    def DestrVidgs(self): 
        self.DestrMainBdayVidg()
        self.DestrTop25Vidgs()
        root.update()
        
    def DestrMainBdayVidg(self):
        self.BdayInfoLab.destroy()
        self.BdayInfoLabls = None
            
    def DestrTop25Vidgs(self):     
        for i in range(len(self.BdayTop25Labs)):
            self.BdayTop25Labs[i].destroy()
        self.BdayTop25Labs.clear() 
        
    def CreateNewUser(self):
        answer = simpledialog.askstring(AppInfo.text['input']['name'], AppInfo.text['input']['id'],
                                parent=self.root)
        if answer is None:
            return False
        if len(answer) == 0:
            messagebox.showinfo(AppInfo.text['error']['name'], AppInfo.text['error']['input'])
            return False
        else:
            writer = open(AppInfo.PATHs['user'],"w")
            writer.write(str(answer).strip())
            writer.close()
            return True

    def CreateNewDATAFile(self): 
        if os.path.exists(AppInfo.PATHs['user']):
            reader = open(AppInfo.PATHs['user'],"r")
            ownData = reader.read()
            reader.close()
        else:
            self.CreateNewUser()
            self.CreateNewDATAFile()
            return None
        
        if ownData is not None and len(ownData)>0:
            frListObj = VkFriends.VkFriends(ownData.split(' ')[0], AppInfo.PATHs['token'])
            frListObj.CreateFList()
            return frListObj 
        else:
            return None
           
    def CreateNewVidgs(self, frListObj):
        self.CreateMainBdayVidg(frListObj.NearBDayFriend())
        self.CreateTop25Vidgs(frListObj.GetFrIndexByID(frListObj.NearBDayFriend()['id']))  
        
    def CreateMainBdayVidg(self, friend): 
        self.BdayInfoLab = Label(self.littlePad, font = "courier 18", bg = "#081528", fg = "#d36e70")
        bdate = friend['bdate'][0]+ "." + friend['bdate'][1]
        if self.IsItToday(bdate):
            self.BdayInfoLab.config(text = AppInfo.text['nearestBD'].format(friend['first_name'], 
            friend['last_name'], AppInfo.text['today']))
        else:
            self.BdayInfoLab.config(text = AppInfo.text['nearestBD'].format(friend['first_name'], 
            friend['last_name'], friend['bdate'][0]+ " " + self.GetMonthName(friend['bdate'][1])))
        self.BdayInfoLab.pack(expand = 1)        
    
    def CreateTop25Vidgs(self, ind):
        c = 0      
        firstIDInTop = self.DATA[ind]['id']
        firstEntry = True
        for i in range(len(self.DATA))[ind:]:
            c+=1
            if c>25 or (firstIDInTop == self.DATA[i]['id'] and firstEntry == False):
                break 
            else:
               self.AddToBdateTop25(i)
            firstEntry = False
            
        for i in range(len(self.DATA )):
            c+=1
            if c>25 or firstIDInTop == self.DATA[i]['id']:
                break 
            else:
                self.AddToBdateTop25(i)
                
        for i in range(len(self.BdayTop25Labs)):
            self.BdayTop25Labs[i].place(x = 450, y = i * 20 + 90 )      
        
    def AddToBdateTop25(self, ind):
        f_name, l_name, bdate = self.DATA[ind]['first_name'], self.DATA[ind]['last_name'], '.'.join(self.DATA[ind]['bdate'])
        count = self.DotsCount(l_name + " " + f_name)
        if self.IsItToday(bdate.split('.')[0]+'.'+bdate.split('.')[1]):
            bdate = AppInfo.text['today']
        self.BdayTop25Labs.append(Label(self.pad, font = "courier 12", bg = "#081528", fg = "white",
                                        text = AppInfo.text['userInfo'].format(l_name, f_name, '.'*count, bdate)))

    
    def LoadDATAFile(self):
        if os.path.exists(AppInfo.PATHs['user']):
            reader = open(AppInfo.PATHs['user'],'r')
            userID = reader.read()
            reader.close()
            if (userID is not None and len(userID)>0):
                frListObj = VkFriends.VkFriends(userID.split(' ')[0], AppInfo.PATHs['token'])
                self.DATA = frListObj.GetFList()  
                if self.DATA is None:
                    messagebox.showinfo(AppInfo.text['error']['name'], AppInfo.text['error']['frList'])
                else:
                    self.CreateNewVidgs(frListObj) 
            else:
                 messagebox.showinfo(AppInfo.text['error']['name'], AppInfo.text['error']['id'])
        else:
            messagebox.showinfo(AppInfo.text['error']['name'], AppInfo.text['error']['id'])
       
    def DotsCount(self, str, lenAllStr = 52):
        return lenAllStr-len(str)
    
    def GetMonthName(self,month):
        if str(month) in AppInfo.months.keys():
            return AppInfo.months[str(month)]
        else:
            return month
            
    def IsItToday(self, data):
        dtime = datetime.now()   
        today = str(dtime.day)+'.'+str(dtime.month)
        if data == today:
               return True
        return False
        

if __name__ == '__main__':             
    root = Tk()
    root.title(AppInfo.text['title'])
    
    try:
        stream = open(AppInfo.PATHs['position'],'r')
        root.geometry("340x500+{0}".format(stream.read()))
        stream.close()
    except:
        print("appPlace file not found")
        root.geometry("340x500+0+0")
    try:
        root.iconbitmap(AppInfo.PATHs['icon'])
    except:
        print("icon not found")
    root.overrideredirect(1)
    app = Application(root)
    root.mainloop()

