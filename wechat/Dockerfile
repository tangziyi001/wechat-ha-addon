FROM debian:12-slim

# Cache buster: 1791034773.2308254
RUN echo "build 1791034773.2308383"

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb scrot xdotool x11-utils python3 \
    libatomic1 \
    libwayland-client0 libwayland-egl1 \
    libegl1 libgl1 libopengl0 \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 \
    libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 \
    wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.deb" -O /tmp/wechat.deb \
    && apt-get update \
    && apt-get install -y /tmp/wechat.deb \
    && rm /tmp/wechat.deb \
    && ls -la /opt/wechat/wechat

COPY patch_wechat.py /tmp/patch_wechat.py
RUN python3 /tmp/patch_wechat.py /opt/wechat/wechat \
    && python3 -c "import sys; d=open('/opt/wechat/wechat','rb').read(); o=135545057; print('VERIFY:', d[o:o+8].hex())" \
    && rm /tmp/patch_wechat.py

ENV WECHAT_HOME=/data/wechat-home
ENV QT_QPA_PLATFORM=xcb
RUN mkdir -p $WECHAT_HOME /data/shots

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
