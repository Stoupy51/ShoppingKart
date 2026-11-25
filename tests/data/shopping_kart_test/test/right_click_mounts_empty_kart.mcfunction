
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy mount_rider spawn
execute as mount_rider at @s run function shopping_kart:kart/summon
await entity @a[name=mount_rider,predicate=shopping_kart:has_kart_vehicle]
execute as mount_rider on vehicle run tag @s add mount.kart
await delay 5t
assert not entity @e[tag=mount.kart,predicate=shopping_kart:has_mount_passenger]

ride mount_rider dismount
await entity @e[tag=mount.kart,predicate=shopping_kart:has_mount_passenger]
execute as @e[tag=mount.kart] on passengers if entity @s[tag=shopping_kart.mount] run tag @s add mount.interaction
dummy mount_rider use entity @e[tag=mount.interaction,limit=1]
await entity @a[name=mount_rider,predicate=shopping_kart:has_kart_vehicle]
await not entity @e[tag=mount.interaction]
