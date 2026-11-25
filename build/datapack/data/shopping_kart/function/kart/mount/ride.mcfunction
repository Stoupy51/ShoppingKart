
#> shopping_kart:kart/mount/ride
#
# @executed	as @e[type=interaction,tag=shopping_kart.mount,distance=..8]
#
# @within	shopping_kart:kart/mount/clicked [ as @e[type=interaction,tag=shopping_kart.mount,distance=..8] ]
#

# The interaction's target is the last player who right clicked it
execute on target run tag @s add shopping_kart.clicker
execute on vehicle store success score #success shopping_kart.data run ride @p[tag=shopping_kart.clicker] mount @s
execute if score #success shopping_kart.data matches 1 on target at @s run function #shopping_kart:signals/kart_mounted
execute on target run tag @s remove shopping_kart.clicker
kill @s

