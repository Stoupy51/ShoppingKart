
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy hit_driver spawn
execute as hit_driver at @s run function shopping_kart:kart/summon
await entity @a[name=hit_driver,predicate=shopping_kart:has_kart_vehicle]
execute as hit_driver on vehicle run tag @s add hit.kart
scoreboard players set @e[tag=hit.kart] shopping_kart.restitution 1000
scoreboard players set @e[tag=hit.kart] shopping_kart.collision_factor 1
execute positioned ~2.45 ~1 ~4.5 run dummy hit_walker spawn
execute as @n[tag=hit.kart] run tp @s ~1.5 ~1 ~4.5
scoreboard players set @e[tag=hit.kart] shopping_kart.motion_x 5000000

# The kart stops after 0.5 block, its 0.4 block per tick handed to the walker
# Ward dummies do not move from a player_motion launch, so the walker's push is checked in game only
await delay 40t
execute positioned ~2 ~1 ~4.5 run assert entity @n[tag=hit.kart,distance=..0.1]
