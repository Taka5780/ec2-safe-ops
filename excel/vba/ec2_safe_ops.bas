Attribute VB_Name = "ec2_safe_ops"
Sub LoadCsv()

    Dim ws As Worksheet
    Set ws = ActiveSheet

    Dim filePath As String
    filePath = Application.GetOpenFilename("CSV Files (*.csv), *.csv")
    If filePath = "False" Then Exit Sub

    Application.ScreenUpdating = False

    ' 既存データクリア（5行目以降）
    ws.Rows("5:" & ws.Rows.Count).ClearContents

    Dim fso As Object
    Dim ts As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set ts = fso.OpenTextFile(filePath, 1)

    Dim line As String
    Dim row As Long
    row = 5

    Dim isHeader As Boolean
    isHeader = True

    Do Until ts.AtEndOfStream

        line = ts.ReadLine

        If isHeader Then
            isHeader = False
        Else
            Dim cols As Variant
            cols = Split(line, ",")

            Dim i As Integer
            For i = 0 To UBound(cols)
                ws.Cells(row, i + 2).Value = cols(i) ' ← B列スタート
            Next i

            row = row + 1
        End If

    Loop

    ts.Close

    Call ApplyHumanCheckControl
    Call ApplySheetProtection
    Call ApplyConditionalFormatting

    Application.ScreenUpdating = True

    MsgBox "CSV読み込み完了: " & (row - 5) & "件", vbInformation

End Sub


Sub ApplyHumanCheckControl()

    Dim ws As Worksheet
    Set ws = ActiveSheet

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).row

    Dim i As Long

    For i = 5 To lastRow

        Dim env As String
        env = LCase(Trim(ws.Cells(i, 2).Value)) ' B列

        ws.Cells(i, 9).Validation.Delete ' I列

        If env = "prod" Then

            ws.Cells(i, 9).Value = "SKIP"

            ws.Cells(i, 9).Validation.Add _
                Type:=xlValidateList, _
                Formula1:="SKIP"

        Else

            ws.Cells(i, 9).Validation.Add _
                Type:=xlValidateList, _
                Formula1:="SKIP,START,STOP,DELETE"

        End If

    Next i

End Sub


Sub ApplySheetProtection()

    Dim ws As Worksheet
    Set ws = ActiveSheet

    ws.Unprotect

    ws.Cells.Locked = False

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).row

    ' 編集禁止（B?H）
    ws.Range("B5:H" & lastRow).Locked = True

    ' 編集OK（I, J）
    ws.Range("I5:I" & lastRow).Locked = False
    ws.Range("J5:J" & lastRow).Locked = False

    ws.Protect Password:="lock", UserInterfaceOnly:=True

End Sub


Sub ExportExecutionCsv()

    Dim ws As Worksheet
    Set ws = ThisWorkbook.Sheets(1)

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "C").End(xlUp).row

    Dim output As String
    output = "env,name,instance_id,action,HumanCheck" & vbCrLf

    Dim i As Long
    Dim env As String, name As String, instanceId As String
    Dim human As String

    Dim skipCount As Long, prodCount As Long, exportCount As Long

    For i = 5 To lastRow

        env = Trim(ws.Cells(i, "B").Value)
        name = Trim(ws.Cells(i, "C").Value)
        instanceId = Trim(ws.Cells(i, "D").Value)
        human = Trim(UCase(ws.Cells(i, "I").Value))

        ' ① HumanCheck未入力 → スキップ
        If human = "" Then
            skipCount = skipCount + 1
            GoTo ContinueLoop
        End If

        ' ② prod除外
        If LCase(env) Like "*prod*" Then
            prodCount = prodCount + 1
            GoTo ContinueLoop
        End If

        ' ③ 出力（action = HumanCheck）
        output = output & _
            env & "," & _
            name & "," & _
            instanceId & "," & _
            human & "," & _
            human & vbCrLf

        exportCount = exportCount + 1

ContinueLoop:
    Next i

    ' ファイル保存
    If ThisWorkbook.Path = "" Then
        MsgBox "ファイルを保存してから実行してください", vbExclamation
        Exit Sub
    End If

    Dim filePath As String
    filePath = ThisWorkbook.Path & "\ec2_execution_" & Format(Now, "yyyymmdd_hhnnss") & ".csv"

    Dim fileNum As Integer
    fileNum = FreeFile

    Open filePath For Output As #fileNum
    Print #fileNum, output
    Close #fileNum

    MsgBox "CSV出力完了" & vbCrLf & _
           "出力: " & exportCount & "件" & vbCrLf & _
           "未入力: " & skipCount & "件" & vbCrLf & _
           "prod除外: " & prodCount & "件"

End Sub


Sub ApplyConditionalFormatting()

    Dim ws As Worksheet
    Set ws = ActiveSheet

    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, "B").End(xlUp).row

    Dim i As Long

    For i = 5 To lastRow

        Dim env As String
        Dim action As String

        env = LCase(Trim(ws.Cells(i, 2).Value))       ' Env
        action = UCase(Trim(ws.Cells(i, 8).Value))    ' SuggestedAction

        ' リセット
        ws.Range("B" & i & ":J" & i).Interior.ColorIndex = xlNone

        ' prodは最優先（赤）
        If env = "prod" Then
            ws.Range("B" & i & ":J" & i).Interior.Color = RGB(255, 200, 200)
        
        Else
            Select Case action
                Case "STOP"
                    ws.Cells(i, 8).Interior.Color = RGB(255, 255, 150) ' 黄
                Case "DELETE"
                    ws.Cells(i, 8).Interior.Color = RGB(255, 150, 150) ' 赤
                Case "SKIP"
                    ws.Cells(i, 8).Interior.Color = RGB(220, 220, 220) ' グレー
            End Select
        End If

    Next i

End Sub
