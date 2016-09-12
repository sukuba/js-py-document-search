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

' it's not nice, but uses global variable to keep the application between open and quit.
' because texts object is an Ichitaro object, it disappears when the app quit.
Dim app

Sub Main(Opts, Src, Dest)
  If Opts.Exists("nojxw") Then
    texts = ForDebug()
  Else
    Set texts = GetIchitaroText(Src)
  End If
  
  If Opts.Exists("dump") Then
    DumpTexts texts
  End If
  
  DestFileName = MergePath(Src, Dest)
  WScript.Echo Src, DestFileName
  
  If Opts.Exists("ansi") Then
    SaveTextFile texts, DestFileName
  Else
    SaveUtf8TextFile texts, DestFileName
  End If
  
  If Not Opts.Exists("nojxw") Then
    Set texts = Nothing
    QuitIchitaro
  End If
  
  If Opts.Exists("normalize") Then
    RunCmd "normalize-text.bat " & DestFileName
  End If
End Sub

Function GetIchitaroText(FileName)
  Set app = CreateObject("JXW.Application")
  app.Visible = True
  app.Documents.Open FileName
  app.TaroLibrary.SelectAll 1
  Set texts = app.TaroLibrary.GetString()
  app.TaroLibrary.QuitDocumentWindow
  'app.Quit
  'Set app = Nothing
  
  Set GetIchitaroText = texts
End Function

Sub QuitIchitaro()
  app.Quit
  Set app = Nothing
End Sub

Sub DumpTexts(texts)
  For Each text in texts
    WScript.Echo text
  Next
End Sub

Sub SaveTextFile(texts, dest)
  Const TristateFalse = 0
  Const TristateTrue = -1 ' this will save as utf-8 with BOM
  Const ForWriting = 2
  
  Set FileSystem = CreateObject("Scripting.FileSystemObject")
  Set Stream = FileSystem.OpenTextFile(dest, ForWriting, True, TristateFalse)
  ' TristateTrue is required to save a text including non-ANSI characters.
  If Stream Is Nothing Then Err.Raise 52    ' invalid file name
  
  For Each text in texts
    Stream.WriteLine text
  Next
  
  Stream.Close
  Set Stream = Nothing
  Set FileSystem = Nothing
End Sub

Sub SaveUtf8TextFile(texts, dest)
  SaveUtf8TextFileWithBom texts, dest
  RemoveBomFromFile dest
End Sub

Sub RemoveBomFromFile(dest)
  ' remove BOM after ADODB.Stream done.
  ' this removes 3 bytes at the beginning of file,
  ' whether they are bom or not.
  Const adTypeBinary = 1
  Const adModeWrite = 2
  Const adModeReadWrite = 3
  Const adSaveCreateOverWrite = 2
  
  Set infs = CreateObject("ADODB.Stream")
  With infs
      .Type = adTypeBinary
      .Open
  End With
  
  Set outfs = CreateObject("ADODB.Stream")
  With outfs
      .Mode = adModeReadWrite
      .Type = adTypeBinary
      .Open
  End With
  
  infs.LoadFromFile dest
  infs.Position = 3  ' skip BOM
  
  infs.CopyTo outfs
  'outfs.Write infs.Read
  infs.flush
  infs.Close
  Set infs = Nothing
  
  outfs.SaveToFile dest, adSaveCreateOverWrite
  outfs.Close
  Set outfs = Nothing
End Sub

Sub SaveUtf8TextFileWithBom(texts, dest)
  ' ADODB.Stream saves utf-8 with BOM.
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
  pos = InStrRev(src, "\")
  srcDir = Left(src, pos)  ' includes the last \
  srcName = Mid(src, pos + 1)
  If Right(dest, 1) <> "\" Then dest = dest & "\"
  destFullPath = dest & srcName & ".txt"
  
  MergePath = destFullPath
End Function

Sub RunCmd(command)
  Set Shell = CreateObject("WScript.Shell")
  cmd = "cmd /D /U /C " & command
  WScript.Echo cmd
  rc = Shell.Run(cmd, 8, True)
  Set Shell = Nothing
End Sub

Function ForDebug()
  ForDebug = Array("apple", "ÇèÇíÇÅÇéÇáÇÖ", "grape")
End Function
