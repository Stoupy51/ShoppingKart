
#> shopping_kart:kart/mount/init
#
# @executed	at @s[tag=!shopping_kart.forced_acceleration]
#
# @within	shopping_kart:kart/tick/calculations
#

# A passenger sits 0.87 above a pig's feet, so this box covers the top of the kart
tag @s add shopping_kart.mount
data merge entity @s {width:1.2f,height:0.4f}
ride @s mount @n[tag=shopping_kart.kart,tag=shopping_kart.temp,distance=..0.01]

