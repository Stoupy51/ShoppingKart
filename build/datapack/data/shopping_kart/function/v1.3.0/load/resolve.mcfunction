
#> shopping_kart:v1.3.0/load/resolve
#
# @within	#shopping_kart:resolve
#

# If correct version, load the datapack
execute if score #shopping_kart.major load.status matches 1 if score #shopping_kart.minor load.status matches 3 if score #shopping_kart.patch load.status matches 0 run function shopping_kart:v1.3.0/load/main

