extends Node2D

var world_w: int = 256
var zoom: float = 1.0
var pan: Vector2 = Vector2.ZERO
var dragging: bool = false
var last_mouse: Vector2 = Vector2.ZERO

var cells: Array = []
var show_threat: bool = false
var show_value: bool = true
var show_will: bool = false
var show_coherence: bool = false
var show_grid: bool = true

var tex_threat: Texture2D
var tex_value: Texture2D
var tex_will: Texture2D
var tex_coherence: Texture2D
var tex_terrain: Texture2D
var tex_veg: Texture2D
var tex_farm: Texture2D
var tex_farm_paddy: Texture2D
var tex_farm_field: Texture2D
var tex_river: Texture2D

var show_veg: bool = true
var show_farm: bool = true
var show_help: bool = true
var time_phase: float = 0.0
var selected_id: String = ""
var selected_pos: Vector2 = Vector2.ZERO
var sim_rate: float = 1.0

# High-level civilization / caravan lens (fed from frame["civ"])
var show_demo_caravan: bool = true
var demo_civ_nodes: Array = []
var demo_caravans: Array = []
@onready var spr_village_a: Sprite2D = $"Markers/VillageA"
@onready var spr_village_b: Sprite2D = $"Markers/VillageB"
@onready var spr_caravan: Sprite2D = $"Markers/Caravan"


func _ready() -> void:
	set_process(true)


func _process(delta: float) -> void:
	var client: Node = get_node_or_null("/root/Client") as Node
	var status: Label = get_node_or_null("Status") as Label

	if client:
		if client.init_msg.has("world"):
			world_w = int(client.init_msg["world"].get("width", world_w))

		var frame: Dictionary = client.pop_frame()
		if frame.size() > 0:
			cells = frame.get("cells", cells)
			var ov: Dictionary = frame.get("overlays", {})
			tex_terrain = _decode_tex(ov.get("terrain"))
			tex_veg = _decode_tex(ov.get("veg"))
			tex_farm = _decode_tex(ov.get("farm"))
			tex_farm_paddy = _decode_tex(ov.get("farm_paddy"))
			tex_farm_field = _decode_tex(ov.get("farm_field"))
			tex_river = _decode_tex(ov.get("river"))
			tex_threat = _decode_tex(ov.get("threat"))
			tex_value = _decode_tex(ov.get("value"))
			tex_will = _decode_tex(ov.get("will"))
			tex_coherence = _decode_tex(ov.get("coherence"))

			if frame.has("civ"):
				_update_civ_from_frame(frame.get("civ"))

			var tinfo: Dictionary = frame.get("time", {})
			if tinfo.has("phase"):
				var ph = tinfo.get("phase")
				if typeof(ph) == TYPE_FLOAT or typeof(ph) == TYPE_INT:
					time_phase = clamp(float(ph), 0.0, 1.0)

	if status:
		var msg := ""
		if client and client.connected:
			msg = "연결됨 | 셀: %d" % cells.size()
		else:
			msg = "연결 대기(ws://127.0.0.1:8765)"
		status.text = msg

	_update_demo_caravan(delta)
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP and event.pressed:
			var world_before: Vector2 = _screen_to_world(event.position)
			zoom = clamp(zoom * 1.1, 0.25, 8.0)
			_recenter_on_world(event.position, world_before)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN and event.pressed:
			var world_before_down: Vector2 = _screen_to_world(event.position)
			zoom = clamp(zoom / 1.1, 0.25, 8.0)
			_recenter_on_world(event.position, world_before_down)
		elif event.button_index == MOUSE_BUTTON_MIDDLE or event.button_index == MOUSE_BUTTON_RIGHT:
			dragging = event.pressed
			last_mouse = event.position
		elif event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
			var client: Node = get_node_or_null("/root/Client") as Node
			if client:
				var coords: Vector2 = _screen_to_world(event.position)
				client.send_input({"select_x": int(coords.x), "select_y": int(coords.y)})
	elif event is InputEventMouseMotion and dragging:
		var d: Vector2 = event.position - last_mouse
		pan += d
		last_mouse = event.position
	elif event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_T:
				show_threat = !show_threat
			KEY_V:
				show_value = !show_value
			KEY_I:
				show_will = !show_will
			KEY_U:
				show_coherence = !show_coherence
			KEY_G:
				show_grid = !show_grid
			KEY_Y:
				show_veg = !show_veg
			KEY_F:
				show_farm = !show_farm
			KEY_H:
				show_help = !show_help
			KEY_C:
				show_demo_caravan = !show_demo_caravan
			KEY_1:
				_set_sim_rate(0.5)
			KEY_2:
				_set_sim_rate(1.0)
			KEY_3:
				_set_sim_rate(2.0)
			KEY_4:
				_set_sim_rate(4.0)
			KEY_F9:
				var client: Node = get_node_or_null("/root/Client") as Node
				if client:
					var p: Vector2 = get_viewport().get_mouse_position()
					var coords: Vector2 = _screen_to_world(p)
					client.send_input({"disaster": {"kind": "FLOOD", "x": int(coords.x), "y": int(coords.y), "radius": 8}})
			KEY_F10:
				var client2: Node = get_node_or_null("/root/Client") as Node
				if client2:
					var p2: Vector2 = get_viewport().get_mouse_position()
					var coords2: Vector2 = _screen_to_world(p2)
					client2.send_input({"disaster": {"kind": "VOLCANO", "x": int(coords2.x), "y": int(coords2.y), "radius": 8}})


func _screen_to_world(p: Vector2) -> Vector2:
	var vp: Vector2 = get_viewport_rect().size
	var base: float = float(min(vp.x, vp.y))
	var s: float = (base / float(world_w)) * zoom
	var off: Vector2 = Vector2((vp.x - world_w * s) / 2.0, (vp.y - world_w * s) / 2.0)
	var tl: Vector2 = off + pan
	var wx: float = (p.x - tl.x) / s
	var wy: float = (p.y - tl.y) / s
	return Vector2(clamp(wx, 0.0, world_w - 1.0), clamp(wy, 0.0, world_w - 1.0))


func _world_to_screen(world_pos: Vector2) -> Vector2:
	var vp: Vector2 = get_viewport_rect().size
	var base: float = float(min(vp.x, vp.y))
	var s: float = (base / float(world_w)) * zoom
	var off: Vector2 = Vector2((vp.x - world_w * s) / 2.0, (vp.y - world_w * s) / 2.0)
	var tl: Vector2 = off + pan
	return tl + world_pos * s


func _recenter_on_world(screen_pos: Vector2, world_pos: Vector2) -> void:
	var vp: Vector2 = get_viewport_rect().size
	var base: float = float(min(vp.x, vp.y))
	var s: float = (base / float(world_w)) * zoom
	var off: Vector2 = Vector2((vp.x - world_w * s) / 2.0, (vp.y - world_w * s) / 2.0)
	pan = screen_pos - off - world_pos * s


func _set_sim_rate(new_rate: float) -> void:
	sim_rate = clamp(new_rate, 0.25, 8.0)
	var client: Node = get_node_or_null("/root/Client") as Node
	if client:
		client.send_input({"sim_rate": sim_rate})


func _decode_tex(b64):
	if typeof(b64) != TYPE_STRING or b64 == "":
		return null
	var buf: PackedByteArray = Marshalls.base64_to_raw(b64)
	var img := Image.new()
	var err := img.load_png_from_buffer(buf)
	if err != OK:
		return null
	return ImageTexture.create_from_image(img)


func _update_civ_from_frame(civ: Dictionary) -> void:
	var nodes: Array = civ.get("nodes", [])
	var caravans: Array = civ.get("caravans", [])

	if nodes.size() > 0:
		demo_civ_nodes.clear()
		for n in nodes:
			var nx: float = float(n.get("x", 0.0))
			var ny: float = float(n.get("y", 0.0))
			demo_civ_nodes.append({
				"id": str(n.get("id", "")),
				"label": str(n.get("label", "")),
				"pos": Vector2(nx, ny),
			})

	if caravans.size() > 0:
		demo_caravans.clear()
		for c in caravans:
			demo_caravans.append({
				"id": str(c.get("id", "")),
				"origin_id": str(c.get("origin_id", "")),
				"target_id": str(c.get("target_id", "")),
				"t": float(c.get("t", 0.0)),
				"dir": 1,
				"speed": 0.0,
				"color": Color(1.0, 0.8, 0.2),
			})

	_update_civ_sprites()


func _update_civ_sprites() -> void:
	# Position village icons on civ nodes (if present)
	if demo_civ_nodes.size() > 0 and spr_village_a:
		var n0: Dictionary = demo_civ_nodes[0]
		var pos0: Vector2 = n0.get("pos", Vector2.ZERO)
		spr_village_a.position = _world_to_screen(pos0)

	if demo_civ_nodes.size() > 1 and spr_village_b:
		var n1: Dictionary = demo_civ_nodes[1]
		var pos1: Vector2 = n1.get("pos", Vector2.ZERO)
		spr_village_b.position = _world_to_screen(pos1)

	# Position caravan icon along the road between first two civ nodes
	if spr_caravan and demo_civ_nodes.size() > 1 and demo_caravans.size() > 0:
		var c: Dictionary = demo_caravans[0]
		var t: float = float(c.get("t", 0.0))
		var a_world: Vector2 = demo_civ_nodes[0].get("pos", Vector2.ZERO)
		var b_world: Vector2 = demo_civ_nodes[1].get("pos", Vector2.ZERO)
		var caravan_world: Vector2 = a_world.lerp(b_world, t)
		spr_caravan.position = _world_to_screen(caravan_world)


func _draw() -> void:
	var vp: Vector2 = get_viewport_rect().size
	var base: float = float(min(vp.x, vp.y))
	var s: float = (base / float(world_w)) * zoom
	var off: Vector2 = Vector2((vp.x - world_w * s) / 2.0, (vp.y - world_w * s) / 2.0)
	var tl: Vector2 = off + pan

	# Background
	draw_rect(Rect2(Vector2.ZERO, vp), Color(0.03, 0.03, 0.06), true)

	var rect: Rect2 = Rect2(tl, Vector2(world_w * s, world_w * s))
	if tex_terrain != null:
		draw_texture_rect(tex_terrain, rect, false)
	if tex_river != null:
		draw_texture_rect(tex_river, rect, false, Color(0.4, 0.7, 1.0, 0.45))

	# Grid
	if show_grid:
		var step_world: int = max(8, world_w / 32)
		var x: int = 0
		while x <= world_w:
			var xp: float = tl.x + float(x) * s
			draw_line(Vector2(xp, tl.y), Vector2(xp, tl.y + world_w * s), Color(1, 1, 1, 0.08), 1.0)
			x += step_world
		var y: int = 0
		while y <= world_w:
			var yp: float = tl.y + float(y) * s
			draw_line(Vector2(tl.x, yp), Vector2(tl.x + world_w * s, yp), Color(1, 1, 1, 0.08), 1.0)
			y += step_world

	if show_veg and tex_veg != null:
		draw_texture_rect(tex_veg, rect, false, Color(0.5, 1.0, 0.6, 0.30))
	if show_farm and tex_farm != null:
		draw_texture_rect(tex_farm, rect, false, Color(1.0, 0.9, 0.4, 0.35))
	if show_threat and tex_threat != null:
		draw_texture_rect(tex_threat, rect, false, Color(1, 0.2, 0.1, 0.35))
	if show_value and tex_value != null:
		draw_texture_rect(tex_value, rect, false, Color(1.0, 0.9, 0.4, 0.35))
	if show_will and tex_will != null:
		draw_texture_rect(tex_will, rect, false, Color(0.3, 0.6, 1.0, 0.35))
	if show_coherence and tex_coherence != null:
		draw_texture_rect(tex_coherence, rect, false, Color(1.0, 0.95, 0.6, 0.35))

	# High-level civ / caravan overlay
	_draw_demo_civ_and_caravan(tl, s)

	# Cells
	for cd in cells:
		var x_cell: float = float(cd.get("x", 0.0))
		var y_cell: float = float(cd.get("y", 0.0))
		var alive: bool = bool(cd.get("alive", true))
		var typ: String = str(cd.get("type", ""))
		var col: Color
		if typ == "human":
			col = Color(0.90, 0.85, 0.50)
		elif typ == "animal":
			col = Color(0.50, 0.70, 1.00)
		elif typ == "life":
			col = Color(0.50, 0.90, 0.55)
		else:
			col = Color(0.85, 0.85, 0.90)
		if not alive:
			col = Color(col.r * 0.5, col.g * 0.5, col.b * 0.5, 1.0)

		var p: Vector2 = tl + Vector2(x_cell * s, y_cell * s)
		var radius: float = clamp(3.0 * s, 3.0, 14.0)
		if selected_id != "" and String(cd.get("id", "")) == selected_id:
			draw_circle(p, radius + 5.0, Color(0.4, 0.8, 1.0, 0.9), 2.5)
		draw_circle(p, radius, col)

	# Help text
	if show_help:
		var line_view := "[보기] 위협(T): " + ("ON" if show_threat else "OFF")
		line_view += "  가치(V): " + ("ON" if show_value else "OFF")
		line_view += "  의지(I): " + ("ON" if show_will else "OFF")
		line_view += "  구조(U): " + ("ON" if show_coherence else "OFF")
		line_view += "  그리드(G): " + ("ON" if show_grid else "OFF")

		var line_map := "[지도] 숲/초목(Y): " + ("ON" if show_veg else "OFF")
		line_map += "  농경지(F): " + ("ON" if show_farm else "OFF")
		line_map += "  상단/캐러밴(C): " + ("ON" if show_demo_caravan else "OFF")

		var line_time := "[시간] 1~4: 시간 배속 (현재 x%.1f)" % sim_rate
		var line_ctrl := "[조작] 휠:줌  우/휠 드래그:이동  좌클릭:선택  F9/F10:재해"
		var line_color := "[색] 초록:숲  노랑:농지  파랑:강  붉은빛:위협  금색:가치"

		var lines := [line_view, line_map, line_time, line_ctrl, line_color]
		var y0 := vp.y - 96.0
		var font = get_tree().root.get_theme_default_font()
		if font:
			for l in lines:
				draw_string(font, Vector2(12, y0), l, HORIZONTAL_ALIGNMENT_LEFT, -1.0, 13, Color(0.92, 0.94, 0.96, 0.95))
				y0 += 16.0


func _update_demo_caravan(delta: float) -> void:
	if not show_demo_caravan:
		return
	if demo_civ_nodes.size() < 2:
		return

	for i in range(demo_caravans.size()):
		var c = demo_caravans[i]
		var t: float = float(c.get("t", 0.0))
		var dir: int = int(c.get("dir", 1))
		var speed: float = float(c.get("speed", 0.15))

		var step := speed * delta * sim_rate
		t += step * float(dir)
		if t >= 1.0:
			t = 1.0
			dir = -1
		elif t <= 0.0:
			t = 0.0
			dir = 1

		c["t"] = t
		c["dir"] = dir
		demo_caravans[i] = c


func _draw_demo_civ_and_caravan(tl: Vector2, s: float) -> void:
	if not show_demo_caravan:
		return
	if demo_civ_nodes.size() < 2:
		return

	var a_world: Vector2 = demo_civ_nodes[0].get("pos", Vector2.ZERO)
	var b_world: Vector2 = demo_civ_nodes[1].get("pos", Vector2.ZERO)
	var a_screen: Vector2 = tl + Vector2(a_world.x * s, a_world.y * s)
	var b_screen: Vector2 = tl + Vector2(b_world.x * s, b_world.y * s)
	draw_line(a_screen, b_screen, Color(0.7, 0.6, 0.4, 0.9), max(2.0, 0.012 * s * float(world_w)))
	# 실제 정착지/캐러밴 이미지는 Sprite2D 노드(spr_village_a/b, spr_caravan)가 담당하므로
	# 여기서는 도로만 그린다.
