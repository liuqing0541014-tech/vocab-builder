#!/bin/bash
cd "$(dirname "$0")"
echo "正在启动生词本..."
python3 -m http.server 8080 > /dev/null 2>&1 &
if [ $? -ne 0 ]; then
    python -m http.server 8080 > /dev/null 2>&1 &
fi
sleep 2
open http://localhost:8080
echo "已打开浏览器"
