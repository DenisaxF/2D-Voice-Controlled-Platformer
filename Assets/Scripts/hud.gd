extends CanvasLayer
class_name HUD

@export var energy_cell_label : Label

func update_energy_cell_label(number):
	energy_cell_label.text = "x " + str(number)
