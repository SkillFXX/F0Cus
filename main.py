import sys
import win32event
import win32api
import winerror

from app import F0CusApp
from data import migrate, t

mutex = None
def is_already_running():
    global mutex
    mutex_name = "Global\\F0CusAppMutex"

    mutex = win32event.CreateMutex(None, False, mutex_name)

    return win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS

if __name__ == "__main__":
    if is_already_running():
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()

        messagebox.showerror("F0Cus", t("already_running"))

        root.destroy()
        sys.exit(0)

    migrate()
    app = F0CusApp()
    app.mainloop()