extends Node

@export var server_url: String = "ws://127.0.0.1:8877"


var ws: WebSocketPeer = WebSocketPeer.new()
var connected: bool = false
var frames: Array = []
var init_msg: Dictionary = {}
var last_error: int = 0

func _ready():
	var err: int = ws.connect_to_url(server_url)
	last_error = err
	set_process(true)

func _process(_delta: float) -> void:
	ws.poll()
	var st: int = ws.get_ready_state()
	if st == WebSocketPeer.STATE_OPEN and not connected:
		connected = true
		print("[Client] connected to ", server_url)
	if st != WebSocketPeer.STATE_OPEN:
		return
	while ws.get_available_packet_count() > 0:
		var pkt: PackedByteArray = ws.get_packet()
		var txt: String = pkt.get_string_from_utf8()
		var data := {}
		if txt.length() > 0:
			data = JSON.parse_string(txt)
		if typeof(data) == TYPE_DICTIONARY:
			var t: String = str(data.get("type",""))
			if t == "init":
				init_msg = data
			elif t == "frame":
				frames.append(data)
				if frames.size() > 6:
					frames.pop_front()

func pop_frame() -> Dictionary:
	if frames.is_empty():
		return {}
	return frames.pop_front()

func peek_frame() -> Dictionary:
	if frames.is_empty():
		return {}
	return frames[frames.size() - 1]

func send_input(payload: Dictionary) -> void:
	payload["type"] = "input"
	var txt: String = JSON.stringify(payload)
	ws.send_text(txt)
