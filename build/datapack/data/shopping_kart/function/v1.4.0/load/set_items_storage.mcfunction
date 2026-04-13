
#> shopping_kart:v1.4.0/load/set_items_storage
#
# @within	shopping_kart:v1.4.0/load/confirm_load
#

# Items storage
data modify storage shopping_kart:items all set value {}
data modify storage shopping_kart:items all.shopping_kart set value {"id": "minecraft:command_block","count": 1,"components": {"minecraft:item_model": "shopping_kart:shopping_kart","minecraft:item_name": {"text": "Shopping Kart"},"minecraft:lore": [["",{"text": "I","color": "white","italic": false,"font": "shopping_kart:icons"},{"text": " ShoppingKart","italic": true,"color": "blue"}]],"minecraft:custom_data": {"shopping_kart": {"shopping_kart": true},"smithed": {"id": "shopping_kart:shopping_kart","origin": "shopping_kart","ignore": {"functionality": true,"crafting": true}}}}}

