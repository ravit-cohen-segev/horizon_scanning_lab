#SingleInstance Forcehttps://platform.socrates-insights.com/investigations/create?type=Topic

CoordMode Mouse, Absolute



soc_address=https://platform.socrates-insights.com/investigations/create?type=Topic


;address line
x1:=413
y1:=55

;topic text box
x2:=730
y2:=520

;topic search
x3:=1225
y3:=700


#v::

Loop, read, 3.csv
{
	SetTimer, Skipper, 600000
    LineNumber := A_Index
	if LineNumber>1
	{
		Loop, parse, A_LoopReadLine, CSV
		{
			cnt:=0
			if A_Index=1
			{
				Term_Name:=A_LoopField
				ToolTip %Term_Name%: Starting 
				;MsgBox Field %LineNumber%-%A_Index% is:`n%A_LoopField%`n`nContinue?
			
				MouseClick, left, %x1%, %y1%
				Sleep 303
				send %soc_address%
				Sleep 303
				send {Enter}
				Sleep 3000
				MouseClick, left, %x2%, %y2%
				Sleep 303
				send %A_LoopField%
				MouseClick, left, %x3%, %y3%
				Sleep 303
				ToolTip %Term_Name%: Waiting...
				Loop, 
				{
					PixelSearch, Px, Py, 540, 340, 542, 342, 0xfff9f0, 3, Fast
					if ErrorLevel
					{
						if cnt=1
								Goto, Skipterm
					Sleep, 1000
					}
					else {
					break
					}
				}
				
			}
			if A_Index=2
			{
				ToolTip %Term_Name%: Adding dictionaries and synonyms
				sleep 2000
				;dictionaries
				xd1:=809
				yd1:=402
				
				xd2:=809
				yd2:=432

				
				MouseClick, left, 1708, 110
				sleep 400
				MouseClick, left, 1708, 170
				sleep 400
				MouseClick, left, 638, 361
				sleep 400
				
				dict_line_x:=950
				dict_line_y:=280
				
				dict_box_x1:=780
				dict_box_y1:=310
				dict_box_x2:=850
				dict_box_y2:=465
				
				MouseClick, left, %dict_line_x%, %dict_line_y%
				;MouseClick, left, 950, 280
				Sleep 303
				send ^a
				Sleep 303
				send {Delete}
				sleep 200
				send commercial
				Sleep 200
				PixelSearch, Px, Py, %dict_box_x1%, %dict_box_y1%, %dict_box_x2%, %dict_box_y2%, 0xd2d2d2, 3, Fast
					MouseClick, left, %Px% ,%Py%

				MouseClick, left, %dict_line_x%, %dict_line_y%
				Sleep 303
				send ^a
				Sleep 303
				send {Delete}
				sleep 200
				send Countries in Text
				Sleep 200
				PixelSearch, Px, Py, %dict_box_x1%, %dict_box_y1%, %dict_box_x2%, %dict_box_y2%, 0xd2d2d2, 3, Fast
					MouseClick, left, %Px% ,%Py%

				MouseClick, left, %dict_line_x%, %dict_line_y%
				Sleep 303
				send ^a
				Sleep 303
				send {Delete}
				sleep 200
				send emerging
				Sleep 200
				PixelSearch, Px, Py, %dict_box_x1%, %dict_box_y1%, %dict_box_x2%, %dict_box_y2%, 0xd2d2d2, 3, Fast
					MouseClick, left, %Px% ,%Py%

				MouseClick, left, %dict_line_x%, %dict_line_y%
				Sleep 303
				send ^a
				Sleep 303
				send {Delete}
				sleep 200
				send r&d
				Sleep 200
				PixelSearch, Px, Py, %dict_box_x1%, %dict_box_y1%, %dict_box_x2%, %dict_box_y2%, 0xd2d2d2, 3, Fast
					MouseClick, left, %Px% ,%Py%


				;click save button
				MouseClick, left, %dict_line_x%, %dict_line_y%
				Sleep 303
				send ^a
				Sleep 303
				send {Delete}
				sleep 2000
				PixelSearch, Px, Py, 1240, 745, 1420, 1200, 0xffd333, 3, Fast
					MouseClick, left, %Px% ,%Py%
				Sleep 3030
				Loop, 
				{
					PixelSearch, Px, Py, 540, 340, 542, 342, 0xfff9f0, 3, Fast
					if ErrorLevel
					{
						if cnt=1
								Goto, Skipterm
					Sleep, 1000
					}
					else {
					break
					}
				}
				
				;multiple terms
				if (A_LoopField)
				{
					MouseClick, left, 376, 410
					Sleep 303
					MouseClick, left, 320, 485
					Sleep 303
					send %A_LoopField%
					MouseClick, left, 1256, 700
					sleep 1000
					sleep 2000
					PixelSearch, Px, Py, 1180, 600, 1430, 900, 0xffd333, 3, Fast
						MouseClick, left, %Px% ,%Py%
					sleep 1000
					Px:=Px-180
					MouseClick, left, %Px% ,%Py%
					
			}
				Sleep 3030
				ToolTip %Term_Name%: Refreshing results
				
				Loop, 
				{
					PixelSearch, Px, Py, 540, 340, 542, 342, 0xfff9f0, 3, Fast
					if ErrorLevel
					{
						if cnt=1
								Goto, Skipterm
					Sleep, 1000
					}
					else {
					break
					}
				}

				sleep 5000
				
				
				refresh_box_x1:=1296
				refresh_box_y1:=217
				refresh_box_x2:=1296
				refresh_box_y2:=227
				
				
				Loop, 
				{
					PixelSearch, Px, Py, %refresh_box_x1%, %refresh_box_y1%, %refresh_box_x2%, %refresh_box_y2%, 0xffb000, 3, Fast
					if ErrorLevel
					{
						if cnt=1
								Goto, Skipterm
					 MouseClick, left, %refresh_box_x1%, %refresh_box_y1%
					 Sleep, 5000
					}
					else {
					break
					}
				}
				
				Sleep 5000
				;MsgBox saving
				Sleep, 60000
				Loop, 
				{
					PixelSearch, Px, Py, 1164, 248, 1240, 294, 0xffd633, 3, Fast
					if ErrorLevel
					{
						break
					}
					else 
					{
						Loop, https://platform.socrates-insights.com/investigations/create?type=Topic
							
						{
							PixelSearch, Px, Py, %refresh_box_x1%, %refresh_box_y1%, %refresh_box_x2%, %refresh_box_y2%, 0xffb000, 3, Fast
							if ErrorLevel
							{
							 MouseClick, left, %refresh_box_x1%, %refresh_box_y1%
							Sleep, 5000
							if cnt=1
								Goto, Skipterm
							}
							else {
							break
							}
						}
						if cnt=1
								Goto, Skipterm
						Sleep, 2000
						
					
					}
				}
				
				Sleep, 60000
				
				
				MouseClick, left, 1708, 110
				sleep 200
				MouseClick, left, 1708, 286Computer and information sciences 
				sleep 200
				
				
				ToolTip %Term_Name%: Done, saving
				;MsgBox Field %LineNumber%-%A_Index% is:`n%A_LoopField%`n`n now to save
				sleep 5000
				
				
			}
			Skipterm:
		}
	}


}


Skipper:
{
   cnt := 1
 }
return
