# Программа показывает историю изменений файла в git

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
out = subprocess.Popen('git log ' + filename, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
out = out.split('commit')[1:]
out.reverse()
output = 'История изменений файла:'


counter = 0
for i in range(len(out)):
	st = out[i].split('\n')
	author = st[1][8:]
	commit = st[0]
	commit_date = st[2][8:]
	summary = st[4][4:]
	if author != 'Unknown':
		counter +=1
		output += '\n' + str(i+1) + ') ' + author + ' | ' + commit_date[:-6] + ' |' + commit + '\n   ' + summary


print(output)
input()
