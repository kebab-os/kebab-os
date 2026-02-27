cd ~
if (!(Test-Path .kebab)) { mkdir .kebab }
cd .kebab
curl.exe -L https://github.com/kebab-os/kebab-os/archive/refs/heads/main.zip -o kebab-os.zip
Expand-Archive -Path kebab-os.zip -DestinationPath . -Force
cd kebab-os-main
pip install pygame requests html2image
