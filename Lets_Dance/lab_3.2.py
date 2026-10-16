#Библиотеки
from math import ceil, sqrt
from pathlib import Path # Библиотека для работы с файлами и их адресами
from scipy.stats import f
from scipy.stats import chi2
from scipy.stats import norm
import math # Библиотка для математический действий
import pandas as pd # Красивые таблицы в питоне
from random import randint

def calculate_n (d):# Высчитываем объем группы для одной выборки
   y = 0.95 # надежность из условия из условия
   b = 3 # точность оценки математического ожидания из условия
   f_t = (y+1) / 2
   t = norm.ppf(f_t) 
   n = t**2 * d**2 / b**2
   n = int(math.ceil(n))  # округляем в большую сторону чтобы n было целым числом
   return n

def lets_make_a_groops (numbers, n, N): # создаем 2 группы по полученному n (объему выборки) из функции calculate_n
    k = 2 # количество групп из условия
    all_selections = [] # список со списками выборок, 2 штук
    for selection in range(k):
        one = [] # одна выборка
        for num in range(n):
            i = randint(0, N - 1) # выбор случайных чисел по условию репрезитативности выборки
            one.append(numbers[i]) # добавление элемента выборку
        all_selections.append(one) # добавление одной выборки в список выборок
    return all_selections # возвращает список списокв выборок и списком средних

def calculating_dispersia_s (selection): # функция для расчета  ско исправленной дисперсии
    n = len(selection)
    sn = set(selection) # уникальные значения выбокри
    k = n - 1 # число свободы
    x_midl = sum([i * selection.count(i) for i in sn]) / n # среднее
    d = sum([selection.count(i) * (i - x_midl)**2 for i in sn]) / k # исправленная дисперсия
    return d

def observed_f (s1, s2):# функция для расчета  F набл.
    max_s = max(s1, s2)
    min_s = min(s1, s2)
    f_nabl = max_s/min_s
    return f_nabl

def calc_f_criet (s1, s2, k1, k2, two_sided): # функция для расчета  F критического.
    if s1 >= s2: 
        k_big, k_small = k1, k2
    else:
        k_big, k_small = k2, k1
    alpha = 0.05
    if two_sided == False: # проверка на двухсторонность
        # Правосторонняя (H1: D1 > D2)
        return f.ppf(1 - alpha, k_big, k_small)
    else:
        # Двусторонняя (H1: D1 != D2)
        return f.ppf(1 - alpha/2, k_big, k_small)

def output (f_nabl, F_kr): # функция которая по результатам F критического и F набл делает вывод об гипотезе H0
    string = ""
    if f_nabl < F_kr:
        string = f"Нет оснований отвергнуть H0 (дисперсии равны)."
    else:
        string = "H0 отвергается (дисперсии различаются)."
    return string

def analize_res (f_kr_right, f_kr_two, n1, n2, s1, s2, k1, k2, f_nabl):
    print(f"Выборка 1: n1 = {n1}, s1^2 = {s1:.4f}")
    print(f"Выборка 2: n2 = {n2}, s2^2 = {s2:.4f}")
    print(f"k1 = {k1}, k2 = {k2}")
    print(f"F_набл = {f_nabl:.4f}")
    alpha = 0.05
    print(f"F_кр (α = {alpha}, правосторонняя) = {f_kr_right:.4f}")
    print(f"F_кр (α = {alpha}, двусторонняя) = {f_kr_two:.4f}")
    print("----а) H1: D1 > D2-----")
    print(f"Вывод для правосторонней критической области: {output (f_nabl, f_kr_right)}")
    print()
    print("----б) H1: D1 != D2----")
    print(f"Вывод для двухсторонней критической области: {output (f_nabl, f_kr_two)}")

def task (all_selections, n): 
    # Число степеней свободы
    # Выборки
    selection1 = all_selections[0]
    selection2 = all_selections[1]
    # Их исправленные дисперсии
    s1 = calculating_dispersia_s (selection1)
    s2 = calculating_dispersia_s (selection2)
    # Их объемы
    n1 = len(selection1)
    n2 = len(selection2)
    # Их степени свободы
    k1 = n1 - 1
    k2 = n2 - 1
    # Вычисление наблюдаемого f
    f_nabl = observed_f(s1, s2)
    # Рассчет правостороннего и двухстороннего критерия
    f_kr_right =  calc_f_criet (s1, s2, k1, k2, False) # Правосторонняя
    f_kr_two =  calc_f_criet (s1, s2, k1, k2, True) # Двухсторонняя 
    #Прокоментировать результаты и подвести вывод
    analize_res(f_kr_right, f_kr_two, n1, n2, s1, s2, k1, k2, f_nabl)


fp = Path("./Москва_2021.txt") 
if fp.exists():
    with open(fp, "r", encoding="utf-8") as file: # Открыть и прочитать файл, на любом языке с переменной файла file
        numbers = sorted([int(line.strip()) for line in file if line.strip()])
    sn = sorted(set(numbers))
    N = 0 # Сумма частот
    x_midl = 0 # Среднее +
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
    all_selections = lets_make_a_groops(numbers, n, N) # получаем список списков групп + список средних
    task(all_selections, n) # строим интервальный ряд
else:
    print("Скачайте или создайте файл Москва_2021.txt")