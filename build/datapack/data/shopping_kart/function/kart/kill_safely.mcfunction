
#> shopping_kart:kart/kill_safely
#
# @within	shopping_kart:kart/switch_model/
#

# Unride passengers
execute on passengers run ride @s dismount

# Teleport to 0 -10000 0 and kill self
tp @s 0 -10000 0
kill @s

