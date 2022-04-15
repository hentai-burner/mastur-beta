#Requires -RunAsAdministrator
Add-Type -AssemblyName System.Windows.Forms

####    SETUP.PS1
##    Needs to:
##    * Install the program and any dependencies
##      * Disclaimer
##      * Setup all of the Config; Including:
##          * Details for fake blackmail
##          * Location of Porn Folder for file overwrite (ask for it to customise the experience, say will use the images)
##          * Info abt Kinks etc 
##          * any words that trigger them (use it all in lowercase)
##          * Safety Options:
##              * Turn off Typing Prompts
##              * Turn off File Replacement
##              * Create Blacklisted Times when it won't turn on
##      * Install all images and content based on what kinks are selected


##DISCLAIMER
Write-Host "==DISCLAIMER=="
Write-Host "This Software is for adults 18+ only. It contains sexually explicit content and taboo themes."
Write-Host "This software is considered Malware. While everything is theoretically reversible, I am not responsible for any permanent damages caused by this software."
Write-Host "Nor I am responsible for any Emotional or Relationship Damage, caused by degrading content, nor getting fired or similar issues." #word this better holy
Write-Host "You also acknowledge that while this program will not distribute any of the data provided to it, all of the data will be exposed in plain-text"
Write-Host "If you do not accept these terms, or are under 18; Press Ctrl+C now."
Pause

Write-Host "Alright! We're getting you setup; Hold Tight, I'll be with you shortly."

$Directory = "C:\.masturbeta" #maybe change this to a folder-browser
if (-not (test-path "$Directory") ) {
	New-Item -ItemType directory -Path $Directory | Out-Null  
}
else {
	Write-Host "Directory Already Exists. If you're updating, run update.ps1 instead."
	Write-Host "Do you want to reset and replace the directory? (Y/n)"
	$tmp = Read-Host
	if (-not ("$tmp" -like "*n*")) {
		New-Item -ItemType directory -Path $Directory -Force | Out-Null
	}
}
Set-Location $Directory

$repoUrl = "https://github.com/hentai-burner/mastur-beta.git"

#get info 
Write-Host "What's your name?"
$name = if (($result = Read-Host "Press enter to accept default value [$env:UserName], or manually insert a value.") -eq '') { $env:UserName } else { $result }

Write-Host "This program will use your normal Porn Collection as incentive from time to time, so make sure you select a folder with only porn."
Write-Host "Assuming you have a Porn folder, press Enter, and then select it in the Pop-Up."
Pause

#Find Hentai Folder
$FileBrowser = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{ 
																				RootFolder = 'MyComputer'
																				Description = 'Select the folder where you keep your porn.'
																			}
$null = $FileBrowser.ShowDialog()
$pornFolder = $FileBrowser.SelectedPath

#List Kinks
Write-Host "Here's a list of Kinks and Fetishes; If any of them make you uncomfortable, type something in the prompt, otherwise, just press Enter."
$kinks = @("Blacked","Censored","Furry","Gay","Hypno","MLP","Fart","Toilet","Futanari","Humiliation")
#$kinkOn = @($true,   $true,     $true,  $true,$true,  $true,$true, $true,   $true,     $true)
$kinkOn = @()
for ($i = 0; $i -lt $kinks.Count; $i++) {
	$kink = $kinks[$i]
	$ans = Read-Host "Are you okay with $kink porn?"
	#$kinkOn[$i] = if($ans -eq ''){$true} else{$false} 
	$kinkOn += if($ans -eq ''){$true} else{$false} 
}

#save info
$UserData = New-Object PSObject -Property @{
		Version = 0.1
		Name = $name 
		PornFolder = $pornFolder
	} # see https://devblogs.microsoft.com/powershell/new-object-psobject-property-hashtable/
	for ($i = 0; $i -lt $kinkOn.Count; $i++) {
		$UserData | Add-Member -NotePropertyName $kinks[$i] -NotePropertyValue $kinkOn[$i]
	}

#check if info is correct
Write-Host ($UserData | Format-Table | Out-String)
Read-Host "Is this Correct? (Y/n)"
#TODO check if the read-host works




#install everything

Write-Progress -Activity 'Installing' -Status 'Initial Setup' -SecondsRemaining 1 -PercentComplete 9 -CurrentOperation 'Creating Directory'

if ($null -eq $env:ChocolateyInstall) {
	Write-Host "This computer doesn't Chocolatey Installed. Installing Chocolatey for dependencies. It will be removed after installation."
	Write-Progress -Activity 'Installing' -Status 'Installing Chocolatey' -SecondsRemaining  -PercentComplete 
	$InstallDir = "$Directory\chocoportable" | Out-Null
	$env:ChocolateyInstall = "$InstallDir" | Out-Null
	Set-ExecutionPolicy Bypass -Scope Process -Force | Out-Null
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
	Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
}

#Clear-Host
Write-Host "Installing Dependencies; Check the top of the shell for more info; The program may seem unresponsive, so don't panic."
Write-Progress -Activity 'Installing' -Status 'Installing Chocolatey' -SecondsRemaining 1 -PercentComplete 1  -CurrentOperation "Updating Existing Packages; The program may seem unresponsive, so don't panic."
Invoke-Expression "$env:ChocolateyInstall\choco.exe upgrade all -y" | Out-Null
Write-Progress -Activity 'Installing' -Status 'Installing Chocolatey' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Installing Dependencies - git'
Invoke-Expression "$env:ChocolateyInstall\choco.exe install git -y" | Out-Null
Write-Progress -Activity 'Installing' -Status 'Installing Chocolatey' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Installing Dependencies - python'
Invoke-Expression "$env:ChocolateyInstall\choco.exe install python --params ""/NoLockdown"" -y" | Out-Null
Write-Progress -Activity 'Installing' -Status 'Installing Chocolatey' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Installing Dependencies - pip'
Invoke-Expression "$env:ChocolateyInstall\choco.exe install pip -y" | Out-Null
Write-Progress -Activity 'Installing' -Status 'Installing MasturBeta' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Resetting Path'
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User") #reset path
Write-Progress -Activity 'Installing' -Status 'Installing MasturBeta' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Cloning Repository'

Invoke-Expression "git init" | Out-Null
Invoke-Expression "git remote add origin $repoURL" | Out-Null
Invoke-Expression "git fetch" | Out-Null
Invoke-Expression "git reset origin/main" | Out-Null  # Required when the versioned files existed in path before "git init" of this repo.
Invoke-Expression "git checkout -t origin/main" | Out-Null
#Invoke-Expression "git clone -q --recursive $repoUrl $Directory" | Out-Null #clone doesn't work on non-empty dir

Write-Progress -Activity 'Installing' -Status 'Installing MasturBeta' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Saving Configuration'
#send info to JSON
$UserData | ConvertTo-Json | Out-File -FilePath "$Directory\config.json" #unsure if this works

Write-Progress -Activity 'Installing' -Status 'Installing MasturBeta' -SecondsRemaining 1 -PercentComplete 1 -CurrentOperation 'Hiding Directory and Contents'
#hide directory and all child objects
$DIR = Get-Item $Directory -Force
$DIR.attributes = "Hidden"
Get-ChildItem -path $Directory -Recurse -Force | ForEach-Object { $_.attributes = "Hidden" } | Out-Null

Write-Progress -Activity 'Installing' -Status 'Installing MasturBeta' -SecondsRemaining 1  -PercentComplete 1 -CurrentOperation 'Setting Up Run at Startup'
#Set to run at Startup
"PowerShell -NoProfile -ExecutionPolicy Bypass -Command ""& { Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File """"C:\.masturbeta\start.ps1"""" -Verb RunAs}" | Out-File -FilePath "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\masturbeta.bat" # -Encoding utf8

#TODO Get porn for individual kinks
#TODO Edit C:\Windows\System32\drivers\etc\hosts to contain a bunch of redirects to the porn router

Write-Progress -Activity 'Installing' -Status 'Finished' -SecondsRemaining 0 -PercentComplete 100 -Completed

Invoke-Expression "$Directory\start.ps1"

#Clear-Host

