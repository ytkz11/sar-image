@echo off
set datetimef=%date:~-4%_%date:~3,2%_%date:~0,2%__%time:~0,2%_%time:~3,2%_%time:~6,2%
git add .
git commit -m"Auto-committed on %datetimef%"&&git push origin master
echo. & pause