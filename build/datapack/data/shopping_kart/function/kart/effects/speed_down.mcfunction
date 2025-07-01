
#> shopping_kart:kart/effects/speed_down
#
# @within	shopping_kart:kart/tick/main
#

# Slow down engine 28 per tick
scoreboard players remove @s shopping_kart.engine 28
scoreboard players set @s[scores={shopping_kart.engine=..-1}] shopping_kart.engine 0

