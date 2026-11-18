import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import shutil
import platform
import sys
from datetime import datetime

# eSim Tool Dependency Configuration
TOOLS = {
    "Python": {
        "commands": ["python", "python3"],
        "version": ["--version"],
        "hint": "Install Python from python.org"
    },
    "Ngspice": {
        "commands": ["ngspice"],
        "version": ["--version"],
        "hint": "Install Ngspice from ngspice.sourceforge.io"
    },
    "KiCad": {
        "commands": ["kicad-cli"],
        "version": ["version"],
        "hint": "Install KiCad from kicad.org"
    },
    "Git": {
        "commands": ["git"],
        "version": ["--version"],
        "hint": "Install Git from git-scm.com"
    }
}


# Dependency Checker
def check_dependency(tool, details):

    for command in details["commands"]:

        path = shutil.which(command)

        if path:
            try:
                result = subprocess.run(
                    [path] + details["version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

                version = (
                    result.stdout.strip()
                    or result.stderr.strip()
                    or "Version unavailable"
                )

                return "Installed", version, path

            except Exception:
                return "Installed", "Version unavailable", path

    return "Missing", "Not Installed", details["hint"]


# GUI Application
class EsimManager:

    def __init__(self, root):

        self.root = root
        self.root.title("eSim Automated Tool Manager")
        self.root.geometry("850x600")
        self.root.configure(bg="#eef2f7")

        title = tk.Label(
            root,
            text="eSim Dependency Checker",
            font=("Arial", 22, "bold"),
            bg="#eef2f7",
            fg="#263b80"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            root,
            text="Check required tools and their installation status",
            font=("Arial", 11),
            bg="#eef2f7"
        )
        subtitle.pack()

        # System Information
        system = tk.Label(
            root,
            text="Operating System: " + platform.system(),
            font=("Arial", 10, "bold"),
            bg="#eef2f7"
        )
        system.pack(pady=10)

        # Dependency Table
        columns = ("Tool", "Status", "Version")

        self.table = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=9
        )

        self.table.heading("Tool", text="Tool Name")
        self.table.heading("Status", text="Installation Status")
        self.table.heading("Version", text="Version")

        self.table.column("Tool", width=180)
        self.table.column("Status", width=180)
        self.table.column("Version", width=350)

        self.table.pack(padx=20, pady=15, fill="x")

        # Buttons
        button_frame = tk.Frame(root, bg="#eef2f7")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Check Dependencies",
            command=self.scan_tools,
            bg="#263b80",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Clear Log",
            command=self.clear_log,
            bg="#555555",
            fg="white",
            font=("Arial", 11),
            padx=15,
            pady=8
        ).grid(row=0, column=1, padx=10)

        # Result
        self.result = tk.Label(
            root,
            text="Click Check Dependencies to start scanning.",
            font=("Arial", 11, "bold"),
            bg="#eef2f7",
            fg="#263b80"
        )
        self.result.pack(pady=10)

        # Action Log
        tk.Label(
            root,
            text="Activity Log",
            font=("Arial", 13, "bold"),
            bg="#eef2f7"
        ).pack()

        self.log_box = tk.Text(
            root,
            height=8,
            width=95,
            font=("Consolas", 9)
        )
        self.log_box.pack(padx=20, pady=10)

        self.log("eSim Tool Manager Started")
        self.log("System: " + platform.system())

    # Log Function
    def log(self, message):

        time = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            tk.END,
            f"[{time}] {message}\n"
        )

        self.log_box.see(tk.END)

    # Scan Dependencies
    def scan_tools(self):

        for item in self.table.get_children():
            self.table.delete(item)

        installed = 0
        missing = 0

        self.log("Starting dependency scan...")

        for tool, details in TOOLS.items():

            status, version, info = check_dependency(
                tool, details
            )

            self.table.insert(
                "",
                tk.END,
                values=(tool, status, version)
            )

            if status == "Installed":

                installed += 1
                self.log(
                    tool + " is installed: " + version
                )

            else:

                missing += 1
                self.log(
                    tool + " is missing. " + info
                )

        self.result.config(
            text=f"Scan Complete: {installed} Installed | "
                 f"{missing} Missing"
        )

        self.log("Dependency scan completed.")

        if missing == 0:
            messagebox.showinfo(
                "Success",
                "All configured dependencies are installed!"
            )
        else:
            messagebox.showwarning(
                "Missing Dependencies",
                f"{missing} dependencies are missing. "
                "Check the activity log for installation guidance."
            )

    # Clear Log
    def clear_log(self):

        self.log_box.delete("1.0", tk.END)
        self.log("Log cleared.")


# Main Program
if __name__ == "__main__":

    root = tk.Tk()

    app = EsimManager(root)

    root.mainloop()
