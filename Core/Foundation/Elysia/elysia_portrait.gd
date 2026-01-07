extends Node3D

var time: float = 0.0

var portrait: Sprite3D
var portrait_overlay: Sprite3D

@export var tex_neutral: Texture2D       # 기본
@export var tex_joy: Texture2D           # 기쁨
@export var tex_sad: Texture2D           # 슬픔
@export var tex_pout: Texture2D          # 삐짐
@export var tex_worry: Texture2D         # 걱정
@export var tex_happy: Texture2D         # 행복
@export var tex_relief: Texture2D        # 안도
@export var tex_curious: Texture2D       # 궁금
@export var tex_blue: Texture2D          # 울적
@export var tex_angry: Texture2D         # 분노
@export var tex_surprised: Texture2D     # 놀람

const DEFAULT_TEXTURE_PATH := "res://assets/icons/Gemini_Generated_Image_3f48fs3f48fs3f48.png"

# mood keys: neutral / joy / sad / pout / worry / happy / relief / curious / blue / angry / surprised
var mood: String = "neutral"
var react_strength: float = 0.0

var current_tex: Texture2D
var target_tex: Texture2D
var crossfade: float = 1.0


func _ready() -> void:
	# Camera
	if not has_node("Camera3D"):
		var cam := Camera3D.new()
		cam.name = "Camera3D"
		add_child(cam)
		cam.position = Vector3(0.0, 0.0, 2.6)
		cam.look_at(Vector3.ZERO, Vector3.UP)
		cam.current = true

	# Light
	if not has_node("Light"):
		var light := DirectionalLight3D.new()
		light.name = "Light"
		light.position = Vector3(0.0, 2.0, 2.0)
		light.rotation_degrees = Vector3(-45.0, 0.0, 0.0)
		add_child(light)

	# initial texture
	current_tex = tex_neutral
	if current_tex == null:
		var fallback := load(DEFAULT_TEXTURE_PATH)
		if fallback is Texture2D:
			current_tex = fallback

	# base portrait
	portrait = Sprite3D.new()
	portrait.name = "ElysiaPortrait"
	portrait.texture = current_tex
	portrait.pixel_size = 0.002
	portrait.position = Vector3(0.0, 0.0, 0.0)
	portrait.modulate = Color(1.0, 1.0, 1.0, 1.0)
	add_child(portrait)

	# overlay portrait (for crossfade)
	portrait_overlay = Sprite3D.new()
	portrait_overlay.name = "ElysiaPortraitOverlay"
	portrait_overlay.texture = current_tex
	portrait_overlay.pixel_size = portrait.pixel_size
	portrait_overlay.position = portrait.position
	portrait_overlay.modulate = Color(1.0, 1.0, 1.0, 0.0)
	portrait_overlay.visible = false
	add_child(portrait_overlay)


func _process(delta: float) -> void:
	time += delta
	react_strength = max(react_strength - delta * 2.0, 0.0)

	# Follow Elysia's current mood if a Client is present.
	var client := get_node_or_null("/root/Client")
	if client:
		var frame: Dictionary = client.peek_frame()
		if frame.has("elysia") and typeof(frame["elysia"]) == TYPE_DICTIONARY:
			var elysia_state: Dictionary = frame["elysia"]
			var mood_key := str(elysia_state.get("mood", mood))
			if mood_key != "" and mood_key != mood:
				set_mood(mood_key)

	if portrait:
		# breathing + floating
		var breathe_amount := sin(time * 1.5) * 0.03 + 1.0
		var mood_scale := 1.0 + react_strength * 0.08
		var scale_factor := breathe_amount * mood_scale

		var base_y := sin(time * 1.1) * 0.05 + react_strength * 0.03

		for sprite in [portrait, portrait_overlay]:
			if sprite:
				sprite.scale = Vector3(scale_factor, scale_factor, 1.0)
				sprite.position.y = base_y

		# color / tilt per mood
		var tint := Color(1.0, 1.0, 1.0, 1.0)
		var tilt_z := 0.0

		match mood:
			"joy", "happy":
				tint = Color(1.08, 1.03, 1.1, 1.0)
				tilt_z = sin(time * 3.0) * 1.5 * react_strength
			"sad", "blue":
				tint = Color(0.95, 0.98, 1.1, 1.0)
				tilt_z = 2.0 * (0.3 + react_strength)
			"pout":
				tint = Color(1.05, 0.97, 1.05, 1.0)
				tilt_z = -3.0 * (0.4 + react_strength)
			"worry":
				tint = Color(0.98, 0.98, 1.05, 1.0)
				tilt_z = sin(time * 4.0) * 1.0 * react_strength
			"relief":
				tint = Color(1.02, 1.05, 1.05, 1.0)
				tilt_z = -1.5 * react_strength
			"curious":
				tint = Color(1.0, 1.02, 1.08, 1.0)
				tilt_z = sin(time * 2.5) * 1.5 * react_strength
			"angry":
				tint = Color(1.1, 0.9, 0.95, 1.0)
				tilt_z = -2.0 * (0.5 + react_strength)
			"surprised":
				tint = Color(1.08, 1.08, 1.1, 1.0)
				tilt_z = sin(time * 6.0) * 2.0 * react_strength
			_:
				pass

		for sprite2 in [portrait, portrait_overlay]:
			if sprite2:
				sprite2.rotation_degrees.z = tilt_z
				var sprite_color := tint
				sprite_color.a = sprite2.modulate.a
				sprite2.modulate = sprite_color

	# texture crossfade
	if target_tex and portrait and portrait_overlay and crossfade < 1.0:
		crossfade = min(crossfade + delta * 3.0, 1.0)
		var t := crossfade
		portrait.modulate.a = 1.0 - t
		portrait_overlay.modulate.a = t
		portrait_overlay.visible = true

		if crossfade >= 1.0:
			current_tex = target_tex
			portrait.texture = current_tex
			portrait.modulate.a = 1.0
			portrait_overlay.visible = false
			portrait_overlay.modulate.a = 0.0
			target_tex = null

	# keyboard test mapping (임시)
	if Input.is_action_just_pressed("ui_accept") or Input.is_key_pressed(KEY_SPACE):
		react_as("joy")

	if Input.is_key_pressed(KEY_1):
		set_mood("neutral")
	if Input.is_key_pressed(KEY_2):
		react_as("joy")       # 기쁨 / 행복
	if Input.is_key_pressed(KEY_3):
		react_as("sad")       # 슬픔
	if Input.is_key_pressed(KEY_4):
		react_as("pout")      # 삐짐
	if Input.is_key_pressed(KEY_5):
		react_as("worry")     # 걱정
	if Input.is_key_pressed(KEY_6):
		react_as("relief")    # 안도
	if Input.is_key_pressed(KEY_7):
		react_as("curious")   # 궁금
	if Input.is_key_pressed(KEY_8):
		react_as("blue")      # 울적
	if Input.is_key_pressed(KEY_9):
		react_as("angry")     # 분노
	if Input.is_key_pressed(KEY_0):
		react_as("surprised") # 놀람


func _get_tex_for_mood(mood_key: String) -> Texture2D:
	match mood_key:
		"joy":
			return tex_joy if tex_joy else tex_neutral
		"sad":
			return tex_sad if tex_sad else tex_neutral
		"pout":
			return tex_pout if tex_pout else tex_neutral
		"worry":
			return tex_worry if tex_worry else tex_neutral
		"happy":
			return tex_happy if tex_happy else tex_joy if tex_joy else tex_neutral
		"relief":
			return tex_relief if tex_relief else tex_neutral
		"curious":
			return tex_curious if tex_curious else tex_neutral
		"blue":
			return tex_blue if tex_blue else tex_sad if tex_sad else tex_neutral
		"angry":
			return tex_angry if tex_angry else tex_neutral
		"surprised":
			return tex_surprised if tex_surprised else tex_neutral
		_:
			return tex_neutral


func set_mood(new_mood: String) -> void:
	mood = new_mood

	var new_tex := _get_tex_for_mood(new_mood)
	if new_tex and new_tex != current_tex:
		_start_crossfade_to(new_tex)


func react_as(new_mood: String) -> void:
	mood = new_mood
	react_strength = 1.0

	var new_tex := _get_tex_for_mood(new_mood)
	if new_tex and new_tex != current_tex:
		_start_crossfade_to(new_tex)


func _start_crossfade_to(texture: Texture2D) -> void:
	target_tex = texture
	if portrait_overlay:
		portrait_overlay.texture = texture
		portrait_overlay.visible = true
		portrait_overlay.modulate.a = 0.0
	crossfade = 0.0
