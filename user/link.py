
# Imports
from stewbeet import Context, write_load_file, write_tick_file


# Main function is run just before making finalyzing the build process (zip, headers, lang, ...)
def beet_default(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_tick_file(f"""
# Detect if a player is moving
execute as @a[gamemode=!spectator,predicate={ns}:has_kart_vehicle,predicate={ns}:input/any] at @s run function {ns}:kart/player_moving

# Kart ticking
execute as @e[tag={ns}.kart] at @s run function {ns}:kart/tick/main

# Kart visual
execute as @e[tag={ns}.kart_visual] run function {ns}:kart/tick/visual

# Detect model change
scoreboard players enable @a {ns}.trigger_model
execute as @a unless score @s {ns}.trigger_model matches 0 at @s run function {ns}:kart/switch_model/trigger
""")

	write_load_file(f"""
scoreboard objectives add {ns}.data dummy
scoreboard objectives add {ns}.id dummy
scoreboard objectives add {ns}.engine dummy
scoreboard objectives add {ns}.max_engine dummy
scoreboard objectives add {ns}.motion_x dummy
scoreboard objectives add {ns}.motion_z dummy
scoreboard objectives add {ns}.predicted_pos_x dummy
scoreboard objectives add {ns}.predicted_pos_z dummy
scoreboard objectives add {ns}.old_pos_x dummy
scoreboard objectives add {ns}.old_pos_y dummy
scoreboard objectives add {ns}.old_pos_z dummy
scoreboard objectives add {ns}.booster_timer dummy
scoreboard objectives add {ns}.reactor_boost dummy
scoreboard objectives add {ns}.cruise_control dummy

scoreboard objectives add {ns}.trigger_model trigger
scoreboard objectives add {ns}.current_model dummy

scoreboard players set #default_max_engine {ns}.data 1500

#define storage {ns}:main
#define storage {ns}:temp
#define score_holder #success
#define score_holder #valid
#define score_holder #count
#define score_holder #temp
#define score_holder #pos

## Setup tellraw prefix
data modify storage {ns}:main ShoppingKart set value [{{"text":"[ShoppingKart]","color":"green"}}]

scoreboard players set #-1 {ns}.data -1
scoreboard players set #2 {ns}.data 2
scoreboard players set #3 {ns}.data 3
scoreboard players set #10 {ns}.data 10
scoreboard players set #15 {ns}.data 15
scoreboard players set #20 {ns}.data 20
scoreboard players set #30 {ns}.data 30
scoreboard players set #60 {ns}.data 60
scoreboard players set #99 {ns}.data 99
scoreboard players set #100 {ns}.data 100
scoreboard players set #120 {ns}.data 120
scoreboard players set #1000 {ns}.data 1000
scoreboard players set #10000 {ns}.data 10000
scoreboard players set #14142 {ns}.data 14142
""")

