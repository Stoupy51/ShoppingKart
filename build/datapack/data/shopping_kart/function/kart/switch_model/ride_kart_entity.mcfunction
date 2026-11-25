
#> shopping_kart:kart/switch_model/ride_kart_entity
#
# @executed	at @s
#
# @within	shopping_kart:kart/switch_model/ride_kart_schedule [ at @s ]
#

# Teleport the nearest player to self, and make him ride self
tp @p[predicate=!shopping_kart:has_vehicle] @s
execute store success score #success shopping_kart.data run ride @p[predicate=!shopping_kart:has_vehicle] mount @s
execute if score #success shopping_kart.data matches 1 on passengers if entity @s[type=player] at @s run function #shopping_kart:signals/kart_mounted

# Remove the waiting for passenger tag
tag @s remove shopping_kart.waiting_for_passenger

