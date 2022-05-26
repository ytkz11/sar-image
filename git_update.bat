@echo off
git add .
git commit -m"Auto-committed on %date% %time%"&&git push origin master
echo. & pause