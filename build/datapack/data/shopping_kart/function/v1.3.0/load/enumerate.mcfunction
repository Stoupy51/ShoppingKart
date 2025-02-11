
#> shopping_kart:v1.3.0/load/enumerate
#
# @within	#shopping_kart:enumerate
#

# If current major is too low, set it to the current major
execute unless score #shopping_kart.major load.status matches 1.. run scoreboard players set #shopping_kart.major load.status 1

# If current minor is too low, set it to the current minor (only if major is correct)
execute if score #shopping_kart.major load.status matches 1 unless score #shopping_kart.minor load.status matches 3.. run scoreboard players set #shopping_kart.minor load.status 3

# If current patch is too low, set it to the current patch (only if major and minor are correct)
execute if score #shopping_kart.major load.status matches 1 if score #shopping_kart.minor load.status matches 3 unless score #shopping_kart.patch load.status matches 0.. run scoreboard players set #shopping_kart.patch load.status 0

