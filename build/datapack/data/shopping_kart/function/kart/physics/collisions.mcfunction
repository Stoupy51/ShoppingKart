
#> shopping_kart:kart/physics/collisions
#
# @executed	at @s[tag=!shopping_kart.forced_acceleration]
#
# @within	shopping_kart:kart/physics/calculation
#

# Vanilla never pushes an entity carrying passengers, so karts collide here with the karts and players on foot they touch
# Velocities are the motion scores, in 10^-7 block per tick, and a kart with a factor of 0 takes no part on either side
scoreboard players operation #vx shopping_kart.data = @s shopping_kart.motion_x
scoreboard players operation #vz shopping_kart.data = @s shopping_kart.motion_z
scoreboard players operation #restitution shopping_kart.data = @s shopping_kart.restitution
scoreboard players set #collision_x shopping_kart.data 0
scoreboard players set #collision_z shopping_kart.data 0
execute as @e[tag=shopping_kart.kart,distance=0.01..0.9,scores={shopping_kart.collision_factor=1..}] at @s run function shopping_kart:kart/physics/collide_kart
execute as @a[gamemode=!spectator,predicate=!shopping_kart:has_vehicle,distance=0.01..0.75] at @s run function shopping_kart:kart/physics/collide_player

# Push apart along the summed unit vectors at scale 1000: halved, a factor of 1000 gives the 0.05 block per tick of vanilla
scoreboard players operation #collision_x shopping_kart.data *= @s shopping_kart.collision_factor
scoreboard players operation #collision_z shopping_kart.data *= @s shopping_kart.collision_factor
scoreboard players operation #collision_x shopping_kart.data /= #2 shopping_kart.data
scoreboard players operation #collision_z shopping_kart.data /= #2 shopping_kart.data
scoreboard players operation #vx shopping_kart.data += #collision_x shopping_kart.data
scoreboard players operation #vz shopping_kart.data += #collision_z shopping_kart.data
scoreboard players operation @s shopping_kart.motion_x = #vx shopping_kart.data
scoreboard players operation @s shopping_kart.motion_z = #vz shopping_kart.data

