# P6 NSIS Build Script
# (c) 2005, Nathan R. Yergler, Creative Commons
#
# Notes:
#  Before running the bootstrap script must be built using py2exe; this is
#  currently in the autopackage folder -- python setup.py py2exe
#
#  The zope.proxy extension module must also be built.  

Name "P6"

# Defines
!define REGKEY "SOFTWARE\P6"
!define VERSION 2.0
!define COMPANY "Creative Commons"
!define URL http://creativecommons.org

# MUI defines
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\box-install.ico"
!define MUI_FINISHPAGE_NOAUTOCLOSE
!define MUI_STARTMENUPAGE_REGISTRY_ROOT HKCU
!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_REGISTRY_KEY Software\ccPublisher
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME StartMenuGroup
!define MUI_STARTMENUPAGE_DEFAULT_FOLDER ccPublisher
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\box-uninstall.ico"
!define MUI_UNFINISHPAGE_NOAUTOCLOSE

# Included files
!include Sections.nsh
!include MUI.nsh

# Reserved Files

# Variables

# Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE ..\..\resources\LICENSE.txt
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Installer languages
!insertmacro MUI_LANGUAGE English

# Installer attributes
OutFile setup.exe
InstallDir "$PROGRAMFILES\Common Files\P6"
CRCCheck on
XPStyle on
ShowInstDetails show
VIProductVersion 2.0.0.0
VIAddVersionKey ProductName P6
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey CompanyWebsite "${URL}"
VIAddVersionKey FileVersion ""
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
InstallDirRegKey HKLM "${REGKEY}" Path
ShowUninstDetails show

# Installer sections
Section -Main SEC0000
    SetOutPath "$INSTDIR\site-packages\"
    SetOverwrite on
    # core P6 files
    File /r ..\..\zope
    File /r ..\..\p6

    # P6 support libraries
    File /r ..\..\ccwsclient
    File /r ..\..\ccwx
    #File /r ..\..\tagger
    #File /r ..\..\eyeD3

    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

Section -post SEC0001
    WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
    WriteRegStr HKLM "${REGKEY}" SharedPath "$INSTDIR\site-packages"
    WriteRegStr HKLM "${REGKEY}" CurrentVersion ${VERSION}
    WriteUninstaller $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayName "$(^Name)"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayVersion "${VERSION}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" Publisher "${COMPANY}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" URLInfoAbout "${URL}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" DisplayIcon $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" UninstallString $INSTDIR\uninstall.exe
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoModify 1
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)" NoRepair 1
SectionEnd

# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    Goto done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

# Uninstaller sections
Section /o un.Main UNSEC0000
    RMDir /r /REBOOTOK $INSTDIR
    DeleteRegValue HKLM "${REGKEY}\Components" Main
SectionEnd

Section un.post UNSEC0001
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\$(^Name)"
    #Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\$(^UninstallLink).lnk"
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    #DeleteRegValue HKLM "${REGKEY}" StartMenuGroup
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /ifempty HKLM "${REGKEY}\Components"
    DeleteRegKey /ifempty HKLM "${REGKEY}"
    RMDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RMDir /REBOOTOK $INSTDIR
SectionEnd

# Installer functions
Function .onInit
    InitPluginsDir
FunctionEnd

# Uninstaller functions
Function un.onInit
    ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
    # ReadRegStr $StartMenuGroup HKLM "${REGKEY}" StartMenuGroup
    !insertmacro SELECT_UNSECTION Main ${UNSEC0000}
FunctionEnd

