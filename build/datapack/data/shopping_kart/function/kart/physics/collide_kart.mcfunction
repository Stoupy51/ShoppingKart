
#> shopping_kart:kart/physics/collide_kart
#
# @executed	at @s
#
# @within	shopping_kart:kart/physics/collisions [ at @s ]
#

execute facing entity @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] feet rotated ~ 0 positioned 0.0 0.0 0.0 positioned ^ ^ ^1 summon marker run function shopping_kart:kart/physics/store_normal
scoreboard players operation #rel_x shopping_kart.data = @s shopping_kart.motion_x
scoreboard players operation #rel_z shopping_kart.data = @s shopping_kart.motion_z
scoreboard players operation #e shopping_kart.data = #restitution shopping_kart.data
scoreboard players operation #e shopping_kart.data < @s shopping_kart.restitution
execute unless function shopping_kart:kart/physics/impulse run return 0
scoreboard players operation @s shopping_kart.motion_x -= #ix shopping_kart.data
scoreboard players operation @s shopping_kart.motion_z -= #iz shopping_kart.data

