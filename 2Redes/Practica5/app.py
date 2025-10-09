from flask import Flask, jsonify
import psutil, time, logging
import threading, os, requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
def flood():
    app.logger.info("Flood thread iniciado: generando tráfico hacia speed.hetzner.de")
    while True:
        try:
            r = requests.get("https://speed.hetzner.de/10MB.bin", stream=True, timeout=5)
            for _ in r.iter_content(chunk_size=64 * 1024):
                pass
            app.logger.info("Descarga completada (100MB). Reintentando...")
        except Exception as e:
            app.logger.debug(f"Error en flood: {e}")
            time.sleep(1)

if os.getenv("ENABLE_FLOOD", "0") in ("1", "true", "True"):
    t = threading.Thread(target=flood, daemon=True)
    t.start()
    app.logger.info("Flood thread solicitado por ENABLE_FLOOD=1")
else:
    app.logger.info("Flood thread deshabilitado (poner ENABLE_FLOOD=1 para activarlo)")

@app.get("/")
def health():
    return "OK", 200

@app.get("/net")
def net_stats():
    io1 = psutil.net_io_counters()
    time.sleep(1)
    io2 = psutil.net_io_counters()

    sent_kBps = (io2.bytes_sent - io1.bytes_sent) / 1024
    recv_kBps = (io2.bytes_recv - io1.bytes_recv) / 1024

    payload = {
        "upload_kBps": round(sent_kBps, 2),
        "download_kBps": round(recv_kBps, 2),
    }
    app.logger.info(payload)
    return jsonify(payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
