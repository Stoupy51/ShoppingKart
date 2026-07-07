
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



## Calculate new motion : motion = (player motion * multiplier) + old_motion + booster
# If player motion is null : motion = old_motion
scoreboard players set #booster {ns}.data 0
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=west] run scoreboard players set #booster {ns}.data 1
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=east] run scoreboard players set #booster {ns}.data 2
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=north] run scoreboard players set #booster {ns}.data 3
execute if score #booster {ns}.data matches 0 if block ~ ~-1 ~ magenta_glazed_terracotta[facing=south] run scoreboard players set #booster {ns}.data 4


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

	write_function(f"{ns}:kart/physics/predict_position", f"""
## Try to predict position after 1 tick
# (new_pos = old_pos + new_motion)
scoreboard players operation #new_motion_x {ns}.data /= #1000 {ns}.data
scoreboard players operation #new_motion_z {ns}.data /= #1000 {ns}.data
scoreboard players operation @s {ns}.predicted_pos_x += #new_motion_x {ns}.data
scoreboard players operation @s {ns}.predicted_pos_z += #new_motion_z {ns}.data
""")

	write_function(f"{ns}:kart/physics/water", f"""
## Water specification
execute if entity @s[tag={ns}.in_water,scores={{{ns}.engine=1300..}}] run data modify entity @s Motion[1] set value 0.65d
execute unless block ~ ~ ~ water run tag @s remove {ns}.in_water
execute if block ~ ~ ~ water run tag @s add {ns}.in_water
execute if entity @s[tag={ns}.in_water,scores={{{ns}.engine=750..}}] if block ~ ~ ~ water run data modify entity @s Motion[1] set value -0.5d
""")

