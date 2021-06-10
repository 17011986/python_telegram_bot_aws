from dataclasses import dataclass
from emoji import emojize


@dataclass(frozen=True)
class Messages:
    start:   str = f'Приветсвую тебя !!!\nЭтот бот поможет тебе найти авто твой мечты\nжми --->> /start что бы начать\nжми --->> /help что бы узнать как он работает'
    plat:    str = "Выбери площадку где хочешь найти авто"
    make:    str = "Выбери марку авто"
    model:   str = "Выбери модель авто"
    cen :    str = "Ведитие цену ниже которой желаете получить авто"
    errcena :str = "Ведите цену числом"
    otch :   str = "Вы купили отчет на неделю"
    otchpod: str = "Отчет по подписке"
    god_po:  str = " года по "
    god_do:  str = " год с ценой ниже "
    no_res:  str = "Пока не чего не найдено"
    entergd: str = "Выберите с какого года искать"
    inpgod:  str = "Выберете по какой год"
    help:    str = f'Этот бот будет проверить выбранный вами ресурс \nи проверять все варианты с фиксированной ценой\nцелую неделю каждые пол часа.\nТем самым вы не пропустете в продаже ваш авто\nпо вашей  цене жми --->> /start чтобы начать '
    admin_set_messages: str = "Бот запущен"
    back:    str = "Назад"
    buy:     str = "Купить"
    edit:    str = "Проверьте что Вы выбрали"


msg = Messages()
