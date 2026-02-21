#!/bin/bash

# ==========================================
# 𝖤𝗅𝗂𝗍𝖾 𝖤𝗇𝖼𝗈𝖽𝖾𝗋 𝖷𝟫 - 𝖬𝖺𝗌𝗍𝖾𝗋 𝖡𝗈𝗈𝗍 𝖲𝗒𝗌𝗍𝖾𝗆
# 𝖢𝗈𝖽𝖾𝖽 𝖲𝗉𝖾𝖼𝗂𝖺𝗅𝗅𝗒 𝖿𝗈𝗋: 𝖬𝖺𝗌𝗍𝖾𝗋 𝖩𝖾𝖾𝗍
# ==========================================

# 𝖢𝗈𝗅𝗈𝗋 𝖢𝗈𝖽𝖾𝗌 𝖿𝗈𝗋 𝖯𝗋𝗈𝖿𝖾𝗌𝗌𝗂𝗈𝗇𝖺𝗅 𝖫𝗈𝗀𝗌
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Elite Encoder Engine...${NC}"

# 𝖴𝗉𝖽𝖺𝗍𝗂𝗇𝗀 𝖲𝗒𝗌𝗍𝖾𝗆 𝖺𝗇𝖽 𝖨𝗇𝗌𝗍𝖺𝗅𝗅𝗂𝗇𝗀 𝖤𝗌𝗌𝖾𝗇𝗍𝗂𝖺𝗅𝗌
echo -e "${YELLOW}⚙️ Updating system packages...${NC}"
apt-get update && apt-get upgrade -y

# 𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀 𝖺𝗇𝖽 𝖨𝗇𝗌𝗍𝖺𝗅𝗅𝗂𝗇𝗀 𝖥𝖥𝗆𝗉𝖾𝗀 (𝖬𝗎𝗌𝗍 𝖿𝗈𝗋 𝖤𝗇𝖼𝗈𝖽𝗂𝗇𝗀)
if ! command -v ffmpeg &> /dev/null
then
    echo -e "${YELLOW}⚠️ FFmpeg not found, installing now...${NC}"
    apt-get install ffmpeg -y
    echo -e "${GREEN}✅ FFmpeg installed successfully.${NC}"
else
    echo -e "${GREEN}✅ FFmpeg is already available.${NC}"
fi

# 𝖨𝗇𝗌𝗍𝖺𝗅𝗅𝗂𝗇𝗀 𝖯𝗒𝗍𝗁𝗈𝗇 𝖣𝖾𝗉𝖾𝗇𝖽𝖾𝗇𝖼𝗂𝖾𝗌
echo -e "${YELLOW}📦 Installing Python requirements...${NC}"
pip3 install -U -r requirements.txt

# 𝖨𝗇𝖿𝗂𝗇𝗂𝗍𝖾 𝖫𝗈𝗈𝗉 𝗍𝗈 𝖾𝗇𝗌𝗎𝗋𝖾 𝟤𝟦/𝟩 𝖴𝗉𝗍𝗂𝗆𝖾
echo -e "${GREEN}💎 Launching the Main Engine [main.py]...${NC}"

while true
do
    # 𝖱𝗎𝗇𝗇𝗂𝗇𝗀 𝗍𝗁𝖾 𝖡𝗈𝗍
    python3 main.py
    
    # 𝖨𝖿 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗌𝗍𝗈𝗉𝗌, 𝗐𝖺𝗂𝗍 𝟧 𝗌𝖾𝖼𝗈𝗇𝖽𝗌 𝖺𝗇𝖽 𝗋𝖾𝗌𝗍𝖺𝗋𝗍
    echo -e "${YELLOW}⚠️ Bot engine stopped unexpectedly! Restarting in 5 seconds...${NC}"
    sleep 5
done

