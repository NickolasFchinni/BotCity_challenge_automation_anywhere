$exclude = @("venv", "customer_onboarding.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "customer_onboarding.zip" -Force