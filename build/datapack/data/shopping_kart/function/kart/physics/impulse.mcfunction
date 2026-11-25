
#> shopping_kart:kart/physics/impulse
#
# @within	string in shopping_kart:kart/physics/collide_kart
#			string in shopping_kart:kart/physics/collide_player
#

# Impulse between equal masses along n, the unit vector from the other body to the kart: j = -(1 + e) (v_kart - v_other) . n / 2
# Takes #vx/#vz the kart's velocity, #rel_x/#rel_z the other body's, #nx/#nz the normal at scale 1000 and #e the restitution at scale 1000
# Adds #ix/#iz, the velocity j n, to #vx/#vz; the caller takes it from the other body

# Closing speed (v_other - v_kart) . n at scale 10^7, divided by 1000 before the products so they fit in an int
scoreboard players operation #rel_x shopping_kart.data -= #vx shopping_kart.data
scoreboard players operation #rel_z shopping_kart.data -= #vz shopping_kart.data
scoreboard players operation #rel_x shopping_kart.data /= #1000 shopping_kart.data
scoreboard players operation #rel_z shopping_kart.data /= #1000 shopping_kart.data
scoreboard players operation #rel_x shopping_kart.data *= #nx shopping_kart.data
scoreboard players operation #rel_z shopping_kart.data *= #nz shopping_kart.data
scoreboard players operation #j shopping_kart.data = #rel_x shopping_kart.data
scoreboard players operation #j shopping_kart.data += #rel_z shopping_kart.data
execute if score #j shopping_kart.data matches ..0 run return fail

# j at scale 10^4, capped at 1 block per tick
scoreboard players add #e shopping_kart.data 1000
scoreboard players operation #j shopping_kart.data /= #1000 shopping_kart.data
scoreboard players operation #j shopping_kart.data *= #e shopping_kart.data
scoreboard players operation #j shopping_kart.data /= #1000 shopping_kart.data
scoreboard players operation #j shopping_kart.data /= #2 shopping_kart.data
scoreboard players operation #j shopping_kart.data < #10000 shopping_kart.data
scoreboard players operation #ix shopping_kart.data = #nx shopping_kart.data
scoreboard players operation #iz shopping_kart.data = #nz shopping_kart.data
scoreboard players operation #ix shopping_kart.data *= #j shopping_kart.data
scoreboard players operation #iz shopping_kart.data *= #j shopping_kart.data
scoreboard players operation #vx shopping_kart.data += #ix shopping_kart.data
scoreboard players operation #vz shopping_kart.data += #iz shopping_kart.data
return 1

