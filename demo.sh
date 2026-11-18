echo "Demo Time!"
# downloads precompiled binaries of cloudflared
curl -L --output cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
#sets execute permission
chmod +x cloudflared
#runs flask app (MAKE SURE VENV IS ENABLED)
echo "starting flask app"
python3 app/serve.py > flask.log 2>&1 & FLASK_PID=$!
#delay
sleep 2
#starting up url thingy
echo "starting cloudflared"
./cloudflared --protocol http2 --url http://localhost:5000 > cloudflare.log 2>&1 & 
CLOUDFLARED_PID=$!
sleep 3
for i in {1..30}; do
    URL=$(grep -aoE 'https://[a-zA-Z0-9.-]+\.trycloudflare\.com' cloudflare.log | head -n 1)
    if [[ -n "$URL" ]]; then
        break
    fi
    sleep 1
done
if [[ -n "$URL" ]]; then
    echo "found url"
    echo "url: " >> url.txt
    echo "$URL" >> url.txt
else
    echo "ERROR: Couldn't find the cloudflare url"
fi


wait $FLASK_PID
wait $CLOUDFLARED_PID