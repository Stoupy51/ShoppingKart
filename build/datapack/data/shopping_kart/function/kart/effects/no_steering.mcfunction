
#> shopping_kart:kart/effects/no_steering
#
# @within	shopping_kart:kart/called_by_player
#

data modify storage shopping_kart:main Rotation set from entity @s Rotation
execute positioned 0 0 0 summon marker run function shopping_kart:kart/effects/no_steering_marker

