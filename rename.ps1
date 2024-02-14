# Navigate to the directory (change to your actual path)
cd "C://git/read-letters/rename"
# Get the list of files
$files = Get-ChildItem -File

foreach ($file in $files) {
    $originalFileName = $file.BaseName
    $extension = $file.Extension
    # Split the file name by dashes
    $parts = $originalFileName -split '-'

    # Extract individual parts
    $year = $parts[0]
    $month = $parts[1]
    $day = $parts[2]
    $person = $parts[3]
    $number = $parts[4]  # Assuming this is the numeric part
    $location = $parts[5]   
    $pad = "_000"
    # Construct the new name
    $newName = "$year-$month-$day-$person-$location$pad$number$extension"
    Rename-Item -Path $file.FullName -NewName $newName
    Write-Host $newName

}
