
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup kart effects functions
def setup_kart_effects_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:kart/effects/booster", f"""
execute if score @s {ns}.booster_timer matches 0 if score #booster {ns}.data matches 1..2 run scoreboard players operation #old {ns}.data = #new_motion_x {ns}.data
execute if score @s {ns}.booster_timer matches 0 if score #booster {ns}.data matches 3..4 run scoreboard players operation #old {ns}.data = #new_motion_z {ns}.data
execute if score #booster {ns}.data matches 1 run scoreboard players add #new_motion_x {ns}.data 2500000
execute if score #booster {ns}.data matches 2 run scoreboard players remove #new_motion_x {ns}.data 2500000
execute if score #booster {ns}.data matches 3 run scoreboard players add #new_motion_z {ns}.data 2500000
execute if score #booster {ns}.data matches 4 run scoreboard players remove #new_motion_z {ns}.data 2500000
execute if score @s {ns}.booster_timer matches 0 if score #booster {ns}.data matches 1..2 run scoreboard players operation #new {ns}.data = #new_motion_x {ns}.data
execute if score @s {ns}.booster_timer matches 0 if score #booster {ns}.data matches 3..4 run scoreboard players operation #new {ns}.data = #new_motion_z {ns}.data
execute unless score #new {ns}.data matches -2500000..2500000 run scoreboard players add @s {ns}.engine 120
execute unless score #new {ns}.data matches -2500000..2500000 run particle happy_villager ~ ~.5 ~ 1 1 1 0 10
execute unless score #new {ns}.data matches -2500000..2500000 if score @s {ns}.engine > @s {ns}.max_engine run scoreboard players operation @s {ns}.engine = @s {ns}.max_engine
execute if score #new {ns}.data matches -2500000..2500000 run scoreboard players remove @s {ns}.engine 120
execute if score #new {ns}.data matches -2500000..2500000 run particle angry_villager ~ ~.5 ~ 1 1 1 0 10
execute if score @s {ns}.booster_timer matches 0 if score #new {ns}.data matches -2500000..2500000 run scoreboard players set @s {ns}.booster_timer 20
execute on passengers at @s run playsound block.note_block.harp block @s ~ ~ ~ .5

# tellraw @a [{{"text":"Old / New : ","color":"yellow"}},{{"score":{{"name":"#old","objective":"{ns}.data"}},"color":"aqua"}},{{"text":" / "}},{{"score":{{"name":"#new","objective":"{ns}.data"}},"color":"aqua"}}]
""")

	write_function(f"{ns}:kart/effects/forced_acceleration", f"""
# If not no_steering tag, get rotation from player, else keep rotation
execute if entity @s[tag=!{ns}.no_steering] on passengers run data modify storage {ns}:main Rotation set from entity @s Rotation
execute if entity @s[tag=!{ns}.no_steering] run data modify entity @s Rotation[0] set from storage {ns}:main Rotation[0]

# Reuse not steering marker function
execute positioned 0 0 0 summon marker run function {ns}:kart/effects/no_steering_marker
function {ns}:kart/called_by_player

""")

	write_function(f"{ns}:kart/effects/no_steering", f"""
data modify storage {ns}:main Rotation set from entity @s Rotation
execute positioned 0 0 0 summon marker run function {ns}:kart/effects/no_steering_marker
""")

	write_function(f"{ns}:kart/effects/no_steering_marker", f"""
data modify entity @s Rotation[0] set from storage {ns}:main Rotation[0]
execute at @s run tp @s ^ ^ ^1000
execute store result score #motion_x {ns}.data run data get entity @s Pos[0] 17.5671456314799
execute store result score #motion_z {ns}.data run data get entity @s Pos[2] 17.5671456314799
kill @s
""")

	write_function(f"{ns}:kart/effects/speed_down", f"""
# Slow down engine 28 per tick
scoreboard players remove @s {ns}.engine 28
scoreboard players set @s[scores={{{ns}.engine=..-1}}] {ns}.engine 0
""")

	write_function(f"{ns}:kart/effects/speed_up", f"""
## Speed up engine progressively depending on surface
# Surface : 0 = normal, 1 = fast, 2 = slippery, 3 = slow, 4 = very slow
# When in air : surface = 0
function {ns}:kart/physics/get_surface

# Real gain is (add - 28) cause of speed_down.mcfunction
scoreboard players set #add {ns}.engine 36
execute if score #surface {ns}.data matches 0 unless entity @s[tag={ns}.can_fly] if block ~ ~-.1 ~ air run scoreboard players set #add {ns}.engine 26
execute if score #surface {ns}.data matches 1..2 run scoreboard players set #add {ns}.engine 34
execute if score #surface {ns}.data matches 3 run scoreboard players set #add {ns}.engine 32
execute if score #surface {ns}.data matches 4 run scoreboard players set #add {ns}.engine 30

## Inspired from trackmania
execute unless score @s {ns}.engine matches 0 if entity @s[tag={ns}.engine_off] run scoreboard players set #add {ns}.engine 22
execute if score @s {ns}.engine matches 0 if entity @s[tag={ns}.engine_off] run scoreboard players set #add {ns}.engine 0
execute if score @s {ns}.reactor_boost matches 1.. run scoreboard players set #add {ns}.engine 56

scoreboard players operation @s {ns}.engine += #add {ns}.engine
execute if score @s {ns}.engine > @s {ns}.max_engine run scoreboard players operation @s {ns}.engine = @s {ns}.max_engine
tag @s remove {ns}.speed_up
""")

