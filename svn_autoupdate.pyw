# -*- coding: utf-8 -*-
import subprocess, os

rep_paths = ['E:\\SVN\\Папка 1', 'E:\\SVN\\Папка 2', 'E:\\SVN\\Папка 3']

print('Не прерывать!')
for i in range(len(rep_paths)):
    print('Обновляю ' + rep_paths[i])
    os.popen('svn up "' + rep_paths[i] + '"')
    print('ok')
print('Все папки обновлены. Нажмите на любую клавишу для выхода.')
#os.popen('@pause')
