extends Control


func _on_button_pressed() -> void:
	GameManager.reset_energy_cells()
	get_tree().change_scene_to_file("res://Assets/Scenes/Areas/area_1.tscn")


func _on_button_2_pressed() -> void:
	get_tree().quit()
