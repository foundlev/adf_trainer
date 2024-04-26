import aui
import ctypes


def main():
    app = aui.App()
    app.load()


if __name__ == "__main__":
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    main()
