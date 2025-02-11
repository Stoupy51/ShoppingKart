
#> shopping_kart:kart/add_motion_from_marker_pos
#
# @within	shopping_kart:kart/motion_from_input
#

# Collect marker position
execute store result score #temp_x shopping_kart.data run data get entity @s Pos[0] 1.5
execute store result score #temp_z shopping_kart.data run data get entity @s Pos[2] 1.5

# Add marker position to motion
scoreboard players operation #motion_x shopping_kart.data += #temp_x shopping_kart.data
scoreboard players operation #motion_z shopping_kart.data += #temp_z shopping_kart.data

# Remember the number of added motion (for normalizing)
scoreboard players add #added shopping_kart.data 1

# Remove marker
kill @s

