
#> shopping_kart:v1.3.0/load/main
#
# @within	shopping_kart:v1.3.0/load/resolve
#

# Avoiding multiple executions of the same load function
execute unless score #shopping_kart.loaded load.status matches 1 run function shopping_kart:v1.3.0/load/secondary

