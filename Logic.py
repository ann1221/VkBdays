import MyRequests
import MyErrors
import json
import os
from time import sleep
from datetime import datetime

class VkClient(object):
    def __init__(self, userPageID, token):
        self.ID = str(userPageID)
        self.__TOKEN = str(token)
        dtime = datetime.now()
        self.today = [dtime.day, dtime.month]

    def GetFriendsList(self):
        friendsList = self.__FindFrList()
        if friendsList is None:
            return MyErrors.Error.message['Nothing']
        if MyErrors.Error.Search(friendsList) is None:
            return friendsList  
        if len(friendsList) < 1 :
            return MyErrors.Error.message['Nothing']
        return self.UpdateFriendsList()
 
    def __FindFrList(self):
        return FileWorker.JsonReader()
 
    def UpdateFriendsList(self):
        friendsList = self.__FillOutFriendsList('bdate')
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        sortedList = self.__DateSort(friendsList)
        FileWorker.JsonWriter(sortedList)
        return sortedList
    
    def __FillOutFriendsList(self, options):
        vkRequest = MyRequests.VkRequest(self.__TOKEN)
        friendsID = vkRequest.GetAllFriendsID(self.ID)
        if MyErrors.Error.Search(friendsID) is not None:
            return friendsID
        topList = []
        for currID in friendsID:
            persData = vkRequest.GetPersonalData(currID, options)
            print(persData)
            if self.__isHavePrincipOpts(persData, options):
                topList.append(persData)
            sleep(0.4)
        return topList
    
    def __isHavePrincipOpts(self, list, options):
        for i in options.split(','):
            if i.strip() not in list:
                return False
        return True
       
    def __DateSort(self, friendsList):
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        topList = []
        for i in friendsList:
            if self.__isHavePrincipOpts(i,'bdate'):
                bdate = i['bdate'].split('.')
                i['bdate'] = bdate
                topList.append(i)
        return sorted(topList, key = lambda x: (int(x['bdate'][1]),int(x['bdate'][0])))   

    def GetSoonestBdayFriend(self):
        friendsList = self.GetFriendsList()
        friend = self.__GetClosestToTodayListEntry()
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        return self.__ConvToSoonestBdayFormat(friend)
    
    def __GetClosestToTodayListEntry(self):
        friendsList = self.GetFriendsList()
        if friendsList is None or len(friendsList) == 0:
            return MyErrors.Error.message['List']
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        friendIndex = 0
        for i in friendsList:
            friendIndex+=1
            if int(self.today[1]) == int(i['bdate'][1]):
                for j in friendsList[friendIndex:]:
                    if int(self.today[0]) <= int(j['bdate'][0]):
                        return j
                    if int(self.today[1]) < int(j['bdate'][1]):
                        return j
            elif int(self.today[1]) < int(i['bdate'][1]):
                return i
        return friendsList[0]
        
    def __ConvToSoonestBdayFormat(self, person):
        pattern = 'БЛИЖАЙШИЙ\nДЕНЬ РОЖДЕНИЯ:\n\n{0}\n{1}\n\nДАТА РОЖДЕНИЯ:\n{2}'
        bdate = person['bdate'].copy()
        if self.__IsItToday(bdate):
            bdate = 'СЕГОДНЯ'
        else:
            bdate[1] = self.__GetMonthName(bdate[1])
        return pattern.format(person['last_name'], person['first_name'], ' '.join(bdate))
    
    def __IsItToday(self, data): 
        if str(data[0]) == str(self.today[0]) and str(data[1]) == str(self.today[1]):
               return True
        return False    
    
    def __GetMonthName(self, inpMonth):
        months = {
            '1':'января',
            '2':'февраля',
            '3':'марта',
            '4':'апреля',
            '5':'мая',
            '6':'июня',
            '7':'июля',
            '8':'августа',
            '9':'сентября',
            '10':'октября',
            '11':'ноября',
            '12':'декабря'
        }
        if str(inpMonth) in months.keys():
            return months[str(inpMonth)]
        else:
            return inpMonth


    def GetTopSoonestBday(self, TotalTop = 25):
        friendsList = self.GetFriendsList()
        topCounter = 0      
        soonestBdayFriend = self.__GetClosestToTodayListEntry()
        if MyErrors.Error.Search(soonestBdayFriend) is not None:
            return soonestBdayFriend
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        ind = self.__GetFriendIndByID(soonestBdayFriend['id'])
        beginWith = friendsList[ind]['id']
        firstEntry = True
        topList = []
        
        for i in range(len(friendsList))[ind:]:
            topCounter+=1
            if topCounter>TotalTop or (beginWith == friendsList[i]['id'] and firstEntry == False):
                break 
            else:
                topList.append(self.__ConvToTopFormat(i))
            firstEntry = False
            
        for i in range(len(friendsList)):
            topCounter+=1
            if topCounter>TotalTop or beginWith == friendsList[i]['id']:
                break 
            else:
                topList.append(self.__ConvToTopFormat(i))
        return topList 
        
    def __GetFriendIndByID(self, ID):
        friendsList = self.GetFriendsList()
        count = 0;
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        for i in friendsList:
            if int(i['id']) == int(ID):
                return count
            count+=1
        return MyErrors.Error.Search('Nothing')

    def __ConvToTopFormat(self, ind):
        friendsList = self.GetFriendsList()
        if MyErrors.Error.Search(friendsList) is not None:
            return friendsList
        person = friendsList[ind]
        count = self.__DotsCount(person['last_name'] + " " + person['first_name'])
        if self.__IsItToday(person['bdate']):
            person['bdate'] = 'СЕГОДНЯ'
        else:
            person['bdate'][1] = self.__GetMonthName(person['bdate'][1])
            person['bdate'] = ' '.join(person['bdate'])
        return '{0} {1}{2} {3}'.format(person['first_name'], person['last_name'], '.'*count, person['bdate'])
        
    def __DotsCount(self, inputStr, TotalLen = 52):
        return TotalLen-len(inputStr)     


class FileWorker(object):
    __DATA_PATH =  '.\\data_file.igAdopt'
    __TOKEN_PATH =  '.\\Admiss.igAdopt'
    __USER_PATH  =  '.\\ownerData.igAdopt'
    __POSITION_PATH  =  '.\\AppPosition.igAdopt'
            
    def RemoveFile(path):
        os.remove(path)
    
    def GetUser():
        return FileWorker.__ReadFile(FileWorker.__USER_PATH)
    def GetToken():
        return FileWorker.__ReadFile(FileWorker.__TOKEN_PATH) 
        
    def GetPosition():
        return FileWorker.__ReadFile(FileWorker.__POSITION_PATH) 
        
    def __ReadFile(path):
        if not os.path.exists(path):
            return MyErrors.Error.message['File']
        with open(path) as reader: out = reader.read()
        if len(out) == 0:
            return MyErrors.Error.message['Nothing']
        return out
            
    def ChangeToken(text):
        if text is None:
            return None     
        if len(text)<30:
            return MyErrors.Error.message['Len']  
        return FileWorker.__WriteIntoFile(FileWorker.__TOKEN_PATH, text)
        
    def ChangeUser(text):
        if len(text)<1:
            return MyErrors.Error.message['Len']  
        return FileWorker.__WriteIntoFile(FileWorker.__USER_PATH,text)
        
    def ChangePosition(text):
        if len(text)<1:
            return MyErrors.Error.message['Len']  
        return FileWorker.__WriteIntoFile(FileWorker.__POSITION_PATH,text)
    
    def __WriteIntoFile(path, text):
        try:
            writer = open(path,"w")
            writer.write(text.strip())
            writer.close() 
        except IOError:
            return MyErrors.Error.message['Path']
    
    def JsonReader():
        try:
            with open(FileWorker.__DATA_PATH, 'r') as read_file: friendsList = json.load(read_file)
        except IOError:
            return MyErrors.Error.Search('List')
        except json.decoder.JSONDecodeError:
            os.remove(FileWorker.__DATA_PATH)
            return MyErrors.Error.Search('JSON')    
        if len(friendsList) == 0:
            os.remove(FileWorker.__DATA_PATH)
            return MyErrors.Error.Search('List')
        return friendsList
        
    def JsonWriter(list):
        with open(FileWorker.__DATA_PATH, 'w') as write_file: json.dump(list, write_file)
        