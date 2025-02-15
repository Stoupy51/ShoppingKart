
#> shopping_kart:kart/init_visual
#
# @within	shopping_kart:kart/init
#

# Add NBT
tag @s add shopping_kart.kart_visual
data modify entity @s transformation.translation[1] set value -0.38f
execute if score #model shopping_kart.data matches 1 run data modify entity @s transformation.scale set value [0.75f,0.75f,0.75f]
execute if score #model shopping_kart.data matches 1 run data modify entity @s transformation.translation[1] set value -0.07f
data modify entity @s teleport_duration set value 2

# Scoreboard + Model
scoreboard players operation @s shopping_kart.id = #next_id shopping_kart.id
item replace entity @s container.0 with golden_hoe[item_model="shopping_kart:shopping_kart"]

# Ride the kart
ride @s mount @e[tag=shopping_kart.current_kart,sort=nearest,limit=1]

