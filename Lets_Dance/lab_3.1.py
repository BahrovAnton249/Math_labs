#Библиотеки
from math import ceil, sqrt
from pathlib import Path # Библиотека для работы с файлами и их адресами
from scipy.stats import t
from scipy.stats import norm
from scipy.stats import chi2
import math # Библиотка для математический действий
import matplotlib.pyplot as plt # библиотека для рисования графико и диаграмм в в питоне.
import pandas as pd # Красивые таблицы в питоне
from random import randint
pd.set_option('display.max_columns', None)   # показать все столбцы
pd.set_option('display.width', 200)          # ширина вывода
pd.set_option('display.max_colwidth', 30)    # ширина столбцов

def make_intervals (numbers, k=7): # построение интервального ряда из лабы 1.1: k групп с равными интервалами
    x_min = min(numbers)
    x_max = max(numbers)
    h = math.ceil((x_max - x_min) / k) # длина одного интервала
    edges = [x_min + i * h for i in range(k + 1)] # границы интервалов
    return [[edges[i], edges[i + 1]] for i in range(k)]

def make_intervals_unit(data):# построение интервального ряда средних: от floor(min) до ceil(max), длина интервала 1 год
    left = math.floor(min(data))
    right = math.ceil(max(data))
    intervals = []
    for x in range(left, right):
        intervals.append([x, x + 1])
    return intervals

def calculate_n (d):# Высчитываем объем группы для одной выборки
   y = 0.95 # надежность из условия из условия
   b = 3 # точность оценки математического ожидания из условия
   f_t = (y+1) / 2
   t = norm.ppf(f_t) 
   n = t**2 * d**2 / b**2
   n = int(math.ceil(n))  # округляем в большую сторону чтобы n было целым числом
   return n

# Создание групп и нахождение средних
def lets_make_a_groops (numbers, n, N): # создаем 36 групп по полученному n (объему выборки) из функции calculate_n
    k = 36 # количество групп из условия
    all_selections = [] # список со списками выборок, 36 штук
    mid = [] # среднии для каждой выборки
    for selection in range(k):
        one = [] # одна выборка
        sum_ = 0 # сумма для подсчета среднего
        for num in range(n):
            i = randint(0, N - 1) # выбор случайных чисел по условию репрезитативности выборки
            one.append(numbers[i]) # добавление элемента выборку
            sum_ += numbers[i]
        mid.append(sum_ / len(one)) # подсчет средней
        all_selections.append(one) # добавление одной выборки в список выборок
    return all_selections, mid # возвращает картеж со списком списокв выборок и списком средних

# Общая функция для высчитывания частот для обоих рядов
def caclulating_chastots(numbers, all_someth, mids=None): 
    chastots = []
    data = mids if mids is not None else numbers # услоиве на другое поведение если в функцию передаются средние
    for i, interval in enumerate(all_someth):
        k = 0
        if i == len(all_someth) - 1:
            for val in data:
                if interval[0] <= val <= interval[1]:# включаем последний элемент
                    k += 1
            chastots.append(k)
        else:
            for val in data:
                if interval[0] <= val < interval[1]:
                    k += 1
            chastots.append(k)
    return chastots

# Общая функция для высчитывания СКО и среднего  для обоих рядов
def calulate_SKO (chastots, intervals, N):
    mids = []
    for interval in intervals:
        mids.append((interval[0] + interval[-1])/2)
    midle_x = sum([ mids[i] * chastots[i]   for i in range(0, len(mids))]) / N # среднее
    sko = sqrt(sum( [chastots[i] * (mids[i] - midle_x)**2   for i in range(0, len(mids))]) / N) # СКО
    return midle_x, sko

# Общая функция нормирования для обоих рядов
def normirovanie(x_midle, d, intervals):
    # Начинаем с левой границы первого интервала
    normirovan_raw = [(intervals[0][0] - x_midle) / d]
    # Добавляем правую границу каждого интервала
    for interval in intervals:
        normirovan_raw.append((interval[1] - x_midle) / d)
    # Крайние значения — бесконечности
    normirovan_raw[0] = -math.inf
    normirovan_raw[-1] = math.inf
    return normirovan_raw

# Общая функция для лапласа
def laplace(z_val):
    return norm.cdf(z_val) - 0.5

# Общая функция для вычисления вероятностей для нормированного ряда
def laplace_function (z):
    val_laplse = [laplace(z[i]) for i in range(len(z) - 1)]
    p = [laplace(z[i+1]) - laplace(z[i]) for i in range(len(z) - 1)]
    return p, val_laplse
# Общая функция для вычисления теоретического ряда
def teor_chastots_calc (p, n):
    teor = []
    for i in range(0, len(p)):
        teor.append(p[i] * n)
    return teor
# Общая функция для вывода ответа 
def considering_x (x_nabl, x_kr):
    answer = ""
    if(x_nabl < x_kr):
        answer = f"X(наблюдаемое)=={x_nabl:.4f} < X(критического)=={x_kr:.4f}, значит нет оснований отвергнуть нулевую гипотезу (данные согласуются с нормальным распределением)."
    else:
        answer = f"X(наблюдаемое)=={x_nabl:.4f} >= X(критического)=={x_kr:.4f}, значит нулевая гипотеза отвергается (данные не согласуются с нормальным распределением).."
    return answer

# Общая функция для вычисления критериев 
def calc_values_of_criteries(chastots, teor, alpha):
    x_nabl = sum([(chastots[i] - teor[i])**2 / teor[i] for i in range(len(chastots))])
    k = len(chastots) - 3 # k = s - 1 - r, r = 2 (оцениваем среднее и СКО)
    x_kr = chi2.ppf(1 - alpha, k)
    return x_nabl, x_kr, k, considering_x(x_nabl, x_kr)

# Объединение малочисленных интервалов (теоретическая частота < 5)
def merge_small_intervals(intervals, norm_raw, laplace_val, p, chastots, teor, min_teor=5):
    groups = [] # каждая группа: [первый индекс, последний индекс]
    start = 0
    acc = 0 # накопленная теоретическая частота текущей группы
    for i in range(len(teor)):
        acc += teor[i]
        if acc >= min_teor:
            groups.append([start, i])
            start = i + 1
            acc = 0
    if start < len(teor): # остался малый хвост — присоединяем к последней группе
        if groups:
            groups[-1][1] = len(teor) - 1
        else:
            groups.append([0, len(teor) - 1])
    new_int, new_norm, new_lap, new_p, new_ch, new_teor = [], [], [], [], [], []
    for first, last in groups:
        new_int.append([intervals[first][0], intervals[last][1]])
        new_norm.append(norm_raw[first])
        new_lap.append(laplace_val[first])
        new_p.append(sum(p[first:last + 1]))
        new_ch.append(sum(chastots[first:last + 1]))
        new_teor.append(sum(teor[first:last + 1]))
    new_norm.append(norm_raw[-1])
    return new_int, new_norm, new_lap, new_p, new_ch, new_teor

# Функция для вывода таблицы с ответами
def print_table(intervals, norm_raw, laplace_value, p, imper_chastots, teor_chastots, answer):
    data = []
    for i in range(len(intervals)):
        if i == len(intervals) - 1:
            string = [
            f"[{intervals[i][0]:.2f}, {intervals[i][1]:.2f}]",
            f"({norm_raw[i]:.2f}, {norm_raw[i+1]:.2f})",
            f"{laplace_value[i]:.4f}",
            f"{p[i]:.4f}",
            imper_chastots[i],
            f"{teor_chastots[i]:.2f}",]
        else:
            string = [
            f"[{intervals[i][0]:.2f}, {intervals[i][1]:.2f})",
            f"({norm_raw[i]:.2f}, {norm_raw[i+1]:.2f})",
            f"{laplace_value[i]:.4f}",
            f"{p[i]:.4f}",
            imper_chastots[i],
            f"{teor_chastots[i]:.2f}",]
        data.append(string)
    df = pd.DataFrame(data, columns=[
        "Интервалы", "Норм. границы", "Ф(z)", "Вероятности",
        "Эмпир. частоты", "Теор. частоты"
    ])
    print(df)
    print("-" * 64)
    print("Проверка нулевой гипотезы:")
    print(answer)
    

# Проверка нулевой гипотезы о нормальном распределении по критерию Пирсона
# intervals — интервальный ряд, chastots — эмпирические частоты, alpha — уровень значимости
def pearson_test(intervals, chastots, alpha, title):
    n = sum(chastots)
    midx, sko = calulate_SKO(chastots, intervals, n) # среднее и СКО
    norm_raw = normirovanie(midx, sko, intervals) # нормированные границы
    p, laplace_val = laplace_function(norm_raw) # вероятности и значения Лапласа
    teor = teor_chastots_calc(p, n) # теоретические частоты
    # объединяем интервалы, где теоретическая частота меньше 5
    intervals, norm_raw, laplace_val, p, chastots, teor = merge_small_intervals(
        intervals, norm_raw, laplace_val, p, chastots, teor)
    x_nabl, x_kr, k, answer = calc_values_of_criteries(chastots, teor, alpha)
    print(title)
    print(f"n = {n}, x_ср = {midx:.4f}, СКО = {sko:.4f}, α = {alpha}, число интервалов s = {len(intervals)}, k = {k}")
    print_table(intervals, norm_raw, laplace_val, p, chastots, teor, answer)
    return x_nabl, x_kr

def inteval_raw_building(numbers, n, N, alpha=0.05):
    # === Ряд № 1: возраст ===
    intervals_1 = make_intervals(numbers) # получение интервального ряда
    ch_n = caclulating_chastots(numbers, intervals_1)# вычисление частот
    pearson_test(intervals_1, ch_n, alpha, "-----Ряд № 1: Возраст-----")

    # === Ряд № 2: средний возраст ===
    all_selections, mid = lets_make_a_groops(numbers, n, N)
    intervals_2 = make_intervals_unit(mid) # интервалы длиной 1 год
    ch_mids = caclulating_chastots(mid, intervals_2) # вычисление частот
    pearson_test(intervals_2, ch_mids, alpha, "----Ряд № 2: Средний возраст-----")

fp = Path("./Москва_2021.txt") 
if fp.exists():
    with open(fp, "r", encoding="utf-8") as f: # Открыть и прочитать файл, на любом языке с переменной файла f
        numbers = sorted([int(line.strip()) for line in f if line.strip()])
    sn = set(numbers)
    N = 0 # Сумма частот
    x_midl = 0 # Среднее
    for i in sn:
        n = numbers.count(i) # кол. элемента
        x_midl += i * n # высчитываем сумму среднего, но пока без деления на сумму частот
        N+= n
    x_midl /= N
    D = 0
    for i in sn:
        D += (i - x_midl)**2 * numbers.count(i)
    D = D / N # Дисперсия
    d = math.sqrt(D) # среднее квадратичное отклонение
    n = calculate_n(d) # высчитываем объем
    inteval_raw_building(numbers, n, N) # получаем список списков групп + список средних
    
else:
    print("Скачайте или создайте файл Москва_2021.txt")