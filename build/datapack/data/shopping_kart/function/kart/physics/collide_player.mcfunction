
#> shopping_kart:kart/physics/collide_player
#
# @executed	at @s
#
# @within	shopping_kart:kart/physics/collisions [ at @s ]
#

execute facing entity @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] feet rotated ~ 0 positioned 0.0 0.0 0.0 positioned ^ ^ ^1 summon marker run function shopping_kart:kart/physics/store_normal
# The server does not track a player's velocity, so the player counts as standing still
scoreboard players set #rel_x shopping_kart.data 0
scoreboard players set #rel_z shopping_kart.data 0
scoreboard players operation #e shopping_kart.data = #restitution shopping_kart.data
execute unless function shopping_kart:kart/physics/impulse run return 0

# The player takes the opposite impulse, and player_motion counts 10000 per block per tick
scoreboard players operation $x player_motion.api.launch = #ix shopping_kart.data
scoreboard players operation $z player_motion.api.launch = #iz shopping_kart.data
scoreboard players operation $x player_motion.api.launch /= #1000 shopping_kart.data
scoreboard players operation $z player_motion.api.launch /= #1000 shopping_kart.data
scoreboard players operation $x player_motion.api.launch *= #-1 shopping_kart.data
scoreboard players operation $z player_motion.api.launch *= #-1 shopping_kart.data
scoreboard players operation $y player_motion.api.launch = #player_lift shopping_kart.data
function player_motion:api/launch_xyz

