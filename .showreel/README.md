# Showreel Cimenta · inversores

Vídeo motion design de 58 s (1920×1080, 30 fps, H.264 + AAC) que explica Cimenta en clave de
venta a inversores. Resultado: `Cimenta-Showreel-Inversores.mp4`.

## Guion

| Tiempo | Escena | Mensaje |
|---|---|---|
| 0–5 s | Gancho | «Comparar ofertas de obra sigue siendo un ejercicio de fe.» |
| 5–11 s | Problema | Tres constructoras, tres mediciones distintas del mismo hormigón. Nada compara con nada. |
| 11–15 s | Marca | CIMENTA · Marketplace B2B de licitación privada de obra. |
| 15–20 s | La idea | Una sola medición, la del promotor (.BC3 congelado). La constructora solo pone precio y marca. |
| 20–44 s | Cómo funciona | 01 Publica · 02 Cupo cerrado (3–5 plazas, fee 500 € reembolsable) · 03 Oferta partida a partida · 04 Matriz, baja temeraria y contrato eIDAS · 05 Ejecución (roadmap) |
| 44–49 s | Negocio | Comisión de intermediación · fee de acceso · servicios de ejecución (roadmap). |
| 49–54 s | Producto | Grabación real de la beta + 4 vistas, 42 tests, RLS. |
| 54–58 s | Cierre | «Una medición. Todas las ofertas, comparables.» · Buscamos inversores para el piloto. |

Los datos salen del repositorio: expediente «Edificio plurifamiliar 12 viviendas» (Torrevieja,
1.480.000 €, 1.190 m², 1.244 €/m², 20 meses), las cuatro constructoras del seed, la baja del
22,8 % sobre la media y los 16 + 26 tests de `bc3` y `pricing`. Las cifras de ofertas y
certificaciones son ilustrativas y cuadran entre sí (p. ej. 1.417.840 € = −4,2 % sobre el PBL;
fianza 5 % = 70.892 €).

## Cómo regenerarlo

Todo es determinista: `showreel.html` expone `render(t)` y cada fotograma se captura con
Playwright; la música se sintetiza en `synth.py` (original, sin licencias de terceros).

```bash
./extract-clips.sh                          # fragmentos reales de ../set05.mp4
python3 synth.py                            # music.wav (requiere numpy)
FFMPEG=ffmpeg node render.js video_noaudio.mp4 30 0 58
ffmpeg -i video_noaudio.mp4 -i music.wav -c:v copy \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:a aac -b:a 192k -shortest \
  -movflags +faststart Cimenta-Showreel-Inversores.mp4
```

`render.js` importa Playwright desde la instalación global de Node; ajusta la ruta del
`require` si en tu máquina está en otro sitio. Para revisar fotogramas sueltos:
`node render.js --stills 12,30,50` (los deja en `stills/`).
