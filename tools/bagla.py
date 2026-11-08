# -*- coding: utf-8 -*-
"""Avrasya2 Baglama ve Derleme Araci (tools/bagla.py).

Oyunun kendi python27.dll kutuphanesini (tools/bin/py27c.exe uzerinden)
kullanarak source/sitecustomize.py dosyasini derler ve:
  1. Kullanici bazli (%APPDATA%\\Python\\Python27\\site-packages\\sitecustomize.pyc)
     konumuna Yonetici izni gerektirmeden ve oyun klasorune hic dokunmadan kurar.
  2. Istenirse lib/sitecustomize.pyc konumuna da yedekli kurabilir veya kaldirir.

Kullanim:
    python tools/bagla.py durum
    python tools/bagla.py kur
    python tools/bagla.py kaldir
    python tools/bagla.py derle
"""

import hashlib
import os
import shutil
import subprocess
import sys
import time

PROJECT_ROOT = r"C:\Users\erenk\Desktop\Avrasya2"
CLIENT_DIR = r"C:\Program Files (x86)\Avrasya2"
SOURCE_DIR = os.path.join(PROJECT_ROOT, "source")
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
BIN_DIR = os.path.join(TOOLS_DIR, "bin")
BACKUP_DIR = os.path.join(PROJECT_ROOT, "yedek")

SRC_SITECUSTOMIZE = os.path.join(SOURCE_DIR, "sitecustomize.py")
BUILT_PYC = os.path.join(BIN_DIR, "sitecustomize.pyc")
PY27C_EXE = os.path.join(BIN_DIR, "py27c.exe")
PY27C_CS = os.path.join(BIN_DIR, "py27c.cs")
CSC_EXE = r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"

APPDATA_DIR = os.environ.get("APPDATA", os.path.expanduser(r"~\AppData\Roaming"))
USER_SITE_DIR = os.path.join(APPDATA_DIR, "Python", "Python27", "site-packages")
USER_SITECUSTOMIZE_PYC = os.path.join(USER_SITE_DIR, "sitecustomize.pyc")
USER_USERCUSTOMIZE_PYC = os.path.join(USER_SITE_DIR, "usercustomize.pyc")

TARGET_PYC = os.path.join(CLIENT_DIR, "lib", "sitecustomize.pyc")
PY27_MAGIC = bytes.fromhex("03f30d0a")


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def check_ascii():
    """Oyun icinde calisacak Python 2.7 dosyalarinda >127 bayt kontrolu yapar."""
    files = []
    for root_dir in (SOURCE_DIR,):
        for r, _dirs, fnames in os.walk(root_dir):
            for fn in fnames:
                if fn.endswith(".py"):
                    files.append(os.path.join(r, fn))
    kesif = os.path.join(TOOLS_DIR, "oyun_ici_kesif.py")
    if os.path.isfile(kesif):
        files.append(kesif)

    bad = []
    for p in files:
        with open(p, "rb") as f:
            data = f.read()
        for idx, b in enumerate(data):
            if b > 127:
                line_no = data[:idx].count(b"\n") + 1
                bad.append((p, line_no, hex(b)))
                break
    if bad:
        for p, ln, bval in bad:
            print("HATA: ASCII disi karakter: %s satir %d (%s)" % (p, ln, bval))
        raise SystemExit(1)
    print("ASCII kontrolu temiz (%d dosya)." % len(files))


def ensure_py27c():
    if os.path.isfile(PY27C_EXE) and os.path.getmtime(PY27C_EXE) >= os.path.getmtime(PY27C_CS):
        return
    if not os.path.isfile(CSC_EXE):
        raise SystemExit("HATA: 32-bit csc.exe bulunamadi: %s" % CSC_EXE)
    subprocess.check_call([CSC_EXE, "/nologo", "/platform:x86", "/out:" + PY27C_EXE, PY27C_CS])


def compile_sitecustomize():
    check_ascii()
    ensure_py27c()
    if os.path.exists(BUILT_PYC):
        os.remove(BUILT_PYC)
    rc = subprocess.call([PY27C_EXE, CLIENT_DIR, SRC_SITECUSTOMIZE, BUILT_PYC])
    if rc != 0 or not os.path.isfile(BUILT_PYC):
        raise SystemExit("HATA: sitecustomize.py derlenemedi (kod=%d)" % rc)
    with open(BUILT_PYC, "rb") as f:
        magic = f.read(4)
    if magic != PY27_MAGIC:
        raise SystemExit("HATA: gecersiz .pyc magic: %s" % magic.hex())
    print("Derlendi: %s (magic=%s, md5=%s)" % (BUILT_PYC, magic.hex(), md5(BUILT_PYC)))


def cmd_durum():
    print("Istemci dizini      : %s" % CLIENT_DIR)
    print("User-Site hedefi    : %s" % USER_SITECUSTOMIZE_PYC)
    if os.path.isfile(USER_SITECUSTOMIZE_PYC):
        print("User-Site durumu    : KURULU (md5=%s)" % md5(USER_SITECUSTOMIZE_PYC))
    else:
        print("User-Site durumu    : KURULU DEGIL")
    print("Istemci lib hedefi  : %s" % TARGET_PYC)
    if os.path.isfile(TARGET_PYC):
        print("Istemci lib durumu  : KURULU (md5=%s)" % md5(TARGET_PYC))
    else:
        print("Istemci lib durumu  : TEMIZ (oyun klasorune dokunulmadi)")


def cmd_kur():
    compile_sitecustomize()
    if not os.path.isdir(USER_SITE_DIR):
        os.makedirs(USER_SITE_DIR)
    shutil.copy2(BUILT_PYC, USER_SITECUSTOMIZE_PYC)
    if os.path.isfile(USER_USERCUSTOMIZE_PYC):
        try:
            os.remove(USER_USERCUSTOMIZE_PYC)
        except Exception:
            pass
    print("Kuruldu (User-Site, Yonetici izinsiz & Oyun klasoru %100 temiz):")
    print("  -> %s (md5=%s)" % (USER_SITECUSTOMIZE_PYC, md5(USER_SITECUSTOMIZE_PYC)))


def cmd_kaldir():
    for p in (USER_SITECUSTOMIZE_PYC, USER_USERCUSTOMIZE_PYC, TARGET_PYC):
        if os.path.isfile(p):
            try:
                os.remove(p)
                print("Kaldirildi: %s" % p)
            except PermissionError:
                print("UYARI: %s kaldirmak icin Yonetici izni gerekiyor." % p)


def cmd_test():
    ensure_py27c()
    rc = subprocess.call([PY27C_EXE, CLIENT_DIR, "--sim"])
    if rc != 0:
        raise SystemExit("HATA: Oyun system.py simulasyonu basarisiz (kod=%d)" % rc)


def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "durum"
    if cmd == "durum":
        cmd_durum()
    elif cmd == "kur":
        cmd_kur()
    elif cmd in ("kaldir", "geri_al"):
        cmd_kaldir()
    elif cmd == "derle":
        compile_sitecustomize()
    elif cmd == "test":
        cmd_test()
    else:
        raise SystemExit("Kullanim: python tools/bagla.py [durum|kur|kaldir|derle|test]")


if __name__ == "__main__":
    main()
