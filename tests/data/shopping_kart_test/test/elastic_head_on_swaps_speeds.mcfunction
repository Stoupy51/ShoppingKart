
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy head_on_a spawn
execute positioned ~4 ~1 ~4 run dummy head_on_b spawn
execute as head_on_a at @s run function shopping_kart:kart/summon
execute as head_on_b at @s run function shopping_kart:kart/summon
await entity @a[name=head_on_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=head_on_b,predicate=shopping_kart:has_kart_vehicle]
execute as head_on_a on vehicle run tag @s add head_on.a
execute as head_on_b on vehicle run tag @s add head_on.b
scoreboard players set @e[tag=head_on.a] shopping_kart.restitution 1000
scoreboard players set @e[tag=head_on.b] shopping_kart.restitution 1000
scoreboard players set @e[tag=head_on.a] shopping_kart.collision_factor 1
scoreboard players set @e[tag=head_on.b] shopping_kart.collision_factor 1
execute as @n[tag=head_on.a] run tp @s ~3.3 ~1 ~4.5
execute as @n[tag=head_on.b] run tp @s ~4.7 ~1 ~4.5
scoreboard players set @e[tag=head_on.a] shopping_kart.motion_x 3000000
scoreboard players set @e[tag=head_on.b] shopping_kart.motion_x -3000000

# Each kart rolls 0.3 block in, then bounces back 1.2 blocks at the speed the other one came with
await delay 40t
execute positioned ~2.4 ~1 ~4.5 run assert entity @n[tag=head_on.a,distance=..0.15]
execute positioned ~5.6 ~1 ~4.5 run assert entity @n[tag=head_on.b,distance=..0.15]
