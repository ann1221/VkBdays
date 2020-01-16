# -*- coding: utf-8 -*-
class Error(object):
    message = {
            'Error'   : 'Ошибка',
            'File'    : 'Файл не был найден',    
            'Token'   : 'Токен не был найден',
            'User'    : 'Пользователь не был найден',
            'Vk'      : '',
            'Connect' : 'Связь с Интернетом не найдена', 
            'List'    : 'Список друзей не найден или пуст', 
            'JSON'    : 'Файл с данными некорректен, он был удален',
            'Nothing' : 'Данные не найдены',
            'Path'    : 'Ошибка пути',
            'Len'     : 'Длина входных данных слишком мала',
            'Icon'    : 'Иконка не была найдена'
    }
    
    def Translate(inpKey):
        translated = {
            'One of the parameters specified was missing or invalid: user_id not integer' : 'ID должен быть представлен числом',
            'User authorization failed: invalid access_token (4).' : 'Токен неверен',
            'User was deleted or banned': 'Пользователь забанен или удален',
        }    
        if inpKey in translated:
            return translated[inpKey]
        return inpKey
        
    def Search(inpValue):
        for k, v in Error.message.items():
            if str(v) == str(inpValue):
                return k
        return None
