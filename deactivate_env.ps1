# Deactivates the virtual environment for the cryptography web app project.

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
} else {
    Write-Host "Deactivate command not found. Make sure the virtual environment is activated."
}
