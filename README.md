F0Cus is an open-source screen time tracking program designed for Windows. Unlike other available tools, F0Cus uses different methods to detect whether you are actually using your computer or have simply left it on without using it.

> This project was designed to solve a personal issue and may contain bugs and still lack some features. I coded it myself with the help of AI, particularly for the Tkinter interfaces.

![Screenshot](https://i.ibb.co/yFwqtMFH/Capture-d-cran-2026-03-16-203941.png)

## Features:

- Smart activity tracking: with cursor and keyboard activity detection
- Application tracking: records every application used.
- Setting limits: ability to set daily time limits for each application or for the entire computer to display a reminder or directly close the application/computer.
- Stats display: displays daily and weekly usage stats for the most frequently used software in graph form.
- Application minimization: option to minimize the software so the interface doesn’t get in the way while still tracking activity.

## Installation

_This software is designed exclusively for Windows and has only been tested on Windows 11._

### Pre-compiled version

You can download a pre-compiled version from the [Releases](https://github.com/SkillFXX/F0Cus/releases/) page.

### Compile the project yourself

```bash
    git clone https://github.com/SkillFXX/F0Cus # Clone the repository
    cd F0Cus

    pip install -r requirements.txt # Download dependencies

    python main.py # Launch the app
```

You can also build it using `PyInstaller`

```bash
    pyinstaller --onefile --noconsole --name "F0Cus" --add-data "assets;assets" --icon "assets/icon.ico" main.py
```
