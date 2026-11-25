
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy apart_a spawn
execute positioned ~4 ~1 ~4 run dummy apart_b spawn
execute as apart_a at @s run function shopping_kart:kart/summon
execute as apart_b at @s run function shopping_kart:kart/summon
await entity @a[name=apart_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=apart_b,predicate=shopping_kart:has_kart_vehicle]
execute as apart_a on vehicle run tag @s add apart.a
execute as apart_b on vehicle run tag @s add apart.b
execute as @n[tag=apart.a] run tp @s ~4.25 ~1 ~4.5
execute as @n[tag=apart.b] run tp @s ~4.75 ~1 ~4.5

await delay 20t
execute positioned ~4.25 ~1 ~4.5 run assert entity @n[tag=apart.a,distance=0.5..]
execute positioned ~4.75 ~1 ~4.5 run assert entity @n[tag=apart.b,distance=0.5..]
execute at @n[tag=apart.a] run assert entity @n[tag=apart.b,distance=1.5..]
