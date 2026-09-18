"""
Задача фибоначи
import math
N = int(input("Введите N: ")) - 1
Fibonachi_num = 1
j = 1;
i = 0
while N != 0:
    i += j
    Fibonachi_num = i
    i = j
    j = Fibonachi_num
    N-=1
print(Fibonachi_num)
"""

N = int(input("Число изучаемых слов: "))
words = {}
for i in range(0, N):
    word = input("Изучаемое слово: ")
    print("   ---   ", end = "")
    words[word] = input().split(',')
print(words)



    


    


