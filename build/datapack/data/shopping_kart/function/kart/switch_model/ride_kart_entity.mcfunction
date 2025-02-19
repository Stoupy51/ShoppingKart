
#> shopping_kart:kart/switch_model/ride_kart_entity
#
# @within	shopping_kart:kart/switch_model/ride_kart_schedule
#

# Teleport the nearest player to self, and make him ride self
tp @p[predicate=!shopping_kart:has_vehicle] @s
ride @p[predicate=!shopping_kart:has_vehicle] mount @s

# Remove the waiting for passenger tag
tag @s remove shopping_kart.waiting_for_passenger

