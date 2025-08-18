
#> shopping_kart:kart/motion_from_input
#
# @executed	as @a[gamemode=!spectator,predicate=...] & at @s
#
# @within	shopping_kart:kart/player_moving
#

scoreboard players set #motion_x shopping_kart.data 0
scoreboard players set #motion_z shopping_kart.data 0

# Add motion depending on input
scoreboard players set #added shopping_kart.data 0
execute if predicate shopping_kart:input/forward rotated ~ 0 positioned 0 0 0 positioned ^ ^ ^10000 summon marker run function shopping_kart:kart/add_motion_from_marker_pos
execute if predicate shopping_kart:input/backward rotated ~ 0 positioned 0 0 0 positioned ^ ^ ^-10500 summon marker run function shopping_kart:kart/add_motion_from_marker_pos
execute if predicate shopping_kart:input/right rotated ~ 0 positioned 0 0 0 positioned ^-10000 ^ ^ summon marker run function shopping_kart:kart/add_motion_from_marker_pos
execute if predicate shopping_kart:input/left rotated ~ 0 positioned 0 0 0 positioned ^10000 ^ ^ summon marker run function shopping_kart:kart/add_motion_from_marker_pos

# Normalize motion if 2 inputs (divide by 1.41421356237 = sqrt(2))
execute if score #added shopping_kart.data matches 2 run function shopping_kart:kart/normalize_motion

