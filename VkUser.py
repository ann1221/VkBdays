import requests 

class VkUser(object):
    def __init__(self, pageID, pathToToken):
        self.ID = str(pageID)
        self.URL = 'https://api.vk.com/method/'
        self.__PATH = str(pathToToken)

    def __getAccesToken(self):
        reader = open(str(self.__PATH), 'r')
        token = reader.read()
        reader.close()
        return token
    
    def __GetJsonResponse(self, fillURL, options):
        try:
            resp = requests.get(fillURL, params = options).json()
            if 'error' in resp:
                return None
            return resp
        except:
            return None
    
    def GetPersonalData(self, options =  
                                         '''
                                            photo_id, verified, sex, bdate, city, country, home_town, has_photo, 
                                            photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, 
                                            online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, 
                                            followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, 
                                            exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, 
                                            can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, 
                                            is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, 
                                            career, military, blacklisted, blacklisted_by_me, can_be_invited_group
                                            
                                          '''):
        if self.ID is None or self.ID == '':
            return None     
        USING_METHOD = 'users.get'
        try:
            options = {
                            'user_ids' : self.ID,
                            'fields': options,
                            'access_token': self.__getAccesToken(), 
                            'v' : '5.103'
                         }
        except:
            return None
        return self.__GetJsonResponse(self.URL + USING_METHOD, options)

     
    def GetFriendsIDs(self):
        if self.GetPersonalData() is None:
            return None   
        USING_METHOD = 'friends.get'
        try:
            options = {
                            'user_id' : self.GetPersonalData()['response'][0]['id'],
                            'access_token': self.__getAccesToken(), 
                            'order' : 'name',
                            'v' : '5.103'
                      }
        except:
            return None
        return self.__GetJsonResponse(self.URL + USING_METHOD, options)

