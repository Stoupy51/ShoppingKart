
#> shopping_kart:kart/signal_parties/add_victim
#
# @executed	at @s
#
# @within	shopping_kart:kart/physics/collide_kart
#

tag @s add shopping_kart.victim
execute on passengers if entity @s[type=player] run tag @s add shopping_kart.victim

