import random
from datetime import datetime, timedelta

TODAY = datetime(2026, 6, 29)

class Rng:
    def __init__(self, seed=20260629):
        self._r = random.Random(seed)
    def int(self, a, b): return self._r.randint(a, b)
    def float(self, a, b, d=1): return round(self._r.uniform(a, b), d)
    def pick(self, lst): return self._r.choice(lst)

rng = Rng()

DOMAINS = ['ERP','CRM','BI / Аналитика','Инфраструктура','Кибербезопасность','ИИ-платформа','DWH','HRMS','Финансы']
SYS_NAMES = [
    'SAP ERP','1С:ERP','Salesforce CRM','Microsoft Dynamics','Tableau / BI',
    'Active Directory','Zabbix / Мониторинг','ML Platform','Oracle DWH',
    'Kafka / Шина данных','1С:ЗУП','Финансовая система','SIEM / SOC','K8s Кластер',
    'API Gateway','Data Lake'
]
OWNERS = ['А. Иванов','М. Петрова','С. Кузнецов','Д. Смирнова','Р. Волков','Е. Новикова','К. Лебедев']

def get_systems():
    rows = []
    for i, name in enumerate(SYS_NAMES):
        avail = rng.float(96.5, 99.95, 2)
        sla = rng.pick([98.0, 99.0, 99.5])
        status = '🟢 Норма' if avail >= sla else ('🟡 Внимание' if avail >= sla - 1 else '🔴 Критично')
        rows.append({
            'Система': name, 'Домен': DOMAINS[i % len(DOMAINS)],
            'Критичность': rng.pick(['Критическая','Высокая','Средняя']),
            'Доступность %': avail, 'SLA-цель %': sla,
            'Статус': status, 'Владелец': rng.pick(OWNERS),
            'Обновлено': (TODAY - timedelta(days=rng.int(0,5))).strftime('%d.%m.%Y')
        })
    return rows

INC_TITLES = [
    'Недоступность SAP ERP в регионах','Сбой интеграции CRM → DWH','Деградация API Gateway',
    'Инцидент безопасности: аномальный трафик','Ошибки в отчётах BI','Падение ML-платформы',
    'Перебои в 1С:ЗУП','Задержки репликации данных','Сбой Kafka','Превышение SLA по финансовой системе',
    'Уязвимость в AD','Недоступность Data Lake','Ошибки в SIEM','Отказ K8s нод',
    'Потеря сессий в CRM','Аварийный рестарт Oracle DWH'
]

def get_incidents():
    rows = []
    for i, title in enumerate(INC_TITLES):
        sev = rng.pick(['Критический','Высокий','Средний','Низкий'])
        stat = rng.pick(['Открыт','В работе','Закрыт'])
        created = TODAY - timedelta(days=rng.int(0, 60))
        closed = (created + timedelta(days=rng.int(1,10))).strftime('%d.%m.%Y') if stat == 'Закрыт' else '—'
        rows.append({
            'ID': f'INC-{1000+i}', 'Заголовок': title,
            'Система': rng.pick(SYS_NAMES),
            'Критичность': sev, 'Статус': stat,
            'Создан': created.strftime('%d.%m.%Y'), 'Закрыт': closed,
            'Владелец': rng.pick(OWNERS), 'Реакция (ч)': rng.float(0.5, 48, 1)
        })
    return rows

RISK_NAMES = [
    'Потеря доступности ключевых систем','Утечка персональных данных','Дрейф ML-моделей',
    'Несоответствие данных регуляторным требованиям','Атака на периметр','Критические уязвимости в ПО',
    'Недостаточное качество данных для ИИ','Несанкционированный доступ к DWH',
    'Аппаратный отказ в ЦОД','Зависимость от единственного вендора ПО',
    'Ошибка AI-решения в prod','Нехватка компетенций по MLOps'
]
RISK_CATS = ['Технологический','Данные','Кибербезопасность','AI']
PLANS = [
    'Внедрить резервирование','Провести аудит безопасности','Настроить алерты дрейфа',
    'Обновить регламенты','Усилить защиту периметра','Патчинг критичных систем',
    'Улучшить DQ-процессы','Расширить права доступа с MFA','Обновить железо ЦОД',
    'Диверсифицировать вендоров','Расширить мониторинг AI','Нанять MLOps-инженеров'
]

def get_risks():
    rows = []
    for i, name in enumerate(RISK_NAMES):
        prob = rng.int(1, 5)
        impact = rng.int(1, 5)
        level = prob * impact
        rows.append({
            'Риск': name, 'Категория': RISK_CATS[i % len(RISK_CATS)],
            'Вероятность': prob, 'Влияние': impact, 'Уровень': level,
            'Статус': '🔴 Критично' if level >= 15 else ('🟡 Внимание' if level >= 8 else '🟢 Норма'),
            'Владелец': rng.pick(OWNERS), 'План митигации': PLANS[i]
        })
    return sorted(rows, key=lambda x: -x['Уровень'])

PROJ_NAMES = [
    'Внедрение ML Platform v2','Миграция на облако (Azure)','Трансформация DWH',
    'Программа киберзащиты 2026','BI Next Generation','Data Governance программа',
    'Автоматизация HR-процессов','Масштабирование AI use-cases','Переход на SAP S/4HANA',
    'Внедрение SIEM нового поколения'
]
PROJ_ROLES = ['CIO','CDO','CTO','CAIO','CEO']

def get_projects():
    rows = []
    for i, name in enumerate(PROJ_NAMES):
        progress = rng.int(10, 95)
        budget_plan = rng.int(20, 200)
        dev = rng.float(-5, 35, 1)
        budget_fact = round(budget_plan * (1 + dev / 100), 1)
        status = '🟢 Норма' if (progress >= 70 and dev < 10) else ('🟡 Внимание' if (progress >= 40 or dev < 20) else '🔴 Критично')
        deadline = (TODAY + timedelta(days=rng.int(-30, 180))).strftime('%d.%m.%Y')
        rows.append({
            'Проект': name, 'Роль': PROJ_ROLES[i % len(PROJ_ROLES)],
            'Прогресс %': progress, 'Бюджет план (млн)': budget_plan,
            'Бюджет факт (млн)': budget_fact, 'Отклонение %': dev,
            'Статус': status, 'Срок': deadline, 'Владелец': rng.pick(OWNERS)
        })
    return rows

DQ_SOURCES = ['SAP ERP','1С:ЗУП','Oracle DWH','Salesforce CRM','Kafka','Data Lake','Финансовая система','HRMS']

def get_data_quality():
    rows = []
    for source in DQ_SOURCES:
        comp = rng.float(72, 99.5, 1)
        acc  = rng.float(75, 99.5, 1)
        tim  = rng.float(70, 99.5, 1)
        score = round((comp + acc + tim) / 3, 1)
        status = '🟢 Норма' if score >= 90 else ('🟡 Внимание' if score >= 75 else '🔴 Критично')
        int_st = rng.pick(['✅ OK','⚠️ Деградация','❌ Ошибка'])
        rows.append({
            'Источник': source, 'Полнота %': comp, 'Точность %': acc,
            'Своевременность %': tim, 'Индекс качества': score,
            'Интеграция': int_st, 'Статус': status
        })
    return rows

AI_NAMES = [
    'Предиктивное обслуживание оборудования','AI-ассистент для поддержки клиентов',
    'Оптимизация цепочки поставок (ML)','Fraud Detection в финансах',
    'Автоматическая сегментация клиентов','Прогнозирование спроса',
    'AI-генерация отчётов','Аномалии в логах (SIEM AI)',
    'Рекомендательная система для CRM','NLP-обработка документов'
]
AI_DOMAINS = ['Производство','Продажи','Логистика','Финансы','Маркетинг','Коммерция','Аналитика','Безопасность']
AI_MATURITY = ['Идея','Пилот','Тестирование','Масштабируется','Производство']

def get_ai_initiatives():
    rows = []
    for i, name in enumerate(AI_NAMES):
        maturity = rng.pick(AI_MATURITY[1:])
        adoption = rng.int(5, 95)
        effect = rng.float(0.5, 45, 1)
        status = '🟢 Норма' if adoption >= 60 else ('🟡 Внимание' if adoption >= 30 else '🔴 Критично')
        rows.append({
            'AI Use-case': name, 'Домен': AI_DOMAINS[i % len(AI_DOMAINS)],
            'Зрелость': maturity, 'Внедрение %': adoption,
            'Эффект (млн/мес)': effect, 'Статус': status, 'Владелец': rng.pick(OWNERS)
        })
    return rows

def get_recommendations():
    return [
        {'Рекомендация': 'Немедленно эскалировать инцидент INC-1000 (SAP ERP) — нарушен SLA.', 'Роль': 'CIO', 'Приоритет': '🔴 Высокий', 'Срок': '30.06.2026'},
        {'Рекомендация': 'Утвердить бюджет на устранение уязвимости в AD до конца недели.', 'Роль': 'CTO', 'Приоритет': '🔴 Высокий', 'Срок': '02.07.2026'},
        {'Рекомендация': 'Пересмотреть приоритеты портфеля AI: проекты с дрейфом модели требуют ревью.', 'Роль': 'CAIO', 'Приоритет': '🔴 Высокий', 'Срок': '04.07.2026'},
        {'Рекомендация': 'Согласовать Data Governance политику — 3 источника не соответствуют требованиям.', 'Роль': 'CDO', 'Приоритет': '🔴 Высокий', 'Срок': '06.07.2026'},
        {'Рекомендация': 'Запланировать стратегическую сессию по миграции в облако.', 'Роль': 'CEO', 'Приоритет': '🟡 Средний', 'Срок': '13.07.2026'},
        {'Рекомендация': 'Расширить команду MLOps: дефицит компетенций тормозит масштабирование AI.', 'Роль': 'CAIO', 'Приоритет': '🟡 Средний', 'Срок': '13.07.2026'},
        {'Рекомендация': 'Инициировать аудит поставщика BI-системы — SLA нарушался 3 раза за квартал.', 'Роль': 'CIO', 'Приоритет': '🟡 Средний', 'Срок': '20.07.2026'},
        {'Рекомендация': 'Обновить регламент обработки данных согласно новым требованиям регулятора.', 'Роль': 'CDO', 'Приоритет': '🟢 Низкий', 'Срок': '13.08.2026'},
        {'Рекомендация': 'Организовать демонстрацию AI-эффекта для совета директоров (ROI).', 'Роль': 'CEO', 'Приоритет': '🟢 Низкий', 'Срок': '29.07.2026'},
        {'Рекомендация': 'Пересмотреть архитектуру Kafka — задержки репликации влияют на качество данных.', 'Роль': 'CTO', 'Приоритет': '🟢 Низкий', 'Срок': '29.07.2026'},
    ]
