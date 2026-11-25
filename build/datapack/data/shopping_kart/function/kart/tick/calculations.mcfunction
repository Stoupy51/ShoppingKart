
#> shopping_kart:kart/tick/calculations
#
# @executed	at @s[tag=!shopping_kart.forced_acceleration]
#
# @within	shopping_kart:kart/called_by_player
#			shopping_kart:kart/tick/main
#

tag @s add shopping_kart.temp
execute if score #instant_engine_max shopping_kart.data matches 1 run scoreboard players operation @s shopping_kart.engine = @s shopping_kart.max_engine

## Conditions if the vehicle have a passenger
function shopping_kart:kart/visual_passenger

## Water specification
function shopping_kart:kart/physics/water

## Physics calculation depending on engine speed, surface, old motion, booster, etc.
function shopping_kart:kart/physics/calculation

## Apply new motion & update old motion
function shopping_kart:kart/physics/apply_motion

## An empty kart at rest carries an interaction, so a right click mounts it again
scoreboard players set #mountable shopping_kart.data 0
execute if score #have_passenger shopping_kart.data matches 0 if score @s shopping_kart.motion_x matches -10000..10000 if score @s shopping_kart.motion_z matches -10000..10000 run scoreboard players set #mountable shopping_kart.data 1
execute if score #mountable shopping_kart.data matches 0 on passengers if entity @s[tag=shopping_kart.mount] run kill @s
execute if score #mountable shopping_kart.data matches 1 unless predicate shopping_kart:has_mount_passenger summon interaction run function shopping_kart:kart/mount/init

## Try to predict position after 1 tick (new_pos = old_pos + new_motion)
function shopping_kart:kart/physics/predict_position

## Title actionbar
execute if score #have_passenger shopping_kart.data matches 1 run function shopping_kart:kart/title_actionbar

# Remove temp tag & Add tag to avoid double calculation
tag @s remove shopping_kart.temp
tag @s add shopping_kart.calculated

