@echo off
echo Тест 1: Запуск со всеми параметрами
python src/vfs.py --vfs-path "C:\vfs_data" --startup-script "scripts\commands.vfs"
pause