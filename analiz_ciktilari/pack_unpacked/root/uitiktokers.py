import app, net, ui, urllib2, localeInfo, constInfo, uiScriptLocale, uiCommon
from _weakref import proxy

if constInfo.TIKTOK_PANEL:
	import threading

IMAGE_PATH = "d:/ymir work/ui/public/patchnote/"

USE_WEB_CACHE = 1
if USE_WEB_CACHE == 1:
	import time
	from datetime import datetime, timedelta
	cached_time = None
	cache_duration = timedelta(minutes=15)

if constInfo.TIKTOK_PANEL:
	constInfo.cache_duration = timedelta(minutes=4)  # Önbellek süresi
	class WebPageReader:
		def __init__(self, callback):
			self.lock = threading.Lock()  # Veriye eþzamanlý eriþimi engellemek için
			self.callback = callback  # UI'yi güncellemek için callback fonksiyonu

		def read_webpage(self):
			if len(constInfo.TIKTOK_DATA) != 0 and constInfo.cached_time and (datetime.now() - constInfo.cached_time) < constInfo.cache_duration:
				self.callback(constInfo.TIKTOK_DATA)
				return constInfo.TIKTOK_DATA

			thread = threading.Thread(target=self._fetch_webpage)
			thread.start()

		def _fetch_webpage(self):
			constInfo.TIKTOK_DATA = []
			try:
				response = urllib2.urlopen("http://metin2ler.com/check_kuzey2.php")
				content = response.read()

				live_status = self.manual_json_parse(content)

				with self.lock:
					constInfo.TIKTOK_DATA = live_status
					constInfo.cached_time = datetime.now()

				self.callback(live_status)

			except urllib2.URLError as e:
				print("URL Hatasý:", e)
				self.callback(None)

		def manual_json_parse(self, content):
			live_status = {}

			content = content.strip('{}')
			entries = content.split(',')

			for entry in entries:
				key_value = entry.split(':')
				if len(key_value) == 2:
					key = key_value[0].strip().strip('"')
					value = key_value[1].strip().strip('"')
					live_status[key] = value

			return live_status
