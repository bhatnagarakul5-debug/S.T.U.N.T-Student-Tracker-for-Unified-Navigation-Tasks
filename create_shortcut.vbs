Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set oShellLink = WshShell.CreateShortcut(strDesktop & "\STUNT.lnk")
oShellLink.TargetPath = "c:\Users\Akul\Desktop\STUNT\STUNT_Launcher.bat"
oShellLink.WorkingDirectory = "c:\Users\Akul\Desktop\STUNT"
oShellLink.WindowStyle = 1
oShellLink.Description = "STUNT: Student Tracker for Unified Navigation & Tasks"
oShellLink.IconLocation = "c:\Users\Akul\Desktop\STUNT\assets\RedandBlackGlitchcoreStuntLogo.png"
oShellLink.Save
