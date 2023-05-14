#!/usr/bin/env python

from boofuzz import *

# List of all blocks defined here (for easy copy/paste)
"""
sess.connect(s_get("HTTP VERBS"))
sess.connect(s_get("HTTP VERBS BASIC"))
sess.connect(s_get("HTTP VERBS POST"))
sess.connect(s_get("HTTP HEADERS"))
sess.connect(s_get("HTTP COOKIE"))
"""

def main():
	session = Session(
			target=Target(
				connection=SocketConnection("192.168.0.100", 80, proto='tcp')
			),
	)

	s_initialize("HTTP VERBS")
	s_group("verbs", values=["GET", "HEAD", "POST", "OPTIONS", "TRACE", "PUT", "DELETE", "PROPFIND"])
	if s_block_start("body", group="verbs"):
		s_delim(" ")
		s_delim("/")
		s_string("index.html")
		s_delim(" ")
		s_string("HTTP")
		s_delim("/")
		s_string("1")
		s_delim(".")
		s_string("1")
		s_static("\r\n\r\n")
	s_block_end()

	s_initialize("HTTP VERBS BASIC")
	s_group("verbs", values=["GET", "HEAD"])
	if s_block_start("body", group="verbs"):
		s_delim(" ")
		s_delim("/")
		s_string("index.html")
		s_delim(" ")
		s_string("HTTP")
		s_delim("/")
		s_string("1")
		s_delim(".")
		s_string("1")
		s_static("\r\n\r\n")
	s_block_end()

	s_initialize("HTTP VERBS POST")
	s_static("POST / HTTP/1.1\r\n")
	s_static("Content-Type: ")
	s_string("multipart/form-data; boundary=----WebKitFormBoundaryIupbmAnQgEQ1mgRl")
	s_static("Content-Length: ")
	s_size("1632", output_format="ascii", signed=True, fuzzable=True)
	s_static("\r\n\r\n")

	s_initialize("HTTP HEADERS")
	s_static("GET / HTTP/1.1\r\n")

	# let's fuzz random headers with malformed delimiters.
	s_string("Host")
	s_delim(":")
	s_delim(" ")
	s_string("192.168.0.100")
	s_delim("\r\n")

	# let's fuzz the value portion of some popular headers.
	s_static("User-Agent: ")
	s_string("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36")
	s_static("\r\n")

	s_static("Accept-Language: ")
	s_string("en-us")
	s_delim(",")
	s_string("en;q=0.9")
	s_static("\r\n")

	s_static("Keep-Alive: ")
	s_string("300")
	s_static("\r\n")

	s_static("Connection: ")
	s_string("keep-alive")
	s_static("\r\n")

	s_static("Referer: ")
	s_string("http://192.168.0.100/index.php?page=master&menu1=Maintenance&menu2=Remote%20Management&menu3=SNMP&menu4=")
	s_static("\r\n")
	s_static("\r\n")

	s_initialize("HTTP COOKIE")
	s_static("GET / HTTP/1.1\r\n")

	if s_block_start("cookie"):
		s_static("Cookie: ")
		s_string("PHPSESSID")
		s_delim("=")
		s_string("5fcb6cff3bbb88508fe9b4574b223219")
		s_static("\r\n")
		s_block_end()

	s_repeat("cookie", max_reps=5000, step=500)
	s_static("\r\n")

	session.connect(s_get("HTTP VERBS"))
	session.connect(s_get("HTTP VERBS BASIC"))
	session.connect(s_get("HTTP VERBS POST"))
	session.connect(s_get("HTTP HEADERS"))
	session.connect(s_get("HTTP COOKIE"))
	
	session.fuzz()

if __name__ == "__main__":
	main()
