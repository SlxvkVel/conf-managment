import tkinter as tk
from tkinter import scrolledtext, Entry, Frame, Label
import sys
import os
class VFSEmulator:
    def __init__(self, root, vfs_path=None, startup_script=None):
        self.root = root
        self.root.title("VFS")
        self.root.geometry("800x600")

        self.vfs_path = vfs_path or os.path.abspath(".")
        self.startup_script = startup_script

        self.current_directory = "/home/user"
        self.create_interface()
        self.display_welcome()

        if self.startup_script and os.path.exists(self.startup_script):
            self.execute_script(self.startup_script)

        self.command_entry.focus()
        self.command_entry.bind('<Return>', self.execute_command)

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
                        elif command == "conf-dump":
                            self.cmd_conf_dump()
        except Exception as e:
            self.display_output(f"Ошибка выполнения скрипта: {e}\n")

    def cmd_exit(self):
        self.root.destroy()

    def cmd_ls(self, args):
        self.display_output(f"Команда 'ls' вызвана с аргументами: {args}\n")

    def cmd_cd(self, args):
        self.display_output(f"Команда 'cd' вызвана с аргументами: {args}\n")
        if args:
            if args[0] == "..":
                if self.current_directory != "/":
                    parts = self.current_directory.rstrip("/").split("/")
                    if len(parts) > 1:
                        self.current_directory = "/".join(parts[:-1]) or "/"
            elif args[0].startswith("/"):
                self.current_directory = args[0]
            else:
                if self.current_directory == "/":
                    self.current_directory = f"/{args[0]}"
                else:
                    self.current_directory = f"{self.current_directory}/{args[0]}"

        self.update_prompt()
    def cmd_conf_dump(self):
        self.display_output("Конфигурация эмулятора:\n")
        self.display_output(f"  VFS путь: {self.vfs_path}\n")
        self.display_output(f"  Стартовый скрипт: {self.startup_script}\n")
        self.display_output(f"  Текущая директория: {self.current_directory}\n")


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