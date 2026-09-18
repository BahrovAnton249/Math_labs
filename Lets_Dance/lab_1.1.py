# py -m pip install matplotlib
#Библиотеки
from math import ceil
from pathlib import Path # Библиотека для работы с файлами и их адресами
from collections import Counter #
import math # Библиотка для математический действий
import matplotlib.pyplot as plt # библиотека для рисования графико и диаграмм в в питоне.

# Раздел 2. Функции для вычисления стат. характеристик.
def Calc_stat_Haracteristiki (numbers):
    sn = sorted(set(numbers)) # Отсортированный список без повторений элементов
    N = 0 # Сумма частот
    x_midl = 0 # Среднее +
    moda = 0 # Мода +
    r = float("-inf")# Частота моды + 
    mediana = 0 # медиана + 
    mi = min(sn) # минимум +
    ma = max(sn) # максимум +
    razmah = ma - mi # размах +
    for i in sn:
        n = numbers.count(i) # кол. элемента
        x_midl += i * n # высчитываем сумму среднего, но пока без деления на сумму частот
        N+= n
        if(n > r):
            moda = i
            r = n
    x_midl /= N

    #Высчитывание медианы
    half = N / 2 # индекс медианы
    sbor = 0 # накопленная частота
    mediana = 0 # Запись медианы
    for i in sn:
        sbor += numbers.count(i)
        if sbor >= half:
            mediana = i
            break
    print("  ")

    print (f"Среднее: {x_midl}")
    print (f"Мода: {moda} с частотой {r}")
    print (f"Медиана: {mediana}")
    print (f"Минимум: {mi}; Максимум: {ma}; Размах: {razmah}")
    Dispersia(x_midl, sn, numbers, N)

#Функция для вычисления дисперсии и зависщих от ее значения стат. харак.
def Dispersia (x_midl, sn, numbers, N):
     D = 0
     for i in sn:
        D += (i - x_midl)**2 * numbers.count(i)
     D = D / N # Дисперсия
     d = math.sqrt(D) # среднее квадратичное отклонение
     v_x = d / x_midl * 100 # коэфф. вариации в процентах
     print (f"Дисперсия: {D}")
     print (f"Cреднее квадратичное отклонение: {d}")
     print (f"Коэфф. вариации: {v_x}%")

#Раздел 1. Ряды распределения и интервалы с последующими .
# Читаем путь к файлу
fp = Path("./Москва_2021.txt") 
# Дискретный ряд
if fp.exists():
    with open(fp, "r", encoding="utf-8") as f: # Открыть и прочитать файл, на любом языке с переменной файла f
        numbers = sorted([int(line.strip()) for line in f if line.strip()])
    
    print("   ")
    print("Дискретный ряд:")
    print("   ")
    print(f"| {'Значение варианты (x)':>12} | {'Частота (n)':>11} |")
    print("   ")

    counts = Counter(numbers)              # считаем частоты с помощью counter
    discret_val = sorted(counts.keys())         # уникальные значения по возрастанию
    disc_list_of_n = [counts[v] for v in discret_val]
    for val in discret_val:
        print(f"|    {val}| {counts[val]}|")
    print("    ---    ")
    print(f"  | {'Итого'} | {sum(counts.values())} |")

    # Интервальный ряд из 7 групп:
    x_min = min(numbers)
    x_max = max(numbers)
    k = 7
    h = int(ceil((x_max - x_min) / k)) # длина одного интервала

    print("    ---    ")
    print("Интервальный ряд")
    print("    ---    ")
    print(f"min = {x_min}, max = {x_max}, количество групп(k) = {k}, длина интервалов групп(h) = {h:.4f}")
    print("   ")
    print(f"| {'№':>2} | {'Интервал':>18} | {'Середина':>9} | {'Частота':>8} |")

    # границы интервалов
    Edges = [x_min + i * h for i in range(k + 1)]

    # Разбиение на интервалы
    int_f = [0, 0, 0, 0, 0, 0, 0] # сколько n частот попало в каждый интервал
    for num in numbers:
        for i in range(k):
            left_elem = Edges[i]
            right_element = Edges[i + 1]
            # Последний интервал включает правую границу
            if left_elem <= num < right_element:
                    int_f[i] = int_f[i] + 1
                    break
            if i == k - 1 and num == right_element:
                int_f[i] = int_f[i] + 1
                break
    # Вывод интервалов
    for i in range(k):
        left_elem = int(Edges[i])
        right_element = int(Edges[i + 1])
        mid_element = (left_elem + right_element) / 2
        if i == k-1:
            print(f"|{i+1:>2}[{left_elem:>7.2f} – {right_element:<7.2f}]{mid_element:>9.2f}|{int_f[i]:>8}|")
        else:
            print(f"|{i+1:>2}[{left_elem:>7.2f} – {right_element:<7.2f}){mid_element:>9.2f}|{int_f[i]:>8}|")

    print("    ---    ")
    print(f"| {'':>2} | {'Итого':>18} | {'':>9} | {sum(int_f):>8} |")
    mids = [(Edges[i] + Edges[i + 1]) / 2 for i in range(k)]
    print("   ")
    print("Дискретный ряд:")
    print("   ")
    Calc_stat_Haracteristiki(numbers)
    # Создаем здесь список для интервалов, который подойдет под функцую Calc
    print("   ")
    print("Интервальный ряд:")
    print("   ")
    exp = [] # пустой список для развёрнутых значения.
    for mid, freq in zip(mids, int_f):
        exp.extend([mid] * freq)   # добавляем mid freq раз, 
    Calc_stat_Haracteristiki(exp)

    # Раздел 3. Полегон частот и гистограмма для дискретных и интервалных рядов
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Полигон и гистограмма для дискретного ряда
    axes[0, 0].plot(discret_val, disc_list_of_n, marker='o', color='steelblue') # определение переменных для осей
    axes[0, 0].set_title("Полигон частот для дискретного ряда)")
    axes[0, 0].set_xlabel("Возраст")
    axes[0, 0].set_ylabel("Частота")
    axes[0, 0].grid(True, alpha=0.3) # сетка

    axes[0, 1].bar(discret_val, disc_list_of_n, color='steelblue', edgecolor='black', width=0.8)
    axes[0, 1].set_title("Гистограмма частот (дискретный ряд)")
    axes[0, 1].set_xlabel("Возраст")
    axes[0, 1].set_ylabel("Частота")
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # Полигон и гистограмма для интервального ряда
    axes[1, 0].plot(mids, int_f, marker='s', color='darkorange')
    axes[1, 0].set_title("Полигон частот (интервальный ряд)")
    axes[1, 0].set_xlabel("Середина интервала")
    axes[1, 0].set_ylabel("Частота")
    axes[1, 0].grid(True, alpha=0.3)

    axes[1, 1].bar(mids, int_f, width=h * 0.9, color='darkorange', edgecolor='black')
    axes[1, 1].set_title("Гистограмма частот (интервальный ряд)")
    axes[1, 1].set_xlabel("Возраст")
    axes[1, 1].set_ylabel("Частота")
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout() # отступы между графиками.
    plt.show() # отображение общего листа с 4 графиками
else:
    print("Скачайте или создайте файл Москва_2021.txt")