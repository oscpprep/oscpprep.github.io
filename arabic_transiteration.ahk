#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance Force  ; stops replacing running old script instance
;KeyHistory
#InstallKeybdHook

!+p::
Send,ʾ
return

!p::
Send,ʿ
return

!(::
Send,«
return

!)::
Send,»
return

^!(::
Send,‏﴿‏
return

^!)::
Send,‏﴾‏
return

!|::
Send,۝
return

!w::
Send,ﷺ
return

!a::
Send,ā
return

!+a::
Send,Ā
return

!d::
Send,ḍ
return

!+d::
Send,Ḍ
return

!i::
Send,ī
return

!+i::
Send,Ī
return

!u::
Send,ū
return

!+u::
Send,Ū
return

!h::
Send,ḥ
return

!+h::
Send,Ḥ
return

!s::
Send,ṣ
return

!+s::
Send,Ṣ
return

!t::
Send,ṭ
return

!+t::
Send,Ṭ
return

!z::
Send,ẓ
return

!+z::
Send,Ẓ
return

!sc021::Send,پ
return

!sc028::Send,ٹ
return

!sc01b::Send,ڈ
return

!sc027::Send,گ
return

!sc025::Send,ں
return

!sc02f::Send,ڑ
return

!sc034::Send,ژ
return

!sc031::Send,ے
return

!sc01a::Send,چ
return

!sc02d::Send,ۓ
return

!+sc02d::Send,ۂ
return

^!sc017::Send,ھ
return