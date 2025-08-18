
#> shopping_kart:kart/summon
#
# @within	???
#

# Tag the current player to ride the new kart
tag @s add shopping_kart.owner

# Summon the pig
scoreboard players set #model shopping_kart.data 0
data modify storage shopping_kart:data ForcedRotation set from entity @s Rotation
execute summon pig at @s run function shopping_kart:kart/switch_model/init_functions

# Remove the temporary player tag
tag @s remove shopping_kart.owner

