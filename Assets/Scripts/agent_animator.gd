extends Node2D

@export var player_controller : PlayerController
@export var animation_player : AnimationPlayer
@export var sprite : Sprite2D

func _process(delta):
	if abs(player_controller.velocity.x) > 0.0:
		animation_player.play("move")
	else:
		animation_player.play("idle")
		
	if abs(player_controller.velocity.y) < 0.0:
		animation_player.play("jump")
	elif  abs(player_controller.velocity.y) > 0.0:
		animation_player.play("fall")
