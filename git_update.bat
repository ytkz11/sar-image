@echo off
set mydate=%date:/=%
set mytime=%time::=%
set mytimestamp=%mydate: =_%_%mytime:.=_%
git add .
git commit -m"Auto-committed on %mytimestamp%"&&git push origin master
echo. & pause
