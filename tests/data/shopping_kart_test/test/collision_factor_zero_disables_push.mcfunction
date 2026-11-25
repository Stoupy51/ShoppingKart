
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy zero_a spawn
execute positioned ~4 ~1 ~4 run dummy zero_b spawn
execute as zero_a at @s run function shopping_kart:kart/summon
execute as zero_b at @s run function shopping_kart:kart/summon
await entity @a[name=zero_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=zero_b,predicate=shopping_kart:has_kart_vehicle]
execute as zero_a on vehicle run tag @s add zero.a
execute as zero_b on vehicle run tag @s add zero.b
scoreboard players set @e[tag=zero.a] shopping_kart.collision_factor 0
scoreboard players set @e[tag=zero.b] shopping_kart.collision_factor 0
execute as @n[tag=zero.a] run tp @s ~1.5 ~1 ~4.5
execute as @n[tag=zero.b] run tp @s ~2.45 ~1 ~4.5
scoreboard players set @e[tag=zero.a] shopping_kart.motion_x 3000000

# The moving kart rolls its full 1.5 blocks through the still one, which is neither hit nor pushed
await delay 40t
execute positioned ~3 ~1 ~4.5 run assert entity @n[tag=zero.a,distance=..0.15]
execute positioned ~2.45 ~1 ~4.5 run assert entity @n[tag=zero.b,distance=..0.01]
