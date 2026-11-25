
# @template shopping_kart_test:room
# @timeout 140
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy once_driver spawn
execute as once_driver at @s run function shopping_kart:kart/summon
await entity @a[name=once_driver,predicate=shopping_kart:has_kart_vehicle]
execute as once_driver on vehicle run tag @s add once.kart
execute positioned ~2.45 ~1 ~4.5 run dummy once_walker spawn
execute as @n[tag=once.kart] run tp @s ~1.5 ~1 ~4.5
scoreboard players set @e[tag=once.kart] shopping_kart.motion_x 5000000

# A Ward dummy stays where it is when launched, so the kart keeps closing in for several ticks of the same hit
await delay 40t
assert entity @a[name=once_walker,scores={shopping_kart_test.hits=1}]

execute as @n[tag=once.kart] run tp @s ~1.5 ~1 ~4.5
scoreboard players set @e[tag=once.kart] shopping_kart.motion_x 5000000
await delay 40t
assert entity @a[name=once_walker,scores={shopping_kart_test.hits=2}]
