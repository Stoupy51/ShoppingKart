
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup kart physics functions
def setup_kart_physics_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:kart/physics/apply_motion", f"""
## Apply new motion & update old motion (80% or 96.66% of new motion)
# Depending on the surface, the kart will slide or not
data modify entity @s Motion[0] set from storage {ns}:main Motion[0]
data modify entity @s Motion[2] set from storage {ns}:main Motion[2]
execute if score #surface {ns}.data matches 0..1 store result score @s {ns}.motion_x run data get storage {ns}:main Motion[0] 8000000
execute if score #surface {ns}.data matches 0..1 store result score @s {ns}.motion_z run data get storage {ns}:main Motion[2] 8000000
execute if score #surface {ns}.data matches 2 store result score @s {ns}.motion_x run data get storage {ns}:main Motion[0] 9777777
execute if score #surface {ns}.data matches 2 store result score @s {ns}.motion_z run data get storage {ns}:main Motion[2] 9777777
execute if score #surface {ns}.data matches 3..4 store result score @s {ns}.motion_x run data get storage {ns}:main Motion[0] 8000000
execute if score #surface {ns}.data matches 3..4 store result score @s {ns}.motion_z run data get storage {ns}:main Motion[2] 8000000
data remove storage {ns}:main Motion
""")

	write_function(f"{ns}:kart/physics/calculation", f"""
# Define multiplier depending on engine speed & block stepping on
# Surface : 0 = normal, 1 = fast, 2 = slippery, 3 = slow, 4 = very slow
# When in air : surface = 0
function {ns}:kart/physics/get_surface

scoreboard players operation #engine {ns}.data = @s {ns}.engine
execute if score #surface {ns}.data matches 0..1 run scoreboard players set #multiplier {ns}.data 10
execute if score #surface {ns}.data matches 2 run scoreboard players set #multiplier {ns}.data 3
execute if score #surface {ns}.data matches 3..4 run scoreboard players set #multiplier {ns}.data 1
execute if score #surface {ns}.data matches 0 run scoreboard players operation #engine {ns}.data /= #20 {ns}.data
execute if score #surface {ns}.data matches 1 run scoreboard players operation #engine {ns}.data /= #15 {ns}.data
execute if score #surface {ns}.data matches 2 run scoreboard players operation #engine {ns}.data /= #120 {ns}.data
execute if score #surface {ns}.data matches 3 run scoreboard players operation #engine {ns}.data /= #30 {ns}.data
execute if score #surface {ns}.data matches 4 run scoreboard players operation #engine {ns}.data /= #60 {ns}.data
scoreboard players operation #multiplier {ns}.data += #engine {ns}.data
execute if score @s {ns}.reactor_boost matches 1.. run scoreboard players operation #multiplier {ns}.data *= #2 {ns}.data


## Stop motion when predicted position isn't reached
execute store result score #new_pos_x {ns}.data run data get entity @s Pos[0] 10000
execute store result score #new_pos_z {ns}.data run data get entity @s Pos[2] 10000
execute store result score #pos_y {ns}.data run data get entity @s Pos[1] 10
execute if score #pos_y {ns}.data = @s {ns}.old_pos_y run function {ns}:kart/physics/check_predictions
scoreboard players operation @s {ns}.old_pos_y = #pos_y {ns}.data
scoreboard players operation @s {ns}.predicted_pos_x = #new_pos_x {ns}.data
scoreboard players operation @s {ns}.predicted_pos_z = #new_pos_z {ns}.data



## Calculate new motion : motion = (player motion * multiplier) + old_motion + booster + collisions
# If player motion is null : motion = old_motion
scoreboard players set #booster {ns}.data 0
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=west] run scoreboard players set #booster {ns}.data 1
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=east] run scoreboard players set #booster {ns}.data 2
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=north] run scoreboard players set #booster {ns}.data 3
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=south] run scoreboard players set #booster {ns}.data 4


execute if score @s {ns}.collision_factor matches 1.. run function {ns}:kart/physics/collisions


## Store calculated motion into storage {ns}:main Motion[0] & Motion[2]
data modify storage {ns}:main Motion set value [0.0d, 0.0d, 0.0d]
scoreboard players set #new_motion_x {ns}.data 0
scoreboard players set #new_motion_z {ns}.data 0
execute unless score @s {ns}.engine matches 0 run scoreboard players operation #new_motion_x {ns}.data = #motion_x {ns}.data
execute unless score @s {ns}.engine matches 0 run scoreboard players operation #new_motion_x {ns}.data *= #multiplier {ns}.data
scoreboard players operation #new_motion_x {ns}.data += @s {ns}.motion_x
execute unless score @s {ns}.engine matches 0 run scoreboard players operation #new_motion_z {ns}.data = #motion_z {ns}.data
execute unless score @s {ns}.engine matches 0 run scoreboard players operation #new_motion_z {ns}.data *= #multiplier {ns}.data
scoreboard players operation #new_motion_z {ns}.data += @s {ns}.motion_z
execute unless score #booster {ns}.data matches 0 run function {ns}:kart/effects/booster
execute store result storage {ns}:main Motion[0] double 0.0000001 run scoreboard players get #new_motion_x {ns}.data
execute store result storage {ns}:main Motion[2] double 0.0000001 run scoreboard players get #new_motion_z {ns}.data
scoreboard players set #motion_x {ns}.data 0
scoreboard players set #motion_z {ns}.data 0
# tellraw @a {{"score":{{"name":"#new_motion_x","objective":"{ns}.data"}},"color":"red"}}
# tellraw @a {{"score":{{"name":"#new_motion_z","objective":"{ns}.data"}},"color":"blue"}}
""")

	write_function(f"{ns}:kart/physics/check_predictions", f"""
## Stop motion when predicted position isn't reached
scoreboard players operation @s {ns}.predicted_pos_x -= #new_pos_x {ns}.data
scoreboard players operation @s {ns}.predicted_pos_z -= #new_pos_z {ns}.data
scoreboard players operation @s {ns}.predicted_pos_x *= #10 {ns}.data
scoreboard players operation @s {ns}.predicted_pos_z *= #10 {ns}.data
scoreboard players operation @s {ns}.predicted_pos_x /= @s {ns}.engine
scoreboard players operation @s {ns}.predicted_pos_z /= @s {ns}.engine
scoreboard players add @s[scores={{{ns}.predicted_pos_x=0}}] {ns}.predicted_pos_x 1
scoreboard players add @s[scores={{{ns}.predicted_pos_z=0}}] {ns}.predicted_pos_z 1
execute if score @s {ns}.engine matches 100.. if score @s {ns}.predicted_pos_x matches -2..2 unless score @s {ns}.predicted_pos_z matches -3..3 run function {ns}:kart/stop_motion
execute if score @s {ns}.engine matches 100.. if score @s {ns}.predicted_pos_z matches -2..2 unless score @s {ns}.predicted_pos_x matches -3..3 run function {ns}:kart/stop_motion
""")

	write_function(f"{ns}:kart/physics/collide_kart", f"""
execute facing entity @n[tag={ns}.kart,tag={ns}.temp,distance=..1] feet rotated ~ 0 positioned 0.0 0.0 0.0 positioned ^ ^ ^1 summon marker run function {ns}:kart/physics/store_normal
scoreboard players operation #rel_x {ns}.data = @s {ns}.motion_x
scoreboard players operation #rel_z {ns}.data = @s {ns}.motion_z
scoreboard players operation #e {ns}.data = #restitution {ns}.data
scoreboard players operation #e {ns}.data < @s {ns}.restitution
execute unless function {ns}:kart/physics/impulse run return 0
scoreboard players operation @s {ns}.motion_x -= #ix {ns}.data
scoreboard players operation @s {ns}.motion_z -= #iz {ns}.data
function {ns}:kart/signal_parties/add_victim
execute as @n[tag={ns}.kart,tag={ns}.temp,distance=..1] run function {ns}:kart/signal_parties/add_attacker
function #{ns}:signals/kart_collision
tag @e[tag={ns}.attacker] remove {ns}.attacker
tag @e[tag={ns}.victim] remove {ns}.victim
""")

	write_function(f"{ns}:kart/physics/collide_player", f"""
execute facing entity @n[tag={ns}.kart,tag={ns}.temp,distance=..1] feet rotated ~ 0 positioned 0.0 0.0 0.0 positioned ^ ^ ^1 summon marker run function {ns}:kart/physics/store_normal
# The server does not track a player's velocity, so the player counts as standing still
scoreboard players set #rel_x {ns}.data 0
scoreboard players set #rel_z {ns}.data 0
scoreboard players operation #e {ns}.data = #restitution {ns}.data
execute unless function {ns}:kart/physics/impulse run return 0

# The server sees a launched player move a tick later or more, so a kart still closing in on them the next tick is the same hit
execute store result score #now {ns}.data run time query gametime
scoreboard players operation #since_hit {ns}.data = #now {ns}.data
scoreboard players operation #since_hit {ns}.data -= @s {ns}.hit_tick
scoreboard players operation @s {ns}.hit_tick = #now {ns}.data
execute if score #since_hit {ns}.data matches 1 run scoreboard players operation #vx {ns}.data -= #ix {ns}.data
execute if score #since_hit {ns}.data matches 1 run scoreboard players operation #vz {ns}.data -= #iz {ns}.data
execute if score #since_hit {ns}.data matches 1 run return 0

# The player takes the opposite impulse, and player_motion counts 10000 per block per tick
scoreboard players operation $x player_motion.api.launch = #ix {ns}.data
scoreboard players operation $z player_motion.api.launch = #iz {ns}.data
scoreboard players operation $x player_motion.api.launch /= #1000 {ns}.data
scoreboard players operation $z player_motion.api.launch /= #1000 {ns}.data
scoreboard players operation $x player_motion.api.launch *= #-1 {ns}.data
scoreboard players operation $z player_motion.api.launch *= #-1 {ns}.data
scoreboard players operation $y player_motion.api.launch = #player_lift {ns}.data
function player_motion:api/launch_xyz
tag @s add {ns}.victim
execute as @n[tag={ns}.kart,tag={ns}.temp,distance=..1] run function {ns}:kart/signal_parties/add_attacker
function #{ns}:signals/player_hit
tag @e[tag={ns}.attacker] remove {ns}.attacker
tag @s remove {ns}.victim
""")

	write_function(f"{ns}:kart/physics/collisions", f"""
# Vanilla never pushes an entity carrying passengers, so karts collide here with the karts and players on foot they touch
# Velocities are the motion scores, in 10^-7 block per tick, and a kart with a factor of 0 takes no part on either side
scoreboard players operation #vx {ns}.data = @s {ns}.motion_x
scoreboard players operation #vz {ns}.data = @s {ns}.motion_z
scoreboard players operation #restitution {ns}.data = @s {ns}.restitution
scoreboard players set #collision_x {ns}.data 0
scoreboard players set #collision_z {ns}.data 0
execute as @e[tag={ns}.kart,distance=0.01..0.9,scores={{{ns}.collision_factor=1..}}] at @s run function {ns}:kart/physics/collide_kart
execute as @a[gamemode=!spectator,predicate=!{ns}:has_vehicle,distance=0.01..0.75] at @s run function {ns}:kart/physics/collide_player

# Push apart along the summed unit vectors at scale 1000: halved, a factor of 1000 gives the 0.05 block per tick of vanilla
scoreboard players operation #collision_x {ns}.data *= @s {ns}.collision_factor
scoreboard players operation #collision_z {ns}.data *= @s {ns}.collision_factor
scoreboard players operation #collision_x {ns}.data /= #2 {ns}.data
scoreboard players operation #collision_z {ns}.data /= #2 {ns}.data
scoreboard players operation #vx {ns}.data += #collision_x {ns}.data
scoreboard players operation #vz {ns}.data += #collision_z {ns}.data
scoreboard players operation @s {ns}.motion_x = #vx {ns}.data
scoreboard players operation @s {ns}.motion_z = #vz {ns}.data
""")

	write_function(f"{ns}:kart/signal_parties/add_attacker", f"""
tag @s add {ns}.attacker
execute on passengers if entity @s[type=player] run tag @s add {ns}.attacker
""")

	write_function(f"{ns}:kart/signal_parties/add_victim", f"""
tag @s add {ns}.victim
execute on passengers if entity @s[type=player] run tag @s add {ns}.victim
""")

	write_function(f"{ns}:kart/physics/get_surface", f"""
# Define multiplier depending on engine speed & block stepping on
# Surface : 0 = normal, 1 = fast, 2 = slippery, 3 = slow, 4 = very slow
# When in air : surface = 0
scoreboard players set #surface {ns}.data 0
execute if entity @s[tag=!{ns}.in_water] if block ~ ~-.1 ~ #{ns}:kart_surfaces/fast run scoreboard players set #surface {ns}.data 1
execute if entity @s[tag=!{ns}.in_water] if block ~ ~-.1 ~ #{ns}:kart_surfaces/slippery run scoreboard players set #surface {ns}.data 2
execute if entity @s[tag=!{ns}.in_water] if block ~ ~-.1 ~ #{ns}:kart_surfaces/slow run scoreboard players set #surface {ns}.data 3
execute if entity @s[tag=!{ns}.in_water] if block ~ ~-.1 ~ #{ns}:kart_surfaces/very_slow run scoreboard players set #surface {ns}.data 4
execute if entity @s[tag={ns}.no_grip] run scoreboard players set #surface {ns}.data 2
""")

	write_function(f"{ns}:kart/physics/impulse", f"""
# Impulse between equal masses along n, the unit vector from the other body to the kart: j = -(1 + e) (v_kart - v_other) . n / 2
# Takes #vx/#vz the kart's velocity, #rel_x/#rel_z the other body's, #nx/#nz the normal at scale 1000 and #e the restitution at scale 1000
# Adds #ix/#iz, the velocity j n, to #vx/#vz; the caller takes it from the other body

# Closing speed (v_other - v_kart) . n at scale 10^7, divided by 1000 before the products so they fit in an int
scoreboard players operation #rel_x {ns}.data -= #vx {ns}.data
scoreboard players operation #rel_z {ns}.data -= #vz {ns}.data
scoreboard players operation #rel_x {ns}.data /= #1000 {ns}.data
scoreboard players operation #rel_z {ns}.data /= #1000 {ns}.data
scoreboard players operation #rel_x {ns}.data *= #nx {ns}.data
scoreboard players operation #rel_z {ns}.data *= #nz {ns}.data
scoreboard players operation #j {ns}.data = #rel_x {ns}.data
scoreboard players operation #j {ns}.data += #rel_z {ns}.data
execute if score #j {ns}.data matches ..0 run return fail

# j at scale 10^4, capped at 1 block per tick
scoreboard players add #e {ns}.data 1000
scoreboard players operation #j {ns}.data /= #1000 {ns}.data
scoreboard players operation #j {ns}.data *= #e {ns}.data
scoreboard players operation #j {ns}.data /= #1000 {ns}.data
scoreboard players operation #j {ns}.data /= #2 {ns}.data
scoreboard players operation #j {ns}.data < #10000 {ns}.data
scoreboard players operation #ix {ns}.data = #nx {ns}.data
scoreboard players operation #iz {ns}.data = #nz {ns}.data
scoreboard players operation #ix {ns}.data *= #j {ns}.data
scoreboard players operation #iz {ns}.data *= #j {ns}.data
scoreboard players operation #vx {ns}.data += #ix {ns}.data
scoreboard players operation #vz {ns}.data += #iz {ns}.data
return 1
""")

	write_function(f"{ns}:kart/physics/predict_position", f"""
## Try to predict position after 1 tick
# (new_pos = old_pos + new_motion)
scoreboard players operation #new_motion_x {ns}.data /= #1000 {ns}.data
scoreboard players operation #new_motion_z {ns}.data /= #1000 {ns}.data
scoreboard players operation @s {ns}.predicted_pos_x += #new_motion_x {ns}.data
scoreboard players operation @s {ns}.predicted_pos_z += #new_motion_z {ns}.data
""")

	write_function(f"{ns}:kart/physics/store_normal", f"""
# The marker stands at n, the unit vector from the other body to the kart, so its position at scale 1000 is n
# Callers summon it from 0.0 0.0 0.0 and not 0 0 0, which would centre x and z on the block and add 0.5
execute store result score #nx {ns}.data run data get entity @s Pos[0] 1000
execute store result score #nz {ns}.data run data get entity @s Pos[2] 1000
scoreboard players operation #collision_x {ns}.data += #nx {ns}.data
scoreboard players operation #collision_z {ns}.data += #nz {ns}.data
kill @s
""")

	write_function(f"{ns}:kart/physics/water", f"""
## Water specification
execute if entity @s[tag={ns}.in_water,scores={{{ns}.engine=1300..}}] run data modify entity @s Motion[1] set value 0.65d
execute unless block ~ ~ ~ water run tag @s remove {ns}.in_water
execute if block ~ ~ ~ water run tag @s add {ns}.in_water
execute if entity @s[tag={ns}.in_water,scores={{{ns}.engine=750..}}] if block ~ ~ ~ water run data modify entity @s Motion[1] set value -0.5d
""")

