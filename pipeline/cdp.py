# -*- coding: utf-8 -*-
"""Client Chrome DevTools Protocol minimal : WebSocket ecrit a la main (RFC 6455),
   sans dependance externe. Suffisant pour naviguer, evaluer du JS et capturer."""
import json, os, socket, base64, struct, time, urllib.request, subprocess, tempfile

class WS:
    def __init__(self, url, timeout=30):
        assert url.startswith("ws://")
        rest = url[5:]
        hostport, _, path = rest.partition("/")
        host, _, port = hostport.partition(":")
        self.s = socket.create_connection((host, int(port or 80)), timeout=timeout)
        self.s.settimeout(timeout)
        cle = base64.b64encode(os.urandom(16)).decode()
        req = ("GET /%s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\n"
               "Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
               "Sec-WebSocket-Version: 13\r\n\r\n" % (path, hostport, cle))
        self.s.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            d = self.s.recv(4096)
            if not d: raise RuntimeError("handshake ferme")
            buf += d
        if b"101" not in buf.split(b"\r\n")[0]:
            raise RuntimeError("handshake refuse : %r" % buf[:120])
        self.reste = buf.split(b"\r\n\r\n", 1)[1]

    def _lire(self, n):
        while len(self.reste) < n:
            d = self.s.recv(max(65536, n - len(self.reste)))
            if not d: raise RuntimeError("connexion fermee")
            self.reste += d
        out, self.reste = self.reste[:n], self.reste[n:]
        return out

    def envoyer(self, texte):
        charge = texte.encode()
        n = len(charge)
        cadre = bytearray([0x81])
        if n < 126:   cadre.append(0x80 | n)
        elif n < 1 << 16: cadre.append(0x80 | 126); cadre += struct.pack(">H", n)
        else:         cadre.append(0x80 | 127); cadre += struct.pack(">Q", n)
        m = os.urandom(4); cadre += m
        cadre += bytes(b ^ m[i % 4] for i, b in enumerate(charge))
        self.s.sendall(bytes(cadre))

    def recevoir(self):
        morceaux = []
        while True:
            b0, b1 = self._lire(2)
            fin, op = b0 & 0x80, b0 & 0x0F
            n = b1 & 0x7F
            if n == 126:   n = struct.unpack(">H", self._lire(2))[0]
            elif n == 127: n = struct.unpack(">Q", self._lire(8))[0]
            charge = self._lire(n)
            if op == 0x8: raise RuntimeError("le navigateur a ferme la connexion")
            if op == 0x9: continue                      # ping : ignore
            morceaux.append(charge)
            if fin: break
        return b"".join(morceaux).decode("utf-8", "replace")

class Chrome:
    def __init__(self, chemin, port=9222, largeur=852, hauteur=1920):
        self.profil = tempfile.mkdtemp(prefix="cr_")
        self.proc = subprocess.Popen([
            chemin, "--headless=new", "--remote-debugging-port=%d" % port,
            "--user-data-dir=" + self.profil, "--no-first-run", "--no-default-browser-check",
            "--disable-extensions", "--hide-scrollbars", "--mute-audio",
            "--window-size=%d,%d" % (largeur, hauteur), "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ws = None
        for _ in range(60):
            try:
                cibles = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % port, timeout=2))
                pages = [c for c in cibles if c.get("type") == "page"]
                if pages: ws = pages[0]["webSocketDebuggerUrl"]; break
            except Exception: pass
            time.sleep(0.5)
        if not ws: raise RuntimeError("Chrome n'a pas ouvert son port de debogage")
        self.ws = WS(ws); self.n = 0

    def cmd(self, methode, **params):
        self.n += 1
        self.ws.envoyer(json.dumps({"id": self.n, "method": methode, "params": params}))
        while True:
            r = json.loads(self.ws.recevoir())
            if r.get("id") == self.n:
                if "error" in r: raise RuntimeError("%s : %s" % (methode, r["error"]))
                return r.get("result", {})

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if r.get("exceptionDetails"):
            raise RuntimeError("JS : %s" % r["exceptionDetails"].get("text"))
        return r["result"].get("value")

    def capture(self, chemin):
        r = self.cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
        open(chemin, "wb").write(base64.b64decode(r["data"]))

    def fermer(self):
        try: self.proc.terminate()
        except Exception: pass
