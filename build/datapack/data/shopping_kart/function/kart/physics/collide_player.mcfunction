
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

# The server sees a launched player move a tick later or more, so a kart still closing in on them the next tick is the same hit
execute store result score #now shopping_kart.data run time query gametime
scoreboard players operation #since_hit shopping_kart.data = #now shopping_kart.data
scoreboard players operation #since_hit shopping_kart.data -= @s shopping_kart.hit_tick
scoreboard players operation @s shopping_kart.hit_tick = #now shopping_kart.data
execute if score #since_hit shopping_kart.data matches 1 run scoreboard players operation #vx shopping_kart.data -= #ix shopping_kart.data
execute if score #since_hit shopping_kart.data matches 1 run scoreboard players operation #vz shopping_kart.data -= #iz shopping_kart.data
execute if score #since_hit shopping_kart.data matches 1 run return 0

# The player takes the opposite impulse, and player_motion counts 10000 per block per tick
scoreboard players operation $x player_motion.api.launch = #ix shopping_kart.data
scoreboard players operation $z player_motion.api.launch = #iz shopping_kart.data
scoreboard players operation $x player_motion.api.launch /= #1000 shopping_kart.data
scoreboard players operation $z player_motion.api.launch /= #1000 shopping_kart.data
scoreboard players operation $x player_motion.api.launch *= #-1 shopping_kart.data
scoreboard players operation $z player_motion.api.launch *= #-1 shopping_kart.data
scoreboard players operation $y player_motion.api.launch = #player_lift shopping_kart.data
function player_motion:api/launch_xyz
tag @s add shopping_kart.victim
execute as @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..1] run function shopping_kart:kart/signal_parties/add_attacker
function #shopping_kart:signals/player_hit
tag @e[tag=shopping_kart.attacker] remove shopping_kart.attacker
tag @s remove shopping_kart.victim

