extends Node

var energy_cells = 0

func _ready() -> void:
	reset_energy_cells()
	
func get_hud():
	return get_tree().get_first_node_in_group("hud")
	
func add_energy_cell():
	energy_cells += 1
	var hud = get_hud()
	if hud:
		hud.update_energy_cell_label(energy_cells)
	print(energy_cells)
	
func reset_energy_cells():
	energy_cells = 0
	var hud = get_hud()
	if hud:
		hud.update_energy_cell_label(energy_cells)
