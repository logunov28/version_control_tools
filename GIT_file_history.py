# Программа показывает историю изменений файла в git
# Достаточно дарг-эн-дропом перенести файл на иконку программы

import sys, os, subprocess


try:
	#drag'n'drop на иконку
	droppedFile = sys.argv[1]
except:
	droppedFile = input('Введите путь к файлу: ')
	droppedFile = droppedFile.replace('"', '')

filename = droppedFile.split('\\')[-1]
path = '\\'.join(droppedFile.split('\\')[:-1])
os.chdir(path)
out = subprocess.Popen('git blame --incremental ' + filename, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
out = out.split('filename')[:-1]
out.reverse()
output = 'История изменений файла:'

for i in range(len(out)):
	st = out[i].split('\n')
	author = 'Unknown'
	commit = 'Unknown'
	commit_date = 'Unknown'
	for j in range(len(st)):
		if 'author ' in st[j]:
			author = ' '.join(st[j].split(' ')[1:])
			commit = st[j-1].split(' ')[0]
			commit_date = os.popen('git show -s --format=%ci ' + commit).read()
	output += '\n' + str(i+1) + ') ' + author + ' ' + commit_date[:-7] + ' ' + commit


print(output)
input()
