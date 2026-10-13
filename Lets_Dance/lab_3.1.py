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

def calculate_s (numbers): # вычислим число интервалов по формуле Стёрджеса
    N = len(numbers)
    s = 1 + 3.322 * math.log10(N)
    return int(s)
def calculate_h (numbers): #считаем длину одного интервала
    min_age = min(numbers)
    max_age = max(numbers)
    h = math.ceil((max_age - min_age) / calculate_s(numbers))
    return h
def make_intervals (numbers): # построение интервального ряда 
    h = calculate_h(numbers)
    sn = set(numbers)
    all_intervals = []
    min_val = min(numbers)
    left = min_val
    s = calculate_s(numbers)
    for i in range(s):
        right = left + h
        all_intervals.append([left, right])
        left = right
    return all_intervals

def make_intervals_manual(data, s):# построение интервального ряда по средним
    min_val = min(data)
    max_val = max(data)
    h = (max_val - min_val) / s
    intervals = []
    left = min_val
    for i in range(s):
        right = left + h
        intervals.append([left, right])
        left = right
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
def calc_values_of_criteries(chastots, teor):
    n = sum(chastots)
    x_nabl = sum([(chastots[i] - teor[i])**2 / teor[i] for i in range(len(chastots))])
    k = len(chastots) - 3
    alpha = 0.05
    x_kr = chi2.ppf(1 - alpha, k)
    return x_nabl, x_kr, considering_x(x_nabl, x_kr)

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
    

# 
def inteval_raw_building(numbers, n, N):
    # === Ряд № 1: возраст ===
    intervals_1 = make_intervals(numbers) # получение интервального ряда
    ch_n = caclulating_chastots(numbers, intervals_1)# вычисление частот
    midx, sko = calulate_SKO(ch_n, intervals_1, len(numbers))# вычисление среднего и СКО
    first_normraw = normirovanie(midx, sko, intervals_1)#получение нормированного ряда
    p_first, laplace_val_one = laplace_function(first_normraw) # получение списка вероятностей и значений лапласа
    teor_1 = teor_chastots_calc(p_first, len(numbers)) # получение списка теоретических частот
    x_nabl_1, x_kr_1, answer_1 = calc_values_of_criteries(ch_n, teor_1) # получение X набл. и крит. с ответом
    
    print("-----Ряд № 1: Возраст-----")
    print_table(intervals_1, first_normraw, laplace_val_one, p_first, ch_n, teor_1, answer_1)# построение таблицы для первого ряда
    
    # === Ряд № 2: средний возраст ===
    all_selections, mid = lets_make_a_groops(numbers, n, N) 
    intervals_2 = make_intervals_manual(mid, 4) # получение интервального ряда
    ch_mids = caclulating_chastots(mid, intervals_2) # вычисление частот
    sec_midx, sec_sko = calulate_SKO(ch_mids, intervals_2, len(mid))# вычисление среднего и СКО
    second_normraw = normirovanie(sec_midx, sec_sko, intervals_2)#получение нормированного ряда
    p_second, laplace_val_two = laplace_function(second_normraw)# получение списка вероятностей и значений лапласа
    teor_2 = teor_chastots_calc(p_second, len(mid))# получение списка теоретических частот
    x_nabl_2, x_kr_2, teor_2, answer_2 = calc_values_of_criteries(ch_mids, teor_2)# получение X набл. и крит. с ответом
    
    print("----Ряд № 2: Средний возраст-----")
    print_table(intervals_2, second_normraw, laplace_val_two, p_second, ch_mids, teor_2, answer_2)# построение таблицы для второго ряда

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