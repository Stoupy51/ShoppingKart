
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~2 run dummy x1_a spawn
execute positioned ~4 ~1 ~2 run dummy x1_b spawn
execute positioned ~4 ~1 ~6 run dummy x5_a spawn
execute positioned ~4 ~1 ~6 run dummy x5_b spawn
execute as x1_a at @s run function shopping_kart:kart/summon
execute as x1_b at @s run function shopping_kart:kart/summon
execute as x5_a at @s run function shopping_kart:kart/summon
execute as x5_b at @s run function shopping_kart:kart/summon
await entity @a[name=x1_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=x1_b,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=x5_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=x5_b,predicate=shopping_kart:has_kart_vehicle]
execute as x1_a on vehicle run tag @s add x1.a
execute as x1_b on vehicle run tag @s add x1.b
execute as x5_a on vehicle run tag @s add x5.a
execute as x5_b on vehicle run tag @s add x5.b
scoreboard players set @e[tag=x5.a] shopping_kart.collision_factor 5000
scoreboard players set @e[tag=x5.b] shopping_kart.collision_factor 5000
execute as @n[tag=x1.a] run tp @s ~4.25 ~1 ~2.5
execute as @n[tag=x1.b] run tp @s ~4.75 ~1 ~2.5
execute as @n[tag=x5.a] run tp @s ~4.25 ~1 ~6.5
execute as @n[tag=x5.b] run tp @s ~4.75 ~1 ~6.5

await delay 30t
execute at @n[tag=x1.a] run assert entity @n[tag=x1.b,distance=1.5..2.5]
execute at @n[tag=x5.a] run assert entity @n[tag=x5.b,distance=2.6..]
