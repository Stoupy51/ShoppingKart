
#> shopping_kart:kart/kill_safely
#
# @executed	as @a & at @s
#
# @within	shopping_kart:kart/switch_model/main
#

# Unride passengers
execute on passengers if entity @s[tag=shopping_kart.mount] run kill @s
execute on passengers run ride @s dismount

# Teleport to 0 -10000 0 and kill self
tp @s 0 -10000 0
kill @s

