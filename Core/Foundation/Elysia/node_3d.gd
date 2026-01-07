extends Node3D

var time: float = 0.0

var girl_root: Node3D
var head: MeshInstance3D
var hair_back: MeshInstance3D
var iris_mat: StandardMaterial3D


func _ready() -> void:
	# 3D 카메라가 없으면 하나 만들어서 붙입니다.
	if not has_node("Camera3D"):
		var cam := Camera3D.new()
		cam.name = "Camera3D"
		add_child(cam)
		cam.position = Vector3(0.0, 1.6, 4.0)
		cam.look_at(Vector3(0.0, 1.0, 0.0), Vector3.UP)
		cam.current = true

	# 간단한 방향성 조명
	if not has_node("Light"):
		var light := DirectionalLight3D.new()
		light.name = "Light"
		light.position = Vector3(0.0, 4.0, 0.0)
		light.rotation_degrees = Vector3(-45.0, 45.0, 0.0)
		add_child(light)

	# 엘리시아 소녀 루트
	girl_root = Node3D.new()
	girl_root.name = "ElysiaGirl"
	add_child(girl_root)

	# 재질 설정
	var skin_mat := StandardMaterial3D.new()
	skin_mat.albedo_color = Color(1.0, 0.86, 0.95)

	var dress_mat := StandardMaterial3D.new()
	dress_mat.albedo_color = Color(0.85, 0.7, 1.0)
	dress_mat.emission = Color(0.9, 0.6, 1.5)
	dress_mat.emission_energy = 0.4

	var hair_mat := StandardMaterial3D.new()
	hair_mat.albedo_color = Color(0.7, 0.6, 1.0)

	var eye_white_mat := StandardMaterial3D.new()
	eye_white_mat.albedo_color = Color(1.0, 1.0, 1.0)

	iris_mat = StandardMaterial3D.new()
	iris_mat.albedo_color = Color(0.5, 0.2, 0.8)
	iris_mat.emission = Color(0.8, 0.4, 1.4)
	iris_mat.emission_energy = 0.3

	# 몸통 (원피스 실루엣)
	var body := MeshInstance3D.new()
	body.name = "Body"
	var body_mesh := CapsuleMesh.new()
	body_mesh.radius = 0.3
	body_mesh.height = 1.0
	body.mesh = body_mesh
	body.position = Vector3(0.0, 0.5, 0.0)
	body.set_surface_override_material(0, dress_mat)
	girl_root.add_child(body)

	# 머리
	head = MeshInstance3D.new()
	head.name = "Head"
	var head_mesh := SphereMesh.new()
	head_mesh.radius = 0.32
	head.mesh = head_mesh
	head.position = Vector3(0.0, 1.2, 0.0)
	head.set_surface_override_material(0, skin_mat)
	girl_root.add_child(head)

	# 머리카락 (뒤로 내려오는 덩어리)
	hair_back = MeshInstance3D.new()
	hair_back.name = "HairBack"
	var hair_mesh := CapsuleMesh.new()
	hair_mesh.radius = 0.23
	hair_mesh.height = 0.9
	hair_back.mesh = hair_mesh
	hair_back.position = Vector3(0.0, 1.0, -0.18)
	hair_back.rotation_degrees = Vector3(15.0, 0.0, 0.0)
	hair_back.set_surface_override_material(0, hair_mat)
	girl_root.add_child(hair_back)

	# 눈 (흰자)
	var eye_l := MeshInstance3D.new()
	var eye_r := MeshInstance3D.new()
	eye_l.name = "EyeL"
	eye_r.name = "EyeR"
	var eye_mesh := SphereMesh.new()
	eye_mesh.radius = 0.07
	eye_l.mesh = eye_mesh
	eye_r.mesh = eye_mesh
	eye_l.position = Vector3(-0.11, 1.23, 0.28)
	eye_r.position = Vector3(0.11, 1.23, 0.28)
	eye_l.set_surface_override_material(0, eye_white_mat)
	eye_r.set_surface_override_material(0, eye_white_mat)
	girl_root.add_child(eye_l)
	girl_root.add_child(eye_r)

	# 동공 (보라색)
	var pupil_mesh := SphereMesh.new()
	pupil_mesh.radius = 0.045

	var pupil_l := MeshInstance3D.new()
	pupil_l.name = "PupilL"
	pupil_l.mesh = pupil_mesh
	pupil_l.position = eye_l.position + Vector3(0.0, -0.01, 0.03)
	pupil_l.set_surface_override_material(0, iris_mat)
	girl_root.add_child(pupil_l)

	var pupil_r := MeshInstance3D.new()
	pupil_r.name = "PupilR"
	pupil_r.mesh = pupil_mesh
	pupil_r.position = eye_r.position + Vector3(0.0, -0.01, 0.03)
	pupil_r.set_surface_override_material(0, iris_mat)
	girl_root.add_child(pupil_r)


func _process(delta: float) -> void:
	time += delta

	if girl_root:
		# 숨쉬는 것처럼 살짝 위아래로 움직이고 세로 방향만 부드럽게 늘어납니다.
		var breathe := sin(time * 2.0) * 0.05 + 1.0
		girl_root.scale = Vector3(1.0, breathe, 1.0)
		girl_root.position.y = sin(time * 1.2) * 0.05

	if head:
		# 고개를 살짝살짝 좌우로 끄덕이는 느낌
		head.rotation_degrees.y = sin(time * 1.5) * 5.0

	if hair_back:
		# 머리카락이 아주 약하게 따라 흔들립니다.
		hair_back.rotation_degrees.x = 15.0 + sin(time * 2.5) * 4.0

	if iris_mat:
		# 눈에 은은한 보라색 반짝임
		var glow := (sin(time * 3.0) + 1.0) * 0.5
		iris_mat.emission_energy = 0.3 + glow * 0.3

	# 스페이스나 엔터를 누르면 살짝 부끄러운 듯 리액션
	if Input.is_action_just_pressed("ui_accept") or Input.is_key_pressed(KEY_SPACE):
		_react_shy()


func _react_shy() -> void:
	if not girl_root:
		return

	girl_root.scale = Vector3(1.05, 1.1, 1.05)

	if head:
		head.rotation_degrees.z = -6.0

	var body := girl_root.get_node_or_null("Body") as MeshInstance3D
	if body:
		var dress_mat := body.get_surface_override_material(0)
		if dress_mat:
			dress_mat.emission_energy = 1.0
