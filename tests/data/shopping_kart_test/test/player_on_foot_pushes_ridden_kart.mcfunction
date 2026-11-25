
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy foot_rider spawn
execute as foot_rider at @s run function shopping_kart:kart/summon
await entity @a[name=foot_rider,predicate=shopping_kart:has_kart_vehicle]
execute as foot_rider on vehicle run tag @s add foot.kart
execute positioned ~4 ~1 ~4 run dummy foot_walker spawn
execute as @n[tag=foot.kart] run tp @s ~4.25 ~1 ~4.5
tp foot_walker ~4.75 ~1 ~4.5

await delay 20t
execute positioned ~4.25 ~1 ~4.5 run assert entity @n[tag=foot.kart,distance=0.3..]
