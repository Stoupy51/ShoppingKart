
#> shopping_kart:kart/normalize_motion
#
# @executed	as @a[gamemode=!spectator,predicate=...] & at @s
#
# @within	shopping_kart:kart/motion_from_input
#

# Normalize motion (divide by 1.41421356237 = sqrt(2))
scoreboard players operation #motion_x shopping_kart.data *= #10000 shopping_kart.data
scoreboard players operation #motion_x shopping_kart.data /= #14142 shopping_kart.data

scoreboard players operation #motion_z shopping_kart.data *= #10000 shopping_kart.data
scoreboard players operation #motion_z shopping_kart.data /= #14142 shopping_kart.data

