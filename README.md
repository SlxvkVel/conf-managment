# VFS Emulator

Эмулятор командной строки UNIX-подобной ОС с виртуальной файловой системой.

## Этап 4: Основные команды

### Реализованные команды

#### Навигация и просмотр
- `ls [path]` - список содержимого директории
- `cd [path]` - смена текущей директории
- `tree [path]` - древовидное отображение структуры

#### Работа с файлами
- `tail [file]` - вывод последних 10 строк файла

#### Служебные команды
- `uptime` - время работы эмулятора
- `conf-dump` - вывод конфигурации
- `exit` - выход из эмулятора

### VFS файлы

- `data/minimal.vfs` - минимальная структура
- `data/files.vfs` - несколько файлов и папок  
- `data/complex_structure.vfs` - сложная структура (3+ уровня вложенности)

### Запуск тестов

```cmd
# Тест сложной структуры VFS
python src/vfs.py --vfs-path "data/complex_structure.vfs" --startup-script "scripts/test_commands.vfs"

# Тест минимальной VFS
python src/vfs.py --vfs-path "data/minimal.vfs"

# Тест нескольких файлов
python src/vfs.py --vfs-path "data/files.vfs"