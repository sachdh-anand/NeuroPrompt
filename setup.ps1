# NeuroPrompt Empty Files Setup Script for Windows
# Creates all required empty files in the correct structure

# Display header
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  NeuroPrompt - Empty Files Setup   " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Function to create directories
function Create-DirectoryIfNotExists {
    param (
        [string]$Path
    )
    
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created directory: $Path" -ForegroundColor Green
    } else {
        Write-Host "Directory already exists: $Path" -ForegroundColor Yellow
    }
}

# Function to create empty file
function Create-EmptyFile {
    param (
        [string]$Path
    )
    
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType File -Path $Path -Force | Out-Null
        Write-Host "Created empty file: $Path" -ForegroundColor Green
    } else {
        Write-Host "File already exists: $Path" -ForegroundColor Yellow
    }
}

# Create main directories
Write-Host "Creating directory structure..." -ForegroundColor Cyan
Create-DirectoryIfNotExists -Path "agents"
Create-DirectoryIfNotExists -Path "core"
Create-DirectoryIfNotExists -Path "data"
Create-DirectoryIfNotExists -Path "documents"
Create-DirectoryIfNotExists -Path "documents\frameworks"
Create-DirectoryIfNotExists -Path "logs"
Create-DirectoryIfNotExists -Path "tests"

# Create agent files
Write-Host "`nCreating agent files..." -ForegroundColor Cyan
Create-EmptyFile -Path "agents\prompt_generator.py"
Create-EmptyFile -Path "agents\researcher.py"
Create-EmptyFile -Path "agents\critic.py"
Create-EmptyFile -Path "agents\optimizer.py"
Create-EmptyFile -Path "agents\__init__.py"

# Create core files
Write-Host "`nCreating core files..." -ForegroundColor Cyan
Create-EmptyFile -Path "core\model_manager.py"
Create-EmptyFile -Path "core\crew.py"
Create-EmptyFile -Path "core\__init__.py"

# Create data files
Write-Host "`nCreating data files..." -ForegroundColor Cyan
Create-EmptyFile -Path "data\knowledge_graph.json"
Create-EmptyFile -Path "data\optimization_history.json"
Create-EmptyFile -Path "data\evaluation_criteria.json"

# Create document files
Write-Host "`nCreating document files..." -ForegroundColor Cyan
Create-EmptyFile -Path "documents\latest_trends.md"
Create-EmptyFile -Path "documents\frameworks\PECRA.md"
Create-EmptyFile -Path "documents\frameworks\SCQA.md"
Create-EmptyFile -Path "documents\frameworks\ReAct.md"
Create-EmptyFile -Path "documents\frameworks\RISEN.md"

# Create log file
Write-Host "`nCreating log file..." -ForegroundColor Cyan
Create-EmptyFile -Path "logs\execution.log"

# Create test files
Write-Host "`nCreating test files..." -ForegroundColor Cyan
Create-EmptyFile -Path "tests\test_model_manager.py"
Create-EmptyFile -Path "tests\test_framework_loading.py"
Create-EmptyFile -Path "tests\test_integration.py"
Create-EmptyFile -Path "tests\test_all.py"
Create-EmptyFile -Path "tests\quick_test.py"
Create-EmptyFile -Path "tests\__init__.py"

# Create root files
Write-Host "`nCreating root files..." -ForegroundColor Cyan
Create-EmptyFile -Path "run.py"
Create-EmptyFile -Path ".env.template"
Create-EmptyFile -Path ".gitignore"
Create-EmptyFile -Path "README.md"
Create-EmptyFile -Path "requirements.txt"
Create-EmptyFile -Path "setup.sh"
Create-EmptyFile -Path "Makefile"
Create-EmptyFile -Path "PROJECT_CHECKLIST.md"
Create-EmptyFile -Path "LICENSE"

Write-Host "`nSetup complete! All empty files created." -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Copy and paste the code from your implementation into these files" -ForegroundColor White
Write-Host "2. Ensure you have Python 3.8+ installed" -ForegroundColor White
Write-Host "3. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
Write-Host "4. Run the application: python run.py 'Your prompt request'" -ForegroundColor White
Write-Host ""