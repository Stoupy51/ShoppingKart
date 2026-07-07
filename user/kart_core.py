
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup kart core functions
def setup_kart_core_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:kart/add_motion_from_marker_pos", f"""
# Collect marker position
execute store result score #temp_x {ns}.data run data get entity @s Pos[0] 1.5
execute store result score #temp_z {ns}.data run data get entity @s Pos[2] 1.5

# Add marker position to motion
scoreboard players operation #motion_x {ns}.data += #temp_x {ns}.data
scoreboard players operation #motion_z {ns}.data += #temp_z {ns}.data

# Remember the number of added motion (for normalizing)
scoreboard players add #added {ns}.data 1

# Remove marker
kill @s

""")

	write_function(f"{ns}:kart/called_by_player", f"""
tag @s add {ns}.speed_up
execute if entity @s[tag=!{ns}.no_steering] run data modify entity @s Rotation set from storage {ns}:main Rotation
execute if entity @s[tag={ns}.no_steering] run function {ns}:kart/effects/no_steering

function {ns}:kart/tick/calculations

""")

	write_function(f"{ns}:kart/init", f"""
# Add kart nbt
tag @s add {ns}.kart
data modify entity @s Silent set value 1b
execute unless score #is_vulnerable {ns}.data matches 1 run data modify entity @s Invulnerable set value 1b
data modify entity @s DeathLootTable set value "empty"

# Attribute step height to player default (0.6)
attribute @s step_height base set 0.6

# Can Fly tag
execute if score #can_fly {ns}.data matches 1 run tag @s add {ns}.can_fly

# Add kart scoreboard
scoreboard players operation @s {ns}.max_engine = #default_max_engine {ns}.data
scoreboard players set @s {ns}.booster_timer 0

# Kart Visual
scoreboard players add #next_id {ns}.id 1
execute if score #model {ns}.data matches 0..1 run tag @s add {ns}.current_kart
execute if score #model {ns}.data matches 0..1 at @s summon item_display run function {ns}:kart/init_visual
execute if score #model {ns}.data matches 0..1 run effect give @s invisibility infinite 0 true
execute if score #model {ns}.data matches 0..1 run tag @s remove {ns}.current_kart
scoreboard players operation @s {ns}.id = #next_id {ns}.id

""")

	write_function(f"{ns}:kart/init_visual", f"""
# Add NBT
tag @s add {ns}.kart_visual
data modify entity @s transformation.translation[1] set value -0.38f
execute if score #model {ns}.data matches 1 run data modify entity @s transformation.scale set value [0.75f,0.75f,0.75f]
execute if score #model {ns}.data matches 1 run data modify entity @s transformation.translation[1] set value -0.07f
data modify entity @s teleport_duration set value 2

# Scoreboard + Model
scoreboard players operation @s {ns}.id = #next_id {ns}.id
item replace entity @s container.0 with golden_hoe[item_model="{ns}:{ns}"]

# Ride the kart
ride @s mount @n[tag={ns}.current_kart,sort=nearest]

""")

	write_function(f"{ns}:kart/kill_safely", """
# Unride passengers
execute on passengers run ride @s dismount

# Teleport to 0 -10000 0 and kill self
tp @s 0 -10000 0
kill @s

""")

	write_function(f"{ns}:kart/motion_from_input", f"""
scoreboard players set #motion_x {ns}.data 0
scoreboard players set #motion_z {ns}.data 0

# Add motion depending on input
scoreboard players set #added {ns}.data 0
execute if predicate {ns}:input/forward rotated ~ 0 positioned 0 0 0 positioned ^ ^ ^10000 summon marker run function {ns}:kart/add_motion_from_marker_pos
execute if predicate {ns}:input/backward rotated ~ 0 positioned 0 0 0 positioned ^ ^ ^-10500 summon marker run function {ns}:kart/add_motion_from_marker_pos
execute if predicate {ns}:input/right rotated ~ 0 positioned 0 0 0 positioned ^-10000 ^ ^ summon marker run function {ns}:kart/add_motion_from_marker_pos
execute if predicate {ns}:input/left rotated ~ 0 positioned 0 0 0 positioned ^10000 ^ ^ summon marker run function {ns}:kart/add_motion_from_marker_pos

# Normalize motion if 2 inputs (divide by 1.41421356237 = sqrt(2))
execute if score #added {ns}.data matches 2 run function {ns}:kart/normalize_motion

""")

	write_function(f"{ns}:kart/normalize_motion", f"""
# Normalize motion (divide by 1.41421356237 = sqrt(2))
scoreboard players operation #motion_x {ns}.data *= #10000 {ns}.data
scoreboard players operation #motion_x {ns}.data /= #14142 {ns}.data

scoreboard players operation #motion_z {ns}.data *= #10000 {ns}.data
scoreboard players operation #motion_z {ns}.data /= #14142 {ns}.data


""")

	write_function(f"{ns}:kart/player_moving", f"""
tag @s add {ns}.temp

# Store player motion and call function to the vehicle (Old code < 1.21)
# execute store result score #motion_x {ns}.data run data get entity @s Motion[0] 1000000
# execute store result score #motion_z {ns}.data run data get entity @s Motion[2] 1000000

# Store player motion and call function to the vehicle (New code >= 1.21)
function {ns}:kart/motion_from_input

data modify storage {ns}:main Rotation set from entity @s Rotation
scoreboard players set #instant_engine_max {ns}.data 0

execute on vehicle at @s[tag=!{ns}.forced_acceleration] run function {ns}:kart/called_by_player

data remove storage {ns}:main Rotation
tag @s remove {ns}.temp

scoreboard players set #motion_x {ns}.data 0
scoreboard players set #motion_z {ns}.data 0

""")

	write_function(f"{ns}:kart/stop_motion", f"""
scoreboard players set #collision_type {ns}.data 0
execute if score #collision_type {ns}.data matches 0 if score @s {ns}.engine matches 400.. if score @s {ns}.predicted_pos_x matches -2..2 unless score @s {ns}.predicted_pos_z matches -20..20 run scoreboard players set #collision_type {ns}.data 1
execute if score #collision_type {ns}.data matches 0 if score @s {ns}.engine matches 400.. if score @s {ns}.predicted_pos_z matches -2..2 unless score @s {ns}.predicted_pos_x matches -20..20 run scoreboard players set #collision_type {ns}.data 1
# tellraw @a [{{"text":"Collision detector : (","color":"yellow"}},{{"score":{{"name":"@s","objective":"{ns}.predicted_pos_x"}},"color":"aqua"}},{{"text":","}},{{"score":{{"name":"@s","objective":"{ns}.predicted_pos_z"}},"color":"aqua"}},{{"text":")"}}]

# Small collision
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.motion_x *= #99 {ns}.data
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.motion_x /= #100 {ns}.data
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.motion_z *= #99 {ns}.data
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.motion_z /= #100 {ns}.data
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.engine *= #99 {ns}.data
execute if score #collision_type {ns}.data matches 0 run scoreboard players operation @s {ns}.engine /= #100 {ns}.data
execute if score #collision_type {ns}.data matches 0 run particle smoke ~ ~1 ~ 1 1 1 0 10 force @a[distance=..50]
execute if score #collision_type {ns}.data matches 0 run playsound mechanization:gadgets.epac_overheat block @a ~ ~ ~ .25 0.1

# Large collision
execute if score #collision_type {ns}.data matches 1 run scoreboard players operation @s {ns}.motion_x *= #10 {ns}.data
execute if score #collision_type {ns}.data matches 1 run scoreboard players operation @s {ns}.motion_x /= #100 {ns}.data
execute if score #collision_type {ns}.data matches 1 run scoreboard players operation @s {ns}.motion_z *= #10 {ns}.data
execute if score #collision_type {ns}.data matches 1 run scoreboard players operation @s {ns}.motion_z /= #100 {ns}.data
execute if score #collision_type {ns}.data matches 1 run scoreboard players set @s {ns}.engine 100
execute if score #collision_type {ns}.data matches 1 run particle lava ~ ~ ~ 1 1 1 0 50 force @a[distance=..50]
execute if score #collision_type {ns}.data matches 1 run playsound block.anvil.land block @a ~ ~ ~ 0.05 0.1

""")

	write_function(f"{ns}:kart/summon", f"""
# Tag the current player to ride the new kart
tag @s add {ns}.owner

# Summon the pig
scoreboard players set #model {ns}.data 0
data modify storage {ns}:data ForcedRotation set from entity @s Rotation
execute summon pig at @s run function {ns}:kart/switch_model/init_functions

# Remove the temporary player tag
tag @s remove {ns}.owner

""")

	write_function(f"{ns}:kart/title_actionbar", f"""
# Remember the old position
execute store result score #new_pos_x {ns}.data run data get entity @s Pos[0] 10000
execute store result score #new_pos_z {ns}.data run data get entity @s Pos[2] 10000

# Calculate the speed
scoreboard players operation @s {ns}.old_pos_x -= #new_pos_x {ns}.data
scoreboard players operation @s {ns}.old_pos_z -= #new_pos_z {ns}.data
scoreboard players operation @s[scores={{{ns}.old_pos_x=..-1}}] {ns}.old_pos_x *= #-1 {ns}.data
scoreboard players operation @s[scores={{{ns}.old_pos_z=..-1}}] {ns}.old_pos_z *= #-1 {ns}.data
scoreboard players operation @s {ns}.old_pos_x *= @s {ns}.old_pos_x
scoreboard players operation @s {ns}.old_pos_z *= @s {ns}.old_pos_z
scoreboard players operation @s {ns}.old_pos_x += @s {ns}.old_pos_z
scoreboard players operation #input {ns}.data = @s {ns}.old_pos_x
function {ns}:math/sqrt
scoreboard players operation #output {ns}.data *= #20 {ns}.data
scoreboard players operation @s {ns}.old_pos_x = #output {ns}.data
scoreboard players operation @s {ns}.old_pos_z = #output {ns}.data
scoreboard players operation @s {ns}.old_pos_x /= #10000 {ns}.data
scoreboard players operation @s {ns}.old_pos_z %= #10000 {ns}.data
scoreboard players operation @s {ns}.old_pos_z /= #1000 {ns}.data

# Copy scores and tellraw the speed
scoreboard players operation #t_engine {ns}.data = @s {ns}.engine
scoreboard players operation #t_first_digits {ns}.data = @s {ns}.old_pos_x
scoreboard players operation #t_second_digits {ns}.data = @s {ns}.old_pos_z
execute on passengers run title @s actionbar [{{"text":"Engine: ","color":"yellow"}},{{"score":{{"name":"#t_engine","objective":"{ns}.data"}},"color":"aqua"}},{{"text":" rpm | Speed: "}},{{"score":{{"name":"#t_first_digits","objective":"{ns}.data"}},"color":"aqua"}},{{"text":","}},{{"score":{{"name":"#t_second_digits","objective":"{ns}.data"}},"color":"aqua"}},{{"text":" blocks/s "}}]

# Reset the old position
scoreboard players operation @s {ns}.old_pos_x = #new_pos_x {ns}.data
scoreboard players operation @s {ns}.old_pos_z = #new_pos_z {ns}.data

""")

	write_function(f"{ns}:kart/visual_passenger", f"""
## Conditions if the vehicle have a passenger
scoreboard players set #have_passenger {ns}.data 0
execute store success score #have_passenger {ns}.data on passengers if entity @s[type=player] run scoreboard players set #have_passenger {ns}.data 1
execute if score #have_passenger {ns}.data matches 0 run effect give @s slowness 1 255 true
execute if score #have_passenger {ns}.data matches 1 run effect clear @s slowness

""")

