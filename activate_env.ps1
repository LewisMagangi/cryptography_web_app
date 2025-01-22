# Activates the virtual environment for the cryptography web app project.

$envPath = "C:\Users\User\Documents\GitHub\cryptography_web_app\venv_cryptography\Scripts\Activate.ps1"
if (Test-Path $envPath) {
    & $envPath
} else {
    Write-Host "Virtual environment activation script not found at $envPath"
}
