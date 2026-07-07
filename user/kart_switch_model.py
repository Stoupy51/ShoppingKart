
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup kart switch model functions
def setup_kart_switch_model_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:kart/switch_model/apply_old_data", f"""
# Apply the data from the temporary storage to the entity
data modify entity @s Pos set from storage {ns}:main temp.Pos
data modify entity @s Rotation set from storage {ns}:main temp.Rotation
data modify entity @s Motion set from storage {ns}:main temp.Motion
data modify entity @s Tags set from storage {ns}:main temp.Tags
data modify entity @s active_effects set from storage {ns}:main temp.active_effects
data modify entity @s Fire set from storage {ns}:main temp.Fire
data modify entity @s HurtTime set from storage {ns}:main temp.HurtTime
data modify entity @s Brain set from storage {ns}:main temp.Brain
data modify entity @s NoAI set from storage {ns}:main temp.NoAI
execute store result score @s {ns}.engine run data get storage {ns}:main temp.scores.{ns}.engine
execute store result score @s {ns}.max_engine run data get storage {ns}:main temp.scores.{ns}.max_engine
execute store result score @s {ns}.motion_x run data get storage {ns}:main temp.scores.{ns}.motion_x
execute store result score @s {ns}.motion_z run data get storage {ns}:main temp.scores.{ns}.motion_z
execute store result score @s {ns}.predicted_pos_x run data get storage {ns}:main temp.scores.{ns}.predicted_pos_x
execute store result score @s {ns}.predicted_pos_z run data get storage {ns}:main temp.scores.{ns}.predicted_pos_z
execute store result score @s {ns}.old_pos_x run data get storage {ns}:main temp.scores.{ns}.old_pos_x
execute store result score @s {ns}.old_pos_y run data get storage {ns}:main temp.scores.{ns}.old_pos_y
execute store result score @s {ns}.old_pos_z run data get storage {ns}:main temp.scores.{ns}.old_pos_z
execute store result score @s {ns}.booster_timer run data get storage {ns}:main temp.scores.{ns}.booster_timer
execute store result score @s {ns}.reactor_boost run data get storage {ns}:main temp.scores.{ns}.reactor_boost
execute store result score @s {ns}.cruise_control run data get storage {ns}:main temp.scores.{ns}.cruise_control
execute store result score @s switch.temp.compteur run data get storage {ns}:main temp.scores.switch.temp.compteur

# Remove invisibility if the entity is the model is not the original shopping kart
execute if score #model {ns}.data matches 2.. run effect clear @s invisibility

# Remove the temporary storage
data remove storage {ns}:main temp
""")

	write_function(f"{ns}:kart/switch_model/get_old_data", f"""
# Indicate that the vehicle data have been retrieved
scoreboard players set #has_vehicle {ns}.data 1

# Get all the data from the entity and store it in a temporary storage
data modify storage {ns}:main temp set value {{}}
data modify storage {ns}:main temp.Pos set from entity @s Pos
data modify storage {ns}:main temp.Rotation set from entity @s Rotation
data modify storage {ns}:main temp.Motion set from entity @s Motion
data modify storage {ns}:main temp.Tags set from entity @s Tags
data modify storage {ns}:main temp.active_effects set from entity @s active_effects
data modify storage {ns}:main temp.Fire set from entity @s Fire
data modify storage {ns}:main temp.HurtTime set from entity @s HurtTime
data modify storage {ns}:main temp.Brain set from entity @s Brain
data modify storage {ns}:main temp.NoAI set from entity @s NoAI
execute store result storage {ns}:main temp.scores.{ns}.engine int 1 run scoreboard players get @s {ns}.engine
execute store result storage {ns}:main temp.scores.{ns}.max_engine int 1 run scoreboard players get @s {ns}.max_engine
execute store result storage {ns}:main temp.scores.{ns}.motion_x int 1 run scoreboard players get @s {ns}.motion_x
execute store result storage {ns}:main temp.scores.{ns}.motion_z int 1 run scoreboard players get @s {ns}.motion_z
execute store result storage {ns}:main temp.scores.{ns}.predicted_pos_x int 1 run scoreboard players get @s {ns}.predicted_pos_x
execute store result storage {ns}:main temp.scores.{ns}.predicted_pos_z int 1 run scoreboard players get @s {ns}.predicted_pos_z
execute store result storage {ns}:main temp.scores.{ns}.old_pos_x int 1 run scoreboard players get @s {ns}.old_pos_x
execute store result storage {ns}:main temp.scores.{ns}.old_pos_y int 1 run scoreboard players get @s {ns}.old_pos_y
execute store result storage {ns}:main temp.scores.{ns}.old_pos_z int 1 run scoreboard players get @s {ns}.old_pos_z
execute store result storage {ns}:main temp.scores.{ns}.booster_timer int 1 run scoreboard players get @s {ns}.booster_timer
execute store result storage {ns}:main temp.scores.{ns}.reactor_boost int 1 run scoreboard players get @s {ns}.reactor_boost
execute store result storage {ns}:main temp.scores.{ns}.cruise_control int 1 run scoreboard players get @s {ns}.cruise_control
execute store result storage {ns}:main temp.scores.switch.temp.compteur int 1 run scoreboard players get @s switch.temp.compteur
""")

	write_function(f"{ns}:kart/switch_model/init_functions", f"""
# Run default init function
function {ns}:kart/init

# Apply old data
execute if data storage {ns}:main temp.scores run function {ns}:kart/switch_model/apply_old_data

# data modify storage {ns}:data ForcedRotation set from entity @s Rotation
execute if data storage {ns}:main ForcedRotation run data modify entity @s Rotation set from storage {ns}:data ForcedRotation
data remove storage {ns}:data ForcedRotation

# Make the player ride the kart 1 tick later
function {ns}:kart/switch_model/verify_passengers
schedule function {ns}:kart/switch_model/ride_kart_schedule 1t replace

# Remove temporary tag
tag @s remove {ns}.new_kart
""")

	write_function(f"{ns}:kart/switch_model/main", f"""
# Update the model of the shopping kart just in case
scoreboard players add @s {ns}.current_model 0

# Get old shopping kart information
scoreboard players set #has_vehicle {ns}.data 0
execute on vehicle if entity @s[tag={ns}.kart] run function {ns}:kart/switch_model/get_old_data

# If there is a vehicle, remove it, summon the new one, set the new data and ride it
execute if score #has_vehicle {ns}.data matches 1 on vehicle run function {ns}:kart/kill_safely
execute if score #has_vehicle {ns}.data matches 1 at @s run function {ns}:kart/switch_model/summon_new_kart
""")

	write_function(f"{ns}:kart/switch_model/ride_kart_entity", f"""
# Teleport the nearest player to self, and make him ride self
tp @p[predicate=!{ns}:has_vehicle] @s
ride @p[predicate=!{ns}:has_vehicle] mount @s

# Remove the waiting for passenger tag
tag @s remove {ns}.waiting_for_passenger
""")

	write_function(f"{ns}:kart/switch_model/ride_kart_schedule", f"""
# Run function on every kart that is waiting for a passenger
execute as @e[tag={ns}.waiting_for_passenger] run function {ns}:kart/switch_model/verify_passengers
execute as @e[tag={ns}.waiting_for_passenger] at @s run function {ns}:kart/switch_model/ride_kart_entity
""")

	write_function(f"{ns}:kart/switch_model/summon_new_kart", f"""
# Tag the current player to ride the new kart
tag @s add {ns}.owner

# Copy the score of the selected model and rotation
scoreboard players add @s {ns}.current_model 0
scoreboard players operation #model {ns}.data = @s {ns}.current_model
data modify storage {ns}:data ForcedRotation set from entity @s Rotation

# Summon the kart depending on the selected model
execute if score #model {ns}.data matches 0 run summon pig ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 1 run summon pig ~ ~ ~ {{Tags:["{ns}.new_kart"],Age:-1000000}}
execute if score #model {ns}.data matches 2 run summon wolf ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 3 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:white"}}
execute if score #model {ns}.data matches 4 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:black"}}
execute if score #model {ns}.data matches 5 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:red"}}
execute if score #model {ns}.data matches 6 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:siamese"}}
execute if score #model {ns}.data matches 7 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:british_shorthair"}}
execute if score #model {ns}.data matches 8 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:calico"}}
execute if score #model {ns}.data matches 9 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:persian"}}
execute if score #model {ns}.data matches 10 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:ragdoll"}}
execute if score #model {ns}.data matches 11 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:tabby"}}
execute if score #model {ns}.data matches 12 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:all_black"}}
execute if score #model {ns}.data matches 13 run summon cat ~ ~ ~ {{Tags:["{ns}.new_kart"],variant:"minecraft:jellie"}}
execute if score #model {ns}.data matches 14 run summon ocelot ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 15 run summon fox ~ ~ ~ {{Tags:["{ns}.new_kart"],Type:"red"}}
execute if score #model {ns}.data matches 16 run summon fox ~ ~ ~ {{Tags:["{ns}.new_kart"],Type:"snow"}}
execute if score #model {ns}.data matches 17 run summon chicken ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 18 run summon goat ~ ~ ~ {{Tags:["{ns}.new_kart"],HasLeftHorn:1b,HasRightHorn:1b,IsScreamingGoat:1b}}
execute if score #model {ns}.data matches 19 run summon goat ~ ~ ~ {{Tags:["{ns}.new_kart"],HasLeftHorn:1b,HasRightHorn:0b,IsScreamingGoat:1b}}
execute if score #model {ns}.data matches 20 run summon goat ~ ~ ~ {{Tags:["{ns}.new_kart"],HasLeftHorn:0b,HasRightHorn:1b,IsScreamingGoat:1b}}
execute if score #model {ns}.data matches 21 run summon goat ~ ~ ~ {{Tags:["{ns}.new_kart"],HasLeftHorn:0b,HasRightHorn:0b,IsScreamingGoat:1b}}
execute if score #model {ns}.data matches 22 run summon pig ~ ~ ~ {{Tags:["{ns}.new_kart"],Saddle:1b}}
execute if score #model {ns}.data matches 23 run summon pig ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 24 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Sheared:1b}}
execute if score #model {ns}.data matches 25 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:0}}
execute if score #model {ns}.data matches 26 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:1}}
execute if score #model {ns}.data matches 27 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:2}}
execute if score #model {ns}.data matches 28 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:3}}
execute if score #model {ns}.data matches 29 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:4}}
execute if score #model {ns}.data matches 30 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:5}}
execute if score #model {ns}.data matches 31 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:6}}
execute if score #model {ns}.data matches 32 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:7}}
execute if score #model {ns}.data matches 33 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:8}}
execute if score #model {ns}.data matches 34 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:9}}
execute if score #model {ns}.data matches 35 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:10}}
execute if score #model {ns}.data matches 36 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:11}}
execute if score #model {ns}.data matches 37 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:12}}
execute if score #model {ns}.data matches 38 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:13}}
execute if score #model {ns}.data matches 39 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:14}}
execute if score #model {ns}.data matches 40 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],Color:15}}
execute if score #model {ns}.data matches 41 run summon sheep ~ ~ ~ {{Tags:["{ns}.new_kart"],CustomName:"jeb_"}}
execute if score #model {ns}.data matches 42 run summon cow ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 43 run summon mooshroom ~ ~ ~ {{Tags:["{ns}.new_kart"],Type:"red"}}
execute if score #model {ns}.data matches 44 run summon mooshroom ~ ~ ~ {{Tags:["{ns}.new_kart"],Type:"brown"}}
execute if score #model {ns}.data matches 45 run summon panda ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 46 run summon axolotl ~ ~ ~ {{Tags:["{ns}.new_kart"],Variant:0}}
execute if score #model {ns}.data matches 47 run summon axolotl ~ ~ ~ {{Tags:["{ns}.new_kart"],Variant:1}}
execute if score #model {ns}.data matches 48 run summon axolotl ~ ~ ~ {{Tags:["{ns}.new_kart"],Variant:2}}
execute if score #model {ns}.data matches 49 run summon axolotl ~ ~ ~ {{Tags:["{ns}.new_kart"],Variant:3}}
execute if score #model {ns}.data matches 50 run summon axolotl ~ ~ ~ {{Tags:["{ns}.new_kart"],Variant:4}}
execute if score #model {ns}.data matches 51 run summon sniffer ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 52 run summon sniffer ~ ~ ~ {{Tags:["{ns}.new_kart"],Age:-1000000}}
execute if score #model {ns}.data matches 53 run summon armadillo ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 54 run summon strider ~ ~ ~ {{Tags:["{ns}.new_kart"]}}
execute if score #model {ns}.data matches 55 run summon turtle ~ ~ ~ {{Tags:["{ns}.new_kart"]}}

# Apply init functions to new kart
execute as @e[tag={ns}.new_kart] at @s run function {ns}:kart/switch_model/init_functions

# Remove the temporary player tag
tag @s remove {ns}.owner
""")

	write_function(f"{ns}:kart/switch_model/trigger", f"""
## Manage trigger value
# If trigger == -1, add 1 to current_model
# If trigger == -2, subtract 1 from current_model
# If trigger == -3, ride the nearest vehicle
# If trigger == -4, get a random value between 0 and 55
# If trigger > 0, set current_model to trigger - 1
execute if score @s {ns}.trigger_model matches -1 run scoreboard players add @s {ns}.current_model 1
execute if score @s {ns}.trigger_model matches -2 run scoreboard players remove @s {ns}.current_model 1
execute if score @s {ns}.trigger_model matches -3 run ride @s[predicate=!{ns}:has_vehicle] mount @n[tag={ns}.kart]
execute if score @s {ns}.trigger_model matches -4 on vehicle store result score #random {ns}.current_model run data get entity @s UUID[0]
execute if score @s {ns}.trigger_model matches -4 run scoreboard players set #56 {ns}.data 56
execute if score @s {ns}.trigger_model matches -4 run scoreboard players operation #random {ns}.current_model %= #56 {ns}.data
execute if score @s {ns}.trigger_model matches -4 run scoreboard players operation @s {ns}.current_model = #random {ns}.current_model
execute if score @s {ns}.trigger_model matches 1.. run scoreboard players operation @s {ns}.current_model = @s {ns}.trigger_model
execute if score @s {ns}.trigger_model matches 1.. run scoreboard players remove @s {ns}.current_model 1

## Correct model values
execute if score @s {ns}.current_model matches ..-1 run scoreboard players set @s {ns}.current_model 55
execute if score @s {ns}.current_model matches 56.. run scoreboard players set @s {ns}.current_model 0
scoreboard players operation #temp {ns}.current_model = @s {ns}.current_model
scoreboard players add #temp {ns}.current_model 1
tellraw @s ["",{{"nbt":"ShoppingKart","storage":"{ns}:main","interpret":true}},{{"text":" Current Model: ","color":"dark_green"}},{{"score":{{"name":"#temp","objective":"{ns}.current_model"}},"color":"green"}},{{"text":"/","color":"dark_green"}},{{"text":"56","color":"green"}}]

## Change current vehicle
execute if score @s {ns}.trigger_model matches -2.. run function {ns}:kart/switch_model/main
execute if score @s {ns}.trigger_model matches -4 run function {ns}:kart/switch_model/main

## Reset trigger value
scoreboard players reset @s {ns}.trigger_model
""")

	write_function(f"{ns}:kart/switch_model/verify_passengers", f"""
# Add tag if no passenger, remove if there is one
scoreboard players set #has_passenger {ns}.data 0
execute on passengers if entity @s[type=player] run scoreboard players set #has_passenger {ns}.data 1
execute if score #has_passenger {ns}.data matches 0 run tag @s add {ns}.waiting_for_passenger
execute if score #has_passenger {ns}.data matches 1 run tag @s remove {ns}.waiting_for_passenger
""")

