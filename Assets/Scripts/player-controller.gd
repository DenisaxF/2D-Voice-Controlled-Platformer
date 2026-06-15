extends CharacterBody2D
class_name PlayerController

@export var forward_speed = 100.0
@export var jump_up_speed = -250.0
@export var jump_up_speed_max = -450.0

const PITCH_SILENCE = 120
const PITCH_WALK_MAX = 420
const PITCH_JUMP_MAX = 650

var socket = PacketPeerUDP.new()
var last_voice_time = 0.0
var pitch = 0.0

var is_jumping = false
var jump_start_y = 0.0
var jump_peak_y = 0.0
var jump_start_pitch = 0.0
var jump_force_logged = 0.0
var has_left_floor = false

var jump_log = FileAccess.open("user://jump_log.csv", FileAccess.WRITE)
var latency_log = FileAccess.open("user://latency_log.csv", FileAccess.WRITE)

func _ready():
	socket.bind(5005)
	jump_log.store_line("timestamp,pitch,jump_force,jump_height_px")
	latency_log.store_line("timestamp,latency_ms,chunk_size")

func _physics_process(delta: float) -> void:
	# Gravitație
	if not is_on_floor():
		velocity += get_gravity() * delta

	# ── Citește ultimul pachet UDP ──
	if socket.get_available_packet_count() > 0:
		var msg = ""
		while socket.get_available_packet_count() > 0:
			msg = socket.get_packet().get_string_from_utf8()

		var parts = msg.split(",")
		pitch = clamp(parts[0].to_float(), 0.0, 1500.0)

		if parts.size() > 1:
			var send_time = parts[1].to_float()
			var receive_time = Time.get_unix_time_from_system()
			var latency_ms = (receive_time - send_time) * 1000.0
			var chunk_size = parts[2] if parts.size() > 2 else "?"

			# Loghează latența în CSV
			latency_log.store_line("%d,%.2f,%s" % [
				Time.get_ticks_msec(),
				latency_ms,
				chunk_size
			])
			latency_log.flush()

		last_voice_time = Time.get_ticks_msec()

	# Dacă n-a venit semnal de 200ms → tăcere
	if Time.get_ticks_msec() - last_voice_time > 200:
		pitch = 0.0

	# ── Logică de mișcare ──
	if pitch < PITCH_SILENCE:
		velocity.x = 0.0
	elif pitch < PITCH_WALK_MAX:
		velocity.x = forward_speed
	else:
		var t = clamp((pitch - PITCH_WALK_MAX) / (PITCH_JUMP_MAX - PITCH_WALK_MAX), 0.0, 1.0)
		velocity.x = forward_speed
		if is_on_floor():
			velocity.y = lerp(jump_up_speed, jump_up_speed_max, t)
			jump_start_pitch = pitch
			jump_force_logged = velocity.y
			jump_start_y = global_position.y
			jump_peak_y = global_position.y
			is_jumping = true
			has_left_floor = false

	# Confirmă că a părăsit podeaua
	if is_jumping and not is_on_floor():
		has_left_floor = true
		if global_position.y < jump_peak_y:
			jump_peak_y = global_position.y

	# Loghează după aterizare
	if is_jumping and has_left_floor and is_on_floor():
		var jump_height = abs(jump_start_y - jump_peak_y)
		jump_log.store_line("%d,%.2f,%.2f,%.2f" % [
			Time.get_ticks_msec(),
			jump_start_pitch,
			jump_force_logged,
			jump_height
		])
		jump_log.flush()
		is_jumping = false
		has_left_floor = false

	# ── Debug label ──
	var debug_label = get_node_or_null("DebugLabel")
	if debug_label:
		if pitch < PITCH_SILENCE:
			debug_label.text = "STOP | %.0f Hz" % pitch
		elif pitch < PITCH_WALK_MAX:
			debug_label.text = "MERS | %.0f Hz" % pitch
		else:
			debug_label.text = "SARE | %.0f Hz" % pitch
	
	if global_position.y > 1000:
		get_tree().change_scene_to_file("res://Assets/Scenes/game_over.tscn")

	move_and_slide()
