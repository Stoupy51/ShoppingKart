
# @template shopping_kart_test:room
# @timeout 100
await score #shopping_kart.loaded load.status matches 1
fill ~ ~ ~ ~8 ~ ~8 minecraft:stone
execute positioned ~4 ~1 ~4 run dummy signal_striker spawn
execute positioned ~4 ~1 ~4 run dummy signal_struck spawn
execute as signal_striker at @s run function shopping_kart:kart/summon
execute as signal_struck at @s run function shopping_kart:kart/summon
await entity @a[name=signal_striker,predicate=shopping_kart:has_kart_vehicle]
await entity @a[name=signal_struck,predicate=shopping_kart:has_kart_vehicle]
execute as signal_striker on vehicle run tag @s add signal.striker
execute as signal_struck on vehicle run tag @s add signal.struck
execute as @n[tag=signal.striker] run tp @s ~1.5 ~1 ~4.5
execute as @n[tag=signal.struck] run tp @s ~2.45 ~1 ~4.5
scoreboard players set @e[tag=signal.striker] shopping_kart.motion_x 3000000

# The signal tags the struck kart and its driver as victims, the striking kart and its driver as attackers, then clears both tags
await delay 40t
assert entity @e[tag=signal.struck,scores={shopping_kart_test.hits=1}]
assert entity @a[name=signal_struck,scores={shopping_kart_test.hits=1}]
assert entity @a[name=signal_striker,scores={shopping_kart_test.attacks=1}]
assert not entity @e[tag=signal.striker,scores={shopping_kart_test.hits=1..}]
assert not entity @e[tag=shopping_kart.attacker]
assert not entity @e[tag=shopping_kart.victim]
