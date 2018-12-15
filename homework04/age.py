import datetime as dt
import datetime
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User
import math


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    ages = []

    for friend in friends:
        user = User(**friend)
        if user.bdate is not None:
            date = user.bdate.split('.')
            if len(date) == 3:
                today = datetime.datetime.today()
                date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
                if (today.month >= int(date.month)) and (today.day >= int(date.day)):
                    ages.append(today.year - int(date.year))
                else:
                    ages.append(today.year - int(date.year) - 1)

    ages.sort()

    if len(ages) != 0:
        age = median(ages)
    else:
        age = None
    return age


if __name__ == '__main__':
    age = age_predict(99183468)
    print(age)
