
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy elastic_striker spawn
execute positioned ~4 ~1 ~4 run dummy elastic_leaver spawn
execute as elastic_striker at @s run function shopping_kart:kart/summon
execute as elastic_leaver at @s run function shopping_kart:kart/summon
await entity @a[name=elastic_striker,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=elastic_leaver,predicate=shopping_kart:has_kart_vehicle]
execute as elastic_striker on vehicle run tag @s add elastic.striker
execute as elastic_leaver on vehicle run tag @s add elastic.parked
ride elastic_leaver dismount
dummy elastic_leaver leave
scoreboard players set @e[tag=elastic.striker] shopping_kart.restitution 1000
scoreboard players set @e[tag=elastic.parked] shopping_kart.restitution 1000
scoreboard players set @e[tag=elastic.striker] shopping_kart.collision_factor 1
scoreboard players set @e[tag=elastic.parked] shopping_kart.collision_factor 1
execute as @n[tag=elastic.striker] run tp @s ~1.5 ~1 ~4.5
execute as @n[tag=elastic.parked] run tp @s ~2.45 ~1 ~4.5
scoreboard players set @e[tag=elastic.striker] shopping_kart.motion_x 3000000

# The striker rolls 0.3 block, hands its 0.24 block per tick to the empty kart and stops; the empty kart rolls 1.2 blocks
await delay 40t
execute positioned ~1.8 ~1 ~4.5 run assert entity @n[tag=elastic.striker,distance=..0.15]
execute positioned ~3.65 ~1 ~4.5 run assert entity @n[tag=elastic.parked,distance=..0.15]
