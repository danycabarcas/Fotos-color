[Setup]
AppName=Optimizador de Fotos
AppVersion=1.0.0
AppPublisher=DanyTechCo
AppPublisherURL=mailto:Danycabarcas@gmail.com
DefaultDirName={autopf}\Optimizador de Fotos
DefaultGroupName=Optimizador de Fotos
OutputDir=.\Installer
OutputBaseFilename=Instalador_Optimizador_Fotos
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Optimizador_de_Fotos\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Aseguramos que el icono también se copie a la carpeta de instalación para los accesos directos
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Optimizador de Fotos"; Filename: "{app}\Optimizador_de_Fotos.exe"; IconFilename: "{app}\app_icon.ico"
Name: "{autodesktop}\Optimizador de Fotos"; Filename: "{app}\Optimizador_de_Fotos.exe"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\Optimizador_de_Fotos.exe"; Description: "{cm:LaunchProgram,Optimizador de Fotos}"; Flags: nowait postinstall skipifsilent
