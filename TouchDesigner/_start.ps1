param($env)


function LoadEnvVarObject{
	param($envFile)

	# Creates a powershell object that holds all of the vars in the .env file passed in.
	$envObject = Get-Content $envFile | Out-String | ConvertFrom-StringData
	foreach ($property in $envObject.Keys) {
		Set-Item "Env:$property" $($envObject.($property))
	}
	return $envObject
}

function ClearEnvVarObject {
	param($envFile)

	# Creates a powershell object that holds all of the vars in the .env file passed in.
	$envObject = Get-Content $envFile | Out-String | ConvertFrom-StringData
	foreach ($property in $envObject.Keys) {
		Set-Item "Env:$property" ""
	}
}

function GetTouchDesigner {
	param($version)
	try {
		$command = (get-itemproperty -ErrorAction Stop Registry::HKEY_CLASSES_ROOT\TouchDesigner.$version\shell\open\command)."(default)"
		return $command.replace(' "%1"', "")
	} 
	catch {
		echo "TouchDesigner.$version is not installed on this machine."
		echo "Install it here: https://download.derivative.ca/TouchDesigner.$version.exe"
		exit
	}
}

function RunAsynchronous {
	param (
		$open_command,
		$project_file
	)
	echo "Running asynchronously..."
	Start-Process $open_command $project_file
}

function RunSynchronous {
	param (
		$open_command,
		$project_file
	)
	echo "Running synchronously..."
	Start-Process $open_command $project_file -Wait
}

echo environment:$env

$config = LoadEnvVarObject $env
$tdExe = GetTouchDesigner $config.tdVersion

if($config.SM_BUILD){
	echo "building project..."
	RunSynchronous $tdExe $config.file
} else {
	echo ""
	RunAsynchronous $tdExe $config.file
}

ClearEnvVarObject $env