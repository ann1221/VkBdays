import requests 
import MyErrors

class VkRequest(object):
    def __init__(self, token):
        self.__TOKEN = token
        self.__URL = 'https://api.vk.com/method/'
            
    def GetAllFriendsID(self, id):
        mainClient = self.GetPersonalData(id, '')
        if MyErrors.Error.Search(mainClient) is not None:
            return mainClient
        options = {
                    'user_id' : mainClient['id'],
                    'order' : 'name',
                    'v' : '5.103', 
                    'access_token' : self.__TOKEN 
                }
        response = self.__GetJsonResponse('friends.get', options)
        if MyErrors.Error.Search(response) is not None:
            return response
        return response['response']['items']
        
    def GetPersonalData(self, id, options = 
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
        options = {
                    'user_ids' : id,
                    'fields': options,
                    'v' : '5.103',
                    'access_token' : self.__TOKEN 
                }
        response = self.__GetJsonResponse('users.get', options)
        if MyErrors.Error.Search(response) is not None:
            return response
        return response['response'][0]
  
    def __GetJsonResponse(self, method, options):
        try:
            resp = requests.get(self.__URL + method, params = options).json()
            if 'error' in resp:
                MyErrors.Error.message['Vk'] = resp['error']['error_msg']
                return MyErrors.Error.message['Vk']
            return resp
        except requests.exceptions.ConnectionError:
            return MyErrors.Error.message['Connect']
