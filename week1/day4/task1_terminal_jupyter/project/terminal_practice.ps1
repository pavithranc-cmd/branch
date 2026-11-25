# Terminal practice (Windows PowerShell).
# Run from the folder that CONTAINS "project":  .\project\terminal_practice.ps1
New-Item -ItemType Directory -Force project/data, project/notebooks, project/reports | Out-Null

Write-Host "== mkdir + ls ==";  Get-ChildItem project -Name | Out-Host
Write-Host "== cd ==";          Set-Location project/data; (Get-Location).Path | Out-Host
Write-Host "== cp ==";          Copy-Item employees.csv employees_backup.csv; Get-ChildItem -Name | Out-Host
Write-Host "== mv ==";          Move-Item employees_backup.csv ..\reports\employees_copy.csv -Force; Get-ChildItem ..\reports -Name | Out-Host
Write-Host "== rm ==";          Remove-Item ..\reports\employees_copy.csv; Get-ChildItem ..\reports -Name | Out-Host
Write-Host "== grep -i chennai (Select-String is case-insensitive by default) =="
Select-String -Path employees.csv -Pattern "chennai" | Out-Host
Write-Host "== case-sensitive (like grep without -i) =="
Select-String -Path employees.csv -Pattern "chennai" -CaseSensitive | Out-Host
(Select-String -Path employees.csv -Pattern "chennai").Line | Set-Content ..\reports\chennai_employees.txt
Set-Location ..\..
Write-Host "== structure =="; Get-ChildItem project -Recurse -Name | Out-Host
