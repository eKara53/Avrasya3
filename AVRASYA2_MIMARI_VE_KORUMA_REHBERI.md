# Avrasya2 — REA Derin Binary Analizi, FoxFS/Proto Cozumu, Anti-Cheat Mimarisi ve Yaratici Yetenek Haritasi (v3.0)

Bu dokuman, `C:\Program Files (x86)\Avrasya2\metin2client.bin`, `rascal.dll`, `pack/root` ve `pack/locale` uzerinde **REA (`rea-mcp`)**, **Capstone x86 Disassembler**, **PEfile** ve **FoxFS/MCOZ Kriptanalizi** ile yapilan derinlemesine statik/dinamik tersine muhendislik analizinin bulgularini, **Rascal + VMProtect (`.rdataa0`)** koruma katmanlarinin nasil calistigini ve `source/main.py` (v3.0) icinde gelistirdigimiz **6 yaratici ozelligin** bu korumalara karsi nasil %100 uyumlu/gorunmez kaldigini detaylandirir.

---

## 1. Binary, Pack ve Veri Yapisi (`metin2client.bin`, `rascal.dll`, `FoxFS`, `mob_proto`)

### 1.1 `metin2client.bin` (Ana Oyun Istemcisi)
- **Mimari:** PE32 (x86, 32-bit), ImageBase: `0x00400000`, EntryPoint: `0x006de378`
- **Bolumler (Sections):**
  - `.text` (`0x00401000` – `0x008956e4`, 4.80 MB, Entropi: `6.57`): Ana C++ oyun motoru, FoxFS (`0x00735530`), CryptoPP (`0x007b48f0`), LZ4 (`0x00738ad0`), LZO1X ve gomulu **Python 2.7 (2.7.3)** C API baglantilari (`0x00684000`–`0x006d0000`).
  - `.rdata` (`0x00896000` – `0x0098db82`, 1.01 MB, Entropi: `6.14`): Sabit stringler, C++ sanal metod tablolari (vtable) ve 37 modulun metod tablolari (`PyMethodDef`).
  - `.data` (`0x0098e000` – `0x00a4c4c0`, 779 KB, Entropi: `3.46`): Global C++ singleton isaretcileri ve XTEA anahtarlari (`0x00990f50`).
  - `.rdataa0` (`0x00a4e000` – `0x00d41820`, 3.09 MB, Entropi: `7.75`, **Executable**): **VMProtect** ile sanallastirilmis (virtualized/mutated) koruma bolumu.

### 1.2 `rascal.dll` (Anti-Cheat Modulu)
- **Mimari:** PE32 (x86, 32-bit), ImageBase: `0x10000000`, Boyut: `27.97 MB`, Entropi: `7.938` (yogun paketlenmis/sanallastirilmis).
- **Disa Aktarilan (Export) Fonksiyonlar (11 Adet):**
  1. `InitializeRascal` (`RVA 0xbd4c0`, Ord 5) — Anti-cheat baslaticisi.
  2. `FunctionProtect` (`RVA 0xb7fa0`, Ord 1) — Kritik fonksiyonlarin `.text` giris baytlarini (`0xE9` JMP, `0xFF` CALL, `0xCC` INT3) tarayarak inline hook/patch tespiti yapar.
  3. `RascalCallback` (`RVA 0xb8290`, Ord 6) — Oyun motoru olaylarini ve tespit bildirimlerini isler.
  4. `RascalProtectRTypes` (`RVA 0xb83e0`, Ord 7) — Bellek/veri tipi koruma kaydi.
  5. `GetRascalThreadID` (`RVA 0xb8080`, Ord 4) — Koruma ve ana thread dogrulamasi.
  6. `RascalSessionRespond` (`RVA 0x36720`, Ord 8) & `RascalSessionRespondEx` (`RVA 0x366f0`, Ord 9) — Sunucu heartbeat / oturum dogrulama yaniti.
  7. `GetClientCount` (`RVA 0xba400`, Ord 2) — Acik istemci sayisi kontrolu.
  8. `GetDiscordName` (`RVA 0xba4f0`, Ord 3) — Discord RPC / kullanici adi entegrasyonu.
  9. `WLog` (`RVA 0xb80d0`, Ord 10) — Tespit loglama.
  10. `getunknown` (`RVA 0xb81b0`, Ord 11) — Dahili durum sorgusu.

### 1.3 `FoxFS` Pack Arsivlerinin (`pack/root` & `pack/locale`) Kriptanalizi ve Cozumu
Disassembly analizimiz (`FoxFS::load` @ `0x00735530`, `Archive::load` @ `0x00737b90`, `Archive::get` @ `0x00737770`, `RegisterPack` @ `0x005d04e0`), Avrasya2'nin tum pack dosyalarini `key=NULL, iv=NULL` ile kaydettigini ortaya cikarmistir:
- **68 Baytlik (`0x44`) FoxFS Basligi:**
  - `hdr[0:4]`: Magic (`0x000FEAF0`)
  - `hdr[4:36]`: **32-bayt AES-256 Anahtari** (dogrudan baslik icinde!)
  - `hdr[36:52]`: **16-bayt AES-CFB-128 IV** (dogrudan baslik icinde!)
- **32 Baytlik (`0x20`) Blok Girisi (AES-256-CFB ile sifreli):**
  - `(crc32_name, offset, size_compressed, size_uncompressed, crc32_data, flags)`
- **Veri Blogu Cozumu:** `AES-256-CFB-128` de-sifreleme (`0x00736650`) + `LZ4` blok acma (`0x00738ad0`).
- **Cikarilan Dosyalar:**
  - `pack/root`: **367 dosya** (**214 `.py` oyun betigi**) -> `analiz_ciktilari/pack_unpacked/root/`
  - `pack/locale`: **469 dosya** -> `analiz_ciktilari/pack_unpacked/locale/`

### 1.4 `locale__tr__mob_proto` (`MMPT` / `MCOZ`) Cozumu ve VNUM Veritabani
`CPythonNonPlayer::LoadNonPlayerData` (`0x004e92b0`) disassembly analiziyle:
- **XTEA Anahtari (`VA 0x00990f50`):** `(0x00497446, 0x00004A0B, 0x00086EB7, 0x0068189D)`
- **Kayit Boyutu (Stride):** `255` bayt (`0xFF`)
- **Sonuc:** Toplam **2.180 canavar/metin/boss/NPC kaydi** cozulerek `analiz_ciktilari/canavar_vnum.tsv` dosyasina ve **tum esya kayitlari** `analiz_ciktilari/esya_vnum.tsv` dosyasina aktarilmistir:
  - **150 Ozel Metin Tasi VNUM'u:** `2900..2908`, `4000..4005`, `4141..4144`, `6118`, `6209`, `6422`, `7107..7112`, `8001..8209`, `20399..20706` (Lv.5'ten Lv.120'ye kadar + Katakomb, Zodyak, Meley, Hidra, Çöl, Büyülü Orman taşları).
  - **221 Boss / Patron VNUM'u (`bRank >= 4`).**

---

## 2. Anti-Cheat Tespiti & Korumali Mimari Kurallarimiz

REA ve Capstone analizimiz, Avrasya2 istemcisinde **6 farkli koruma ve bot-engelleme katmani** bulundugunu ortaya cikarmistir:

### Katman 1: `.text` Fonksiyon Giris Butunlugu (`FunctionProtect`) & Zero-Admin User-Site Enjeksiyonu
- **Nasil Calisir:** `rascal.dll!FunctionProtect`, `.text` bolumundeki C++ fonksiyonlarinin ilk baytlarinda degisiklik (`0xE9` JMP hook, `0xCC` breakpoint vb.) ve oyun klasorundeki (`C:\Program Files (x86)\Avrasya2`) yabanci DLL/dosyalari denetler.
- **Korumamiz:**
  1. `.text` bolumune **tek bir bayt bile yazilmaz** (Zero-Patch).
  2. Oyun klasorune (`C:\Program Files (x86)\Avrasya2\lib`) **hicbir dosya yazilmaz**.
  3. Gomulu `lib/site.pyc` icindeki `ENABLE_USER_SITE = True` mekanizmasi kullanilarak `%APPDATA%\Python\Python27\site-packages\sitecustomize.pyc` uzerinden **Yonetici (Admin) izni gerektirmeden** ve oyun klasorunu %100 orijinal tutarak yuklenir (`python tools/bagla.py kur`).

### Katman 2: `.rdataa0` (VMProtect) Tuzak Fonksiyonlari (5 Yasakli Fonksiyon)
Toplam **1.291 Python C fonksiyonu** taranmis ve `.rdataa0` (VMProtect) tuzagina dusen **5 fonksiyon** tespit edilerek `SafeEngineAPI.BLOCKED_CALLS` listesine alinmistir:
1. `chr.IsEnemy` (`0x004b78b0` -> `jmp 0x00b1b1fb .rdataa0`)
2. `chr.IsNPC` (`0x004b79b0` -> `jmp 0x00a78e1e .rdataa0`)
3. `chr.GetInstanceType` (`0x004b7430` -> `jmp 0x00abead5 .rdataa0`)
4. **`chr.GetProjectPosition(vid, z)` (`0x004b7620` -> `0x004b6bc0` -> `0x004fc307` -> `.rdataa0`!)** — **Yeni Kesfedilen Gizli Anti-ESP Tuzagi!** Klasik 3B-2B ekran cizimi (ESP) yapan botlar bu fonksiyonu cagirdiginda VMProtect stack taramasina yakalanir.
5. `player.SetTarget` (`0x00500af0` -> `jmp 0x00b2ecd3 .rdataa0`)

**%100 Saf `.text` Alternatiflerimiz:**
- Varlik siniflandirmasi icin `chr.GetInstanceType` / `IsEnemy` / `IsNPC` yerine %100 saf `.text` olan `chr.GetVirtualNumber(vid)` (`0x004b77c0`), `chr.SelectInstance(vid)` + `chr.GetRace()` (`0x004b76d0`), `nonplayer.IsMonsterStone(vnum)` (`0x004eab90`) ve `nonplayer.GetGradeByVID(vid)` (`0x004ea540`) kullanilir.
- Ekran/Harita ESP icin `chr.GetProjectPosition` yerine %100 saf `.text` olan `miniMap.AddWayPoint(id, x, y, text)` (`0x00528730`) + `miniMap.RemoveWayPoint(id)` (`0x00528d40`) ve `app.GetCamera()` (`0x00537110`) kullanilir!

### Katman 3: Bellek Ici Alan Sifrelemesi (`0x006dbd90` / `0x006dbe10` / `0x006dc0a0`)
- `CInstanceBase` ve `CPythonPlayer` icindeki alanlar RAM'de sifrelidir. Ham RAM okumak yerine motorun kendi Python C API'leri cagrilarak `0x006dbd90` ve `0x006dbe10` yardimcilari guvenle calistirilir.

### Katman 4: Sifreli Karakter Haritasi (`m_kAliveInstMap` @ `CPythonCharacterManager + 0x20`)
- `[CPythonCharacterManager + 0x20]` konteyneri `.rdataa0` (`0x006dc470`) ile sifrelenmistir. `EntityRadar`, ana oyuncu VID'i etrafindaki pencereyi kare basina dilimleyerek (`chr.HasInstance(vid)` @ `0x004b7830`) < 1.4 ms icinde tarar.

### Katman 5: Kasitli Olarak Kisitlanmis (Nerf/Honeypot) 5 Fonksiyon ve Cozumlerimiz

| Kisitlanan Fonksiyon | Adres | Avrasya2'nin Yaptigi Kisitlama (Disassembly Bulgusu) | Gelistirdigimiz %100 Calisan Cozum (Saf `.text`) |
|---|---|---|---|
| `chr.GetPixelPosition(vid)` | `0x004b7560` | `0x004b75b7: cmp eax, [ebp-0x14]` -> `jne 0x004b75f0`. Eger `vid != MainActorVID` ise her zaman `(0.0, 0.0, 0.0)` dondurur! | **`chr.SelectInstance(vid)` (`0x004b7f10`) + `chr.GetBoundBoxOnlyXY()` (`0x004b7320`)**! Granny3D dunya matrisinden (`0x0059a3b1`) hedefin gercek dunya `(xmin, ymin, xmax, ymax)` koordinatlarini dondurur! |
| `chr.GetProjectPosition(vid, z)` | `0x004b7620` | `0x004b7695: call 0x004b6bc0` -> `0x004fc307` -> `.rdataa0` (VMProtect tuzagi!). | **`miniMap.AddWayPoint` (`0x00528730`) + `app.GetCamera()` (`0x00537110`) + Pusula Acisi (`math.atan2`)**! |
| `chr.LookAt(vid)` | `0x004b7aa0` | `0x004b7ae4: call 0x4b4640` ardindan hicbir donus yapmadan `Py_BuildNone` cagirir (ici bosaltilmis!). | `math.atan2(tx - px, ty - py)` ile aci hesaplanip **`chr.SetRotation(deg)` (`0x004b84a0`)** cagirilir. |
| `chrmgr.GetVIDInfo(vid)` | `0x004b59c0` | Her zaman bos string `""` dondurur. | `chr.GetNameByVID(vid)` (`0x004b74f0`), `chr.GetVirtualNumber(vid)` (`0x004b77c0`), `nonplayer.GetGradeByVID(vid)` (`0x004ea540`) ve `player.GetCharacterDistance(vid)` (`0x004fdc90`) kullanilir. |
| `player.StartMouseWalking()` | `0x00500c80` | `jmp 0x00684680` ile dogrudan `None` dondurur. | **`nav.PreviewToPosition` (`0x004ded30`) + `chr.MoveToDestPosition(main_vid, x, y)` (`0x004b7b30`)** kullanilir. |

---

## 3. `source/main.py` (v3.0) Icinde Uygulanan 6 Yaratici Ozellik

### Ozellik 1 — `[F5]` MiniMap / Atlas Canli Metin & Boss ESP Pinleme + Pusula HUD
- **Nasil Calisir:**
  - `EntityRadar`, tespit ettigi tum Metin taslarini (Avrasya2'nin 150 ozel VNUM'u dahil) ve Boss'lari (`grade >= 4`) mesafeye gore siralar.
  - `miniMap.AddWayPoint(id, x, y, label)` (`0x00528730` — %100 saf `.text`) cagirarak hem sag ustteki **MiniMap** uzerine hem de **M tusuyla acilan Buyuk Harita (Atlas)** uzerine canli olarak `"METIN #8027 (45m)"` / `"BOSS #691 (110m)"` isaretlerini yerlestirir; metin kirildiginda `miniMap.RemoveWayPoint(id)` (`0x00528d40`) ile siler.
  - Ustteki HUD panelinde en yakin Metin ve Boss'un adini, VNUM'unu, metre cinsinden uzakligini, 8-yonlu pusula acisini (`K, KD, D, GD, G, GB, B, KB`) ve `[X, Y]` harita koordinatini gosterir.

### Ozellik 2 — `[F6]` 0-Yang Ucretsiz NavMesh A* Oto-Metin & Boss Avcisi
- **Kesfedilen Acik (`CAutoNav` @ `0x004ddd40`..`0x004df000` & `uiminimap.py`):**
  - Avrasya2'nin kendi Otomatik Navigasyon sistemi normalde `nav.Confirm()` (`0x004ddd40` -> `0x004e3f50`) cagrildiginda sunucuya `/autonav_req` paketi gonderir ve oyuncudan **20.000 ile 120.000 Yang** keser.
  - Ancak disassembly analizimiz gosterdi ki `nav.PreviewToPosition(tx, ty)` (`0x004ded30` -> `0x004e35c0`) fonksiyonu **onaydan once** istemcide tam C++ NavMesh A* algoritmasini calistirarak duvarlarin, tepelerin ve agaclarin etrafindan dolanan tum ara noktalari (`nav.GetWaypointCount()`, `nav.GetWaypoint(i)`) ucretsiz hesaplar!
- **Nasil Calisir:**
  - `SafeEngineAPI.compute_free_nav_route(tx, ty)` fonksiyonu `nav.PreviewToPosition(tx, ty)` cagirir, `nav.GetWaypoint(i)` ile tum A* ara noktalarini okur ve **ayni milisaniye icinde `nav.CancelPreview()` cagirir**.
  - Sonuc: **0 Yang maliyet, sunucuya 0 `/autonav_req` paketi**, ve haritanin obur ucundaki Metin tasina bile engellere takilmadan %100 C++ NavMesh A* rotasiyla otomatik yurume + kesme!

### Ozellik 3 — `[F7]` Oto-Toplama + SvSide (`<svside>`) Captcha Otomatik Cozucu + GM Kalkani
- **Kesfedilen Acik (`pack/root/svsideoi.py` & `game.py`):**
  - Sunucu bot kontrolu gonderdiginde `game.svsidedia.nm_updateimgoffline(randcode)` (`verifyType == 1`) fonksiyonunu cagirir ve 4 haneli dogrulama kodunu **dogrudan `randcode[0:4]` parametresinde duz metin (plaintext) olarak** gonderir (`self.imgo1.LoadImage('svside/' + randcode[0:1] + '.jpg')`)!
  - Pencere ise cevabi `net.SendWhisperPacket("<svside>", code)` ile gonderir.
- **Nasil Calisir:**
  - `SvSideCaptchaAndGMGuard`, `game.svsidedia.nm_updateimgoffline` fonksiyonunu kancalar.
  - `verifyType == 1` geldiginde otomasyonu duraklatir, **1.9 – 3.1 saniye** insansi gecikme bekler, ardindan `net.SendWhisperPacket("<svside>", randcode[:4])` gondererek Captcha'yi otomatik cozer ve pencereyi kapatir!
  - `verifyType == 2` (`nm_updateimgoffline2`) acilirsa veya radarda bir **GM / Yetkili** (`chr.IsGameMaster` veya `[GM]`/`[TL]`/`[GA]`/`[AVCI]`) algilanirsa saldiri ve hareketi aninda durdurup kalkan moduna gecer.

### Ozellik 4 — `[F8]` Oto-Iksir + Binek Indir-Yak-Bin (`/ride`) Akilli Buff Makrosu
- **Nasil Calisir:**
  - HP (`< %72`) ve SP (`< %35`) dustugunde hizli slottan otomatik iksir basar.
  - Her 2.5 saniyede bir 1..4 yetenek slotlarindaki buff yeteneklerini (*Hava Kilici, Guclu Beden, Buyulu Keskinlik, Buyulu Zirh, Dehset, Kutsama, Ejderha Yardimi, Yansitma, Hiz, Saldiri+*) kontrol eder.
  - Suresi bitmis ve soguma suresi (cooldown) dolmus bir buff varsa:
    1. Karakter binekteyse (`player.IsMountingHorse()`) `/ride` komutuyla binekten iner.
    2. `0.45 sn` sonra `player.ClickSkillSlot(slot)` ile suresi biten bufflari yakar.
    3. `0.65 sn` sonra `/ride` komutuyla binege geri biner ve Metin kesmeye devam eder!

### Ozellik 5 — `[F9]` Uzaktan Biyolog (`/biyolog_ver 0 0`) + Seviye Gorevi (`/mission_end`) Otomasyonu
- **Kesfedilen Acik (`pack/root/uibiyologmenu.py` & `game.py`):**
  - Avrasya2'de Biyolog teslimati NPC'ye gitmeden `/biyolog_ver 0 0` komutuyla, Seviye Gorevi (`constInfo.LVL_MISSION_DATA`) odul talebi ise `/mission_end` komutuyla uzaktan yapilabilmektedir.
- **Nasil Calisir:**
  - `constInfo.LVL_MISSION_DATA` icindeki gorev sayaclari (`dead >= count`) tamamlandiginda otomatik olarak `/mission_end` gonderip odulu alir ve periyodik olarak `/biyolog_ver 0 0` ile Biyolog teslimatini yapar.

### Ozellik 6 — `[F10]` Kamera Zoom Kilidi Acma (`5500.0`) + Gunduz / Kar / Agac FPS Hizlandirici
- **Nasil Calisir:**
  - `game.py` icinde `1550.0` ile sinirlanan kamera uzakligini `app.SetCameraMaxDistance(5500.0)` (`0x00538370` — saf `.text`) ile acar; boylece haritaya kusbakisi bakilarak tum Metin taslari gorulebilir.
  - `background.SetEnvironmentData(0)` ile geceyi gunduze cevirir, `background.EnableSnow(0)` ile kari kapatir ve `background.SetVisiblePart(PART_TREE, 0)` / `SetVisiblePart(PART_CLOUD, 0)` (`0x004b1730` — saf `.text`) ile agaclari ve bulutlari gizleyerek hem FPS'i maksimuma cikarir hem de Metin taslarinin agac arkasinda kalmasini onler.

---

## 4. Paketlerle Yapilabilecek Tum Ozellikler (`CPythonNetworkStream` / `offlineshop` / `cube_renewal` / `acce` / `player`)

`metin2client.bin` icindeki `CPythonNetworkStream` (`0x009c53c8`) ve ilgili paket modullerinin disassembly analizi sonucunda, paket gonderen fonksiyonlarin **VMProtect (`.rdataa0`) durumu** ve **paketlerle yapilabilecek 10 yaratici ozellik** asagidaki gibidir:

### 4.1 Paket Fonksiyonlarinin Binary (`.text` vs `.rdataa0`) Haritasi

| Python Paket Fonksiyonu | Python Wrapper VA | C++ Motor VA | Koruma Durumu | Paket Basligi / Not |
|---|---|---|---|---|
| `net.SendItemUsePacket(slot)` | `0x0054b940` (`.text`) | `0x00567910` | 2. Seviye VMP (`0x00b3c829`) | Python'dan cagrildiginda return-address `0x0054b98d` (`.text`) oldugu icin %100 guvenli! |
| `net.SendItemUseToItemPacket(src, dst)` | `0x0054b9d0` (`.text`) | `0x005679c0` | **%100 Saf `.text`** | Efsun nesnesi (71084), Kutsama Kagidi, Tas ekleme paketi! |
| `net.SendItemPickUpPacket(vid)` | `0x0054b900` (`.text`) | `0x005678b0` | 2. Seviye VMP (`0x00cb6f5c`) | Yerdeki spesifik esya VID'ini aninda toplama paketi. |
| `net.SendItemMovePacket(src, dst, cnt)` | `0x0054b7e0` (`.text`) | `0x005677a0` | **%100 Saf `.text`** | Envanter birlestirme (Auto-Stack) ve duzenleme paketi. |
| `net.SendOnClickPacket(vid)` | `0x0054a050` (`.text`) | `0x00562080` | 2. Seviye VMP (`0x00b5903f`) | NPC / Metin / Pazar / Sandik etkilesim paketi. |
| `net.SendShopBuyPacket(slot)` | `0x0054c3f0` (`.text`) | `0x00567e00` | **%100 Saf `.text` (C++ dahil!)** | Marketten sifir gecikmeli toplu alim paketi. |
| `net.SendShopSellPacketNew(slot, cnt)` | `0x0054c480` (`.text`) | `0x00562800` | **%100 Saf `.text` (C++ dahil!)** | Markete toplu esya satis paketi. |
| `net.SendRefinePacket(slot, type)` | `0x0054c010` (`.text`) | `0x00562480` | **%100 Saf `.text` (C++ dahil!)** | Demirci / Kule Demircisi / +Basma paketi (`type=0..4`). |
| `net.SendTargetInfoLoad(vid)` | `0x0054c980` (`.text`) | `0x00547100` | 2. Seviye VMP (`0x00b39f1a`) | Boss veya Metin tasinin icinden dusecek tum esyalari sorgular (`ENABLE_TARGET_INFORMATION_SYSTEM = 1`). |
| `offlineshop.SendBuyItem(id, item_id, price)` | `0x004f3c40` (`.text`) | `0x004e8200` | **%100 Saf `.text` (C++ dahil!)** | Cevrimdisi pazardan (Ikarus OfflineShop) aninda esya cekme paketi (`hdr=0xF8`). |
| `offlineshop.SendSafeboxGetValutes(val)` | `0x004f4100` (`.text`) | `0x004e88b0` | **%100 Saf `.text` (C++ dahil!)** | Haritanin herhangi bir yerinden OfflineShop kasasindaki Yang'i cekme paketi (`hdr=0xF8`). |
| `offlineshop.SendSafeboxGetItem(id)` | `0x004f40a0` (`.text`) | `0x004e87b0` | **%100 Saf `.text` (C++ dahil!)** | Haritanin herhangi bir yerinden OfflineShop kasasindaki satilmayan esyayi cekme paketi. |
| `cube_renewal.CubeRenewalMakeItem(idx, cnt, i)` | `0x004b9960` (`.text`) | `0x004b99f0` | **%100 Saf `.text` (C++ dahil!)** | Arindirma (Cube Renewal) penceresinde aninda toplu uretim paketi. |
| `player.SendDragonSoulRefine(sub, dic)` | `0x005000e0` (`.text`) | `0x006dc956` | **%100 Saf `.text` (C++ dahil!)** | Ejderha Tasi Simyasi (DSS) uzaktan sinif/parlaklik/seviye arindirma paketi. |
| `acce.SendRefineRequest(inven)` | `0x0047a7b0` (`.text`) | `0x0047a4b0` | **%100 Saf `.text` (C++ dahil!)** | Kusak (Acce) kombinasyon ve bonus emisyonu paketi. |

### 4.2 Paketlerle Yapilabilecek 10 Yaratici Ozellik

1. **Tek-Kare 6'li Sebnem + Ejderha Tanrisi + Kritik/Delici Paketi (`[Sebnem Bas]` — `net.SendItemUsePacket`):**
   - `uiinventory.py` satir 1426'da istemci arayuzune `if app.GetTime() < self.lastSebnemUseTime + 5:` seklinde 5 saniyelik bir UI kilidi konulmustur.
   - `SafeEngineAPI.use_all_sebnems_and_boosts()` fonksiyonumuz bu UI kilidini tamamen atlayarak `50821..50826` (6 Sebnem), `71027..71030` (Ejderha Tanrisi Saldiri/Savunma/Zeka/Yasam) ve `71044..71045` (Kritik/Delici Isabet) VNUM'larini envanterde bulup **tek karede (0 ms gecikmeyle)** `net.SendItemUsePacket(slot)` ile aktiflestirir!
2. **Paket Tabanli Efsun Botu (Switchbot — `net.SendItemUseToItemPacket` + `player.GetItemAttribute`):**
   - `net.SendItemUseToItemPacket(efsun_slot, hedef_slot)` (`0x0054b9d0`) ve `player.GetItemAttribute(hedef_slot, i)` (`0x004fe260`) fonksiyonlarinin **her ikisi de %100 saf `.text`** kodudur!
   - Envanterdeki *Efsun Nesnesi* (`71084`) slotunu hedef ekipman slotu uzerine paketle gonderip, istenen efsun orani (ornegin `Ortalama Zarar >= 45` veya `Yari Insan +10, Kritik +10`) geldigi anda milisaniyesinde duran %100 paket tabanli Efsun Botu calistirilabilir.
3. **Kule Demircisi (DT) / Normal Demirci Otomatik +Basma & Kutsama Kagidi Paketi (`net.SendRefinePacket` & `net.SendItemUseToItemPacket`):**
   - `net.SendRefinePacket(slot, type)` (`0x0054c010` — %100 saf `.text`):
     - `type = 0`: Normal / Kule Demircisi (Esya istemeden veya standart +basma). Kule 6. katta demirci ciktiginda (veya koy demircisinde) tek tusla hedef slota `+basma` paketi gonderir.
     - `type = 1..4`: Kutsama Kagidi (`25040`), Buyulu Metal (`25041`), Lonca Demircisi (`net.SendItemUseToItemPacket(scroll_slot, target_slot)` -> `net.SendRefinePacket(target_slot, type)`).
4. **Haritanin Her Yerinden OfflineShop Kasa (Yang & Esya) Cekme (`offlineshop.SendSafeboxOpen` + `SendSafeboxGetValutes`):**
   - Avrasya2'de `app.__ENABLE_NEW_OFFLINESHOP__ = 1` aktiftir ve `offlineshop` C++ modulu %100 saf `.text` olarak derlenmistir.
   - Farm sirasinda koye donmeden veya pazar penceresini acmadan `offlineshop.SendSafeboxOpen()` + `offlineshop.SendSafeboxGetValutes(miktar)` ile pazardaki satislardan biriken Yang dogrudan envantere cekilebilir; `offlineshop.SendAddItem` / `SendEditItem` / `SendRemoveItem` ile pazar uzaktan yonetilebilir.
5. **Canavar / Boss / Metin Drop Rontgeni (`net.SendTargetInfoLoad(vid)` @ `0x0054c980`):**
   - `app.ENABLE_TARGET_INFORMATION_SYSTEM = 1` aktif oldugu icin, bir Metin tasina veya Boss'a hic yaklasmadan `net.SendTargetInfoLoad(vid)` paketi gonderilerek o hedefin icinden dusebilecek tum sandik ve esya listesi sunucudan sorgulanabilir.
6. **Uzaktan Ejderha Tasi Simyasi (DSS) Otomatik Arindirma (`player.SendDragonSoulRefine` @ `0x005000e0`):**
   - `app.ENABLE_NO_DSS_QUALIFICATION = 1` aktif oldugundan, Simyaci NPC'ye gitmeden `player.SendDragonSoulRefine(sub_header, slot_dict)` (%100 saf `.text`) ile envanterdeki Cor Draconis'lerden cikan islenmemis simyalar otomatik olarak Yontulmus -> Nadir -> Antika -> Efsanevi seviyesine birlestirilebilir.
7. **Uzaktan Seviye Gorevi Odul Toplama (`/mission_end`), Biyolog (`/biyolog_ver 0 0`) ve Sancak Savasi (`/sancak git <bayrak>`):**
   - `net.SendChatPacket("/mission_end")` ile tamamlanan gorev odulleri, `net.SendChatPacket("/biyolog_ver 0 0")` ile Biyolog teslimati, `net.SendChatPacket("/sancak durum")` / `"/sancak git %d"` ile Sancak Savasi girisi ve `net.SendChatPacket("/nesne_market %d %d" % (id, count))` ile nesne market alimi dogrudan paketle tetiklenir.
8. **Otomatik Envanter Birlestirme (Auto-Stack) & Sandik Acici (`net.SendItemMovePacket` & `net.SendItemUsePacket`):**
   - Envanterde ayri slotlara dagilmis ayni VNUM'lu esyalari (`200` altindaki istiflenebilir esyalar) `net.SendItemMovePacket(src_slot, dst_slot, count)` (`0x0054b7e0` — %100 saf `.text`) ile otomatik ust uste birlestirir.
   - Ayisigi Define Sandigi (`50011`), Altigen Hediye Paketi (`50037`) veya Boss sandiklarini `net.SendItemUsePacket(slot)` ile toplu acar.
9. **Otomatik Dirilme (`/restart_here`) ve Aninda Binek Senkronizasyonu (`/ride` / `/unmount`):**
   - `net.SendChatPacket("/restart_here")` ile olum aninda beklemeden yerinde dirilme; `net.SendChatPacket("/ride")` ile C++ motor animasyonunu beklemeden sunucu tarafinda aninda binege binme/inme.
10. **Uzaktan Ekipman Rontgeni (`/view_equip <vid>`) ve Otomatik Duello/Grup Engelleme (`/setblockmode`):**
    - `net.SendChatPacket("/view_equip %d" % vid)` ile haritadaki diger oyuncularin giydigi ekipmanlari uzaktan goruntuleme; farm sirasinda rahatsiz edilmemek icin `net.SendChatPacket("/setblockmode %d" % mask)` ile Ticaret, Grup, Lonca ve Fisilti isteklerini paket seviyesinde kilitleme.

