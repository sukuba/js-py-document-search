' Extracts entire text from Ichitaro document as utf-8 text file.
' Works only on Windows with Justsystem Ichitaro installed.
' 
' usage> CScript ichitaro-to-text.vbs /normalize IchitaroFile DesDir
' 
' https://github.com/sukuba/js-py-document-search

' On Error Resume Next
Set Args = WScript.Arguments
Main Args.Named, Args.Unnamed(0), Args.Unnamed(1)
' If Err.Number <> 0 Then WScript.Echo Err.Description
WScript.Quit(Err.Number)

Sub Main(Opts, Src, Dest)
  If Opts.Exists("nojxw") Then
    Set texts = ForDebug()
  Else
    Set texts = GetIchitaroText(Src)
  End If
  
  If Opts.Exists("dump") Then
    DumpTexts texts
  End If
  
  DestFileName = MergePath(Src, Dest)
  WScript.Echo Src, DestFileName
  
  If Opts.Exists("ansi") Then
    SaveTextFile DestFileName, texts
  Else
    SaveUtf8TextFile DestFileName, texts
  End If
  
  If Opts.Exists("normalize") Then
    RunCmd "normalize-text.bat " & DestFileName
  End If
End Sub

Function GetIchitaroText(FileName)
  Set app = CreateObject("JXW.Application")
  app.Visible = True
  app.Document.Open FileName
  app.TaroLibrary.SelectAll 1
  Set texts = app.TaroLibrary.GetString()
  app.TaroLibrary.QuitDocumentWindow
  app.Quit
  Set app = Nothing
  
  Set GetIchitaroText = texts
End Function

Sub DumpTexts(texts)
  For Each text in texts
    WScript.Echo text
  Next
End Sub

Sub SaveTextFile(texts, dest)
  Const TristateFalse = 0
  Const TristateTrue = -1
  Const ForWriting = 2
  
  Set FileSystem = CreateObject("Scripting.FileSystemObject")
  Set Stream = FileSystem.OpenTextFile(dest, ForWriting, True, TristateTrue)
  ' TristateTrue is required to save a text including non-ANSI characters.
  If Stream Is Nothing Then Err.Raise 52    ' invalid file name
  
  For Each text in texts
    Stream.WriteLine text
  Next
  
  Stream.Close
  Set Stream = Nothing
  Set FileSystem = Nothing
Ens Sub

Sub SaveUtf8TextFile(texts, dest)
  Const adTypeText = 2
  Const adSaveCreateOverWrite = 2
  
  Set FileStream = CreateObject("ADODB.Stream")
  With FileStream
      .Open
      .Type = adTypeText
      .Charset = "utf-8"
  End With
  
  For Each text in texts
    FileStream.WriteText text & vbLf
  Next
  
  FileStream.SaveToFile dest, adSaveCreateOverWrite
  FileStream.Close
  Set FileStream = Nothing
End Sub

Function MergePath(src, ByVal dest)
  pos = InStrRev(src, 'Å_')
  srcDir = Left(src, pos)  ' includes the last Å_
  srcName = Mid(src, pos + 1)
  If Right(dest, 1) <> 'Å_' Then dest = dest & "Å_"
  destFullPath = dest & srcName & ".txt"
  
  MergePath = destFullPath
End Function

Sub RunCmd(command)
  Set Shell = CreateObject("WScript.Shell")
  cmd = "cmd /D /U /C " & command
  rc = Shell.Run(cmd, 8, True)
  Set Shell = Nothing
End Sub

Function ForDebug()
  ForDebug = Array("apple", "ÇèÇíÇÅÇéÇáÇÖ", "grape")
End Function
