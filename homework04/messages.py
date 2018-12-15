from collections import Counter
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    dates = []

    for message in messages:
        date = message.date
        date = fromtimestamp(date).strftime("%Y-%m-%d")
        dates.append(date)

    frequencies = Counter(dates)
    dates = list(frequencies.keys())
    freq = list(frequencies.values())

    return dates, freq


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """

    x = dates
    y = freq
    data = [go.Scatter(x=x, y=y)]
    py.iplot(data)


if __name__ == '__main__':
    plotly_messages_freq(count_dates_from_messages(messages_get_history(46300036)))
