#!/bin/sh
# Start (or restart) the local PHP dev server on port 8081. Usage: tools/test/serve.sh
DIR=$(cd "$(dirname "$0")/../.." && pwd)
PIDF=/tmp/mpa-php-server.pid
[ -f "$PIDF" ] && kill "$(cat $PIDF)" 2>/dev/null
sleep 0.3
cd "$DIR/site" && nohup php -S 127.0.0.1:8081 -t . "$DIR/tools/test/router.php" > /tmp/mpa-php-server.log 2>&1 &
echo $! > "$PIDF"
sleep 0.8
echo "serving http://127.0.0.1:8081"
