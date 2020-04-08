Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c endofprocess.bat"
oShell.Run strArgs, 0, false