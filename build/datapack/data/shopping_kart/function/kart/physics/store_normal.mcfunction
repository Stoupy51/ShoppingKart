
#> shopping_kart:kart/physics/store_normal
#
# @executed	facing entity @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] feet & rotated ~ 0 & positioned 0.0 0.0 0.0 & positioned ^ ^ ^1
#
# @within	shopping_kart:kart/physics/collide_kart [ facing entity @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] feet & rotated ~ 0 & positioned 0.0 0.0 0.0 & positioned ^ ^ ^1 ]
#			shopping_kart:kart/physics/collide_player [ facing entity @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] feet & rotated ~ 0 & positioned 0.0 0.0 0.0 & positioned ^ ^ ^1 ]
#

# The marker stands at n, the unit vector from the other body to the kart, so its position at scale 1000 is n
# Callers summon it from 0.0 0.0 0.0 and not 0 0 0, which would centre x and z on the block and add 0.5
execute store result score #nx shopping_kart.data run data get entity @s Pos[0] 1000
execute store result score #nz shopping_kart.data run data get entity @s Pos[2] 1000
scoreboard players operation #collision_x shopping_kart.data += #nx shopping_kart.data
scoreboard players operation #collision_z shopping_kart.data += #nz shopping_kart.data
kill @s

