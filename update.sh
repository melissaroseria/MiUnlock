#!/bin/bash
# update.sh - Termux için otomatik güncelleme ve çalıştırma scripti

# Renkli çıktı için
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[+] Repo güncelleniyor...${NC}"

# Eğer repo yoksa klonla, varsa güncelle
if [ ! -d "MiUnlock" ]; then
    git clone https://github.com/melissaroseria/MiUnlock.git
else
    cd MiUnlock
    git pull
    cd ..
fi

echo -e "${GREEN}[+] lock.py çalıştırılıyor...${NC}"

# Python ile lock.py çalıştır
cd MiUnlock
python lock.py
