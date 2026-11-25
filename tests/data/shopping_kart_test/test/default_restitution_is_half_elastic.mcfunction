
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy half_a spawn
execute positioned ~4 ~1 ~4 run dummy half_b spawn
execute as half_a at @s run function shopping_kart:kart/summon
execute as half_b at @s run function shopping_kart:kart/summon
await entity @a[name=half_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=half_b,predicate=shopping_kart:has_kart_vehicle]
execute as half_a on vehicle run tag @s add half.a
execute as half_b on vehicle run tag @s add half.b
scoreboard players set @e[tag=half.a] shopping_kart.collision_factor 1
scoreboard players set @e[tag=half.b] shopping_kart.collision_factor 1
execute as @n[tag=half.a] run tp @s ~1.5 ~1 ~4.5
execute as @n[tag=half.b] run tp @s ~2.45 ~1 ~4.5
scoreboard players set @e[tag=half.a] shopping_kart.motion_x 3000000

# With e = 0.5 the striker keeps a quarter of its 0.24 block per tick and the other kart takes three quarters
await delay 40t
execute positioned ~2.1 ~1 ~4.5 run assert entity @n[tag=half.a,distance=..0.15]
execute positioned ~3.35 ~1 ~4.5 run assert entity @n[tag=half.b,distance=..0.15]
