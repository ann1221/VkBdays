import VkUser
from time import sleep
from datetime import datetime
import json

class VkFriends():
    def __init__(self, ownerID, pathToOwnerToken):
        self.__PATH = pathToOwnerToken
        self.__LIST_HOLDER = VkUser.VkUser(ownerID, pathToOwnerToken)
        self.__F_LIST = []
        self.__FILE_NAME = 'data_file.json'
        
    def __isHavePrincipOpts(self, list, options):
        for i in options.split(','):
            if i.strip() not in list:
                return False
        return True

    def __FillList(self, options):
        friendsIds = self.__LIST_HOLDER.GetFriendsIDs()
        if friendsIds is None:
            return None
        tmp_list = []
        for currID in friendsIds['response']['items']:
            friend = VkUser.VkUser(currID,self.__PATH)
            persData = friend.GetPersonalData(options)
            print(persData)
            info = persData['response'][0]
            if self.__isHavePrincipOpts(info, options):
                tmp_list.append(info)
            sleep(1)
        self.__F_LIST = tmp_list.copy()    
        
    def __SortByBDays(self):
        tmp_list = []
        for i in self.__F_LIST:
            if self.__isHavePrincipOpts(i,'bdate'):
                bdate = i['bdate'].split('.')
                i['bdate'] = bdate
                tmp_list.append(i)
        self.__F_LIST = sorted(tmp_list, key = lambda x: (int(x['bdate'][1]),int(x['bdate'][0])))   
       
    def CreateFList(self):
        print("********************************Please Wait************************************")
        self.__FillList('bdate')
        print(self.__F_LIST)
        self.__SortByBDays()
        
        with open(self.__FILE_NAME, 'w') as write_file: json.dump(self.__F_LIST, write_file)
        print("*******************************File was updated********************************")  
        
    def GetFList(self):
        try:
            with open(self.__FILE_NAME, 'r') as read_file: data = json.load(read_file)
            self.__F_LIST = data.copy()
            if len(self.__F_LIST) == 0:
                return None
            return self.__F_LIST
        except:
            return None
    
    def NearBDayFriend(self):
        if self.__F_LIST is None or len(self.__F_LIST) == 0:
            return None
        dtime = datetime.now()
        today = str(dtime.day)+'.'+str(dtime.month)
        month, day = int(today.split('.')[1]), int(today.split('.')[0])
        iInd = 0
        for i in self.__F_LIST:
            iInd+=1
            if month == int(i['bdate'][1]):
                for j in self.__F_LIST[iInd:]:
                    if day<=int(j['bdate'][0]):
                        return j
                    if month < int(j['bdate'][1]):
                        return j
            elif month < int(i['bdate'][1]):
                return i
        return self.__F_LIST[0]        
            
    def GetFrIndexByID(self, ID):
        count = 0;
        for i in self.__F_LIST:
            if i['id'] == int(ID):
                return count
            count+=1
        return None
