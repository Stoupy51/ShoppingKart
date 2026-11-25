
#> shopping_kart:kart/mount/clicked
#
# @executed	as the player & at current position
#
# @within	advancement shopping_kart:mount_kart
#

# Each clicked interaction mounts the player who clicked it, so two clicks in the same tick are both handled
advancement revoke @s only shopping_kart:mount_kart
execute as @e[type=interaction,tag=shopping_kart.mount,distance=..8] if data entity @s interaction run function shopping_kart:kart/mount/ride

