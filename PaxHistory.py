# -*- coding: utf-8 -*-
"""PAX HISTORIA — ULTIMATE v5.8: подавление бунта"""
import os, sys, time, math, random, zlib, re, unicodedata, threading

if os.name == "nt":
    os.system("")

try:
    import winsound
    SOUND_ON = True
except Exception:
    SOUND_ON = False

class C:
    R="\033[91m";G="\033[92m";Y="\033[93m";B="\033[94m";M="\033[95m"
    Cy="\033[96m";W="\033[97m";Gr="\033[90m";Bold="\033[1m";Dim="\033[2m";End="\033[0m"
def clr(t,c): return f"{c}{t}{C.End}"
def _dw(s):
    s = re.sub(r'\x1b\[[0-9;]*m', '', s)
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)
def pad(s, width): return s + " " * max(0, width - _dw(s))

ANTHEMS = {
    "Россия":        [(523,400),(523,300),(392,300),(392,300),(440,300),(440,400),(392,700),
                      (349,300),(330,300),(294,300),(294,300),(262,300),(262,400),(294,700)],
    "США":           [(392,200),(659,200),(784,400),(659,200),(784,200),(1047,700),
                      (880,300),(784,300),(659,300),(587,300),(523,600),(659,300),(784,800)],
    "Китай":         [(523,200),(523,200),(440,200),(392,200),(330,500),(523,200),
                      (392,200),(330,200),(294,500),(392,300),(330,400),(262,800)],
    "Германия":      [(392,300),(392,500),(494,300),(587,500),(587,300),(494,300),
                      (392,300),(494,300),(440,500),(392,700)],
    "Франция":       [(523,200),(523,200),(523,200),(392,300),(440,300),(440,400),
                      (392,300),(349,300),(330,300),(294,300),(262,600),(262,400),(262,300)],
    "Великобритания":[(523,400),(523,200),(587,200),(494,300),(523,300),(587,300),
                      (784,600),(659,300),(523,300),(587,300),(523,800)],
    "Индия":         [(587,300),(587,300),(659,300),(698,300),(698,300),(784,500),
                      (659,300),(659,300),(587,500),(587,700)],
    "Япония":        [(659,600),(698,400),(784,600),(880,600),(988,500),(880,500),
                      (698,600),(659,500),(587,600),(659,900)],
    "Италия":        [(523,300),(523,300),(523,400),(659,500),(523,400),(523,300),
                      (494,300),(440,400),(494,500),(523,800)],
    "Казахстан":     [(440,300),(523,300),(587,400),(659,500),(587,300),(523,300),
                      (494,500),(440,700)],
    "Бразилия":      [(523,300),(523,300),(659,300),(698,400),(659,300),(587,300),
                      (523,400),(494,300),(440,700)],
    "Турция":        [(440,400),(440,400),(523,400),(587,300),(523,300),(494,400),
                      (440,300),(392,300),(349,700)],
    "Иран":          [(440,400),(523,400),(587,500),(523,300),(494,300),(440,400),
                      (392,500),(349,700)],
    "Польша":        [(587,300),(659,300),(698,400),(698,300),(659,300),(587,400),
                      (523,300),(494,300),(523,700)],
    "Испания":       [(523,300),(587,300),(698,500),(659,300),(587,300),(523,400),
                      (494,300),(440,700)],
    "Украина":       [(659,400),(659,300),(587,300),(523,400),(587,300),(659,300),
                      (698,500),(659,700)],
    "Египет":        [(440,400),(523,300),(587,500),(523,300),(440,400),
                      (392,400),(349,700)],
    "ЮАР":           [(440,400),(523,400),(587,500),(659,400),(587,300),(523,500),(440,700)],
    "Аргентина":     [(523,400),(587,300),(659,400),(587,300),(523,500),(494,300),(440,700)],
    "Австралия":     [(494,400),(587,300),(659,400),(698,500),(659,300),(587,400),(523,700)],
}

class Sound:
    @staticmethod
    def _b(pattern):
        if not SOUND_ON: return
        try:
            for f,d in pattern: winsound.Beep(int(f), int(d))
        except Exception: pass
    @staticmethod
    def war():     Sound._b([(600,180),(500,180),(700,180),(500,180)])
    @staticmethod
    def victory(): Sound._b([(400,180),(500,180),(600,180),(800,350)])
    @staticmethod
    def defeat():  Sound._b([(400,250),(300,250),(200,400)])
    @staticmethod
    def diplomacy(): Sound._b([(500,120),(700,120)])
    @staticmethod
    def tech():    Sound._b([(500,150),(700,150),(900,250)])
    @staticmethod
    def turn():    Sound._b([(500,80)])
    @staticmethod
    def message(): Sound._b([(600,100),(750,100)])
    @staticmethod
    def proposal(): Sound._b([(500,150),(700,150),(500,150)])
    @staticmethod
    def nuke():    Sound._b([(150,900),(100,1200)])
    @staticmethod
    def anthem(name):
        if not SOUND_ON: return
        if name not in ANTHEMS: return
        def _play():
            try:
                for f, d in ANTHEMS[name]:
                    winsound.Beep(int(f), int(d))
            except Exception: pass
        threading.Thread(target=_play, daemon=True).start()

INTENTS = [
    "develop_army","develop_economy","develop_stability","develop_science",
    "collect_taxes","diplomacy_alliance","diplomacy_peace","diplomacy_trade",
    "diplomacy_gift","declare_war","nuke","research","change_law","show_research",
    "show_laws","show_techs","show_map","chat_country","ask_info","suppress_revolt",
    "end_turn","invalid",
]
SOCIETY_TYPES = {
    "Демократия":{"eco":5,"arm":-5,"sta":3,"sci":5,"desc":"Свобода, выборы"},
    "Авторитаризм":{"eco":-3,"arm":10,"sta":5,"sci":-5,"desc":"Вертикаль власти"},
    "Монархия":{"eco":0,"arm":3,"sta":3,"sci":-3,"desc":"Власть по наследству"},
    "Коммунизм":{"eco":-5,"arm":5,"sta":5,"sci":-3,"desc":"Государство решает"},
    "Теократия":{"eco":-5,"arm":0,"sta":10,"sci":-10,"desc":"Религия управляет"},
    "Олигархия":{"eco":8,"arm":-3,"sta":-5,"sci":3,"desc":"Власть кланов"},
    "Анархия":{"eco":5,"arm":-10,"sta":-10,"sci":5,"desc":"Нет власти"},
    "Фашизм":{"eco":-10,"arm":15,"sta":5,"sci":-15,"desc":"Культ силы"},
}
STRICTNESS_LEVELS = {
    "Отсутствующая":{"eco":3,"sta":-5,"sci":2,"desc":"Анархия"},
    "Мягкая":{"eco":2,"sta":-2,"sci":1,"desc":"Минимум ограничений"},
    "Умеренная":{"eco":0,"sta":0,"sci":0,"desc":"Баланс"},
    "Строгая":{"eco":-3,"sta":5,"sci":-3,"desc":"Много запретов"},
    "Жёсткая":{"eco":-5,"sta":8,"sci":-5,"desc":"Строгий контроль"},
    "Репрессивная":{"eco":-8,"sta":10,"sci":-8,"desc":"Карательные меры"},
    "Тотальная":{"eco":-12,"sta":12,"sci":-12,"desc":"Полный контроль"},
}
MODERNITY_LEVELS = {
    "Архаичные":{"eco":-5,"sta":3,"sci":-10,"desc":"Средневековье"},
    "Устаревшие":{"eco":-3,"sta":2,"sci":-7,"desc":"Прошлый век"},
    "Устаревающие":{"eco":-1,"sta":1,"sci":-3,"desc":"Пора обновлять"},
    "Современные":{"eco":0,"sta":0,"sci":0,"desc":"Соответствуют эпохе"},
    "Прогрессивные":{"eco":1,"sta":-1,"sci":5,"desc":"Передовые"},
    "Инновационные":{"eco":2,"sta":-3,"sci":10,"desc":"Мировые тренды"},
    "Футуристические":{"eco":0,"sta":-5,"sci":15,"desc":"Завтрашний день"},
}
TECHS = [
    {"id":"tools","name":"Станки","cost":40,"sci":15,"eff":{"eco":5}},
    {"id":"steam","name":"Паровые машины","cost":60,"sci":25,"eff":{"eco":6,"arm":3}},
    {"id":"rail","name":"Железные дороги","cost":90,"sci":35,"eff":{"eco":10,"arm":5}},
    {"id":"telegraph","name":"Телеграф","cost":55,"sci":30,"eff":{"sta":3,"sci":3}},
    {"id":"medicine","name":"Антибиотики","cost":100,"sci":45,"eff":{"sta":10,"eco":3}},
    {"id":"radio","name":"Радио","cost":110,"sci":50,"eff":{"sta":5,"sci":5}},
    {"id":"tanks","name":"Танки","cost":140,"sci":55,"eff":{"arm":15}},
    {"id":"aviation","name":"Авиация","cost":170,"sci":65,"eff":{"arm":12,"eco":8}},
    {"id":"computers","name":"Компьютеры","cost":200,"sci":70,"eff":{"sci":15,"eco":10}},
    {"id":"internet","name":"Интернет","cost":240,"sci":78,"eff":{"sci":20,"eco":15}},
    {"id":"nuclear","name":"Ядерное оружие","cost":300,"sci":82,"eff":{"arm":40,"sta":5}},
    {"id":"space","name":"Космос","cost":380,"sci":90,"eff":{"sci":25,"sta":15}},
]
REGION = {
    "Россия":"Европа","Германия":"Европа","Франция":"Европа","Польша":"Европа",
    "Великобритания":"Европа","Турция":"Европа","Испания":"Европа","Италия":"Европа",
    "Украина":"Европа",
    "Китай":"Азия","Индия":"Азия","Япония":"Азия","Иран":"Азия","Казахстан":"Азия",
    "США":"Америка","Бразилия":"Америка","Аргентина":"Америка",
    "Египет":"Африка","ЮАР":"Африка","Австралия":"Океания",
}
NEIGHBORS = {
    "Россия":["Польша","Германия","Франция","Турция","Иран","Китай","Япония","Великобритания","Украина","Казахстан"],
    "США":["Бразилия","Великобритания","Япония","Китай","Франция","Аргентина","Австралия"],
    "Китай":["Россия","Индия","Япония","Иран","США","Казахстан","Австралия"],
    "Германия":["Франция","Польша","Россия","Великобритания","Турция","Италия","Украина"],
    "Франция":["Германия","Польша","Великобритания","Россия","Турция","США","Испания","Италия"],
    "Индия":["Китай","Иран","Россия","Турция","Казахстан","Австралия"],
    "Бразилия":["США","Аргентина","ЮАР"],
    "Япония":["Китай","Россия","США","Австралия"],
    "Турция":["Россия","Иран","Германия","Франция","Польша","Индия","Украина","Италия","Египет"],
    "Иран":["Турция","Россия","Индия","Китай","Казахстан","Египет"],
    "Польша":["Германия","Россия","Франция","Великобритания","Турция","Украина"],
    "Великобритания":["Франция","Германия","Польша","Россия","США","Испания"],
    "Украина":["Россия","Польша","Турция","Германия"],
    "Казахстан":["Россия","Китай","Иран","Индия"],
    "Испания":["Франция","Италия","Великобритания"],
    "Италия":["Франция","Германия","Испания","Турция","Египет"],
    "Египет":["Турция","Иран","Италия","ЮАР"],
    "ЮАР":["Египет","Бразилия","Аргентина"],
    "Аргентина":["Бразилия","США","ЮАР"],
    "Австралия":["Япония","Китай","Индия","США"],
}
RESOURCES = {
    "Россия":{"Нефть":8,"Газ":6,"Зерно":4},"США":{"Нефть":5,"Технологии":8,"Зерно":6},
    "Китай":{"Промтовары":10,"Редкозем":5,"Рис":8},"Германия":{"Машины":8,"Химия":5},
    "Франция":{"Вино":4,"Авиация":5,"Парфюм":3},"Индия":{"Рис":8,"Специи":6,"IT":4},
    "Бразилия":{"Кофе":6,"Соя":5,"Железо":4},"Япония":{"Электроника":10,"Авто":8,"Роботы":5},
    "Турция":{"Текстиль":6,"Продукты":4},"Иран":{"Нефть":7,"Газ":4},
    "Польша":{"Продукты":4,"Мебель":3},"Великобритания":{"Финансы":10,"Фарма":5},
    "Украина":{"Зерно":7,"Металл":5},"Казахстан":{"Нефть":5,"Металл":6},
    "Испания":{"Вино":3,"Туризм":5},"Италия":{"Мода":5,"Машины":4,"Продукты":4},
    "Египет":{"Хлопок":4,"Туризм":3},"ЮАР":{"Золото":6,"Алмазы":4},
    "Аргентина":{"Мясо":5,"Зерно":5},"Австралия":{"Железо":6,"Шерсть":4,"Золото":3},
}
FACTION_NAMES = ["Военные", "Бизнес", "Народ", "Элита"]
FACTION_EFFECTS = {
    "army":{"Военные":+5,"Бизнес":-2,"Народ":-1,"Элита":+1},
    "economy":{"Военные":-1,"Бизнес":+5,"Народ":+2,"Элита":+2},
    "stability":{"Военные":+2,"Бизнес":0,"Народ":+3,"Элита":+2},
    "science":{"Военные":0,"Бизнес":+1,"Народ":+1,"Элита":+2},
    "taxes":{"Военные":0,"Бизнес":-8,"Народ":-6,"Элита":-3},
    "war":{"Военные":+10,"Бизнес":-5,"Народ":-3,"Элита":-2},
    "war_win":{"Военные":+5,"Бизнес":-1,"Народ":+5,"Элита":+3},
    "war_lose":{"Военные":-8,"Бизнес":-3,"Народ":-5,"Элита":-5},
    "alliance":{"Военные":+2,"Бизнес":+3,"Народ":+1,"Элита":+3},
    "trade":{"Военные":0,"Бизнес":+4,"Народ":+2,"Элита":+2},
    "peace":{"Военные":-3,"Бизнес":+4,"Народ":+3,"Элита":+1},
    "gift_out":{"Военные":0,"Бизнес":-2,"Народ":0,"Элита":+2},
    "tech":{"Военные":+2,"Бизнес":+1,"Народ":0,"Элита":+3},
    "nuke":{"Военные":+15,"Бизнес":-25,"Народ":-35,"Элита":-25},
}

TRAINING_DATA = [
    ("развивай армию","develop_army"),("увеличь армию","develop_army"),
    ("усиль войска","develop_army"),("наращивай войска","develop_army"),
    ("мобилизуй солдат","develop_army"),("построй дивизии","develop_army"),
    ("купи танки","develop_army"),("тренируй солдат","develop_army"),
    ("военный бюджет","develop_army"),("развивай оборону","develop_army"),
    ("призови резервистов","develop_army"),("укрепи силы","develop_army"),
    ("расширь армию","develop_army"),("закупи оружие","develop_army"),
    ("призови новобранцев","develop_army"),("собери армию","develop_army"),
    ("вложи в вооружение","develop_army"),("усиль флот","develop_army"),
    ("построй самолёты","develop_army"),("развивай впк","develop_army"),
    ("усиль генеральный штаб","develop_army"),("усиль ракетные войска","develop_army"),
    ("нарасти военный потенциал","develop_army"),("укрепи вооружённые силы","develop_army"),
    ("создай новые полки","develop_army"),("обнови военную технику","develop_army"),
    ("развивай экономику","develop_economy"),("улучши экономику","develop_economy"),
    ("инвестируй в промышленность","develop_economy"),("строй заводы","develop_economy"),
    ("развивай бизнес","develop_economy"),("вкладывай в производство","develop_economy"),
    ("реформируй экономику","develop_economy"),("наращивай ввп","develop_economy"),
    ("оживи рынок","develop_economy"),("развивай инфраструктуру","develop_economy"),
    ("экономический рост","develop_economy"),("поддержи бизнес","develop_economy"),
    ("инвестиции","develop_economy"),("подними промышленность","develop_economy"),
    ("строй дороги","develop_economy"),("привлеки инвестиции","develop_economy"),
    ("развивай экспорт","develop_economy"),("модернизируй производство","develop_economy"),
    ("строй электростанции","develop_economy"),("развивай добычу","develop_economy"),
    ("укрепи стабильность","develop_stability"),("успокой народ","develop_stability"),
    ("подними стабильность","develop_stability"),("наведи порядок","develop_stability"),
    ("укрепи власть","develop_stability"),("успокой протесты","develop_stability"),
    ("запусти пропаганду","develop_stability"),("повысь доверие","develop_stability"),
    ("снизь напряжённость","develop_stability"),("успокой население","develop_stability"),
    ("проведи реформы","develop_stability"),("улучши жизнь","develop_stability"),
    ("подними рейтинг","develop_stability"),("укрепи порядок","develop_stability"),
    ("усиль пропаганду","develop_stability"),("укрепи полицию","develop_stability"),
    ("развивай науку","develop_science"),("улучши науку","develop_science"),
    ("вложи в науку","develop_science"),("финансируй науку","develop_science"),
    ("развивай образование","develop_science"),("развивай университеты","develop_science"),
    ("строй лаборатории","develop_science"),("поддержи учёных","develop_science"),
    ("инвестируй в науку","develop_science"),("повысь науку","develop_science"),
    ("спонсируй исследования","develop_science"),("академия наук","develop_science"),
    ("развивай рнд","develop_science"),("привлеки учёных","develop_science"),
    ("научный прогресс","develop_science"),("развивай технологии","develop_science"),
    ("собери налоги","collect_taxes"),("подними налоги","collect_taxes"),
    ("повысь налоги","collect_taxes"),("собирай подати","collect_taxes"),
    ("налоговая реформа","collect_taxes"),("пополни казну","collect_taxes"),
    ("увеличь сбор","collect_taxes"),("доходы бюджета","collect_taxes"),
    ("обложи налогом","collect_taxes"),("пополни бюджет","collect_taxes"),
    ("наполни казну","collect_taxes"),("собери деньги","collect_taxes"),
    ("введи налог","collect_taxes"),("повысь ставку","collect_taxes"),
    ("собери дань","collect_taxes"),("ужесточи налоги","collect_taxes"),
    ("заключи союз","diplomacy_alliance"),("предложи союз","diplomacy_alliance"),
    ("найди союзника","diplomacy_alliance"),("вступи в альянс","diplomacy_alliance"),
    ("создай союз","diplomacy_alliance"),("военный союз","diplomacy_alliance"),
    ("построй коалицию","diplomacy_alliance"),("найди партнёра","diplomacy_alliance"),
    ("союз с китаем","diplomacy_alliance"),("альянс с сша","diplomacy_alliance"),
    ("подружись с индией","diplomacy_alliance"),("союз с германией","diplomacy_alliance"),
    ("заключи союз с россией","diplomacy_alliance"),("создай альянс","diplomacy_alliance"),
    ("договорись о союзе","diplomacy_alliance"),("военный пакт","diplomacy_alliance"),
    ("подпиши союзный договор","diplomacy_alliance"),("объедини усилия","diplomacy_alliance"),
    ("заключи мир","diplomacy_peace"),("предложи мир","diplomacy_peace"),
    ("мирный договор","diplomacy_peace"),("перемирие","diplomacy_peace"),
    ("закончи войну","diplomacy_peace"),("останови войну","diplomacy_peace"),
    ("прекрати войну","diplomacy_peace"),("выйди из войны","diplomacy_peace"),
    ("мирное соглашение","diplomacy_peace"),("договорись о мире","diplomacy_peace"),
    ("подпиши мир","diplomacy_peace"),("сложи оружие","diplomacy_peace"),
    ("останови конфликт","diplomacy_peace"),("прекрати бои","diplomacy_peace"),
    ("закончи конфликт","diplomacy_peace"),("мир с польшей","diplomacy_peace"),
    ("торговое соглашение","diplomacy_trade"),("начни торговлю","diplomacy_trade"),
    ("экономическое сотрудничество","diplomacy_trade"),("торговый договор","diplomacy_trade"),
    ("обмен товарами","diplomacy_trade"),("торговые отношения","diplomacy_trade"),
    ("торговля","diplomacy_trade"),("торгуй","diplomacy_trade"),
    ("открой рынки","diplomacy_trade"),("наладь торговлю","diplomacy_trade"),
    ("торгуй с германией","diplomacy_trade"),("торгуй с китаем","diplomacy_trade"),
    ("торговля с сша","diplomacy_trade"),("экономические связи","diplomacy_trade"),
    ("отправь подарок","diplomacy_gift"),("подари деньги","diplomacy_gift"),
    ("отправь помощь","diplomacy_gift"),("задобри страну","diplomacy_gift"),
    ("спонсируй","diplomacy_gift"),("купи лояльность","diplomacy_gift"),
    ("помоги деньгами","diplomacy_gift"),("сделай подарок","diplomacy_gift"),
    ("отправь золото","diplomacy_gift"),("отправь дары","diplomacy_gift"),
    ("подкупи","diplomacy_gift"),("дай кредит","diplomacy_gift"),
    ("объяви войну","declare_war"),("напади","declare_war"),
    ("атакуй","declare_war"),("война с","declare_war"),
    ("начни войну","declare_war"),("вторгнись","declare_war"),
    ("начни наступление","declare_war"),("разбомби","declare_war"),
    ("напади на польшу","declare_war"),("атакуй германию","declare_war"),
    ("война с турцией","declare_war"),("атакуй китай","declare_war"),
    ("объяви войну сша","declare_war"),("напади на иран","declare_war"),
    ("развяжи войну","declare_war"),("начни агрессию","declare_war"),
    ("применить ядерное оружие","nuke"),("применю ядерное оружие","nuke"),
    ("ядерный удар","nuke"),("ядерный удар по польше","nuke"),
    ("сбрось атомную бомбу","nuke"),("примени ядерку","nuke"),
    ("применить ядерку","nuke"),("атомная бомба","nuke"),
    ("сбрось бомбу","nuke"),("используй ядерное оружие","nuke"),
    ("ядерная атака","nuke"),("нанеси ядерный удар","nuke"),
    ("примени ядерное оружие против сша","nuke"),("пуск ракеты","nuke"),
    ("запусти ядерную ракету","nuke"),("примени оружие массового поражения","nuke"),
    ("сбрось ядерную бомбу","nuke"),("ядерная бомбардировка","nuke"),
    ("уничтожь ядерным ударом","nuke"),
    ("исследуй танки","research"),("изучить танки","research"),
    ("исследуй поезда","research"),("изучить поезда","research"),
    ("исследуй компьютеры","research"),("изучить компьютеры","research"),
    ("исследуй ядерное оружие","research"),("изучить ядерное оружие","research"),
    ("изучить ядерное","research"),("исследуй ядерное","research"),
    ("займись исследованием","research"),("начни исследование","research"),
    ("проведи исследование","research"),("исследуй технологию","research"),
    ("разработай технологию","research"),("изучи технологию","research"),
    ("исследуй космос","research"),("исследуй авиацию","research"),
    ("исследуй радио","research"),("исследуй интернет","research"),
    ("исследуй антибиотики","research"),("исследуй станки","research"),
    ("исследуй телеграф","research"),("исследуй медицину","research"),
    ("исследовать ядерное","research"),("открой ядерное оружие","research"),
    ("разработай ядерное","research"),
    ("смени закон","change_law"),("измени закон","change_law"),
    ("смени строй","change_law"),("смени тип общества","change_law"),
    ("ужесточи законы","change_law"),("ослабь законы","change_law"),
    ("обнови законы","change_law"),("прогрессивные законы","change_law"),
    ("перейди к демократии","change_law"),("установи авторитаризм","change_law"),
    ("введи коммунизм","change_law"),("установи монархию","change_law"),
    ("измени конституцию","change_law"),("реформируй законодательство","change_law"),
    ("сделай законы прогрессивными","change_law"),("смягчи законы","change_law"),
    ("покажи исследования","show_research"),("список исследований","show_research"),
    ("что можно исследовать","show_research"),("наука","show_research"),
    ("исследования","show_research"),("технологии","show_research"),
    ("покажи технологии","show_research"),("что изучаем","show_research"),
    ("покажи законы","show_laws"),("какие у нас законы","show_laws"),
    ("текущие законы","show_laws"),("покажи строй","show_laws"),
    ("какой у нас строй","show_laws"),("правовая система","show_laws"),
    ("покажи конституцию","show_laws"),
    ("покажи изобретения","show_techs"),("что мы изобрели","show_techs"),
    ("изученные технологии","show_techs"),("открытые технологии","show_techs"),
    ("покажи карту","show_map"),("карта","show_map"),
    ("карта мира","show_map"),("покажи мир","show_map"),
    ("открой карту","show_map"),("политическая карта","show_map"),
    ("поговорить с китаем","chat_country"),("чат с сша","chat_country"),
    ("написать германии","chat_country"),("связаться с францией","chat_country"),
    ("поговорить","chat_country"),("написать","chat_country"),
    ("пообщаться с индией","chat_country"),("связь с ираном","chat_country"),
    ("что происходит","ask_info"),("что в мире","ask_info"),
    ("как дела","ask_info"),("покажи состояние","ask_info"),
    ("статистика","ask_info"),("отчёт","ask_info"),
    ("ситуация","ask_info"),("доклад","ask_info"),
    ("подавить бунт","suppress_revolt"),("подави бунт","suppress_revolt"),
    ("подавить восстание","suppress_revolt"),("успокоить фракцию","suppress_revolt"),
    ("успокой фракцию","suppress_revolt"),("подавить недовольство","suppress_revolt"),
    ("разберись с бунтом","suppress_revolt"),("подавить мятеж","suppress_revolt"),
    ("утихомирить бунт","suppress_revolt"),("успокоить бунт","suppress_revolt"),
    ("укрепить лояльность","suppress_revolt"),("поднять лояльность","suppress_revolt"),
    ("успокоить фракции","suppress_revolt"),("успокоить элиты","suppress_revolt"),
    ("успокоить военных","suppress_revolt"),("успокоить бизнес","suppress_revolt"),
    ("заверши ход","end_turn"),("конец хода","end_turn"),
    ("пропустить","end_turn"),("дальше","end_turn"),
    ("следующий ход","end_turn"),("пас","end_turn"),
    ("хватит","end_turn"),("стоп","end_turn"),
    ("привет","invalid"),("как тебя зовут","invalid"),
    ("кто ты","invalid"),("спасибо","invalid"),
]
COUNTRY_STEMS = {
    "Россия":["росси","рф","москв"],"США":["сша","америк","штат","вашингтон"],
    "Китай":["кита","пекин","кнр"],"Германия":["герман","берлин","фрг"],
    "Франция":["франц","париж"],"Индия":["инди","дели"],
    "Бразилия":["бразил"],"Япония":["япон","токио"],
    "Турция":["турц","анкар"],"Иран":["иран","тегеран"],
    "Польша":["польш","варшав"],"Великобритания":["британ","англ","лондон"],
    "Украина":["украин","киев"],"Казахстан":["казах","астан"],
    "Испания":["испан","мадрид"],"Италия":["итал","рим"],
    "Египет":["егип","каир"],"ЮАР":["юар","южно-африк"],
    "Аргентина":["аргентин","буэнос"],"Австралия":["австрал","канберр"],
}
TECH_KEYWORDS = {
    "tools":["станк","механиз"],"steam":["пар","паров"],
    "rail":["поезд","железн","рельс","дорог"],"telegraph":["телеграф"],
    "medicine":["медицин","антибиот"],"radio":["радио"],
    "tanks":["танк","брон"],"aviation":["авиац","самолёт","летат"],
    "computers":["компьютер","комп","эвм"],"internet":["интернет","сеть"],
    "nuclear":["ядерн","атомн","бомб"],"space":["космос","ракет","спутник"],
}
VOCAB_SIZE = 60000
def featurize(text):
    t = " " + text.lower().strip() + " "
    feats = {}
    for i in range(len(t)-1):
        h = zlib.crc32(t[i:i+2].encode("utf-8")) % VOCAB_SIZE
        feats[h] = feats.get(h,0.0)+1.0
    for i in range(len(t)-2):
        h = zlib.crc32(t[i:i+3].encode("utf-8")) % VOCAB_SIZE
        feats[h] = feats.get(h,0.0)+1.5
    for word in t.split():
        if len(word)>2:
            h = zlib.crc32(("W"+word).encode("utf-8")) % VOCAB_SIZE
            feats[h] = feats.get(h,0.0)+3.0
    n = math.sqrt(sum(v*v for v in feats.values()))
    if n>0:
        for k in list(feats.keys()): feats[k] /= n
    return feats

class MultiHeadNet:
    def __init__(self, head_sizes, vocab_size=VOCAB_SIZE, seed=42):
        self.vocab_size = vocab_size; self.head_sizes = head_sizes
        self.W = {n:[dict() for _ in range(k)] for n,k in head_sizes.items()}
        self.b = {n:[0.0]*k for n,k in head_sizes.items()}
        self.rng = random.Random(seed)
    def nominal_params(self): return self.vocab_size*sum(self.head_sizes.values())
    def actual_params(self):
        return sum(len(w) for h in self.W.values() for w in h) + sum(len(b) for b in self.b.values())
    def _scores(self, feats, head):
        n = self.head_sizes[head]; scores = list(self.b[head]); W = self.W[head]
        for f,v in feats.items():
            for c in range(n):
                w = W[c].get(f)
                if w is not None: scores[c] += w*v
        return scores
    @staticmethod
    def _softmax(scores):
        mx = max(scores); exps = [math.exp(s-mx) for s in scores]
        s = sum(exps); return [e/s for e in exps]
    def predict(self, feats, head):
        sc = self._scores(feats, head); pr = self._softmax(sc)
        idx = max(range(len(pr)), key=lambda i: pr[i]); return idx, pr[idx]
    def _step(self, feats, y, head, lr):
        sc = self._scores(feats, head); pr = self._softmax(sc)
        n = self.head_sizes[head]; W = self.W[head]; b = self.b[head]
        for c in range(n):
            g = pr[c] - (1.0 if c==y else 0.0)
            if g==0.0: continue
            b[c] -= lr*g; Wc = W[c]
            for f,v in feats.items(): Wc[f] = Wc.get(f,0.0) - lr*g*v
    def accuracy(self, data, head):
        if not data: return 0.0
        correct = 0
        for feats,y in data:
            sc = self._scores(feats, head)
            if max(range(len(sc)), key=lambda i: sc[i]) == y: correct += 1
        return correct/len(data)
    def train(self, examples, label_maps, head="intent", epochs=500,
              lr_init=0.6, lr_final=0.05, verbose=True):
        if verbose: print(clr("   → векторизация текстов...", C.Cy))
        lab = label_maps[head]; featurized = []
        for t,l in examples:
            if l in lab: featurized.append((featurize(t), lab[l]))
        rng = random.Random(42); idxs = list(range(len(featurized)))
        rng.shuffle(idxs); v = max(1, len(idxs)//10); vi = set(idxs[:v])
        train_data = [featurized[i] for i in range(len(featurized)) if i not in vi]
        val_data = [featurized[i] for i in sorted(vi)]
        order = list(range(len(train_data))); t0 = time.time()
        if verbose: print(f"   → train: {len(train_data)}, val: {len(val_data)}\n")
        for epoch in range(epochs+1):
            frac = epoch/max(1,epochs); lr = lr_init*(1-frac)+lr_final*frac
            self.rng.shuffle(order)
            for i in order:
                feats,y = train_data[i]; self._step(feats,y,head,lr)
            if verbose and (epoch%50==0 or epoch==epochs):
                tr = self.accuracy(train_data, head); va = self.accuracy(val_data, head)
                el = time.time()-t0; pct = epoch/max(1,epochs)
                bw = 26; f = int(bw*pct); bar = "█"*f + "░"*(bw-f)
                sys.stdout.write(f"\r   [{bar}] {int(pct*100):3d}% | эп {epoch:4d}/{epochs} | tr {tr*100:5.1f}% | val {va*100:5.1f}% | {el:4.1f}с   ")
                sys.stdout.flush()
        if verbose:
            sys.stdout.write("\r" + " "*140 + "\r")
            el = time.time()-t0
            tr = self.accuracy(train_data, head); va = self.accuracy(val_data, head)
            print(clr(f"   ✅ Обучение завершено за {el:.1f} сек", C.G))
            print(f"      Точность train: {tr*100:.2f}%   val: {va*100:.2f}%")
        return self

NARRATIVE = """
советники докладывают о растущем напряжении на границах страны
народ встречает новость с воодушевлением на площадях столицы
генералы предлагают укрепить оборонительные рубежи государства
дипломаты отмечают рост напряжённости в отношениях между державами
биржи отреагировали ростом котировок на решение правительства
разведка доносит о переброске вражеских войск у наших границ
экономисты фиксируют умеренный рост ключевых показателей
пропаганда работает над образом сильного и решительного лидера
"""
class MarkovNarrator:
    def __init__(self, corpus):
        w = corpus.lower().split(); self.tri = {}
        for a,b,c in zip(w,w[1:],w[2:]): self.tri.setdefault((a,b),[]).append(c)
        self.starters = [(a,b) for (a,b) in self.tri if len(a)>3 and len(b)>3]
    def generate(self, length=14):
        if not self.starters: return "События развиваются своим чередом."
        a,b = random.choice(self.starters); ws = [a,b]
        for _ in range(length-2):
            nxt = self.tri.get((a,b),[])
            if not nxt: break
            c = random.choice(nxt); ws.append(c); a,b = b,c
        t = " ".join(ws); t = t[0].upper() + t[1:]
        if not t.endswith("."): t += "."
        return t

class CountryDialog:
    def __init__(self, target, player, game):
        self.target = target; self.player = player; self.game = game
        self.history = []; self.pending = None
    def context(self):
        if self.target.name in self.player.at_war_with: return "war"
        if self.target.name in self.player.allies: return "ally"
        ratio = self.target.power() / max(1.0, self.player.power())
        if ratio < 0.6: return "weak"
        if ratio > 1.7: return "strong"
        return "neutral"
    TOPIC_KEYS = {
        "war_threat":["войн","атак","угроз","уничтож","бомб","вторгну","напад","удар"],
        "alliance_offer":["союз","альянс","партнёр","объедин"],
        "trade_offer":["торг","сделк","сотруднич","обмен","контракт"],
        "gift_offer":["подар","дар","золот","дам денег","помощь","кредит"],
        "peace_offer":["мир","перемири","прекрат","оконч","не воюй"],
        "insult":["слаб","дурак","глуп","ничто","ничтож","трус"],
        "compliment":["уважаем","уважаю","сильн","могущест","восхища"],
        "joke":["анекдот","шутк","пошути","смешн"],
        "about_econ":["экономик","богат","финанс","ввп","промышлен"],
        "about_army":["армия","солдат","войск","флот","вооруж"],
        "about_tech":["наук","технолог","изобрет"],
        "about_pop":["населен","жител","граждан"],
        "about_geo":["где вы","далеко","границ","сосед"],
        "about_self":["о себе","расскажи о","кто вы","кто ты"],
        "how_are_you":["как дела","как жизнь","как ты"],
        "thanks":["спасибо","благодар"],
        "bye":["пока","до свидан","прощай"],
        "greeting":["привет","здравств","добр"],
    }
    def detect_topic(self, msg):
        low = msg.lower()
        for topic in ["war_threat","alliance_offer","trade_offer","gift_offer","peace_offer",
                    "insult","compliment","joke","about_econ","about_army","about_tech",
                    "about_pop","about_geo","about_self","how_are_you","thanks","bye","greeting"]:
            for k in self.TOPIC_KEYS[topic]:
                if k in low: return topic
        return "unknown"
    def _is_agree(self, low): return any(w in low for w in ["да","согласен","подпис","принима","ок","давай","хорошо"])
    def _is_disagree(self, low): return any(w in low for w in ["нет","отказ","не хочу","не буду","отмен","не согласен"])
    def respond(self, msg):
        low = msg.lower(); self.history.append(("player", msg))
        if self.pending:
            if self._is_agree(low): reply = self._execute_pending(); self.history.append(("target", reply)); return reply
            if self._is_disagree(low):
                self.pending = None
                reply = random.choice(["Как хотите.","Жаль.","Понимаем."])
                self.history.append(("target", reply)); return reply
            topic = {"trade":"trade_offer","alliance":"alliance_offer",
                     "gift":"gift_offer","peace":"peace_offer"}[self.pending]
        else:
            topic = self.detect_topic(msg)
            if topic in ("trade_offer","alliance_offer","gift_offer","peace_offer"):
                self.pending = {"trade_offer":"trade","alliance_offer":"alliance",
                                "gift_offer":"gift","peace_offer":"peace"}[topic]
        ctx = self.context(); reply = self._build_reply(topic, ctx, msg)
        self.history.append(("target", reply))
        if len(self.history) > 30: self.history = self.history[-30:]
        return reply
    def _execute_pending(self):
        action = self.pending; self.pending = None
        result = self.game.do_diplomacy(self.target, action)
        confirm = {"trade":"Отлично! Подписываем.","alliance":"Союз заключён!",
                   "gift":"Благодарим!","peace":"Мир подписан."}[action]
        return f"{confirm}  [{result}]"
    def _build_reply(self, topic, ctx, msg):
        t = self.target; p = self.player
        if ctx == "war":
            if topic == "peace_offer":
                ratio = t.power() / max(1.0, p.power())
                dur = self.game.war_duration(t, p)
                if dur >= 4 or ratio < 0.7: return "Мы устали. Обсудим условия?"
                if ratio > 1.5: return "Зачем нам мир?"
                return "Пока идёт война — нет диалога."
            if topic in ("alliance_offer","trade_offer","gift_offer"): return "Во время войны это невозможно."
            if topic == "greeting": return "У нас нет времени на любезности."
            return "Ответ — нет."
        if ctx == "ally":
            if topic == "greeting": return "Привет, брат!"
            if topic == "how_are_you": return "Справляемся. Вместе мы сильны."
            if topic == "alliance_offer": return "Мы уже союзники."
            if topic == "trade_offer": return "Всегда рады торговле."
            if topic == "gift_offer": return "Щедрость ваша тронула нас."
            if topic == "war_threat": return "Угрозы союзнику? Странно."
            if topic == "compliment": return "Взаимно."
            if topic == "insult": return "Обидно слышать это от союзника."
            return "Мы готовы поддержать вас."
        if topic == "greeting":
            if ctx == "weak": return "Приветствуем вас, могущественный сосед!"
            if ctx == "strong": return "Здравствуйте. Мы слушаем."
            return "Рады слышать от вас."
        if topic == "how_are_you": return f"Всё по плану. Экономика {t.economy}, армия {t.army}."
        if topic == "about_self": return f"Мы — {t.name}. Строй: {t.law_society}."
        if topic == "about_econ": return f"Экономика {t.economy}, казна {t.money}."
        if topic == "about_army": return f"Армия — {t.army} дивизий."
        if topic == "about_pop": return f"У нас {t.population:.0f} млн граждан."
        if topic == "about_geo": return f"Мы в регионе {REGION.get(t.name,'?')}."
        if topic == "about_tech": return f"Наука {t.science}, открыто {len(t.techs)} технологий."
        if topic == "joke": return "Дипломат обещал мир, а объявил войну."
        if topic == "thanks": return "Всегда рады."
        if topic == "bye": return "До свидания."
        if topic == "alliance_offer":
            if ctx == "weak": return "Союз с вами — честь! Подтверждаем?"
            if ctx == "strong": return "Зачем нам союз с вами?"
            return "Союз возможен. Подтверждаете?"
        if topic == "peace_offer": return "Мы не воюем с вами."
        if topic == "trade_offer":
            if ctx == "weak": return "Конечно! Подтверждаете?"
            if ctx == "strong": return "Торговля на наших условиях. Согласны?"
            return "Готовы обсудить. Заключаем?"
        if topic == "gift_offer":
            if ctx == "strong": return "Подарок? Смешно. Но примем."
            return "Щедро! Принимаем?"
        if topic == "war_threat":
            if ctx == "weak": return "Мы не хотим войны! Умоляем..."
            if ctx == "strong": return "Ваши угрозы смешны."
            return "Не советуем угрожать."
        if topic == "compliment": return random.choice(["Благодарим.","Взаимно."])
        if topic == "insult":
            if ctx == "strong": return "Нам плевать."
            if ctx == "weak": return "Простите, если обидели..."
            return "Следите за словами."
        if ctx == "weak": return "Слушаем вас..."
        if ctx == "strong": return "Говорите по существу."
        return "Понятно. Что-то ещё?"

REPLY_TEMPLATES = {
    "develop_army":["Приказываю мобилизовать новые силы."],
    "develop_economy":["Приступаю к экономическим реформам."],
    "develop_stability":["Работаю с народом."],
    "develop_science":["Открываю новые лаборатории."],
    "collect_taxes":["Объявляю сбор налогов."],
    "diplomacy_alliance":["Отправляю дипломатическую миссию."],
    "diplomacy_peace":["Отправляю мирную инициативу."],
    "diplomacy_trade":["Начинаю торговые переговоры."],
    "diplomacy_gift":["Отправляю дары."],
    "declare_war":["Объявляю войну!"],
    "nuke":["☢️ ГОТОВЛЮ ЯДЕРНЫЙ УДАР!"],
    "research":["Запускаю исследование."],
    "change_law":["Провожу реформу законодательства."],
    "show_research":["Вот список исследований."],
    "show_laws":["Вот правовая система."],
    "show_techs":["Вот наши технологии."],
    "show_map":["Разворачиваю карту."],
    "chat_country":["Открываю канал связи..."],
    "ask_info":["Докладываю."],
    "suppress_revolt":["Подавляю бунт."],
    "end_turn":["Передаю слово советникам."],
    "invalid":["Не понял команду."],
}
NEEDS_TARGET = {"diplomacy_alliance","diplomacy_peace","diplomacy_trade",
                "diplomacy_gift","declare_war","chat_country","nuke"}
CHAT_TRIGGERS = ["поговор","чат с","написать","пообщат","связаться","связь с",
                 "поболтат","общатьс","диалог с","побеседов","разговор с"]
NUKE_TRIGGERS = ["ядерный удар","ядерн удар","примен ядерн","примени ядерн",
                 "применить ядерн","применю ядерн",
                 "примени ядерку","применить ядерку","применю ядерку",
                 "сбрось ядерн","сбросить ядерн","сбрось атомн","сбросить атомн",
                 "запусти ядерн","запусти атомн","нанеси ядерн","используй ядерн",
                 "примени оружие массового","применю оружие массового",
                 "ядерн атака","ядерн бомбардировк"]
REVOLT_TRIGGERS = ["бунт","восстани","мятеж","подавить недоволь"]

HELP_TEXT = f"""
{clr('═══ СПРАВКА ═══', C.Cy)}
{clr('🛠 ВНУТРЕННЯЯ', C.Y)}    развивай армию / экономику / науку / стабильность / налоги
{clr('👊 БУНТ', C.Y)}         «подавить бунт» — успокоить нелояльную фракцию (30💰)
{clr('🔬 НАУКА', C.Y)}        «покажи исследования»  «исследуй танки»
                     «изучить ядерное оружие» — исследование ЯО
{clr('⚖️ ЗАКОНЫ', C.Y)}       «покажи законы»  «смени строй на демократию»
{clr('🤝 ДИПЛОМАТИЯ', C.Y)}    союз с Китаем / мир с Польшей / торговля с США
{clr('⚔️ ВОЙНА', C.Y)}         война с Польшей (только с соседями!)
{clr('☢️ ЯДЕРКА', C.Y)}       «применить ядерное оружие против США»
                     (РФ, США, Китай, Франция, Великобритания, Индия — уже имеют ЯО)
                     ⚠️ После удара мир осуждает 10 ходов
{clr('🗺 КАРТА', C.Y)}         «карта»
{clr('💬 ЧАТ', C.Y)}           «поговорить с Китаем»
{clr('ℹ️ ПРОЧЕЕ', C.Y)}        «что в мире?»  «дальше»  «меню»  «помощь»  «выход»
"""

class MasterBrain:
    def __init__(self):
        self._banner()
        print(clr("╔" + "═"*58 + "╗", C.M))
        print(clr("║  🧠 ОБУЧЕНИЕ НЕЙРОСЕТИ ИИ-МАСТЕРА" + " "*24 + "║", C.M))
        print(clr("╚" + "═"*58 + "╝", C.M))
        print(f"  Словарь: {VOCAB_SIZE:,}".replace(",", " "))
        print(f"  Классов: {len(INTENTS)}  •  Примеров: {len(TRAINING_DATA)}\n")
        label_map = {lbl:i for i,lbl in enumerate(INTENTS)}
        self.label_map = label_map
        self.net = MultiHeadNet({"intent": len(INTENTS)})
        self.net.train(TRAINING_DATA, {"intent": label_map}, head="intent",
                       epochs=500, lr_init=0.6, lr_final=0.05)
        self.net.head_sizes["country"] = 20
        self.net.b["country"] = [0.0]*20
        self.net.W["country"] = [dict() for _ in range(20)]
        self.narrator = MarkovNarrator(NARRATIVE)
        print(clr("\n  ✅ Мозг мастера готов!\n", C.G))
    @staticmethod
    def _banner():
        os.system("cls" if os.name=="nt" else "clear")
        print(clr("╔" + "═"*62 + "╗", C.M))
        print(clr("║" + " "*62 + "║", C.M))
        print(clr("║" + "   P A X  H I S T O R I A — ULTIMATE v5.8".center(62) + "║", C.Bold+C.M))
        print(clr("║" + "  👊 Бунт • 🎵 Гимны • ☢️ Ядерка".center(62) + "║", C.Cy))
        print(clr("║" + " "*62 + "║", C.M))
        print(clr("╚" + "═"*62 + "╝", C.M))
    def _extract_country(self, text, names):
        t = text.lower()
        for n in names:
            for s in COUNTRY_STEMS.get(n, [n.lower()[:4]]):
                if s in t: return n
        return None
    def _extract_tech(self, text):
        t = text.lower()
        for tid, keys in TECH_KEYWORDS.items():
            for k in keys:
                if k in t: return tid
        return None
    def _extract_law(self, text):
        t = text.lower()
        for name in SOCIETY_TYPES:
            if name.lower()[:5] in t: return ("society", name)
        for name in STRICTNESS_LEVELS:
            if name.lower()[:5] in t: return ("strictness", name)
        for name in MODERNITY_LEVELS:
            if name.lower()[:5] in t: return ("modernity", name)
        if any(w in t for w in ["ужесточ","жёстч","репресс"]): return ("strictness","Репрессивная")
        if any(w in t for w in ["смягч","ослаб","либерал"]): return ("strictness","Мягкая")
        if any(w in t for w in ["прогресс","передов","инновац"]): return ("modernity","Прогрессивные")
        if any(w in t for w in ["устарел","архаич"]): return ("modernity","Устаревшие")
        return (None, None)
    def interpret(self, text, names):
        low = text.lower()
        if any(k in low for k in REVOLT_TRIGGERS):
            return {"intent":"suppress_revolt","country":None,
                    "tech_id":None,"law_col":None,"law_val":None,
                    "confidence":1.0,"reply":"Подавляю бунт."}
        is_research_nuke = any(w in low for w in ["изуч","исслед","разработ","откр","освоить"])
        if any(k in low for k in NUKE_TRIGGERS) and not is_research_nuke:
            country = self._extract_country(text, names)
            if country:
                return {"intent":"nuke","country":country,
                        "tech_id":None,"law_col":None,"law_val":None,
                        "confidence":1.0,
                        "reply":f"☢️ Готовлю ядерный удар по {country}!"}
        if any(k in low for k in CHAT_TRIGGERS):
            country = self._extract_country(text, names)
            if country:
                return {"intent":"chat_country","country":country,
                        "tech_id":None,"law_col":None,"law_val":None,
                        "confidence":1.0,"reply":f"Открываю канал связи с {country}."}
        feats = featurize(text); idx, conf = self.net.predict(feats, "intent")
        intent = INTENTS[idx]
        country = self._extract_country(text, names) if intent in NEEDS_TARGET else None
        tech_id = self._extract_tech(text) if intent == "research" else None
        law_col, law_val = (None, None)
        if intent == "change_law": law_col, law_val = self._extract_law(text)
        reply = random.choice(REPLY_TEMPLATES.get(intent, ["..."]))
        if intent in NEEDS_TARGET and not country:
            conf *= 0.5; reply = "С какой страной?"
        if intent == "research" and not tech_id:
            conf *= 0.6; reply = "Что исследовать?"
        if intent == "change_law" and not law_col:
            conf *= 0.6; reply = "Какой закон менять?"
        return {"intent":intent,"country":country,"tech_id":tech_id,
                "law_col":law_col,"law_val":law_val,"confidence":conf,"reply":reply}
    def narrate(self, outcome):
        return self.narrator.generate(length=random.randint(12, 18))

class Country:
    def __init__(self, name, money, army, economy, stability, science, population):
        self.name = name; self.money = money; self.army = army
        self.economy = economy; self.stability = stability; self.science = science
        self.population = float(population)
        self.is_player = False
        self.at_war_with = set(); self.allies = set(); self.trades = set()
        self.alive = True; self.techs = set()
        self.law_society = "Авторитаризм"
        self.law_strictness = "Умеренная"
        self.law_modernity = "Современные"
        self.territory = {name}
        self.battles_lost = 0
        self.factions = {n: 70 for n in FACTION_NAMES}
        self.resources = dict(RESOURCES.get(name, {}))
    def has_nuke(self): return "nuclear" in self.techs
    def power(self):
        return self.army*1.2 + self.economy + self.stability*0.5 + self.science*0.7 + self.population*0.05
    def pop_pressure(self): return max(0.0, min(1.0, self.population/2000.0))
    def pop_growth(self):
        b = 1.0 + self.population*0.002
        if self.stability >= 70: b *= 1.4
        elif self.stability <= 25: b *= 0.5
        if self.economy >= 70: b *= 1.2
        elif self.economy <= 20: b *= 0.6
        if self.at_war_with: b *= 0.5
        b *= (1.0 - self.pop_pressure()*0.5)
        return max(0.1, b)
    def work_penalty(self): return 0.5 if self.population<30 else 0.75 if self.population<60 else 1.0
    def sci_penalty(self): return 0.5 if self.population<30 else 0.75 if self.population<60 else 1.0
    def law_mod(self, key):
        s = 0
        for tbl, n in ((SOCIETY_TYPES,self.law_society),(STRICTNESS_LEVELS,self.law_strictness),(MODERNITY_LEVELS,self.law_modernity)):
            s += tbl.get(n,{}).get(key,0)
        return s
    def faction_change(self, kind):
        for f, delta in FACTION_EFFECTS.get(kind, {}).items():
            self.factions[f] = max(0, min(100, self.factions[f] + delta))
    def faction_tick(self):
        stab = 0; money = 0; events = []
        for f in list(self.factions.keys()):
            loy = self.factions[f]
            if loy < 15 and random.random() < 0.30:
                stab -= 8; money -= 20
                events.append(f"💥 Бунт фракции «{f}» в {self.name}!")
            elif loy < 30: stab -= 2
            self.factions[f] += int((50 - self.factions[f]) * 0.05)
            self.factions[f] = max(0, min(100, self.factions[f]))
        return stab, money, events
    def trade_income(self, game):
        income = 0
        for pname in list(self.trades):
            p = game.get_country(pname)
            if p and p.alive and self.name in p.trades:
                income += 5 + int(min(self.economy, p.economy) * 0.1)
            else: self.trades.discard(pname)
        return income
    def resource_income(self): return int(sum(self.resources.values()) * 0.5)
    def show_stats(self):
        p = self
        g = p.pop_growth(); pr = p.pop_pressure()
        pi = "🟢" if pr<0.3 else "🟡" if pr<0.7 else "🔴"
        def line(inner): return clr("║", C.Cy) + pad(inner, 58) + clr("║", C.Cy)
        print(clr("╔" + "═"*58 + "╗", C.Cy))
        nuke_mark = clr(" ☢️", C.R) if p.has_nuke() else ""
        print(line(f"  🏛  {clr(p.name, C.Bold+C.Y)}{nuke_mark}"))
        print(clr("╠" + "═"*58 + "╣", C.Cy))
        print(line(f"  💰 Казна: {p.money:>4}   ⚔️ Армия: {p.army:>4}"))
        print(line(f"  🏭 Экономика: {p.economy:>4}   🕊️ Стабильность: {p.stability:>4}"))
        print(line(f"  🔬 Наука: {p.science:>4}   👥 {p.population:>6.1f} млн (+{g:.1f}/ход {pi})"))
        print(clr("╠" + "═"*58 + "╣", C.Cy))
        print(line(f"  ⚖️ {p.law_society} | {p.law_strictness} | {p.law_modernity}"))
        if len(p.territory) > 1:
            lands = ", ".join(sorted(p.territory - {p.name}))
            print(line(f"  🏴 Территория: {p.name} + {lands}"))
        print(clr("╠" + "═"*58 + "╣", C.Cy))
        fac_str = "  👥 "
        for f, loy in p.factions.items():
            icon = "🟢" if loy>=60 else "🟡" if loy>=30 else "🔴"
            fac_str += f"{f} {loy}{icon}  "
        print(line(fac_str.rstrip()))
        if p.resources:
            print(line("  📦 " + ", ".join(f"{k}({v})" for k,v in p.resources.items())))
        if p.trades:
            print(line("  💱 " + ", ".join(sorted(p.trades))))
        if p.allies:
            print(line(f"  🤝 Союзники: {', '.join(p.allies)}"))
        if p.at_war_with:
            print(line(f"  🔥 Войны: {', '.join(p.at_war_with)}"))
        if p.battles_lost > 0:
            print(line(f"  ⚠️ Поражений подряд: {p.battles_lost}/3"))
        print(clr("╚" + "═"*58 + "╝", C.Cy))

class Game:
    def __init__(self, brain):
        self.countries = []; self.turn = 1; self.max_turns = 50
        self.player = None; self.brain = brain
        self.war_started = {}
        self.world_anger = 0
        self._setup()
    def _setup(self):
        data = [
            ("Россия",120,90,70,65,55,145),("США",150,100,95,70,85,330),
            ("Китай",130,95,90,75,70,1400),("Германия",100,40,85,80,80,83),
            ("Франция",90,50,75,75,72,67),("Индия",80,70,60,60,50,1400),
            ("Бразилия",70,50,55,60,45,215),("Япония",110,45,88,85,88,125),
            ("Турция",75,65,55,55,50,85),("Иран",60,60,40,45,55,85),
            ("Польша",70,50,60,70,60,38),("Великобритания",105,55,80,78,82,67),
            ("Украина",65,55,50,60,50,42),("Казахстан",60,40,45,55,45,19),
            ("Испания",85,45,70,72,65,47),("Италия",85,45,72,70,68,60),
            ("Египет",55,50,40,50,40,105),("ЮАР",60,40,50,55,45,60),
            ("Аргентина",60,45,50,55,50,46),("Австралия",90,40,75,80,75,26),
        ]
        for row in data: self.countries.append(Country(*row))
        defs = {
            "Россия":("Авторитаризм","Жёсткая","Устаревающие"),
            "США":("Демократия","Умеренная","Прогрессивные"),
            "Китай":("Коммунизм","Строгая","Современные"),
            "Германия":("Демократия","Умеренная","Прогрессивные"),
            "Франция":("Демократия","Умеренная","Современные"),
            "Индия":("Демократия","Строгая","Устаревающие"),
            "Бразилия":("Демократия","Мягкая","Современные"),
            "Япония":("Монархия","Умеренная","Инновационные"),
            "Турция":("Авторитаризм","Строгая","Современные"),
            "Иран":("Теократия","Репрессивная","Устаревшие"),
            "Польша":("Демократия","Умеренная","Современные"),
            "Великобритания":("Монархия","Умеренная","Прогрессивные"),
            "Украина":("Демократия","Умеренная","Современные"),
            "Казахстан":("Авторитаризм","Строгая","Устаревающие"),
            "Испания":("Монархия","Умеренная","Современные"),
            "Италия":("Демократия","Умеренная","Современные"),
            "Египет":("Авторитаризм","Жёсткая","Устаревшие"),
            "ЮАР":("Демократия","Умеренная","Современные"),
            "Аргентина":("Демократия","Мягкая","Современные"),
            "Австралия":("Демократия","Умеренная","Прогрессивные"),
        }
        for n,(so,st,mo) in defs.items():
            c = self.get_country(n)
            if c: c.law_society, c.law_strictness, c.law_modernity = so,st,mo
        nuclear_powers = ["Россия","США","Китай","Великобритания","Франция","Индия"]
        for name in nuclear_powers:
            c = self.get_country(name)
            if c: c.techs.add("nuclear")
    def territory_owner(self, region):
        for c in self.countries:
            if region in c.territory: return c
        return None
    def get_neighbors(self, name):
        c = self.get_country(name)
        if not c: return []
        res = set()
        for t in c.territory: res.update(NEIGHBORS.get(t, []))
        alive_names = {x.name for x in self.countries if x.alive}
        result = []
        for n in res:
            if n in c.territory: continue
            owner = self.territory_owner(n)
            if owner and owner.name == c.name: continue
            if n in alive_names: result.append(n)
        return sorted(set(result))
    def are_neighbors(self, a, b): return b in self.get_neighbors(a)
    def _war_key(self, a, b): return tuple(sorted([a,b]))
    def _track_war_start(self, a, b):
        k = self._war_key(a,b)
        if k not in self.war_started: self.war_started[k] = self.turn
    def _end_war_tracking(self, a, b):
        self.war_started.pop(self._war_key(a,b), None)
    def war_duration(self, a, b):
        return self.turn - self.war_started.get(self._war_key(a.name,b.name), self.turn)
    def get_country(self, name):
        if not name: return None
        for c in self.countries:
            if c.name.lower() == name.lower(): return c
        return None
    def alive_countries(self, exclude_player=True):
        return [c for c in self.countries if c.alive and (not exclude_player or c != self.player)]
    def show_map(self):
        print(clr("\n╔" + "═"*66 + "╗", C.M))
        print(clr("║" + "  🗺  КАРТА МИРА  ".center(66) + "║", C.M))
        print(clr("╚" + "═"*66 + "╝", C.M))
        regions = {}
        for c in self.countries:
            r = REGION.get(c.name, "Прочие"); regions.setdefault(r, []).append(c)
        for r in ["Европа","Азия","Америка","Африка","Океания","Прочие"]:
            if r not in regions: continue
            print(clr(f"\n  🌍 {r.upper()}", C.Bold+C.Cy))
            print(clr("  " + "─"*62, C.Dim))
            for c in regions[r]:
                if c.alive:
                    if c == self.player: icon = clr("★", C.Y); tag = clr(" [ВЫ]", C.Y)
                    elif c.name in self.player.at_war_with: icon = clr("🔥", C.R); tag = clr(" (война)", C.R)
                    elif c.name in self.player.allies: icon = clr("🤝", C.G); tag = clr(" (союз)", C.G)
                    elif c.name in self.player.trades: icon = clr("💱", C.Cy); tag = clr(" (торговля)", C.Cy)
                    else: icon = clr("●", C.W); tag = ""
                    terr = f" [{len(c.territory)} т.]" if len(c.territory) > 1 else ""
                    warn = clr(f" ⚠️{c.battles_lost}/3", C.R) if c.battles_lost > 0 else ""
                    nk = clr(" ☢️", C.R) if c.has_nuke() else ""
                    print(f"    {icon} {c.name:<16} сила {c.power():>5.0f}  👥 {c.population:>6.1f} млн{tag}{clr(terr, C.Dim)}{warn}{nk}")
                else:
                    owner = self.territory_owner(c.name)
                    if owner: print(f"    {clr('✝', C.Gr)} {clr(c.name, C.Gr):<16} {clr('→ отошла', C.Gr)} {clr(owner.name, C.Y)}")
                    else: print(f"    {clr('✝', C.Gr)} {clr(c.name, C.Gr)}")
        print()
        return ""
    def chat_with_country(self, target):
        if not target or not target.alive:
            print(clr("❌ Страна недоступна.", C.R)); return ""
        if target == self.player:
            print(clr("❌ Нельзя поговорить с собой.", C.R)); return ""
        dialog = CountryDialog(target, self.player, self)
        print()
        print(clr("╔" + "═"*62 + "╗", C.Cy))
        print(clr("║" + f"  💬 КАНАЛ СВЯЗИ С {target.name.upper()}".center(62) + "║", C.Cy))
        print(clr("╚" + "═"*62 + "╝", C.Cy))
        rel = ("🔥 ВОЙНА" if target.name in self.player.at_war_with
               else "🤝 СОЮЗ" if target.name in self.player.allies
               else "💱 ТОРГОВЛЯ" if target.name in self.player.trades
               else "⚪ нейтралитет")
        nk = " ☢️ есть ЯО" if target.has_nuke() else ""
        print(clr(f"  Отношения: {rel}{nk}", C.Dim))
        print(clr("  Пиши своими словами. Ход НЕ тратится. Для выхода — 'выйти'.", C.Dim))
        print()
        Sound.diplomacy()
        print(clr(f"🌐 {target.name}: ", C.Bold+C.M) + random.choice([
            "Наш посол готов вас выслушать.",
            "Приветствуем. О чём хотите говорить?",
            "Мы слушаем."]) + "\n")
        while True:
            try:
                msg = input(clr(f"🧑 Ты → {target.name}: ", C.Bold+C.Y)).strip()
            except (KeyboardInterrupt, EOFError):
                print(); break
            if not msg: continue
            low = msg.lower()
            if low in ("выйти","выход","exit","q","quit","пока","до свидания","закрыть"):
                print(clr(f"\n🌐 {target.name}: ", C.Bold+C.M) + random.choice([
                    "До свидания.","Наши двери всегда открыты."]))
                print(clr(f"  📴 Канал закрыт. Ход не потрачен.\n", C.Dim))
                return ""
            reply = dialog.respond(msg)
            Sound.message()
            if "[" in reply and "]" in reply:
                idx = reply.rfind("  [")
                txt = reply[:idx]; result = reply[idx+3:-1]
                print(clr(f"🌐 {target.name}: ", C.Bold+C.M) + txt)
                print(clr("⚙️  ", C.Gr) + result + "\n")
            else:
                print(clr(f"🌐 {target.name}: ", C.Bold+C.M) + reply + "\n")
        return ""
    def choose_country(self):
        print(clr("\n╔" + "═"*76 + "╗", C.M))
        print(clr("║" + "  ВЫБОР СТРАНЫ".center(76) + "║", C.M))
        print(clr("╚" + "═"*76 + "╝", C.M))
        print(clr(f"  {'№':>2}  {'Страна':<16}{'Регион':<10}{'💰':>5}{'⚔️':>5}{'🏭':>5}{'🕊️':>5}{'🔬':>5}{'👥':>8}{'ЯО':>4}", C.Bold))
        print(clr("  " + "─"*76, C.Dim))
        for i, c in enumerate(self.countries, 1):
            r = REGION.get(c.name, "?")
            nk = "☢️" if c.has_nuke() else "  "
            print(f"  {i:>2}  {c.name:<16}{r:<10}{c.money:>5}{c.army:>5}{c.economy:>5}{c.stability:>5}{c.science:>5}{c.population:>8.0f}{nk:>4}")
        while True:
            try:
                ch = int(input(clr("\n  Номер страны: ", C.Y)))
                if 1 <= ch <= len(self.countries):
                    self.player = self.countries[ch-1]
                    self.player.is_player = True
                    nk = " ☢️ ЯО есть" if self.player.has_nuke() else ""
                    print(clr(f"\n  ✅ Вы управляете: {self.player.name}{nk}\n", C.G))
                    print(clr(f"  🗺  Соседи: {', '.join(self.get_neighbors(self.player.name))}\n", C.Cy))
                    return
            except ValueError: pass
            print(clr("  Неверный выбор.", C.R))
    def do_internal(self, kind):
        c = self.player
        cost = {"army":15,"economy":20,"stability":15,"taxes":0,"science":25}[kind]
        if cost and c.money < cost:
            return clr(f"❌ Не хватает денег ({cost}💰 нужно, есть {c.money}).", C.R)
        if kind == "army" and c.population < 10:
            return clr(f"❌ Мало людей! Нужно 10+ млн.", C.R)
        if kind == "army": ch = 0.75 if c.army < 60 else 0.6
        elif kind == "economy": ch = 0.75 if c.economy < 60 else 0.6
        elif kind == "stability": ch = 0.8 if c.stability < 50 else 0.55
        elif kind == "science": ch = 0.8 if c.science < 40 else 0.6
        else: ch = 0.8 if c.stability > 50 else 0.5
        if kind == "stability": ch -= c.pop_pressure() * 0.15
        ch += {"army":c.law_mod("arm"),"economy":c.law_mod("eco"),
               "stability":c.law_mod("sta"),"science":c.law_mod("sci"),
               "taxes":c.law_mod("eco")}[kind] * 0.005
        ch = max(0.1, min(0.95, ch))
        if cost: c.money -= cost
        roll = random.random()
        oc = "success" if roll < ch else "partial" if roll < ch + 0.15 else "fail"
        c.faction_change(kind)
        if kind == "army":
            rec = {"success":5.0,"partial":2.0,"fail":0.5}[oc]
            c.population = max(0.5, c.population - rec)
            if oc == "success": c.army += 10; return clr(f"✅ Набор: +10 ⚔️ (призвано {rec:.1f} млн).", C.G)
            if oc == "partial": c.army += 4; return clr(f"⚠️ Частичный: +4 ⚔️.", C.Y)
            c.stability = max(0, c.stability - 2)
            return clr("❌ Провал, -2 🕊️.", C.R)
        if kind == "economy":
            m = c.work_penalty()
            if oc == "success":
                g = int(8*m); c.economy += g
                return clr(f"✅ Реформы: +{g} 🏭.", C.G if m>=1 else C.Y)
            if oc == "partial":
                g = int(3*m); c.economy += g; return clr(f"⚠️ +{g} 🏭.", C.Y)
            return clr("❌ Реформы провалились.", C.R)
        if kind == "stability":
            if oc == "success": c.stability = min(100, c.stability + 8); return clr("✅ +8 🕊️.", C.G)
            if oc == "partial": c.stability = min(100, c.stability + 3); return clr("⚠️ +3 🕊️.", C.Y)
            c.stability = max(0, c.stability - 2); return clr("❌ -2 🕊️.", C.R)
        if kind == "science":
            m = c.sci_penalty()
            if oc == "success":
                g = int(10*m); c.science += g; return clr(f"✅ Наука: +{g} 🔬.", C.G if m>=1 else C.Y)
            if oc == "partial":
                g = int(4*m); c.science += g; return clr(f"⚠️ +{g} 🔬.", C.Y)
            return clr("❌ Провал.", C.R)
        pm = 1.0 + c.population / 500.0
        if oc == "success":
            g = int(25*pm); c.money += g; c.stability = max(0, c.stability - 5)
            return clr(f"✅ Налоги: +{g} 💰, -5 🕊️.", C.G)
        if oc == "partial":
            g = int(15*pm); c.money += g; c.stability = max(0, c.stability - 8)
            return clr(f"⚠️ +{g} 💰, -8 🕊️.", C.Y)
        g = int(8*pm); c.money += g; c.stability = max(0, c.stability - 15)
        return clr(f"❌ Бунт! +{g} 💰, -15 🕊️.", C.R)
    def do_suppress_revolt(self):
        c = self.player
        cost = 30
        if c.money < cost:
            return clr(f"❌ Нужно {cost}💰 на подавление (есть {c.money}).", C.R)
        c.money -= cost
        worst = min(c.factions.items(), key=lambda x: x[1])
        fname, floy = worst
        ch = 0.5 + (c.stability - 50) * 0.005 + (30 - floy) * 0.01
        ch = max(0.15, min(0.9, ch))
        roll = random.random()
        if roll < ch:
            c.factions[fname] = min(100, c.factions[fname] + 25)
            c.stability = max(0, c.stability - 3)
            c.factions["Народ"] = max(0, c.factions["Народ"] - 3)
            c.factions["Элита"] = min(100, c.factions["Элита"] + 2)
            return clr(f"✅ Бунт фракции «{fname}» подавлен! Лояльность +25, стабильность -3.", C.G)
        if roll < ch + 0.2:
            c.factions[fname] = min(100, c.factions[fname] + 10)
            c.stability = max(0, c.stability - 5)
            return clr(f"⚠️ Частичный успех: «{fname}» +10 лояльности, но -5 стабильности.", C.Y)
        c.factions[fname] = max(0, c.factions[fname] - 5)
        c.stability = max(0, c.stability - 8)
        c.population = max(1.0, c.population - 1.5)
        return clr(f"❌ Подавление провалилось! «{fname}» -5, стабильность -8, погибло 1.5 млн.", C.R)
    def do_research(self, tid):
        c = self.player
        if not tid: return clr("❌ Что исследовать?", C.R)
        t = next((x for x in TECHS if x["id"] == tid), None)
        if not t: return clr("❌ Технология не найдена.", C.R)
        if t["id"] in c.techs: return clr(f"ℹ️ «{t['name']}» уже изучена.", C.Y)
        if c.money < t["cost"]: return clr(f"❌ Нужно {t['cost']}💰.", C.R)
        if c.science < t["sci"]: return clr(f"❌ Нужно {t['sci']} 🔬.", C.R)
        c.money -= t["cost"]
        ch = (0.5 + (c.science - t["sci"])*0.02 + c.law_mod("sci")*0.005) * c.sci_penalty()
        ch = max(0.15, min(0.95, ch))
        roll = random.random()
        if roll < ch:
            c.techs.add(t["id"]); c.faction_change("tech")
            for k, v in t["eff"].items():
                if k == "eco": c.economy += v
                if k == "arm": c.army += v
                if k == "sta": c.stability = min(100, c.stability + v)
                if k == "sci": c.science += v
            Sound.tech()
            extra = "  ☢️ Теперь доступно ЯО!" if t["id"] == "nuclear" else ""
            return clr(f"✅ «{t['name']}» открыта!{extra}", C.G)
        if roll < ch + 0.2: return clr(f"⚠️ «{t['name']}» близка.", C.Y)
        c.stability = max(0, c.stability - 2)
        return clr(f"❌ «{t['name']}» провалилась.", C.R)
    def do_change_law(self, col, val):
        c = self.player
        if not col or not val: return clr("❌ Не понял, какой закон менять.", C.R)
        cur = {"society":c.law_society,"strictness":c.law_strictness,"modernity":c.law_modernity}[col]
        if cur == val: return clr(f"ℹ️ Уже установлено: {val}.", C.Y)
        cost = 60
        if c.money < cost: return clr(f"❌ Реформа стоит {cost}💰.", C.R)
        c.money -= cost
        if col == "society": c.law_society = val
        elif col == "strictness": c.law_strictness = val
        elif col == "modernity": c.law_modernity = val
        c.stability = max(0, c.stability - 5)
        if col == "strictness":
            if val in ("Жёсткая","Репрессивная","Тотальная"):
                c.factions["Народ"] -= 5; c.factions["Бизнес"] -= 5
            elif val in ("Мягкая","Отсутствующая"):
                c.factions["Народ"] += 3; c.factions["Бизнес"] += 3
        elif col == "modernity":
            if val in ("Прогрессивные","Инновационные","Футуристические"):
                c.factions["Элита"] += 5; c.factions["Народ"] -= 2
            elif val in ("Архаичные","Устаревшие"):
                c.factions["Народ"] += 3; c.factions["Элита"] -= 3
        for f in list(c.factions.keys()):
            c.factions[f] = max(0, min(100, c.factions[f]))
        col_ru = {"society":"Общество","strictness":"Строгость","modernity":"Современность"}[col]
        return clr(f"✅ {col_ru}: «{cur}» → «{val}» (-60💰, -5🕊️).", C.G)
    def show_research(self):
        c = self.player
        print(clr("\n  🔬 ИССЛЕДОВАНИЯ", C.Bold+C.Cy))
        print(clr("  " + "─"*70, C.Dim))
        avail = []
        for i, t in enumerate(TECHS, 1):
            if t["id"] in c.techs: st = clr("✓", C.G)
            elif c.science < t["sci"]: st = clr("×", C.R)
            else: st = clr("○", C.Y); avail.append(t["name"])
            eff = ", ".join(f"{'+' if v>0 else ''}{v}{k[:3]}" for k,v in t["eff"].items())
            print(f"  {i:>2} {st} {t['name']:<22}{t['cost']:>6}💰{t['sci']:>6}🔬  {eff}")
        print(clr("  " + "─"*70, C.Dim))
        if avail: print(clr(f"  Доступно: {', '.join(avail)}", C.Y))
        else: print(clr(f"  Мало науки (сейчас {c.science}🔬).", C.Dim))
        return ""
    def show_techs(self):
        c = self.player
        print(clr("\n  🎓 ИЗУЧЕНО", C.Bold+C.Cy))
        if not c.techs: print(clr("  Пока ничего.", C.Dim)); return ""
        for tid in c.techs:
            t = next((x for x in TECHS if x["id"] == tid), None)
            if t: print(f"  ✓ {t['name']}")
        return ""
    def show_laws(self):
        c = self.player
        print(clr("\n  ⚖️  ПРАВОВАЯ СИСТЕМА", C.Bold+C.Cy))
        print(clr("  " + "═"*76, C.Dim))
        print(clr(f"  Сейчас: {c.law_society}  |  {c.law_strictness}  |  {c.law_modernity}", C.Bold))
        def fmt(v):
            if v > 0:  return clr(f"+{v}", C.G)
            if v < 0:  return clr(f"{v}", C.R)
            return clr(" 0", C.Dim)
        def row(name, eff, is_current):
            mark = clr(" ◄", C.Y) if is_current else ""
            name_col = clr(f"{name:<20}", C.Bold+C.Y) if is_current else f"{name:<20}"
            print(f"   {name_col}💰{fmt(eff.get('eco',0))}  ⚔️{fmt(eff.get('arm',0))}  "
                  f"🕊️{fmt(eff.get('sta',0))}  🔬{fmt(eff.get('sci',0))}{mark}")
        print(clr("  " + "─"*76, C.Dim))
        print(clr("\n  🏛  ТИП ОБЩЕСТВА", C.Bold+C.Cy))
        for name, eff in SOCIETY_TYPES.items(): row(name, eff, name == c.law_society)
        print(clr("\n  ⚖️  СТРОГОСТЬ", C.Bold+C.Cy))
        for name, eff in STRICTNESS_LEVELS.items(): row(name, eff, name == c.law_strictness)
        print(clr("\n  🕰  СОВРЕМЕННОСТЬ", C.Bold+C.Cy))
        for name, eff in MODERNITY_LEVELS.items(): row(name, eff, name == c.law_modernity)
        print(clr("\n  " + "═"*76, C.Dim))
        print(clr("  📊 ИТОГО:", C.Bold), end="  ")
        print(f"💰{fmt(c.law_mod('eco'))}  ⚔️{fmt(c.law_mod('arm'))}  "
              f"🕊️{fmt(c.law_mod('sta'))}  🔬{fmt(c.law_mod('sci'))}")
        return ""
    def do_diplomacy(self, t, sub):
        p = self.player
        if not t or not t.alive or t == p: return clr("❌ Некорректная цель.", C.R)
        if sub == "alliance":
            if p.money < 20: return clr("❌ Нужно 20💰.", C.R)
            if t.name in p.at_war_with: return clr(f"❌ Нельзя союз с врагом.", C.R)
            if t.name in p.allies: return clr(f"ℹ️ {t.name} уже союзник.", C.Y)
            p.money -= 20
            r = t.power() / max(1.0, p.power())
            ch = 0.5 + (0.2 if 0.7<=r<=1.5 else -0.2 if r>2 else 0)
            if p.at_war_with & t.at_war_with: ch += 0.25
            if not self.are_neighbors(p.name, t.name): ch -= 0.15
            if self.world_anger > 0: ch -= 0.5
            ch = max(0.05, min(0.9, ch))
            if random.random() < ch:
                p.allies.add(t.name); t.allies.add(p.name)
                p.faction_change("alliance")
                Sound.diplomacy()
                return clr(f"✅ {t.name} согласна на союз!", C.G)
            return clr(f"❌ {t.name} отвергает союз.", C.R)
        if sub == "peace":
            if t.name not in p.at_war_with: return clr(f"ℹ️ Вы не воюете.", C.Y)
            r = p.power() / max(1.0, t.power())
            dur = self.war_duration(p, t)
            ch = 0.5
            if r < 0.7: ch += 0.3
            if p.stability < 30: ch += 0.15
            if t.stability < 30: ch += 0.15
            ch += min(0.3, dur*0.05)
            ch = max(0.1, min(0.95, ch))
            if random.random() < ch:
                p.at_war_with.discard(t.name); t.at_war_with.discard(p.name)
                self._end_war_tracking(p.name, t.name)
                p.battles_lost = 0; t.battles_lost = 0
                p.faction_change("peace")
                Sound.diplomacy()
                return clr(f"🕊️ Мир с {t.name} подписан! Счётчик поражений сброшен.", C.G)
            return clr(f"❌ {t.name} отвергает мир.", C.R)
        if sub == "trade":
            if t.name in p.at_war_with: return clr("❌ Нельзя торговать с врагом.", C.R)
            if t.name in p.trades: return clr(f"ℹ️ Уже торгуете с {t.name}.", C.Y)
            ch = 0.75 + (0.15 if t.name in p.allies else 0)
            if not self.are_neighbors(p.name, t.name): ch -= 0.2
            if self.world_anger > 0: ch -= 0.5
            if random.random() < ch:
                p.trades.add(t.name); t.trades.add(p.name)
                p.faction_change("trade")
                Sound.diplomacy()
                return clr(f"💱 Торговое соглашение с {t.name}! Доход добавлен.", C.G)
            return clr(f"❌ {t.name} отказалась.", C.R)
        if sub == "gift":
            if p.money < 20: return clr("❌ Нужно 20💰.", C.R)
            p.money -= 20; t.money += 15
            t.stability = min(100, t.stability + 2)
            p.faction_change("gift_out")
            Sound.diplomacy()
            return clr(f"🎁 Подарок отправлен {t.name}.", C.G)
        return clr("❌ Неизвестное.", C.R)
    def do_war(self, t):
        p = self.player
        if not t or not t.alive or t == p: return clr("❌ Некорректная цель.", C.R)
        if t.name in p.at_war_with: return clr(f"ℹ️ Вы уже воюете.", C.Y)
        if not self.are_neighbors(p.name, t.name):
            return clr(f"❌ Слишком далеко! Нет границы с {t.name}.", C.R)
        if t.name in p.allies:
            p.allies.discard(t.name); t.allies.discard(p.name)
        r = p.power() / max(1.0, t.power())
        ch = (0.85 if r>=1.6 else 0.70 if r>=1.2 else 0.50 if r>=0.9 else 0.30 if r>=0.6 else 0.15)
        if p.stability < 30: ch -= 0.15
        ch = max(0.05, min(0.95, ch))
        roll = random.random()
        if roll < ch:
            p.at_war_with.add(t.name); t.at_war_with.add(p.name)
            self._track_war_start(p.name, t.name)
            p.faction_change("war")
            joined = []
            for an in list(t.allies):
                a = self.get_country(an)
                if a and a.alive and a != p:
                    a.at_war_with.add(p.name); p.at_war_with.add(a.name)
                    self._track_war_start(a.name, p.name)
                    joined.append(a.name)
            Sound.war()
            extra = f" Союзники ({', '.join(joined)}) вступают!" if joined else ""
            return clr(f"🔥 Война объявлена {t.name}!{extra}", C.G)
        elif roll < ch + 0.2:
            p.stability = max(0, p.stability - 5); p.money = max(0, p.money - 10)
            p.at_war_with.add(t.name); t.at_war_with.add(p.name)
            self._track_war_start(p.name, t.name)
            p.faction_change("war")
            Sound.war()
            return clr(f"⚠️ Война с {t.name}, но элиты недовольны.", C.Y)
        else:
            p.stability = max(0, p.stability - 8); p.money = max(0, p.money - 10)
            if random.random() < 0.4:
                p.at_war_with.add(t.name); t.at_war_with.add(p.name)
                self._track_war_start(p.name, t.name)
                Sound.war()
                return clr(f"❌ Провал! {t.name} в ответ объявляет войну.", C.R)
            return clr("❌ Провал.", C.R)
    def do_nuke(self, t):
        p = self.player
        if not t or not t.alive or t == p: return clr("❌ Некорректная цель.", C.R)
        if not p.has_nuke():
            return clr("❌ У вас нет ядерного оружия! Сначала исследуйте его командой 'изучить ядерное оружие'.", C.R)
        if t.has_nuke():
            Sound.nuke()
            p.army = int(p.army * 0.3); t.army = int(t.army * 0.3)
            p.economy = int(p.economy * 0.3); t.economy = int(t.economy * 0.3)
            p.population = max(1.0, p.population * 0.5); t.population = max(1.0, t.population * 0.5)
            p.stability = max(0, p.stability - 40); t.stability = max(0, t.stability - 40)
            p.faction_change("nuke"); t.faction_change("nuke")
            self._world_condemnation()
            return clr(f"☢️ ОБМЕН ЯДЕРНЫМИ УДАРАМИ! {t.name} тоже имеет ЯО. Обе страны наполовину уничтожены. Мир в ужасе.", C.R)
        Sound.nuke()
        p.faction_change("nuke")
        Sound.anthem(p.name)
        print(clr(f"\n☢️ ЯДЕРНЫЙ УДАР ПО {t.name.upper()}! ☢️", C.Bold+C.R))
        print(clr(f"🎵 Звучит гимн {p.name}...", C.Dim))
        t.alive = False
        t.battles_lost = 999
        p.territory |= t.territory
        p.money += 30; p.economy += 5
        p.population += t.population * 0.2
        for o in self.countries: o.at_war_with.discard(t.name)
        for k in list(self.war_started.keys()):
            if t.name in k: self.war_started.pop(k, None)
        self._world_condemnation()
        return clr(
            f"💀 {t.name} УНИЧТОЖЕНА ядерным ударом! Территория переходит к {p.name}.\n"
            f"⚠️ Весь мир осуждает вас: −40 стабильности всем, разрыв союзов и торговли.\n"
            f"😨 Мир будет осуждать вас ещё 10 ходов — никто не предложит союз.", C.R)
    def _world_condemnation(self):
        p = self.player
        for c in self.countries:
            if not c.alive or c == p: continue
            c.stability = max(0, c.stability - 40)
            c.allies.discard(p.name); p.allies.discard(c.name)
            c.trades.discard(p.name); p.trades.discard(c.name)
            c.factions["Народ"] = max(0, c.factions["Народ"] - 20)
            c.factions["Элита"] = max(0, c.factions["Элита"] - 15)
        p.stability = max(0, p.stability - 20)
        self.world_anger = 10
    def execute_action(self, action):
        a = action["intent"]
        if a in ("invalid","ask_info","show_research","show_laws","show_techs",
                 "show_map","chat_country"): return False, None
        if a == "suppress_revolt":
            return True, self.do_suppress_revolt()
        if a == "end_turn": return True, "Ход завершён."
        if a in ("develop_army","develop_economy","develop_stability",
                 "develop_science","collect_taxes"):
            k = {"develop_army":"army","develop_economy":"economy",
                 "develop_stability":"stability","develop_science":"science",
                 "collect_taxes":"taxes"}[a]
            return True, self.do_internal(k)
        if a == "research": return True, self.do_research(action.get("tech_id"))
        if a == "change_law": return True, self.do_change_law(action.get("law_col"), action.get("law_val"))
        if a == "diplomacy_alliance": return True, self.do_diplomacy(self.get_country(action.get("country")), "alliance")
        if a == "diplomacy_peace": return True, self.do_diplomacy(self.get_country(action.get("country")), "peace")
        if a == "diplomacy_trade": return True, self.do_diplomacy(self.get_country(action.get("country")), "trade")
        if a == "diplomacy_gift": return True, self.do_diplomacy(self.get_country(action.get("country")), "gift")
        if a == "declare_war": return True, self.do_war(self.get_country(action.get("country")))
        if a == "nuke": return True, self.do_nuke(self.get_country(action.get("country")))
        return False, clr(f"❌ Неизвестное действие.", C.R)
    def chat_loop(self):
        print(clr("\n💬 Пиши мастеру своими словами.", C.Cy))
        print(clr("   'развивай науку', 'союз с Китаем', 'карта', 'подавить бунт',", C.Dim))
        print(clr("   'изучить ядерное оружие', 'применить ядерное оружие против США'\n", C.Dim))
        names = [c.name for c in self.countries if c != self.player]
        while True:
            try:
                ui = input(clr("🧑 Ты: ", C.Bold+C.Y)).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n👋 До свидания!"); raise SystemExit
            if not ui: continue
            low = ui.lower()
            if low in ("выход","exit","quit","q"): print("👋 До свидания!"); raise SystemExit
            if low in ("меню","menu"): self.menu_turn(); return
            if low in ("помощь","help","?"): print(HELP_TEXT); continue
            if low in ("исследования","наука"): self.show_research(); continue
            if low in ("законы",): self.show_laws(); continue
            if low in ("технологии",): self.show_techs(); continue
            if low in ("карта","map"): self.show_map(); continue
            action = self.brain.interpret(ui, names)
            intent = action["intent"]; conf = action["confidence"]; reply = action["reply"]
            if intent == "chat_country":
                target = self.get_country(action.get("country"))
                if target: self.chat_with_country(target); continue
                else: print(clr("🤔 С какой страной поговорить?\n", C.Y)); continue
            icon = "🎭" if conf>=0.4 else "🤔"
            col = C.G if conf>=0.6 else C.Y if conf>=0.4 else C.R
            print(f"\n{icon} {clr('Мастер', C.Bold)} [{clr(intent, C.Cy)}, {clr(f'{conf:.0%}', col)}]: {reply}\n")
            if intent == "show_research": self.show_research(); continue
            if intent == "show_laws": self.show_laws(); continue
            if intent == "show_techs": self.show_techs(); continue
            if intent == "show_map": self.show_map(); continue
            if intent == "ask_info": self.player.show_stats(); continue
            consumed, result = self.execute_action(action)
            if not consumed: continue
            print(clr("⚙️  ", C.Gr) + result + "\n")
            narr = self.brain.narrate(result)
            print(clr("🎭 ", C.M) + clr(narr, C.Dim) + "\n")
            return
    def menu_turn(self):
        print(clr(f"\n--- Меню (ход {self.turn}/{self.max_turns}) ---", C.Cy))
        print("1.Армия 2.Экономика 3.Стабильность 4.Наука 5.Налоги")
        print("6.Дипломатия 7.Война 8.Исследования 9.Законы 10.Технологии")
        print("11.Карта 12.Инфо 13.Ядерный удар 14.Бунт 15.Завершить ход")
        try: a = int(input(clr("> ", C.Y)))
        except ValueError: return
        if a == 15: return
        if a == 1: print(self.do_internal("army"))
        elif a == 2: print(self.do_internal("economy"))
        elif a == 3: print(self.do_internal("stability"))
        elif a == 4: print(self.do_internal("science"))
        elif a == 5: print(self.do_internal("taxes"))
        elif a == 6: self.menu_diplomacy()
        elif a == 7: self.menu_war()
        elif a == 8: self.show_research()
        elif a == 9: self.show_laws()
        elif a == 10: self.show_techs()
        elif a == 11: self.show_map()
        elif a == 12: self.player.show_stats()
        elif a == 13:
            others = self.alive_countries()
            for i, c in enumerate(others, 1):
                nk = " ☢️" if c.has_nuke() else ""
                print(f"  {i}. {c.name}{nk}")
            try:
                i = int(input(clr("> ", C.Y)))
                if 1 <= i <= len(others): print(self.do_nuke(others[i-1]))
            except (ValueError, IndexError): pass
        elif a == 14: print(self.do_suppress_revolt())
    def menu_diplomacy(self):
        others = self.alive_countries()
        for i, c in enumerate(others, 1):
            rel = ("ВОЙНА" if c.name in self.player.at_war_with
                   else "СОЮЗ" if c.name in self.player.allies
                   else "ТОРГ" if c.name in self.player.trades else "нейтр.")
            print(f"  {i}. {c.name} [{rel}]")
        try:
            i = int(input(clr("> ", C.Y)))
            if 1 <= i <= len(others):
                t = others[i-1]
                print("1.союз 2.мир 3.торговля 4.подарок 5.чат")
                s = int(input(clr("> ", C.Y)))
                if s == 5: self.chat_with_country(t); return
                sub = {1:"alliance",2:"peace",3:"trade",4:"gift"}.get(s)
                if sub: print(self.do_diplomacy(t, sub))
        except (ValueError, IndexError): pass
    def menu_war(self):
        neighbors = self.get_neighbors(self.player.name)
        others = [c for c in self.alive_countries()
                  if c.name not in self.player.at_war_with and c.name in neighbors]
        if not others:
            print(clr("  Нет соседей для войны.", C.Dim)); return
        for i, c in enumerate(others, 1):
            print(f"  {i}. {c.name} (сила {c.power():.0f})")
        try:
            i = int(input(clr("> ", C.Y)))
            if 1 <= i <= len(others): print(self.do_war(others[i-1]))
        except (ValueError, IndexError): pass
    def _ai_try_peace(self, a, b):
        ra = a.power() / max(1.0, b.power())
        dur = self.war_duration(a, b)
        wa = (ra < 0.75 and random.random() < 0.7) or (dur >= 5 and random.random() < 0.6) or \
             ((a.stability < 30 or a.money < 10) and random.random() < 0.5) or (random.random() < 0.1)
        if not wa: return False
        rb = b.power() / max(1.0, a.power())
        wb = (rb < 0.75 and random.random() < 0.7) or (dur >= 5 and random.random() < 0.6) or \
             ((b.stability < 30 or b.money < 10) and random.random() < 0.5) or (random.random() < 0.25)
        if not wb: return False
        a.at_war_with.discard(b.name); b.at_war_with.discard(a.name)
        self._end_war_tracking(a.name, b.name)
        a.battles_lost = 0; b.battles_lost = 0
        return True
    def _ai_declare_war(self, a, t):
        a.at_war_with.add(t.name); t.at_war_with.add(a.name)
        self._track_war_start(a.name, t.name)
        joined = []
        for an in list(t.allies):
            al = self.get_country(an)
            if al and al.alive and al != a:
                al.at_war_with.add(a.name); a.at_war_with.add(al.name)
                self._track_war_start(al.name, a.name)
                joined.append(al.name)
        return joined
    def ai_turn(self):
        events = []
        for c in self.countries:
            if not c.alive or c == self.player: continue
            at_war = bool(c.at_war_with)
            if at_war:
                for en in list(c.at_war_with):
                    e = self.get_country(en)
                    if not e or not e.alive: continue
                    if random.random() < 0.4:
                        if self._ai_try_peace(c, e):
                            events.append(clr(f"🕊️ {c.name} и {e.name} подписали мир.", C.G))
            at_war = bool(c.at_war_with)
            if at_war:
                if c.money >= 15 and c.population > 12 and random.random() < 0.6:
                    c.army += 6; c.money -= 15
                    c.population = max(1.0, c.population - 2)
                elif c.money >= 20 and random.random() < 0.5:
                    c.economy += 4; c.money -= 20
                else:
                    c.money += 10; c.stability = max(0, c.stability - 2)
            else:
                if c.money >= 25 and random.random() < 0.5:
                    c.science += 4; c.money -= 25
                elif c.money >= 20 and random.random() < 0.5:
                    c.economy += 5; c.money -= 20
                elif c.money >= 15 and random.random() < 0.3 and c.population > 15:
                    c.army += 4; c.money -= 15
                    c.population = max(1.0, c.population - 1)
                else:
                    c.money += 15; c.stability = min(100, c.stability + 1)
            if not at_war and random.random() < 0.08 and c.money >= 20:
                ns = self.get_neighbors(c.name)
                cands = []
                for nn in ns:
                    n = self.get_country(nn)
                    if not n or not n.alive or n == c: continue
                    if n.name in c.allies or n.name in c.at_war_with: continue
                    if n == self.player and (random.random() < 0.5 or self.world_anger > 0): continue
                    w = 3.0 if (c.at_war_with & n.at_war_with) else 1.0
                    cands.append((n, w))
                if cands:
                    tw = sum(w for _, w in cands)
                    r = random.random() * tw; cum = 0; pick = cands[0][0]
                    for n, w in cands:
                        cum += w
                        if r <= cum: pick = n; break
                    if random.random() < 0.5:
                        c.money -= 20; c.allies.add(pick.name); pick.allies.add(c.name)
                        events.append(clr(f"🤝 {c.name} и {pick.name} заключили союз.", C.G))
            if not at_war and random.random() < 0.05:
                if c.stability < 35 or c.army < 40: continue
                ns = self.get_neighbors(c.name)
                tgts = []
                for nn in ns:
                    n = self.get_country(nn)
                    if not n or not n.alive or n == c: continue
                    if n.name in c.at_war_with or n.name in c.allies: continue
                    if c.power() / max(1.0, n.power()) >= 1.3:
                        if n == self.player and random.random() < 0.5: continue
                        tgts.append(n)
                if tgts:
                    t = random.choice(tgts)
                    r = c.power() / max(1.0, t.power())
                    wc = min(0.9, 0.3 + (r - 1.3) * 0.4)
                    if random.random() < wc:
                        joined = self._ai_declare_war(c, t)
                        events.append(clr(f"⚔️ {c.name} объявила войну {t.name}!", C.R))
                        if joined: events.append(clr(f"   Союзники {t.name} ({', '.join(joined)}) вступают.", C.Y))
                        if t == self.player:
                            Sound.war()
                            events.append(clr("⚠️ Вас атаковали!", C.R))
            if random.random() < 0.1:
                av = [t for t in TECHS if t["id"] not in c.techs
                      and c.science >= t["sci"] and c.money >= t["cost"]]
                if av:
                    t = random.choice(av); c.money -= t["cost"]
                    if random.random() < 0.7:
                        c.techs.add(t["id"])
                        for k, v in t["eff"].items():
                            if k == "eco": c.economy += v
                            if k == "arm": c.army += v
                            if k == "sta": c.stability = min(100, c.stability + v)
                            if k == "sci": c.science += v
        return events
    def generate_proposals(self):
        proposals = []
        p = self.player
        for c in self.countries:
            if not c.alive or c == p: continue
            if self.world_anger > 0:
                if c.name in p.at_war_with and random.random() < 0.5:
                    proposals.append((c, "peace"))
                continue
            if c.name in p.at_war_with:
                dur = self.war_duration(c, p)
                ratio = c.power() / max(1.0, p.power())
                if (dur >= 3 or ratio < 0.7) and random.random() < 0.3:
                    proposals.append((c, "peace")); continue
            if (c.name not in p.at_war_with and c.name not in p.trades
                and c.money >= 30 and random.random() < 0.06):
                proposals.append((c, "trade")); continue
            if (c.name not in p.at_war_with and c.name not in p.allies
                and c.name not in p.trades):
                r = p.power() / max(1.0, c.power())
                if 0.7 <= r <= 1.5 and random.random() < 0.04:
                    proposals.append((c, "alliance"))
        return proposals
    def present_proposals(self, proposals):
        if not proposals: return
        Sound.proposal()
        print()
        print(clr("╔" + "═"*62 + "╗", C.Y))
        print(clr("║" + "  📨 ВХОДЯЩИЕ ДИПЛОМАТИЧЕСКИЕ ПРЕДЛОЖЕНИЯ".center(62) + "║", C.Y))
        print(clr("╚" + "═"*62 + "╝", C.Y))
        for sender, kind in proposals[:3]:
            text = {
                "trade": f"💱 {sender.name} предлагает торговое соглашение.",
                "alliance": f"🤝 {sender.name} предлагает военный союз.",
                "peace": f"🕊️ {sender.name} предлагает мир.",
            }[kind]
            print()
            print(text)
            try:
                ans = input(clr(f"   Принять от {sender.name}? (да/нет): ", C.Bold+C.Y)).strip().lower()
            except (KeyboardInterrupt, EOFError):
                ans = "нет"
            if ans in ("да","y","yes","д","+","1"):
                result = self.do_diplomacy(sender, kind)
                print(clr("   → ", C.G) + result)
            else:
                print(clr(f"   → {sender.name}: «Жаль.»", C.Dim))
        print()
    def world_reactions(self):
        events = []
        p = self.player
        alive = [c for c in self.countries if c.alive and c != p]
        if not alive: return events
        avg_power = sum(c.power() for c in alive) / len(alive)
        ratio = p.power() / max(1.0, avg_power)
        if ratio > 2.5 and random.random() < 0.35:
            potential = [c for c in alive if c.name not in p.allies and c.name not in p.at_war_with]
            if len(potential) >= 2:
                a, b = random.sample(potential, 2)
                if b.name not in a.allies:
                    a.allies.add(b.name); b.allies.add(a.name)
                    events.append(clr(f"⚠️ {a.name} и {b.name} заключили союз против мощи {p.name}.", C.Y))
        if p.stability < 25:
            for c in alive:
                if self.are_neighbors(c.name, p.name) and p.name not in c.at_war_with:
                    if c.power() > p.power() * 1.3 and random.random() < 0.15:
                        self._ai_declare_war(c, p)
                        Sound.war()
                        events.append(clr(f"⚔️ {c.name} атакует ослабленную {p.name}!", C.R))
                        break
        if p.has_nuke() and random.random() < 0.2:
            for c in alive:
                if c.name not in p.allies and random.random() < 0.3:
                    c.factions["Элита"] = max(0, c.factions["Элита"] - 5)
                    events.append(clr(f"😨 {c.name} обеспокоена вашим ядерным арсеналом.", C.Y))
                    break
        return events
    def check_war_exhaustion(self):
        events = []; done = set()
        for a in self.countries:
            if not a.alive: continue
            for bn in list(a.at_war_with):
                b = self.get_country(bn)
                if not b or not b.alive: continue
                k = self._war_key(a.name, b.name)
                if k in done: continue
                done.add(k)
                dur = self.war_duration(a, b)
                if dur >= 8:
                    r = a.power() / max(1.0, b.power())
                    a.at_war_with.discard(b.name); b.at_war_with.discard(a.name)
                    self._end_war_tracking(a.name, b.name)
                    a.battles_lost = 0; b.battles_lost = 0
                    if 1/1.4 < r < 1.4:
                        events.append(clr(f"🕊️ Война {a.name}—{b.name} → перемирие. Счётчики сброшены.", C.Y))
                    else:
                        w = a if r > 1 else b
                        events.append(clr(f"🏳️ Война {a.name}—{b.name} → победа {w.name}. Счётчики сброшены.", C.Y))
        return events
    def resolve_wars(self):
        handled = set(); log = []
        for a in self.countries:
            if not a.alive: continue
            for en in list(a.at_war_with):
                e = self.get_country(en)
                if not e or not e.alive: continue
                k = tuple(sorted([a.name, e.name]))
                if k in handled: continue
                handled.add(k)
                pa = a.power() * random.uniform(0.7, 1.3)
                pb = e.power() * random.uniform(0.7, 1.3)
                w, l = (a, e) if pa > pb else (e, a)
                dmg = random.randint(10, 25)
                l.army = max(0, l.army - dmg)
                l.stability = max(0, l.stability - random.randint(3, 8))
                l.economy = max(0, l.economy - random.randint(2, 6))
                w.army = max(0, w.army - random.randint(3, 10))
                civ = random.uniform(0.5, 2.5)
                l.population = max(0.5, l.population - civ)
                w.population = max(0.5, w.population - civ * 0.4)
                l.battles_lost += 1
                w.battles_lost = 0
                log.append(clr(
                    f"⚔️ {a.name} vs {e.name}: победа {w.name}, "
                    f"{l.name} -{dmg} ⚔️, -{civ:.1f} 👥 (поражений: {l.battles_lost}/3)", C.Y))
                if l == self.player:
                    Sound.defeat(); l.faction_change("war_lose")
                if w == self.player:
                    Sound.victory(); w.faction_change("war_win")
                capitulated = False; reason = ""
                if l.battles_lost >= 3:
                    capitulated = True; reason = "3 поражения подряд"
                elif l.army <= 5 and l.stability <= 10:
                    capitulated = True; reason = "полный разгром"
                elif l.population < 5:
                    capitulated = True; reason = "вымирание населения"
                if capitulated:
                    log.append(clr(f"💀 {l.name} КАПИТУЛИРУЕТ ({reason})!", C.R))
                    log.append(clr(f"🎵 Звучит гимн {w.name}...", C.Dim))
                    Sound.anthem(w.name)
                    w.territory |= l.territory
                    l.alive = False
                    w.money += 50; w.economy += 10
                    w.population += l.population * 0.3
                    for o in self.countries: o.at_war_with.discard(l.name)
                    for k2 in list(self.war_started.keys()):
                        if l.name in k2: self.war_started.pop(k2, None)
                    log.append(clr(f"🏴 Территория {l.name} переходит к {w.name}!", C.M))
                    if l == self.player:
                        Sound.defeat()
                        self.game_over(False, f"Ваша страна капитулировала ({reason}).")
        return log
    def random_event(self):
        if random.random() > 0.35: return []
        ev = [
            ("Экономический бум", lambda c: (setattr(c,'economy',c.economy+5), setattr(c,'money',c.money+20))),
            ("Коррупционный скандал", lambda c: setattr(c,'stability',max(0,c.stability-8))),
            ("Природная катастрофа", lambda c: setattr(c,'economy',max(0,c.economy-6))),
            ("Военный парад", lambda c: setattr(c,'stability',min(100,c.stability+5))),
            ("Научный прорыв", lambda c: setattr(c,'science',c.science+8)),
            ("Массовые протесты", lambda c: setattr(c,'stability',max(0,c.stability-10))),
            ("Приток инвестиций", lambda c: setattr(c,'money',c.money+30)),
            ("Эпидемия", lambda c: setattr(c,'population',max(1.0,c.population*0.85))),
            ("Наплыв мигрантов", lambda c: setattr(c,'population',c.population+5)),
        ]
        n, fn = random.choice(ev)
        t = random.choice([c for c in self.countries if c.alive])
        fn(t)
        return [clr(f"🎲 {n} — {t.name}", C.Dim)]
    def check_victory(self):
        if not self.player.alive: return
        alive = [c for c in self.countries if c.alive]
        st = max(alive, key=lambda c: c.power())
        if st == self.player and len(alive) <= 3:
            Sound.victory()
            self.game_over(True, "Вы стали доминирующей державой!")
    def game_over(self, win, msg=""):
        col = C.G if win else C.R
        if win: Sound.victory()
        else: Sound.defeat()
        print("\n" + clr("╔" + "═"*58 + "╗", col))
        tag = clr("🎉 ПОБЕДА! ", C.Bold+C.G) if win else clr("💀 ПОРАЖЕНИЕ. ", C.Bold+C.R)
        print(clr("║ ", col) + (tag + msg)[:60] + clr(" ║", col))
        print(clr("╚" + "═"*58 + "╝", col))
        print(f"Итоговый ход: {self.turn}")
        if self.player: self.player.show_stats()
        print(clr("\nФинальный расклад:", C.Bold))
        for c in sorted(self.countries, key=lambda x: -x.power()):
            st = clr("жива", C.G) if c.alive else clr("уничтожена", C.R)
            terr = f" ({len(c.territory)} рег.)" if len(c.territory)>1 else ""
            nk = " ☢️" if c.has_nuke() else ""
            print(f"  {c.name:<16} сила {c.power():>5.0f}  👥 {c.population:>6.1f} млн{terr}{nk}  [{st}]")
        input("\nEnter для выхода...")
        raise SystemExit
    def run(self):
        print(clr("╔" + "═"*62 + "╗", C.M))
        print(clr("║  🎭 ИИ-мастер готов. Нейросеть обучилась прямо сейчас.  ║", C.M))
        print(clr("╚" + "═"*62 + "╝", C.M))
        self.choose_country()
        while self.turn <= self.max_turns:
            if self.world_anger > 0:
                print(clr(f"\n😨 Мир всё ещё осуждает вас за ядерный удар "
                          f"(осталось {self.world_anger} ходов).", C.R))
                self.world_anger -= 1
            self.player.show_stats()
            self.chat_loop()
            for e in self.ai_turn(): print(e)
            for e in self.world_reactions(): print(e)
            for e in self.check_war_exhaustion(): print(e)
            for e in self.resolve_wars(): print(e)
            for e in self.random_event(): print(e)
            for c in self.countries:
                if not c.alive: continue
                c.money += c.resource_income()
                c.money += c.trade_income(self)
                c.money += 5
                c.stability = min(100, c.stability + 1)
                c.science = max(0, c.science + max(-1, c.law_mod("sci") // 5))
                c.population += c.pop_growth()
                stab_d, money_d, fac_events = c.faction_tick()
                c.stability = max(0, c.stability + stab_d)
                c.money = max(0, c.money + money_d)
                for e in fac_events: print(clr(e, C.R))
            proposals = self.generate_proposals()
            self.present_proposals(proposals)
            self.check_victory()
            if not self.player.alive:
                self.game_over(False, "Ваша страна пала.")
            self.turn += 1
            Sound.turn()
        alive = [c for c in self.countries if c.alive]
        st = max(alive, key=lambda c: c.power())
        if st == self.player: self.game_over(True, "Вы — сильнейшая держава мира!")
        else: self.game_over(False, f"Сильнейшая держава — {st.name}.")

if __name__ == "__main__":
    try:
        random.seed(42)
        brain = MasterBrain()
        Game(brain).run()
    except SystemExit:
        raise
    except Exception:
        print("\n" + "=" * 55)
        print("⚠️  Произошла непредвиденная ошибка:")
        print("=" * 55)
        import traceback
        traceback.print_exc()
        input("\nEnter для выхода...")