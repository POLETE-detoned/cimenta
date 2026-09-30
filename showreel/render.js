// Renderiza showreel.html fotograma a fotograma y lo codifica con ffmpeg.
// Uso: node render.js <salida.mp4> [fps] [desde_s] [hasta_s]   |   node render.js --stills t1,t2,...
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
const FF = process.env.FFMPEG;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(__dirname, 'showreel.html'));
  await page.evaluate(() => window.ready);
  if (process.argv[2] === '--stills') {
    require('fs').mkdirSync(path.resolve(__dirname, 'stills'), { recursive: true });
    for (const t of process.argv[3].split(',').map(Number)) {
      await page.evaluate(t => render(t), t);
      await page.screenshot({ path: `${__dirname}/stills/t${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 80 });
    }
    await browser.close(); return;
  }
  const out = process.argv[2], fps = +(process.argv[3] || 30);
  const t0 = +(process.argv[4] || 0), t1 = +(process.argv[5] || 58);
  const ff = spawn(FF, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round((t1 - t0) * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => render(t), t0 + i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
