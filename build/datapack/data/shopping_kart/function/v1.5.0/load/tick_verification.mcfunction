
#> shopping_kart:v1.5.0/load/tick_verification
#
# @within	#minecraft:tick
#

execute if score #shopping_kart.major load.status matches 1 if score #shopping_kart.minor load.status matches 5 if score #shopping_kart.patch load.status matches 0 run function shopping_kart:v1.5.0/tick

