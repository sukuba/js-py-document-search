' Extracts entire text from Ichitaro document as utf-8 text file.
' Works only on Windows with Justsystem Ichitaro installed.
' 
' usage> CScript ichitaro-to-text.vbs IchitaroFile DesDir
' 
' https://github.com/sukuba/js-py-document-search

' On Error Resume Next
Main Args.Unnamed(1), Args.Unnamed(2)
' If Err.Number <> 0 Then WScript.Echo Err.Description
WScript.Quit(Err.Number)

Sub Main(Src, Dest)
  'Set texts = GetIchitaroText(Src)
  Set texts = ForDebug()
  ' DumpTexts texts
  DestFileName = MergePath(Src, Dest)
  WScript.Echo Src, DestFileName
  ' SaveTextFile DestFileName, texts
  SaveUtf8TextFile DestFileName, texts
  RunCmd "normalize-text.bat " & DestFileName
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
  pos = InStrRev(src, '\')
  srcDir = Left(src, pos)  ' includes the last \
  srcName = Mid(src, pos + 1)
  If Right(dest, 1) <> '\' Then dest = dest & "\"
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
  ForDebug = Array("apple", "orange", "grape")
End Function
