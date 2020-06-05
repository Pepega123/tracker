Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\Users\admin\Documents\tracker\tracker.bat" & Chr(34), 0
Set WinScriptHost = Nothing