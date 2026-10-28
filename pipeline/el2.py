# -*- coding: utf-8 -*-
import env
import json, urllib.request, urllib.error
KEY = open(env.CLE_TTS, encoding="utf-8").read().strip()
def say(text, voice_id, out, model="eleven_multilingual_v2", stab=0.75, sim=0.8, style=0.0, lang=None):
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": stab, "similarity_boost": sim,
                               "style": style, "use_speaker_boost": True}}
    if lang: body["language_code"] = lang
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/text-to-speech/%s?output_format=mp3_44100_128" % voice_id,
        data=json.dumps(body).encode(),
        headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            open(out, "wb").write(r.read())
        return True, len(text)
    except urllib.error.HTTPError as e:
        return False, e.read().decode(errors="replace")[:160]
