@@echo off
:CheckPowerShellExecutionPolicy
@@FOR /F "tokens=*" %%i IN ('powershell -noprofile -command Get-ExecutionPolicy') DO Set PSExecMode=%%i
@@if /I "%PSExecMode%"=="unrestricted" goto :RunPowerShellScript
@@if /I "%PSExecMode%"=="remotesigned" goto :RunPowerShellScript
 
@@NET FILE 1>NUL 2>NUL
@@if not "%ERRORLEVEL%"=="0" (
@@echo Elevation required to change PowerShell execution policy from [%PSExecMode%] to RemoteSigned
@@powershell -NoProfile -Command "start-process -Wait -Verb 'RunAs' -FilePath 'powershell.exe' -ArgumentList '-NoProfile Set-ExecutionPolicy RemoteSigned'"
@@) else (
@@powershell -NoProfile Set-ExecutionPolicy RemoteSigned
@@)
 
:RunPowerShellScript
@@set POWERSHELL_BAT_ARGS=%*
@@if defined POWERSHELL_BAT_ARGS set POWERSHELL_BAT_ARGS=%POWERSHELL_BAT_ARGS:"=\"%
@@PowerShell -Command Invoke-Expression $('$args=@(^&{$args} %POWERSHELL_BAT_ARGS%);'+[String]::Join([Environment]::NewLine,$((Get-Content '%~f0') -notmatch '^^@@^|^^:'))) & goto :EOF
 
{ 
	# Start PowerShell
	[reflection.assembly]::LoadWithPartialName("System.Drawing")

    $SizeLimit=10                                                       # required size of picture's long side
    $logfile="resizelog.txt"                                            # log file for errors
    $toresize= $PSScriptRoot    # list of directories to find and resize images. can be empty
    $counter=0
    
    $original=0
    $new=0

    echo $toresize           # visual control

    $error.clear()

    # first part. find and resize jpgs

    Get-ChildItem -recurse $toresize -include *.jpg  | foreach {
      $OldBitmap = new-object System.Drawing.Bitmap $_.FullName # open found jpg
      if ($error.count -ne 0) {                                 # error handling
        $error | out-file $logfile -append -encoding default
        $error[($error.count-1)].TargetObject | out-file $logfile -append -encoding default
        Write-host $_>>$logfile
        $error.clear()
      }
      $LongSide=$OldBitmap.Width                                # locating long side of picture
      if ($OldBitmap.Width -lt $OldBitmap.Height) { $LongSide=$OldBitmap.Height }
      if ($LongSide -ge $SizeLimit) {                           # if long side is greater than our limit, process jpg
       
          $newH=$OldBitmap.Height
          $newW=$OldBitmap.Width

        $NewBitmap = new-object System.Drawing.Bitmap $newW,$newH # create new bitmap
        $g=[System.Drawing.Graphics]::FromImage($NewBitmap)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic # use high quality resize algorythm
        $g.DrawImage($OldBitmap, 0, 0, $newW, $newH)              # resize our picture
        $g.Dispose()

        $name=$_.DirectoryName+"\"+$_.name+".new"                 # generating name for new picture
        $NewBitmap.Save($name, ([system.drawing.imaging.imageformat]::jpeg)) # save newly created resized jpg
        $NewBitmap.Dispose()                                      # cleaning up our mess
        $OldBitmap.Dispose()
        $n=get-childitem $name
        if ($n.length -ge $_.length) {                            # if resized jpg has greater size than original
          Write-host -NoNewLine "+"                               # draw "+"
          $n.delete()                                             # and delete it
        } else {                                                  # if resized jpg is smaller than original
          if ($n.Exists -and $_.Exists) {
            $name=$_.FullName
            $_.Delete()                                           # delete original
            $n.MoveTo($name)                                      # rename new file to original name (replace old file with new)
            Write-host ($Name + " " + $LongSide)                        # write its name for visual control
          }
        }
        $original = $original + $_.length; 
        $new = $new + $n.length;

      } else {                                                    # if long side is smaller than limit, draw dot for visual
        Write-host -NoNewLine "."
        $OldBitmap.Dispose()
      }
      if (($counter % 30) -eq 0){
      Write-host "Garbage Dump"
      
        [System.GC]::Collect()
        Remove-Variable n
        Remove-Variable name
        Remove-Variable g
        Remove-Variable NewBitmap
        Remove-Variable OldBitmap
        Remove-Variable newH
        Remove-Variable newW
        Remove-Variable longSide
      }
        $counter=$counter+1
    }
    Write-Host " "
    Write-Host "Original size: " ($original / (1024 * 1024)) "MB"
    Write-Host "New size: " ($new / (1024 * 1024)) "MB"

    Write-Host "Press any key to continue ..."

    $x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
	# End PowerShell
}.Invoke($args)