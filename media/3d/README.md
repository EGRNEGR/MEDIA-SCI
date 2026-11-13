# media/3d — условное 3D-платье для лонгрида

Все файлы каталога созданы командой кодом, без нейросетей-генераторов изображений и без чужих 3D-моделей. Платье — стилизация по описанию Iridescence в источниках [8; 9] (полупрозрачное голографическое платье-комбинезон). Это **не** модель The Fabricant, и на лендинге это подписывается.

| Файл | Что это | Как получен |
|---|---|---|
| `iridescence-viewer/index.html` | Интерактивная 3D-сцена для GitHub Pages | Код на Three.js 0.170 (MIT), подключается с CDN jsDelivr. Силуэт — поверхность вращения по профилю из 10 точек, складки и шлейф считаются синусоидами, материал — `MeshPhysicalMaterial` с iridescence |
| `turntable/turntable_00.jpg` … `turntable_11.jpg` | 12 кадров оборота по 30°, 960×1200, фон `#0B0D10` | Режим `?frame=N&frames=12&format=jpeg` той же сцены, рендер в Microsoft Edge, сохранение через `tools/frame_server.py` |
| `loop/iridescence_turntable.gif` | Зацикленный оборот, 48 кадров по 7,5°, 400×500 | Кадры 480×600 из того же режима, сборка в GIF через Pillow (96 цветов) |
| `twist/twist_strip_1.jpg` … `_6.jpg` | Кадр 0, разрезанный на 6 горизонтальных полос 960×200 | Pillow, для эффекта «перекрута» (рецепт R6 в мануале) |
| `hud/dial_ring.png`, `hud/dial_needle.png` | Шкала и стрелка компаса 240×240 с прозрачностью | Pillow, шрифт Consolas для подписей шкалы |
| `tools/frame_server.py` | Локальный сервер: раздаёт сцену и сохраняет присланные кадры | asyncio, только стандартная библиотека Python |

Условия использования: код и изображения — работа команды, их можно свободно использовать в проекте. Three.js распространяется по лицензии MIT.

Как собрать лонгрид с этими файлами: [`docs/tilda/zero_block_longread_manual.md`](../../docs/tilda/zero_block_longread_manual.md).

## Пересборка кадров

```bash
python media/3d/tools/frame_server.py --out media/3d/turntable --port 8791
```

Откройте `http://127.0.0.1:8791/iridescence-viewer/index.html?frame=0&frames=12&format=jpeg` в браузере с размером окна 960×1200 и выполните в консоли:

```js
for (let i = 0; i < 12; i++) {
  const url = window.__renderFrame(i);
  await fetch(`/save/turntable_${String(i).padStart(2, '0')}.jpg`, { method: 'POST', body: url });
}
```
