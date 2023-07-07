@echo off
chcp 65001
clear

:: В строке ниже перечислить пути через пробел
set list="D:\SVN\Folder1" "D:\SVN\Folder2" "D:\SVN\Folder3"


for %%A in (%list%) do svn up %%A
@pause