#!/bin/bash
set -e

DISPLAY_NUM="${DISPLAY_NUM:-:99}"
SCREEN="${SCREEN:-1366x768x24}"
WECHAT_HOME="${WECHAT_HOME:-/data/wechat-home}"

mkdir -p "$WECHAT_HOME" /data/shots

echo "[wechat] Starting Xvfb on $DISPLAY_NUM ($SCREEN)"
Xvfb $DISPLAY_NUM -screen 0 $SCREEN &
XVFB_PID=$!
export DISPLAY=$DISPLAY_NUM
sleep 2

# Fake crashpad handler to avoid /proc issues (from chroot lesson)
if [ -f /opt/wechat/crashpad_handler ]; then
    mv /opt/wechat/crashpad_handler /opt/wechat/crashpad_handler.real
    echo -e '#!/bin/sh\nwhile true; do sleep 3600; done' > /opt/wechat/crashpad_handler
    chmod +x /opt/wechat/crashpad_handler
    echo "[wechat] Installed fake crashpad handler"
fi

echo "[wechat] Starting WeChat (HOME=$WECHAT_HOME)"
export HOME="$WECHAT_HOME"
export QT_QPA_PLATFORM=xcb
export QT_XCB_GL_INTEGRATION=xcb_egl
export LIBGL_ALWAYS_SOFTWARE=1

cd /opt/wechat
LD_LIBRARY_PATH=/opt/wechat /opt/wechat/wechat &
WECHAT_PID=$!
echo "[wechat] WeChat PID=$WECHAT_PID, Xvfb PID=$XVFB_PID"

# Keep container alive, restart WeChat if it crashes
while true; do
    if ! kill -0 $WECHAT_PID 2>/dev/null; then
        echo "[wechat] WeChat died, restarting in 5s..."
        sleep 5
        LD_LIBRARY_PATH=/opt/wechat /opt/wechat/wechat &
        WECHAT_PID=$!
        echo "[wechat] WeChat restarted PID=$WECHAT_PID"
    fi
    sleep 10
done
