cd ~
mkdir .kebab
cd .kebab
curl.exe -L -O https://github.com/kebab-os/kebab-os/archive/refs/heads/main.zip
Expand-Archive -Path kebab-os.zip -DestinationPath .
cd kebab-os-main
pip install pygame requests html2image
