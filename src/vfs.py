import tkinter as tk
from tkinter import scrolledtext, Entry, Frame, Label

class VFSEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title("VFS-emulator")
        self.root.geometry("800x700")
        self.current_directory = "/home/user"
        self.create_interface()
        self.display_welcome()
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
        welcome_msg = "Эмулятор VFS v1.0. Для выхода введите 'exit'.\n\n"
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
        elif command == "":
            pass
        else:
            self.display_output(f"vfs: Команда {command} не найдена\n")

        self.output_area.see(tk.END)

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

def main():
    root = tk.Tk()
    app = VFSEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()