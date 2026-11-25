
#> shopping_kart:kart/signal_parties/add_attacker
#
# @executed	as @n[tag=...,distance=..1]
#
# @within	shopping_kart:kart/physics/collide_kart [ as @n[tag=...,distance=..1] ]
#			shopping_kart:kart/physics/collide_player [ as @n[tag=...,distance=..1] ]
#

tag @s add shopping_kart.attacker
execute on passengers if entity @s[type=player] run tag @s add shopping_kart.attacker

