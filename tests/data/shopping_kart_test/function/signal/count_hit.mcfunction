
execute if entity @s[tag=shopping_kart.victim] if entity @e[tag=shopping_kart.kart,tag=shopping_kart.attacker] run scoreboard players add @e[tag=shopping_kart.victim] shopping_kart_test.hits 1
scoreboard players add @a[tag=shopping_kart.attacker] shopping_kart_test.attacks 1
