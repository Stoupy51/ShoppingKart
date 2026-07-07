
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup kart tick functions
def setup_kart_tick_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:kart/tick/calculations", f"""
tag @s add {ns}.temp
execute if score #instant_engine_max {ns}.data matches 1 run scoreboard players operation @s {ns}.engine = @s {ns}.max_engine

## Conditions if the vehicle have a passenger
function {ns}:kart/visual_passenger

## Water specification
function {ns}:kart/physics/water

## Physics calculation depending on engine speed, surface, old motion, booster, etc.
function {ns}:kart/physics/calculation

## Apply new motion & update old motion
function {ns}:kart/physics/apply_motion

## Try to predict position after 1 tick (new_pos = old_pos + new_motion)
function {ns}:kart/physics/predict_position

## Title actionbar
execute if score #have_passenger {ns}.data matches 1 run function {ns}:kart/title_actionbar

# Remove temp tag & Add tag to avoid double calculation
tag @s remove {ns}.temp
tag @s add {ns}.calculated
""")

	write_function(f"{ns}:kart/tick/main", f"""
# Slow down, Speed up engine, refresh booster timer
execute if score @s {ns}.engine matches 1.. run function {ns}:kart/effects/speed_down
execute if score @s {ns}.reactor_boost matches 1.. run particle flame ~ ~ ~ 0.4 0.4 0.4 0 5
execute if score @s {ns}.reactor_boost matches 1.. run scoreboard players remove @s {ns}.reactor_boost 1
execute if entity @s[tag={ns}.speed_up] run function {ns}:kart/effects/speed_up
scoreboard players remove @s[scores={{{ns}.booster_timer=1..}}] {ns}.booster_timer 1

# Forced acceleration
execute if entity @s[tag={ns}.forced_acceleration] run function {ns}:kart/effects/forced_acceleration

# Tick calculations
execute if entity @s[tag=!{ns}.calculated] run function {ns}:kart/tick/calculations
tag @s remove {ns}.calculated

# Add slowness effect
effect give @s slowness infinite 255 true
""")

	write_function(f"{ns}:kart/tick/visual", f"""
## Kill self is there is no vehicle, but take first rotation otherwise
data remove storage {ns}:main Rotation
execute on vehicle run data modify storage {ns}:main Rotation set from entity @s Rotation[0]
execute store result score #rotation {ns}.data run data get entity @s Rotation[0] 10000
execute store result score #rotation {ns}.data run data get storage {ns}:main Rotation 10000
scoreboard players add #rotation {ns}.data 1800000
execute store result entity @s Rotation[0] float 0.0001 run scoreboard players get #rotation {ns}.data
execute unless data storage {ns}:main Rotation run kill @s
""")

