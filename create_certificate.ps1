# Build self-signed certificate for code signing
# This script creates a development code signing certificate

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "MergePDF - Create Self-Signed Certificate" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Warning: Running with administrator privileges is recommended" -ForegroundColor Yellow
    Write-Host "Some operations may require admin rights" -ForegroundColor Yellow
    Write-Host ""
}

# Certificate parameters
$certName = "MergePDF Developer Certificate"
$certSubject = "CN=MergePDF,O=MergePDF Development,C=TW"
$certStore = "Cert:\CurrentUser\My"

Write-Host "Step 1: Checking for existing certificate..." -ForegroundColor Green

# Check for existing certificate
$existingCert = Get-ChildItem -Path $certStore | Where-Object { $_.Subject -eq $certSubject }

if ($existingCert) {
    Write-Host "Found existing certificate:" -ForegroundColor Yellow
    Write-Host "  Subject: $($existingCert.Subject)" -ForegroundColor White
    Write-Host "  Thumbprint: $($existingCert.Thumbprint)" -ForegroundColor White
    Write-Host "  Valid: $($existingCert.NotBefore) to $($existingCert.NotAfter)" -ForegroundColor White
    Write-Host ""
    
    $response = Read-Host "Use existing certificate? (Y/N)"
    if ($response -eq "Y" -or $response -eq "y") {
        $cert = $existingCert
    } else {
        Write-Host "Removing old certificate..." -ForegroundColor Yellow
        $existingCert | Remove-Item
        $cert = $null
    }
} else {
    $cert = $null
}

# Create new certificate if needed
if (-not $cert) {
    Write-Host ""
    Write-Host "Step 2: Creating new self-signed certificate..." -ForegroundColor Green
    
    try {
        # Create self-signed certificate (valid for 3 years)
        $cert = New-SelfSignedCertificate `
            -Type CodeSigningCert `
            -Subject $certSubject `
            -KeyUsage DigitalSignature `
            -FriendlyName $certName `
            -CertStoreLocation $certStore `
            -NotAfter (Get-Date).AddYears(3)
        
        Write-Host "Certificate created successfully!" -ForegroundColor Green
        Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
        Write-Host ""
        
    } catch {
        Write-Host "Failed to create certificate: $($_.Exception.Message)" -ForegroundColor Red
        Read-Host "Press Enter to continue"
        exit 1
    }
}

# Export certificate to trusted root (optional)
Write-Host "Step 3: Install certificate to Trusted Root..." -ForegroundColor Green
Write-Host "This can avoid Windows Unknown Publisher warnings" -ForegroundColor Yellow
Write-Host ""

$installToRoot = Read-Host "Install certificate to Trusted Root? (Y/N, requires admin)"

if ($installToRoot -eq "Y" -or $installToRoot -eq "y") {
    try {
        # Export to temp file
        $tempCerFile = "$env:TEMP\MergePDF_Cert.cer"
        Export-Certificate -Cert $cert -FilePath $tempCerFile -Type CERT | Out-Null
        
        # Import to Trusted Root
        Import-Certificate -FilePath $tempCerFile -CertStoreLocation Cert:\CurrentUser\Root | Out-Null
        
        # Remove temp file
        Remove-Item $tempCerFile -Force
        
        Write-Host "Certificate installed to Trusted Root" -ForegroundColor Green
        Write-Host ""
    } catch {
        Write-Host "Installation failed (may need admin): $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You can install manually later or re-run as administrator" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Save certificate thumbprint
Write-Host "Step 4: Saving certificate info..." -ForegroundColor Green

$configFile = ".\certificate_config.txt"
$cert.Thumbprint | Out-File -FilePath $configFile -Encoding UTF8

Write-Host "Certificate thumbprint saved to: $configFile" -ForegroundColor Green
Write-Host ""

# Display summary
Write-Host "================================================" -ForegroundColor Green
Write-Host "Certificate creation complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Certificate Info:" -ForegroundColor Cyan
Write-Host "  Subject: $($cert.Subject)" -ForegroundColor White
Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
Write-Host "  Valid: $($cert.NotBefore) to $($cert.NotAfter)" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run build_simple.ps1 to compile the program" -ForegroundColor White
Write-Host "  2. Run sign_exe.ps1 to sign the executable" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to continue"
