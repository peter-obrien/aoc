$today = Get-Date
$year = $today.Year
$nextDir = 0
foreach ($child in Get-ChildItem -Path $PSScriptRoot -Directory) {
    if ($year -eq $child.BaseName){
        foreach ($gchild in Get-ChildItem -Path $PSScriptRoot/$year) {
            if ([int]$gchild.BaseName -gt $nextDir) {
                $nextDir = $gchild.BaseName
            }
        }
        break
    }
}
$nextDir = ([int]$nextDir + 1).ToString().PadLeft(2, '0')
New-Item -Path $year/$nextDir -ItemType Directory
Copy-Item -Path '.\template.py' -Destination $year/$nextDir/solution.py
New-Item -Path $year/$nextDir/sample.txt -ItemType File
New-Item -Path $year/$nextDir/input.txt -ItemType File
Set-Location $year/$nextDir