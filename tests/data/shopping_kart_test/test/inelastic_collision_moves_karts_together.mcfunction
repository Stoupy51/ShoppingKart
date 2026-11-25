
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy inelastic_a spawn
execute positioned ~4 ~1 ~4 run dummy inelastic_b spawn
execute as inelastic_a at @s run function shopping_kart:kart/summon
execute as inelastic_b at @s run function shopping_kart:kart/summon
await entity @a[name=inelastic_a,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=inelastic_b,predicate=shopping_kart:has_kart_vehicle]
execute as inelastic_a on vehicle run tag @s add inelastic.a
execute as inelastic_b on vehicle run tag @s add inelastic.b
scoreboard players set @e[tag=inelastic.a] shopping_kart.restitution 0
scoreboard players set @e[tag=inelastic.b] shopping_kart.restitution 0
scoreboard players set @e[tag=inelastic.a] shopping_kart.collision_factor 1
scoreboard players set @e[tag=inelastic.b] shopping_kart.collision_factor 1
execute as @n[tag=inelastic.a] run tp @s ~1.5 ~1 ~4.5
execute as @n[tag=inelastic.b] run tp @s ~2.45 ~1 ~4.5
scoreboard players set @e[tag=inelastic.a] shopping_kart.motion_x 3000000

# After 0.3 block the karts share the striker's 0.24 block per tick and roll 0.6 block side by side
await delay 40t
execute positioned ~2.4 ~1 ~4.5 run assert entity @n[tag=inelastic.a,distance=..0.15]
execute positioned ~3.05 ~1 ~4.5 run assert entity @n[tag=inelastic.b,distance=..0.15]
