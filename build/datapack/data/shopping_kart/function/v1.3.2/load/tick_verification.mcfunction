
#> shopping_kart:v1.3.2/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #shopping_kart.major load.status matches 1 if score #shopping_kart.minor load.status matches 3 if score #shopping_kart.patch load.status matches 2 run function shopping_kart:v1.3.2/tick

