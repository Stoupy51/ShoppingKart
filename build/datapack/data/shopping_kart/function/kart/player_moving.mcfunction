
#> shopping_kart:kart/player_moving
#
# @within	shopping_kart:v1.3.1/tick
#

tag @s add shopping_kart.temp

# Store player motion and call function to the vehicle (Old code < 1.21)
# execute store result score #motion_x shopping_kart.data run data get entity @s Motion[0] 1000000
# execute store result score #motion_z shopping_kart.data run data get entity @s Motion[2] 1000000

# Store player motion and call function to the vehicle (New code >= 1.21)
function shopping_kart:kart/motion_from_input

data modify storage shopping_kart:main Rotation set from entity @s Rotation
scoreboard players set #instant_engine_max shopping_kart.data 0

execute on vehicle at @s[tag=!shopping_kart.forced_acceleration] run function shopping_kart:kart/called_by_player

data remove storage shopping_kart:main Rotation
tag @s remove shopping_kart.temp

scoreboard players set #motion_x shopping_kart.data 0
scoreboard players set #motion_z shopping_kart.data 0

