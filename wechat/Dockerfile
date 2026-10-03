FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb scrot xdotool x11-utils \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 \
    wget ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Download and install official Tencent WeChat for Linux (ARM64)
RUN wget -q "https://dldir1v6.qq.com/weixin/Universal/Linux/WeChatLinux_arm64.deb" -O /tmp/wechat.deb \
    && apt-get update \
    && apt-get install -y /tmp/wechat.deb \
    && rm /tmp/wechat.deb \
    && ls -la /opt/wechat/wechat || (echo "WECHAT NOT FOUND"; exit 1)

ENV WECHAT_HOME=/data/wechat-home
RUN mkdir -p $WECHAT_HOME /data/shots

COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
