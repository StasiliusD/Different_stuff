"""Вам доступен текстовый файл files.txt, содержащий информацию о файлах.
Каждая строка файла содержит три значения, разделенные символом пробела — имя файла,
его размер (целое число) и единицы измерения:

cant-help-myself.mp3 7 MB
keep-yourself-alive.mp3 6 MB
bones.mp3 5 MB
...
Напишите программу, которая группирует данные файлы по расширению, определяя
общий объем файлов каждой группы, и выводит полученные группы файлов,
указывая для каждой ее общий объем. Группы должны быть расположены в
лексикографическом порядке названий расширений, файлы в группах — в лексикографическом порядке их имен.

Примечание 1. Например, если бы файл files.txt имел вид:

input.txt 3000 B
scratch.zip 300 MB
output.txt 1 KB
temp.txt 4 KB
boy.bmp 2000 KB
mario.bmp 1 MB
data.zip 900 MB
то программа должна была бы вывести:

boy.bmp
mario.bmp
----------
Summary: 3 MB

input.txt
output.txt
temp.txt
----------
Summary: 8 KB

data.zip
scratch.zip
----------
Summary: 1 GB"""

with open('C:/Jupyter/files.txt') as f:
    s = {}
    files = {}
    for i in f.readlines():
        i = i.split()
        name,format,volume,unit = i[0].split('.')[0], i[0].split('.')[1],i[1],i[2]
        unit = unit.replace('KB','1024').replace('MB','1048576').replace('GB','1073741824').replace('B','1')
        overall = int(unit) * int(volume)
        s[format] = s.get(format,0) + overall
        files[format] = files.get(format,'') + f'{name}.{format} '
    for key,value in s.items():
        if value//1073741824:
            s[key] = f'{round(value/1073741824)} GB'
            continue
        elif value//1048576:
            s[key] = f'{round(value/1048576)} MB'
            continue
        elif value//1024:
            s[key] = f'{round(value/1024)} KB'
            continue
        else:
            s[key] = f'{round(value)} B'

    files = dict(sorted(files.items(), key=lambda item: item[0]))
    for key, value in files.items():
        files[key] = sorted(value.strip().split())
    print(s)
    print(files)
    for key,value in files.items():
        print(*value, sep = '\n')
        print('----------')
        print(f'Summary: {s[key]}')
        if key != 'zip':
            print()

