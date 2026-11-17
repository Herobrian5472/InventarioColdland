Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Brian\Desktop\Coldland_app"
WshShell.Run "pythonw app.py", 0, False