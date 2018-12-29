import requests
import config
import telebot
from datetime import datetime
from bs4 import BeautifulSoup

telebot.apihelper.proxy = config.proxy
bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page

'''
def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "lxml")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list
'''


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "lxml")

    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    n = 0
    for i in range(len(week)):
        if week[i] == day:
            n = i + 1
            break

    day = str(n) + 'day'

    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list

'''
@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
'''


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    try:
        mess = message.text.split()

        if len(mess) == 2:
            day, group = mess
            web_page = get_page(group)
        else:
            day, group, week = mess
            web_page = get_page(group, week)

        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except AttributeError:
        resp = 'Отдыхай, салага, на учебку не надо'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    cur_day = datetime.weekday(datetime.today())
    cur_week = datetime.isocalendar(datetime.today())[1]
    hour = datetime.today().hour
    minute = datetime.today().minute
    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    _, group = message.text.split()

    try:
        if cur_week % 2 == 0:
            cur_week = '1'
        else:
            cur_week = '2'

        day = week[cur_day]

        web_page = get_page(group, cur_week)
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            start = time[:5]
            start = start.split(':')
            if (int(start[0]) > hour) or ((int(start[1]) > minute) and (int(start[0]) == hour)):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
                break

    except AttributeError:
        cur_day += 1
        if cur_day == 7:
            cur_day = 0
            if cur_week == '1':
                cur_week = '2'
            else:
                cur_week = '1'
        day = week[cur_day]
        web_page = get_page(group, cur_week)
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            break

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    cur_day = datetime.weekday(datetime.today())
    cur_week = datetime.isocalendar(datetime.today())[1]
    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    _, group = message.text.split()

    try:
        if cur_week % 2 == 0:
            cur_week = '1'
        else:
            cur_week = '2'

        if cur_day == 6:
            next_day = 0
            if cur_week == '1':
                cur_week = '2'
            else:
                cur_week = '1'
        else:
            next_day = cur_day + 1

        day = week[next_day]

        web_page = get_page(group, cur_week)
        times_lst, locations_lst, lessons_lst = \
            parse_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except AttributeError:
        resp = 'Отдыхай, салага, на учебку не надо'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """

    cur_week = datetime.isocalendar(datetime.today())[1]
    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    week_resp = ['<b>Понедельник:</b>\n', '<b>Вторник:</b>\n', '<b>Среда:</b>\n', '<b>Четверг:</b>\n', '<b>Пятница:</b>\n', '<b>Суббота:</b>\n', '<b>Воскресенье:</b>\n']
    _, group = message.text.split()
    resp = ''

    if cur_week % 2 == 0:
        cur_week = '1'
    else:
        cur_week = '2'

    web_page = get_page(group, cur_week)

    for i in range(7):
        resp_d = week_resp[i]

        try:
            day = week[i]
            times_lst, locations_lst, lessons_lst = \
                parse_schedule(web_page, day)
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp_d += '<b>{}</b>, {}, {}\n'.format(time, location, lession)

        except AttributeError:
            resp_d += ' Отдыхай, салага, на учебку не надо\n'
        resp += resp_d + '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)

