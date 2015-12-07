; full_build.nsi
;
; Installation script

;--------------------------------

!define APPNAME "DNSifier"

; The name of the installer
Name "${APPNAME}"

RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)

Icon "yaicon.ico"

; The file to write
OutFile "setup.exe"

; The default installation directory
InstallDir $PROGRAMFILES\${APPNAME}

; The text to prompt the user to enter a directory
DirText "This will install DNSifer on your computer. Choose a directory"

!define REG_APP_PATH "Software\Microsoft\Windows\CurrentVersion\App Paths\yadns.exe"
!define UNINSTALL_PATH "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

;--------------------------------

!include "LogicLib.nsh"
!include "UninstallLog.nsh"
!include "MUI2.nsh"

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin" ;Require admin rights on NT4+
        messageBox mb_iconstop "Administrator rights required!"
        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED
        quit
${EndIf}
!macroend

Function .onInit
	setShellVarContext all
	!insertmacro VerifyUserIsAdmin
functionEnd

Function LaunchLink
  ExecShell "" "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
FunctionEnd

Function finishpageaction
  CreateShortcut "$desktop\DNSifier.lnk" "$INSTDIR\yadns.exe" "$INSTDIR\\yaicon.ico"
FunctionEnd

;--------------------------------
; Configure UnInstall log to only remove what is installed
;-------------------------------- 
  ;Set the name of the uninstall log
    !define UninstLog "uninstall.log"
    Var UninstLog
  ;The root registry to write to
    !define REG_ROOT "HKLM"
 
  ;Uninstall log file missing.
    LangString UninstLogMissing ${LANG_ENGLISH} "${UninstLog} not found!$\r$\nUninstallation cannot proceed!"
 
  ;AddItem macro
    !define AddItem "!insertmacro AddItem"
 
  ;BackupFile macro
    !define BackupFile "!insertmacro BackupFile" 
 
  ;BackupFiles macro
    !define BackupFiles "!insertmacro BackupFiles" 
 
  ;Copy files macro
    !define CopyFiles "!insertmacro CopyFiles"
 
  ;CreateDirectory macro
    !define CreateDirectory "!insertmacro CreateDirectory"
 
  ;CreateShortcut macro
    !define CreateShortcut "!insertmacro CreateShortcut"
 
  ;File macro
    !define File "!insertmacro File"
 
  ;Rename macro
    !define Rename "!insertmacro Rename"
 
  ;RestoreFile macro
    !define RestoreFile "!insertmacro RestoreFile"    
 
  ;RestoreFiles macro
    !define RestoreFiles "!insertmacro RestoreFiles"
 
  ;SetOutPath macro
    !define SetOutPath "!insertmacro SetOutPath"
 
  ;WriteRegDWORD macro
    !define WriteRegDWORD "!insertmacro WriteRegDWORD" 
 
  ;WriteRegStr macro
    !define WriteRegStr "!insertmacro WriteRegStr"
 
  ;WriteUninstaller macro
    !define WriteUninstaller "!insertmacro WriteUninstaller"
 
  Section -openlogfile
    CreateDirectory "$INSTDIR"
    IfFileExists "$INSTDIR\${UninstLog}" +3
      FileOpen $UninstLog "$INSTDIR\${UninstLog}" w
    Goto +4
      SetFileAttributes "$INSTDIR\${UninstLog}" NORMAL
      FileOpen $UninstLog "$INSTDIR\${UninstLog}" a
      FileSeek $UninstLog 0 END
  SectionEnd

;-------------------------------

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
 
    # These indented statements modify settings for MUI_PAGE_FINISH
    !define MUI_FINISHPAGE_NOAUTOCLOSE
    # there was an issue in the program where after you launched it from this menu
    # it wasn't possible to utilize a uac privelege elevation script
    #!define MUI_FINISHPAGE_RUN
    #!define MUI_FINISHPAGE_RUN_NOTCHECKED
    #!define MUI_FINISHPAGE_RUN_TEXT "Start DNSifier"
    #!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchLink"
    !define MUI_FINISHPAGE_SHOWREADME ""
    !define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
    !define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
    !define MUI_FINISHPAGE_SHOWREADME_FUNCTION finishpageaction
  !insertmacro MUI_PAGE_FINISH
  
;Languages
!insertmacro MUI_LANGUAGE "English"

; The stuff to install
section "install"

	; Set output path to the installation directory.
	;SetOutPath $INSTDIR
	
	${SetOutPath} $INSTDIR	
	${File} "yadns\bz2.pyd"
	${File} "yadns\gi._gi.pyd"
	${File} "yadns\gi._gi_cairo.pyd"
	${File} "yadns\libatk-1.0-0.dll"
	${File} "yadns\libcairo-gobject-2.dll"
	${File} "yadns\libffi-6.dll"
	${File} "yadns\libfontconfig-1.dll"
	${File} "yadns\libfreetype-6.dll"
	${File} "yadns\libgdk-3-0.dll"
	${File} "yadns\libgdk_pixbuf-2.0-0.dll"
	${File} "yadns\libgio-2.0-0.dll"
	${File} "yadns\libgirepository-1.0-1.dll"
	${File} "yadns\libglib-2.0-0.dll"
	${File} "yadns\libgmodule-2.0-0.dll"
	${File} "yadns\libgobject-2.0-0.dll"
	${File} "yadns\libgtk-3-0.dll"
	${File} "yadns\libharfbuzz-0.dll"
	${File} "yadns\libintl-8.dll"
	${File} "yadns\libjasper-1.dll"
	${File} "yadns\libjpeg-8.dll"
	${File} "yadns\libpango-1.0-0.dll"
	${File} "yadns\libpangocairo-1.0-0.dll"
	${File} "yadns\libpangoft2-1.0-0.dll"
	${File} "yadns\libpangowin32-1.0-0.dll"
	${File} "yadns\libpng16-16.dll"
	${File} "yadns\librsvg-2-2.dll"
	${File} "yadns\libtiff-5.dll"
	${File} "yadns\libwebp-5.dll"
	${File} "yadns\libwinpthread-1.dll"
	${File} "yadns\libxmlxpat.dll"
	${File} "yadns\libzzz.dll"
	${File} "yadns\mfc90.dll"
	${File} "yadns\mfc90u.dll"
	${File} "yadns\mfcm90.dll"
	${File} "yadns\mfcm90u.dll"
	${File} "yadns\Microsoft.VC90.CRT.manifest"
	${File} "yadns\Microsoft.VC90.MFC.manifest"
	${File} "yadns\msvcm90.dll"
	${File} "yadns\msvcp90.dll"
	${File} "yadns\msvcr90.dll"
	${File} "yadns\python27.dll"
	${File} "yadns\pythoncom27.dll"
	${File} "yadns\pywintypes27.dll"
	${File} "yadns\select.pyd"
	${File} "yadns\unicodedata.pyd"
	${File} "yadns\win32api.pyd"
	${File} "yadns\win32com.shell.shell.pyd"
	${File} "yadns\win32event.pyd"
	${File} "yadns\win32process.pyd"
	${File} "yadns\win32trace.pyd"
	${File} "yadns\win32ui.pyd"
	${File} "yadns\_ctypes.pyd"
	${File} "yadns\_hashlib.pyd"
	${File} "yadns\_socket.pyd"
	${File} "yadns\_ssl.pyd"
	${File} "yadns\_win32sysloader.pyd"
	${File} "yadns\hosts.txt"
	
	; create dirs
	${AddItem} "$INSTDIR\etc"
	${AddItem} "$INSTDIR\etc\fonts"
	${AddItem} "$INSTDIR\etc\fonts\cache"
	${AddItem} "$INSTDIR\etc\fonts\conf.d"
	${AddItem} "$INSTDIR\lib"
	${AddItem} "$INSTDIR\lib\gio"
	${AddItem} "$INSTDIR\lib\gio\modules"
	${AddItem} "$INSTDIR\lib\girepository-1.0"
	${AddItem} "$INSTDIR\lib\gdk-pixbuf-2.0"
	${AddItem} "$INSTDIR\lib\gdk-pixbuf-2.0\2.10.0"
	${AddItem} "$INSTDIR\share"
	${AddItem} "$INSTDIR\share\fonts"
	${AddItem} "$INSTDIR\share\glib-2.0"
	${AddItem} "$INSTDIR\share\glib-2.0\schemas"
	${AddItem} "$INSTDIR\share\fontconfig\conf.avail"
	${AddItem} "$INSTDIR\share\fontconfig"
	${AddItem} "$INSTDIR\share\locale"
	${AddItem} "$INSTDIR\share\locale\en"
	${AddItem} "$INSTDIR\share\locale\en\LC_MESSAGES"
	${AddItem} "$INSTDIR\share\icons\"
	${AddItem} "$INSTDIR\share\icons\Adwaita"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\actions"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\apps"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\categories"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\devices"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\emblems"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\emotes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\mimetypes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\places"
	${AddItem} "$INSTDIR\share\icons\Adwaita\16x16\status"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\actions"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\apps"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\categories"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\devices"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\emblems"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\emotes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\mimetypes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\places"
	${AddItem} "$INSTDIR\share\icons\Adwaita\24x24\status"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\actions"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\apps"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\categories"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\devices"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\emblems"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\emotes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\mimetypes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\places"
	${AddItem} "$INSTDIR\share\icons\Adwaita\32x32\status"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\actions"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\apps"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\categories"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\devices"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\emblems"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\emotes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\mimetypes"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\places"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable\status"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable-up-to-32"
	${AddItem} "$INSTDIR\share\icons\Adwaita\scalable-up-to-32\status"
	${AddItem} "$INSTDIR\share\icons\hicolor"
	${AddItem} "$INSTDIR\share\icons\HighContrast"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\actions"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\actions-extra"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\apps"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\apps-extras"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\categories"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\devices"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\emblems"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\mimetypes"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\places"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\places-extras"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\status"
	${AddItem} "$INSTDIR\share\icons\HighContrast\scalable\status-extras"
	${AddItem} "$INSTDIR\share\themes"
	${AddItem} "$INSTDIR\share\themes\Adwaita"
	${AddItem} "$INSTDIR\share\themes\Adwaita\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Ceti"
	${AddItem} "$INSTDIR\share\themes\Ceti\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Default"
	${AddItem} "$INSTDIR\share\themes\Default\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\E17gtk"
	${AddItem} "$INSTDIR\share\themes\E17gtk\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Emacs"
	${AddItem} "$INSTDIR\share\themes\Emacs\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\HighContrast"
	${AddItem} "$INSTDIR\share\themes\HighContrast\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\MS-Windows"
	${AddItem} "$INSTDIR\share\themes\MS-Windows\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Vertex"
	${AddItem} "$INSTDIR\share\themes\Vertex\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Vertex-Dark"
	${AddItem} "$INSTDIR\share\themes\Vertex-Dark\gtk-3.0"
	${AddItem} "$INSTDIR\share\themes\Vertex-Light"
	${AddItem} "$INSTDIR\share\themes\Vertex-Light\gtk-3.0"		
	
	${SetOutPath} $INSTDIR
	File yaicon.ico
	File /r yadns\*.*
	; Tell the compiler to write an uninstaller and to look for a "Uninstall" section
	${WriteUninstaller} $INSTDIR\Uninstall.exe
	
	# Start Menu
	${CreateDirectory} "$SMPROGRAMS\${APPNAME}"
	${CreateShortCut} "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\yadns.exe" "" "$INSTDIR\yaicon.ico" 0
	
	;Write the installation path into the registry
	${WriteRegStr} "${REG_ROOT}" "${REG_APP_PATH}" "Install Directory" "$INSTDIR"
	;Write the Uninstall information into the registry
	${WriteRegStr} ${REG_ROOT} "${UNINSTALL_PATH}" "UninstallString" "$INSTDIR\Uninstall.exe"

sectionEnd ; end the section	

# Uninstaller
 
function un.onInit
	SetShellVarContext all
 
	#Verify the uninstaller - last chance to back out
	MessageBox MB_OKCANCEL "Permanantly remove ${APPNAME}?" IDOK next
		Abort
	next:
	!insertmacro VerifyUserIsAdmin
functionEnd
 
section "uninstall"
 
	# Remove Start Menu launcher
	delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
	# Try to remove the Start Menu folder - this will only happen if it is empty
	rmDir "$SMPROGRAMS\${APPNAME}"
 
	;Can't uninstall if uninstall log is missing!
	IfFileExists "$INSTDIR\${UninstLog}" +3
		MessageBox MB_OK|MB_ICONSTOP "$(UninstLogMissing)"
		Abort
	
	Push $R0
	Push $R1
	Push $R2
	SetFileAttributes "$INSTDIR\${UninstLog}" NORMAL
	FileOpen $UninstLog "$INSTDIR\${UninstLog}" r
	StrCpy $R1 -1
	
	GetLineCount:
		ClearErrors
		FileRead $UninstLog $R0
		IntOp $R1 $R1 + 1
		StrCpy $R0 $R0 -2
		Push $R0   
		IfErrors 0 GetLineCount
	
	Pop $R0
	
	LoopRead:
		StrCmp $R1 0 LoopDone
		Pop $R0
	
		IfFileExists "$R0\*.*" 0 +3
		RMDir $R0  #is dir
		Goto +9
		IfFileExists $R0 0 +3
		Delete $R0 #is file
		Goto +6
		StrCmp $R0 "${REG_ROOT} ${REG_APP_PATH}" 0 +3
		DeleteRegKey ${REG_ROOT} "${REG_APP_PATH}" #is Reg Element
		Goto +3
		StrCmp $R0 "${REG_ROOT} ${UNINSTALL_PATH}" 0 +2
		DeleteRegKey ${REG_ROOT} "${UNINSTALL_PATH}" #is Reg Element
	
		IntOp $R1 $R1 - 1
		Goto LoopRead
	LoopDone:
	FileClose $UninstLog
	# the above isnt working, time for some quick and dirty uglyness
	delete "$INSTDIR\bz2.pyd"
	delete "$INSTDIR\gi._gi.pyd"
	delete "$INSTDIR\gi._gi_cairo.pyd"
	delete "$INSTDIR\libatk-1.0-0.dll"
	delete "$INSTDIR\libcairo-gobject-2.dll"
	delete "$INSTDIR\libffi-6.dll"
	delete "$INSTDIR\libfontconfig-1.dll"
	delete "$INSTDIR\libfreetype-6.dll"
	delete "$INSTDIR\libgdk-3-0.dll"
	delete "$INSTDIR\libgdk_pixbuf-2.0-0.dll"
	delete "$INSTDIR\libgio-2.0-0.dll"
	delete "$INSTDIR\libgirepository-1.0-1.dll"
	delete "$INSTDIR\libglib-2.0-0.dll"
	delete "$INSTDIR\libgmodule-2.0-0.dll"
	delete "$INSTDIR\libgobject-2.0-0.dll"
	delete "$INSTDIR\libgtk-3-0.dll"
	delete "$INSTDIR\libharfbuzz-0.dll"
	delete "$INSTDIR\libintl-8.dll"
	delete "$INSTDIR\libjasper-1.dll"
	delete "$INSTDIR\libjpeg-8.dll"
	delete "$INSTDIR\libpango-1.0-0.dll"
	delete "$INSTDIR\libpangocairo-1.0-0.dll"
	delete "$INSTDIR\libpangoft2-1.0-0.dll"
	delete "$INSTDIR\libpangowin32-1.0-0.dll"
	delete "$INSTDIR\libpng16-16.dll"
	delete "$INSTDIR\librsvg-2-2.dll"
	delete "$INSTDIR\libtiff-5.dll"
	delete "$INSTDIR\libwebp-5.dll"
	delete "$INSTDIR\libwinpthread-1.dll"
	delete "$INSTDIR\libxmlxpat.dll"
	delete "$INSTDIR\libzzz.dll"
	delete "$INSTDIR\mfc90.dll"
	delete "$INSTDIR\mfc90u.dll"
	delete "$INSTDIR\mfcm90.dll"
	delete "$INSTDIR\mfcm90u.dll"
	delete "$INSTDIR\Microsoft.VC90.CRT.manifest"
	delete "$INSTDIR\Microsoft.VC90.MFC.manifest"
	delete "$INSTDIR\msvcm90.dll"
	delete "$INSTDIR\msvcp90.dll"
	delete "$INSTDIR\msvcr90.dll"
	delete "$INSTDIR\python27.dll"
	delete "$INSTDIR\pythoncom27.dll"
	delete "$INSTDIR\pywintypes27.dll"
	delete "$INSTDIR\select.pyd"
	delete "$INSTDIR\unicodedata.pyd"
	delete "$INSTDIR\win32api.pyd"
	delete "$INSTDIR\win32com.shell.shell.pyd"
	delete "$INSTDIR\win32event.pyd"
	delete "$INSTDIR\win32process.pyd"
	delete "$INSTDIR\win32trace.pyd"
	delete "$INSTDIR\win32ui.pyd"
	delete "$INSTDIR\_ctypes.pyd"
	delete "$INSTDIR\_hashlib.pyd"
	delete "$INSTDIR\_socket.pyd"
	delete "$INSTDIR\_ssl.pyd"
	delete "$INSTDIR\_win32sysloader.pyd"
	delete "$INSTDIR\hosts.txt"
	delete "$INSTDIR\${UninstLog}"
	rmdir /r "$INSTDIR\gi_typelibs"
	rmdir /r "$INSTDIR\Include"
	rmdir /r "$INSTDIR\etc"
	rmdir /r "$INSTDIR\lib"
	rmdir /r "$INSTDIR\share"
	delete "$INSTDIR\*.dll"
	delete "$INSTDIR\yadns.exe"
	delete "$INSTDIR\yaicon.ico"
	RMDir "$INSTDIR"
	Pop $R2
	Pop $R1
	Pop $R0
sectionEnd 