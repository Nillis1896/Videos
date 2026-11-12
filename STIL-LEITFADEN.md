# Stil-Leitfaden: Mitmach-Serien für TikTok

Dieser Leitfaden beschreibt den Stil und die Technik, die wir für die Serie **„Gestrandet“** (Ordner `gestrandet/`) entwickelt haben. Neue Accounts und Serien sollen genauso aufgebaut sein.

## 1. Format (was auf TikTok funktioniert)
- **Mitmach-Serie in Tagen:** Tag 1, Tag 2, Tag 3 … Jede Folge ist ein Tag.
- **Regel des Formats:** „Jeder Follower wird ein …“ (Überlebender, Ork, Crewmitglied …). Follower tauchen später namentlich auf.
- **Länge:** 20–28 Sekunden. Längere Folgen (38 s) wurden kaum zu Ende geschaut.
- **Action im ersten Bild:** Kein Logo, kein ruhiger Einstieg. Erstes Bild = Witz oder Gefahr.
- **Ein Ereignis pro Folge, eine Frage am Ende:** „A oder B? Schreib's in die Kommentare!“
- **Running Gag / Maskottchen:** z. B. Harry der Fußball. Wiederkehrend, kommentierbar.
- **Follow-Aufruf als Witz**, nicht als Betteln („sonst bin ich morgen allein mit Harry“).
- **Follower-Ziel** mit Fortschrittsbalken („Bei 500 Followern …“).
- **Kommentare einbauen:** Ideen und Namen aus den Kommentaren in die nächste Folge nehmen und die Leute nennen.
- **Keine fremden Marken/Figuren** (Herr der Ringe, Vereinswappen usw.) – eigene Figuren verwenden.

## 2. Aufbau eines Videos (Beispiel Gestrandet Tag 1)
| Teil | Inhalt |
|---|---|
| 0–3 s | Hook: Figur wird an den Strand gespült, Witz („Ich hab 'ne Kreuzfahrt gewonnen.“) |
| 3–10 s | Welt zeigen: Luftaufnahme, Schild „TAG 1“, Schatzkarte |
| 10–14 s | Inventar wie im Videospiel, Maskottchen vorstellen |
| 14–19 s | Regel + Follow-Animation, Leiste oben (HUD) erscheint |
| 19–22 s | Gefahr (Sturm), Kamera wackelt, Blitz |
| 22–28 s | Zwei Karten A/B, Follow-Witz, Frage an die Kommentare |

## 3. Look
- **3D-Welt mit Three.js** (Version 0.160.0): große Welt aus einer Höhenfunktion, echtes Wasser (`Water`), Himmel (`Sky`), Schatten, Bloom.
- **Figuren:** kostenlose CC0-Modelle (KayKit Adventurers, `KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0` auf GitHub) mit 76 Animationen (Lie_StandUp, PickUp, Cheer …). Proportionen per Knochen-Skalierung anpassbar, Kleidung per Shader umfärbbar.
- **Tiere:** three.js-Beispielmodelle (Parrot, Flamingo, Stork) über raw.githubusercontent.com.
- **Einblendungen mit GSAP 3.12.5:** Holzschild, Inventar-Panel, Schatzkarte, Karten A/B, HUD-Pillen oben.
- **Untertitel:** Wort für Wort (1–3 Wörter), Schrift **Lilita One**, weiß mit dunkler Kontur, Schlüsselwörter gelb (positiv) oder rot (Gefahr). Position etwa auf Brusthöhe, oberhalb des TikTok-Bereichs unten.
- **TikTok-Safe-Zone:** nichts Wichtiges in den oberen 170 px, keine Texte unter ~1330 px, rechts Platz für die Knopfleiste lassen.

## 4. Ton
- **Stimme:** ElevenLabs, Modell `eleven_v4`, mit Ausdrucks-Tags wie `[coughing]`, `[deadpan]`, `[nervous]`, `[whispers]`. Endpoint `with-timestamps` liefert Wortzeiten für die Untertitel. Tempo-Einstellung wird von v4 ignoriert → mit ffmpeg `atempo` beschleunigen (≈1.2–1.3) und Wortzeiten entsprechend umrechnen.
- Gestrandet nutzt die Stimme **Kalle** (rau, energiegeladen).
- **Musik:** ElevenLabs Music API (instrumental, passend zum Thema), mit `dynaudnorm`/`loudnorm` ausgleichen und unter der Stimme per Sidechain absenken.
- **Soundeffekte:** ElevenLabs Sound Generation, alle auf gleiche Lautheit normalisiert.

## 5. Arbeitsweise
1. **Skript schreiben** und vom Nutzer freigeben lassen.
2. **Stimme erzeugen**, Wortzeiten speichern.
3. **Live-Vorschau als HTML-Artifact bauen:** eine Seite 1080×1920, skaliert, Player mit Play/Pause/Zeitleiste. Alles hängt an einer Zeit `t`: `renderAt(t)` setzt Kamera/Figuren, eine pausierte GSAP-Timeline wird mit `tl.seek(t)` gesetzt. Audio: `audio.currentTime` = `t`.
4. Vorschau mit Playwright (headless Chromium, swiftshader) testen, Standbilder prüfen.
5. **Artifact veröffentlichen.** `.glb`-Modelle als `.bin` mit contentType `application/wasm` hochladen.
6. **Rendern:** Seite Bild für Bild (30 fps) per Playwright screenshotten, mit ffmpeg + Tonspur zu MP4 (H.264, 1080×1920).
7. **Branding:** Caption, Abstimmungs-Kommentar (max. 150 Zeichen), Thumbnail (clean: großer Titel, Figur vorne, Welt dahinter).

## 6. Projektstruktur (Beispiel)
```
gestrandet/
  tag1/            Skript, Stimme, Wortzeiten
  audio/           Musik + Effekte (norm/ = normalisiert)
  vorschau-tag1/   template.html, build.py, index.html, render.html, assets/
branding/          Thumbnails und Texte
```
Gemeinsame Werkzeuge (Testskripte, Font-Paket, three/gsap lokal) liegen nur im Scratchpad und müssen in einer neuen Sitzung neu angelegt werden (npm: `three@0.160.0`, `gsap@3.12.5`, `@fontsource/*`).
