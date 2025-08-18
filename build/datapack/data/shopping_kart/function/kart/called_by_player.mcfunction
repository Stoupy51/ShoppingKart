
#> shopping_kart:kart/called_by_player
#
# @executed	at @s
#
# @within	shopping_kart:kart/effects/forced_acceleration
#			shopping_kart:kart/player_moving [ at @s[tag=!shopping_kart.forced_acceleration] ]
#

tag @s add shopping_kart.speed_up
execute if entity @s[tag=!shopping_kart.no_steering] run data modify entity @s Rotation set from storage shopping_kart:main Rotation
execute if entity @s[tag=shopping_kart.no_steering] run function shopping_kart:kart/effects/no_steering

function shopping_kart:kart/tick/calculations

