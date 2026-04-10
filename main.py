from app import F0CusApp
from data import migrate
 
if __name__ == "__main__":
    migrate()
    app = F0CusApp()
    app.mainloop()