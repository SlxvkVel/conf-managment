import tkinter as tk
from tkinter import scrolledtext, Entry, Frame, Label
import sys
import os
import csv
import base64
import time

class VFSNode:
    def __init__(self, name, is_directory=False, content=None):
        self.name = name
        self.is_directory = is_directory
        self.content = content
        self.children = {}

class VFSEmulator:
    def __init__(self, root, vfs_path=None, startup_script=None):
        self.root = root
        self.root.title("VFS emulator")
        self.root.geometry("800x600")
        self.start_time = time.time()
        self.vfs_path = vfs_path
        self.startup_script = startup_script
        self.vfs_root = None
        self.load_vfs()
        self.current_directory = "/"
        self.create_interface()
        self.display_welcome()
        if self.startup_script and os.path.exists(self.startup_script):
            self.execute_script(self.startup_script)
        self.command_entry.focus()
        self.command_entry.bind('<Return>', self.execute_command)

    def load_vfs(self):
        if self.vfs_path and os.path.exists(self.vfs_path):
            try:
                with open(self.vfs_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.vfs_root = VFSNode("", True)
                    next(reader, None)
                    for row in reader:
                        if len(row) >= 2:
                            path = row[0]
                            is_dir = row[1] == "directory"
                            content = row[2] if len(row) > 2 else None
                            self.add_to_vfs(path, is_dir, content)
            except Exception as e:
                pass

    def add_to_vfs(self, path, is_directory, content):
        parts = [p for p in path.split('/') if p]
        current = self.vfs_root
        for part in parts[:-1]:
            if part not in current.children:
                current.children[part] = VFSNode(part, True)
            current = current.children[part]

        if parts:
            last_part = parts[-1]
            if content and not is_directory:
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            current.children[last_part] = VFSNode(last_part, is_directory, content)

    def get_node(self, path):
        if not self.vfs_root:
            return None

        if not path.startswith("/"):
            path = self.current_directory + "/" + path if self.current_directory != "/" else "/" + path
        parts = [p for p in path.split('/') if p]
        current = self.vfs_root

        for part in parts:
            if part not in current.children:
                return None
            current = current.children[part]
        return current

    def create_interface(self):
        self.output_area = scrolledtext.ScrolledText(
            self.root,
            bg='black',
            fg='white',
            font=('Courier New', 12),
            state='disabled'
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        input_frame = Frame(self.root)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        self.prompt_label = Label(
            input_frame,
            text=f"vfs:{self.current_directory}$ ",
            bg='black',
            fg='green',
            font=('Courier New', 12)
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.command_entry = Entry(
            input_frame,
            bg='black',
            fg='white',
            font=('Courier New', 12),
            width=80
        )
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def display_welcome(self):
        welcome_msg = f"Эмулятор VFS v1.0\nVFS путь: {self.vfs_path}\n"
        if self.startup_script:
            welcome_msg += f"Стартовый скрипт: {self.startup_script}\n"
        welcome_msg += "Для выхода введите 'exit'\n\n"
        self.display_output(welcome_msg)

    def display_output(self, text):
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

    def update_prompt(self):
        self.prompt_label.config(text=f"vfs:{self.current_directory}$ ")

    def parse_command(self, command_string):
        if not command_string.strip():
            return "", []
        parts = command_string.strip().split()
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        return command, args

    def execute_command(self, event=None):
        command_string = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        self.display_output(f"vfs:{self.current_directory}$ {command_string}\n")
        command, args = self.parse_command(command_string)
        if command == "exit":
            self.cmd_exit()
        elif command == "ls":
            self.cmd_ls(args)
        elif command == "cd":
            self.cmd_cd(args)
        elif command == "tail":
            self.cmd_tail(args)
        elif command == "uptime":
            self.cmd_uptime(args)
        elif command == "tree":
            self.cmd_tree(args)
        elif command == "mkdir":
            self.cmd_mkdir(args)
        elif command == "conf-dump":
            self.cmd_conf_dump()
        elif command == "":
            pass
        else:
            self.display_output(f"vfs: Команда {command} не найдена\n")
        self.output_area.see(tk.END)

    def execute_script(self, script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.display_output(f"vfs:{self.current_directory}$ {line}\n")
                        command, args = self.parse_command(line)
                        if command == "ls":
                            self.cmd_ls(args)
                        elif command == "cd":
                            self.cmd_cd(args)
                        elif command == "tail":
                            self.cmd_tail(args)
                        elif command == "uptime":
                            self.cmd_uptime(args)
                        elif command == "tree":
                            self.cmd_tree(args)
                        elif command == "mkdir":
                            self.cmd_mkdir(args)
                        elif command == "conf-dump":
                            self.cmd_conf_dump()
        except Exception as e:
            self.display_output(f"Ошибка выполнения скрипта: {e}\n")

    def cmd_exit(self):
        self.root.destroy()

    def cmd_ls(self, args):
        path = args[0] if args else self.current_directory

        if not self.vfs_root:
            self.display_output("Ошибка: VFS не загружена\n")
            return
        node = self.get_node(path)
        if not node:
            self.display_output(f"Ошибка: путь {path} не найден\n")
            return

        if not node.is_directory:
            self.display_output(f"Ошибка: {path} не является директорией\n")
            return

        if not node.children:
            self.display_output("Директория пуста\n")
            return

        for name in sorted(node.children.keys()):
            if node.children[name].is_directory:
                self.display_output(f"{name}/\n")
            else:
                self.display_output(f"{name}\n")

    def cmd_cd(self, args):
        if not args:
            self.current_directory = "/"
            self.update_prompt()
            return
        path = args[0]
        new_path = ""
        if path.startswith("/"):
            new_path = path
        else:
            if self.current_directory == "/":
                new_path = f"/{path}"
            else:
                new_path = f"{self.current_directory}/{path}"

        node = self.get_node(new_path)
        if not node:
            self.display_output(f"Ошибка: путь {new_path} не найден\n")
            return

        if not node.is_directory:
            self.display_output(f"Ошибка: {new_path} не является директорией\n")
            return
        self.current_directory = new_path
        self.update_prompt()

    def cmd_tail(self, args):
        if not args:
            self.display_output("Ошибка: укажите файл\n")
            return

        if not self.vfs_root:
            self.display_output("Ошибка: VFS не загружена\n")
            return

        node = self.get_node(args[0])
        if not node:
            self.display_output(f"Ошибка: файл {args[0]} не найден\n")
            return

        if node.is_directory:
            self.display_output(f"Ошибка: {args[0]} является директорией\n")
            return

        if not node.content:
            self.display_output("Файл пуст\n")
            return

        lines = node.content.split('\n')
        tail_lines = lines[-10:] if len(lines) > 10 else lines
        for line in tail_lines:
            self.display_output(f"{line}\n")

    def cmd_uptime(self, args):
        current_time = time.time()
        uptime_seconds = current_time - self.start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        self.display_output(f"Время работы: {hours:02d}:{minutes:02d}:{seconds:02d}\n")

    def cmd_tree(self, args):
        path = args[0] if args else self.current_directory
        if not self.vfs_root:
            self.display_output("Ошибка: VFS не загружена\n")
            return

        node = self.get_node(path)
        if not node:
            self.display_output(f"Ошибка: путь {path} не найден\n")
            return

        if not node.is_directory:
            self.display_output(f"Ошибка: {path} не является директорией\n")
            return
        self.display_output(f"{path}\n")
        self._print_tree(node, 1)

    def _print_tree(self, node, level):
        prefix = "  " * level + "└── "
        for name, child in sorted(node.children.items()):
            if child.is_directory:
                self.display_output(f"{prefix}{name}/\n")
                self._print_tree(child, level + 1)
            else:
                self.display_output(f"{prefix}{name}\n")

    def cmd_mkdir(self, args):
        if not args:
            self.display_output("Ошибка: укажите имя директории\n")
            return

        if not self.vfs_root:
            self.display_output("Ошибка: VFS не загружена\n")
            return
        dir_name = args[0]
        new_path = ""
        if dir_name.startswith("/"):
            new_path = dir_name
        else:
            if self.current_directory == "/":
                new_path = f"/{dir_name}"
            else:
                new_path = f"{self.current_directory}/{dir_name}"
        existing_node = self.get_node(new_path)
        if existing_node:
            self.display_output(f"Ошибка: путь {new_path} уже существует\n")
            return
        parts = [p for p in new_path.split('/') if p]
        current = self.vfs_root
        for part in parts:
            if part not in current.children:
                current.children[part] = VFSNode(part, True)
            current = current.children[part]
        self.display_output(f"Директория {new_path} создана\n")

    def cmd_conf_dump(self):
        self.display_output("Конфигурация эмулятора:\n")
        self.display_output(f"  VFS путь: {self.vfs_path}\n")
        self.display_output(f"  Стартовый скрипт: {self.startup_script}\n")
        self.display_output(f"  Текущая директория: {self.current_directory}\n")
        self.display_output(f"  VFS загружена: {'да' if self.vfs_root else 'нет'}\n")

def main():
    vfs_path = None
    startup_script = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--vfs-path" and i + 1 < len(sys.argv):
            vfs_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--startup-script" and i + 1 < len(sys.argv):
            startup_script = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    root = tk.Tk()
    app = VFSEmulator(root, vfs_path, startup_script)
    root.mainloop()

if __name__ == "__main__":
    main()