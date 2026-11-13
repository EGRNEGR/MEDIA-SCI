"""Локальный сервер для экспорта кадров турникета из iridescence-viewer.

Отдаёт статические файлы каталога media/3d и принимает кадры:
POST /save/<имя_файла> с телом в виде data URL (image/png или image/jpeg).

Запуск:  python media/3d/tools/frame_server.py --out media/3d/turntable
Затем в браузере (окно 960×1200) откройте
http://127.0.0.1:8791/iridescence-viewer/index.html?frame=0&frames=12&format=jpeg
и выполните в консоли (12 кадров по 30°):

    for (let i = 0; i < 12; i++) {
      const url = window.__renderFrame(i);
      await fetch(`/save/turntable_${String(i).padStart(2, '0')}.jpg`, {method: 'POST', body: url});
    }
"""

import argparse
import asyncio
import base64
import mimetypes
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SAFE_NAME = re.compile(r"^[\w.-]+\.(png|jpe?g)$")


async def respond(writer: asyncio.StreamWriter, status: str, body: bytes, content_type: str = "text/plain; charset=utf-8") -> None:
    head = (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Cache-Control: no-store\r\n"
        "Connection: close\r\n\r\n"
    )
    writer.write(head.encode("ascii") + body)
    await writer.drain()


async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, out_dir: Path) -> None:
    try:
        request_line = (await reader.readline()).decode("latin-1").strip()
        if not request_line:
            return
        method, target, _ = request_line.split(" ", 2)
        headers = {}
        while (line := (await reader.readline()).decode("latin-1").strip()):
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()
        path = unquote(urlsplit(target).path)

        if method == "POST" and path.startswith("/save/"):
            name = path.removeprefix("/save/")
            if not SAFE_NAME.match(name):
                await respond(writer, "400 Bad Request", b"bad file name")
                return
            body = await reader.readexactly(int(headers.get("content-length", "0")))
            _, _, encoded = body.decode("ascii").partition("base64,")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / name).write_bytes(base64.b64decode(encoded))
            print(f"saved {name}")
            await respond(writer, "200 OK", b"ok")
            return

        if method == "GET":
            file = (ROOT / path.lstrip("/")).resolve()
            if file.is_dir():
                file = file / "index.html"
            if ROOT not in file.parents or not file.is_file():
                await respond(writer, "404 Not Found", b"not found")
                return
            content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
            await respond(writer, "200 OK", file.read_bytes(), content_type)
            return

        await respond(writer, "405 Method Not Allowed", b"method not allowed")
    finally:
        writer.close()


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=ROOT / "turntable", help="куда сохранять кадры")
    parser.add_argument("--port", type=int, default=8791)
    args = parser.parse_args()
    out_dir = args.out.resolve()
    server = await asyncio.start_server(lambda r, w: handle(r, w, out_dir), "127.0.0.1", args.port)
    print(f"serving {ROOT} on http://127.0.0.1:{args.port}/ , frames -> {out_dir}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
