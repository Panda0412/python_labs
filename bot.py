import requests
import config
import telebot
from datetime import datetime, timedelta, time as Time
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        group=group.upper(),
        week=week)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    if not schedule_table:
        return None

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info])
                    for lesson_info in lessons_list]

    # Аудитория
    rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
    rooms_list = [room.dd.text for room in rooms_list]

    return times_list, locations_list, lessons_list, rooms_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday',
                               'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    n = message.text.split()
    if len(n) == 3:
        day, group, week = n
    elif len(n) == 2:
        day, group = n
        week = '0'
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды! 😞\n"
                                          "Ожидаемый формат:\n"
                                          "/День  Номер группы  "
                                          "Чётность недели (0 - обе недели;\n"
                                          "                1 - чётная;\n"
                                          "                2 - нечётная)")
        return None

    if len(group) != 5:
        bot.send_message(message.chat.id, "Группа указана неверно")
        return None

    if week not in ['0', '1', '2']:
        bot.send_message(message.chat.id, "Неделя указана неверно")
        return None

    days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day',
            '/thursday': '4day', '/friday': '5day',
            '/saturday': '6day', '/sunday': '7day'}
    day = days[day]
    web_page = get_page(group, week)
    if parse_schedule(web_page, day):
        times_list, locations_list, lessons_list, \
            rooms_list = parse_schedule(web_page, day)
        resp = ''
        for time, location, room, lesson in \
                zip(times_list, locations_list, rooms_list, lessons_list):
            resp += '<b>{}</b>\n {}\n {}{}\n'.format(
                time, location, room, lesson)
        return bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        days = {'1day': 'Понедельник', '2day': 'Вторник', '3day': 'Среда',
                '4day': 'Четверг', '5day': 'Пятница',
                '6day': 'Суббота', '7day': 'Воскресенье'}
        day = days[day]
        return bot.send_message(message.chat.id,
                                '<b>{} - выходной день 😜</b>'.format(day),
                                parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    n = message.text.split()
    if len(n) == 2:
        _, group = n
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды! 😞\n"
                                          "Ожидаемый формат:\n"
                                          "/near  Номер группы")
        return None

    if len(group) != 5:
        bot.send_message(message.chat.id, "Группа указана неверно")
        return None

    days = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
    dayrs = ['Понедельник', 'Вторник', 'Среда',
             'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    today = datetime.fromtimestamp(message.date)
    if today.month >= 9:
        first_september = datetime(today.year, 9, 1)
    else:
        first_september = datetime(today.year - 1, 9, 1)
    for _n in range(10):
        now = Time(today.hour, today.minute)
        week = ((today - first_september).days
                + first_september.weekday()) // 7 % 2
        if week == 0:
            week = 2
        web_page = get_page(group, week)
        if parse_schedule(web_page, days[today.weekday()]):
            times_list, locations_list, lessons_list, rooms_list\
                = parse_schedule(web_page, days[today.weekday()])
            times_list_Time = []
            for time in times_list:
                if time != 'День':
                    time = time.split('-')
                    time = time[0].split(':')
                    times_list_Time.append(Time(int(time[0]), int(time[1])))
                else:
                    times_list_Time.append(Time(23, 59))
            for time, location, room, lesson, time_Time in \
                    zip(times_list, locations_list,
                        rooms_list, lessons_list, times_list_Time):
                if week == 2:
                    if lesson.find('нечетная неделя') != -1 or \
                            lesson.find('четная неделя') == -1 \
                            and time_Time >= now:
                        resp = '<b>{}\n\n{}</b>\n {}\n {}{}\n'.format(
                            dayrs[today.weekday()], time,
                            location, room, lesson)
                        bot.send_message(message.chat.id,
                                         resp, parse_mode='HTML')
                        return None
                elif time_Time >= now:
                    if lesson.find('нечетная неделя') == -1:
                        resp = '<b>{}\n\n{}</b>\n {}\n {}{}\n'.format(
                            dayrs[today.weekday()], time,
                            location, room, lesson)
                        bot.send_message(message.chat.id,
                                         resp, parse_mode='HTML')
                        return None
        today = today.replace(hour=0, minute=0, second=0)
        today = today + timedelta(1)
    else:
        bot.send_message(message.chat.id, '☠☠☠ERROR☠☠☠')


@bot.message_handler(commands=['tomorrow', 'today'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    n = message.text.split()
    if len(n) == 2:
        day, group = n
    else:
        day = n[0]
        bot.send_message(message.chat.id, "Я не знаю такой команды! 😞\n"
                                          "Ожидаемый формат:\n"
                                          "{}  Номер группы".format(day))
        return None

    if len(group) != 5:
        bot.send_message(message.chat.id, "Группа указана неверно")
        return None

    today = datetime.fromtimestamp(message.date)
    tomorrow = today + timedelta(1)
    days = ['/monday', '/tuesday', '/wednesday',
            '/thursday', '/friday', '/saturday', '/sunday']
    if today.month >= 9:
        first_september = datetime(today.year, 9, 1)
    else:
        first_september = datetime(today.year - 1, 9, 1)
    if day == '/tomorrow':
        week = ((tomorrow - first_september).days
                + first_september.weekday()) // 7 % 2
        if week == 0:
            week = 2
        message.text = '{} {} {}'.format(days[tomorrow.weekday()], group, week)
    elif day == '/today':
        week = ((today - first_september).days
                + first_september.weekday()) // 7 % 2
        if week == 0:
            week = 2
        message.text = '{} {} {}'.format(days[today.weekday()], group, week)
    get_schedule(message)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    n = message.text.split()
    if len(n) == 3:
        _, group, week = n
    elif len(n) == 2:
        _, group = n
        week = '0'
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды! 😞\n"
                                          "Ожидаемый формат:\n"
                                          "/День  Номер группы  "
                                          "Чётность недели (0 - обе недели;\n"
                                          "                1 - чётная;\n"
                                          "                2 - нечётная)")
        return None

    if len(group) != 5:
        bot.send_message(message.chat.id, "Группа указана неверно")
        return None

    if week not in ['0', '1', '2']:
        bot.send_message(message.chat.id, "Неделя указана неверно")
        return None

    days = ('1day', '2day', '3day', '4day', '5day', '6day', '7day')
    dayrs = {'1day': 'Понедельник', '2day': 'Вторник', '3day': 'Среда',
             '4day': 'Четверг', '5day': 'Пятница',
             '6day': 'Суббота', '7day': 'Воскресенье'}
    web_page = get_page(group, week)
    resp = ''
    for day in days:
        dayr = dayrs[day]
        if parse_schedule(web_page, day):
            times_list, locations_list, lessons_list, rooms_list\
                = parse_schedule(web_page, day)
            for time, location, room, lesson in \
                    zip(times_list, locations_list, rooms_list, lessons_list):
                resp += '<b>{}</b>\n <b>{}</b>\n {}\n {}{}\n'.format(
                    dayr, time, location, room, lesson)
        else:
            resp += '<b>{} - выходной день 😜</b>\n'.format(dayr)
        resp += '___________________________________\n\n'
    return bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['panda'])
def panda(message):
    return bot.send_message(message.chat.id, '░░░░░░░░▄██▄░░░░░░▄▄░░'
                                             '░░░░░░░▐███▀░░░░░▄███▌'
                                             '░░▄▀░░▄█▀▀░░░░░░░░▀██░'
                                             '░█░░░██░░░░░░░░░░░░░░░'
                                             '█▌░░▐██░░▄██▌░░▄▄▄░░░▄'
                                             '██░░▐██▄░▀█▀░░░▀██░░▐▌'
                                             '██▄░▐███▄▄░░▄▄▄░▀▀░▄██'
                                             '▐███▄██████▄░▀░▄█████▌'
                                             '▐████████████▀▀██████░'
                                             '░▐████▀██████░░█████░░'
                                             '░░░▀▀▀░░█████▌░████▀░░'
                                             '░░░░░░░░░▀▀███░▀▀▀░░░░',
                            parse_mode='HTML')


@bot.message_handler(commands=['command'])
def command(message):
    return bot.send_message(message.chat.id, '<b>Вот что я умею:</b>\n\n'
                                             '/День<i>*</i>  Номер группы  '
                                             'Чётность недели '
                                             '(0 - обе недели;\n'
                                             '                1 - чётная;\n'
                                             '                2 - нечётная)\n'
                                             '<i>*День - день '
                                             'недели (на английском)\n'
                                             'Сегодня(/today)\n'
                                             'Завтра(/tomorrow)\n'
                                             'Все - вся неделя(/all)</i>\n\n'
                                             '/near  Номер группы - '
                                             'ближайшее занятие\n\n'
                                             '/command - вызывает подсказку '
                                             'с командами\n\n'
                                             '/panda - тут всем всё понятно 🐼',
                            parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start(message):
    return bot.send_message(message.chat.id, "░░░░░░░░▄██▄░░░░░░▄▄░░"
                                             "░░░░░░░▐███▀░░░░░▄███▌"
                                             "░░▄▀░░▄█▀▀░░░░░░░░▀██░"
                                             "░█░░░██░░░░░░░░░░░░░░░"
                                             "█▌░░▐██░░▄██▌░░▄▄▄░░░▄"
                                             "██░░▐██▄░▀█▀░░░▀██░░▐▌"
                                             "██▄░▐███▄▄░░▄▄▄░▀▀░▄██"
                                             "▐███▄██████▄░▀░▄█████▌"
                                             "▐████████████▀▀██████░"
                                             "░▐████▀██████░░█████░░"
                                             "░░░▀▀▀░░█████▌░████▀░░"
                                             "░░░░░░░░░▀▀███░▀▀▀░░░░\n\n\n"
                                             "<b>Привет!</b>\n"
                                             "<i>Я Панда и я хочу жить "
                                             "в твоём телефоне)\n"
                                             "Не прогоняй меня, "
                                             "а я буду оперативно "
                                             "сообщать тебе твоё расписание!"
                                             "</i>\n\n\n"
                                             "<b>Вот что я умею:</b>\n\n"
                                             "/День<i>*</i>  Номер группы  "
                                             "Чётность недели "
                                             "(0 - обе недели;\n"
                                             "                1 - чётная;\n"
                                             "                2 - нечётная)\n"
                                             "<i>*День - день "
                                             "недели (на английском)\n"
                                             "Сегодня(/today)\n"
                                             "Завтра(/tomorrow)\n"
                                             "Все - вся неделя(/all)</i>\n\n"
                                             "/near  Номер группы - "
                                             "ближайшее занятие\n\n"
                                             "/command - вызывает подсказку "
                                             "с командами\n\n"
                                             "/panda - тут всем всё понятно 🐼",
                            parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
