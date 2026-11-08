import app
import localeInfo
import random
from constInfo import TextColor

app.ServerName = None

SRV1 = {
	"name": "AvrasyaMt2",
	"host": "185.128.114.71",

	"auth1": 30001,
	"auth2": 30003,
	"auth3": 30005,
	"auth4": 30007,

	"ch1": 30009,
	"ch2": 30013,
	"ch3": 30017,
	"ch4": 30021,
	"ch5": 30025,
	"ch6": 30029,
	"ch7": 30033,
	"ch8": 30037,
	"ch9": 30041,
	"ch10": 30045,
}

STATE_NONE = "..."

STATE_DICT = {
	0: "...",
	1: "NORM",
	2: "BUSY",
	3: "FULL",
}

SERVER1_CHANNEL_DICT = {
	0: {"key": 10, "name": "CH1", "ip": SRV1["host"], "tcp_port": SRV1["ch1"], "udp_port": SRV1["ch1"], "state": STATE_NONE,},
	1: {"key": 11, "name": "CH2", "ip": SRV1["host"], "tcp_port": SRV1["ch2"], "udp_port": SRV1["ch2"], "state": STATE_NONE,},
	2: {"key": 12, "name": "CH3", "ip": SRV1["host"], "tcp_port": SRV1["ch3"], "udp_port": SRV1["ch3"], "state": STATE_NONE,},
	3: {"key": 13, "name": "CH4", "ip": SRV1["host"], "tcp_port": SRV1["ch4"], "udp_port": SRV1["ch4"], "state": STATE_NONE,},
	4: {"key": 14, "name": "CH5", "ip": SRV1["host"], "tcp_port": SRV1["ch5"], "udp_port": SRV1["ch5"], "state": STATE_NONE,},
	5: {"key": 15, "name": "CH6", "ip": SRV1["host"], "tcp_port": SRV1["ch6"], "udp_port": SRV1["ch6"], "state": STATE_NONE,},
	# 6: {"key": 16, "name": "CH7", "ip": SRV1["host"], "tcp_port": SRV1["ch7"], "udp_port": SRV1["ch7"], "state": STATE_NONE,},
	# 7: {"key": 17, "name": "CH8", "ip": SRV1["host"], "tcp_port": SRV1["ch8"], "udp_port": SRV1["ch8"], "state": STATE_NONE,},
	# 8: {"key": 18, "name": "CH9", "ip": SRV1["host"], "tcp_port": SRV1["ch9"], "udp_port": SRV1["ch9"], "state": STATE_NONE,},
	# 9: {"key": 19, "name": "CH10", "ip": SRV1["host"], "tcp_port": SRV1["ch10"], "udp_port": SRV1["ch10"], "state": STATE_NONE,},
}

REGION_NAME_DICT = {
	0: SRV1["name"],
}

REGION_AUTH_SERVER_DICT = {
	0: {
		1: {
			"ip": SRV1["host"],
			"port": random.choice([
				SRV1["auth1"],
				SRV1["auth2"],
				SRV1["auth3"],
				SRV1["auth4"],
			]),
		},
	},
}

REGION_DICT = {
	0: {
		1: {
			"name": SRV1["name"],
			"channel": SERVER1_CHANNEL_DICT,
		},
	},
}

MARKADDR_DICT = {
	10: {
		"ip": SRV1["host"],
		"tcp_port": SRV1["ch1"],
		"mark": "10.tga",
		"symbol_path": "10",
	},
}

TESTADDR = {
	"ip": SRV1["host"],
	"tcp_port": SRV1["ch1"],
	"udp_port": SRV1["ch1"],
}