text = {
    'title': 'ДниРожденияДрузей',
    'btnName':
    [  
        'Сменить пользователя', 
        'Обновить данные', 
        'Выход',
        '?',
    ],
    'info':
        {   'name': 'Информация',
            'wait': '''Подождите, идет сбор информации, 
        это займет некоторое время...''',
            'FAQ': '''1) Для открытия возможности передвижения окна приложения
необходимо нажать Правую Кнопку Мыши. Повторное нажатие на ПКМ 
вновь уберет возможность передвижения.
2) Для расширения окна приложения на весь экран необходмо осуществить
двойное нажатие ЛКМ, в таком варианте будет виден список из 25 ближайших
дней Рождения. Повторное двойное нажатие веренет уменьшенную версию.
3) Для выхода (помимо кнопки "Выход") достаточно нажать клавишу "esc".
4) Если у Вас никак не получается подгрузить дни рождения, возможно, 
не указан токен, или указан, но неверно, тогда, если Вы знаете токен для Вк, 
можете ввести его в строку ниже (если Вы не знаете, что это(...или знаете), 
но все работает, пожалуйста, не трогайте, если не знаете и не работает,
разузнайте, как его заполучить(недра Интернета) и возвращайтесь с ним) ''',
            'token': 
            [
                'Замена существующего токена',
                'Файл токена обнаружен, вы уверены, что хотите изменить токен?',
                'Токен записан в файл, попробуйте снова подгрузить список.',
            ],
            'top25':
            [
                'ТОП-25 БЛИЖАЙШИХ ДНЕЙ РОЖДЕНИЯ:'
            ]
        },
    'input':
        {
            'name' : 'Ввод', 
            'id'   : 'Введите id страницы вк:'
        },
    'error':
        {
            'name'  : 'Ошибка',
            'token' : 'Длина токена должна быть больше 30 символов',
            'frList': '''Список друзей пуст, возможные причины: 
1) ошибка ID/Токена => изменить ID, изменить токен (только в случае крайнего отчаяния)
2) удаление пользователем файла с данными => сделать обновление данных''',
            'input' : 'Ничего не было введено',
            'id'    : 'Данные о пользователе не найдены'
        },
    'nearestBD'     : 'БЛИЖАЙШИЙ\nДЕНЬ РОЖДЕНИЯ:\n\n{0}\n{1}\n\nДАТА РОЖДЕНИЯ:\n{2}',
    'userInfo'      : '{0} {1}{2}дата рождения: {3}',
    'today'         : 'СЕГОДНЯ'
}

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

PATHs = {
    'icon'      : '.\\crown.ico',
    'bgPicture' : '.\\BlueWood.png',
    'user'      : '.\\ownerData.txt',
    'position'  : '.\\AppPosition.txt',
    'api'       : '..\\Api',
    'token'     : '..\\Api\\forVk.txt'
}


