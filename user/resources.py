
# ruff: noqa: E501
# Imports
from beet import BlockTag, Predicate
from stewbeet import Context, JsonDict, set_json_encoder


# Setup json resources (loot tables, predicates, tags, ...)
def setup_resources(ctx: Context) -> None:
	ns: str = ctx.project_id

	json_content: JsonDict

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"vehicle":{"nbt":f"{{Tags:[\"{ns}.kart\"]}}"}}}
	ctx.data[ns].predicates["has_kart_vehicle"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_scores","entity":"this","scores":{f"{ns}.id":{"min":{"type":"minecraft:score","target":{"type":"minecraft:fixed","name":"#predicate"},"score":f"{ns}.id"},"max":{"type":"minecraft:score","target":{"type":"minecraft:fixed","name":"#predicate"},"score":f"{ns}.id"}}}}
	ctx.data[ns].predicates["has_same_id"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"vehicle":{}}}
	ctx.data[ns].predicates["has_vehicle"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"vehicle":{"nbt":f"{{Tags:[\"{ns}.temp\"]}}"}}}
	ctx.data[ns].predicates["has_vehicle_with_tag"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"passenger":{}}}
	ctx.data[ns].predicates["have_passenger"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"passenger":{"minecraft:entity_type":"minecraft:player"}}}
	ctx.data[ns].predicates["have_player_passenger"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"passenger":{"minecraft:entity_type":"minecraft:player","nbt":f"{{Tags:[\"{ns}.temp\"]}}"}}}
	ctx.data[ns].predicates["have_temp_player_passenger"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:location_check","predicate":{"block":{"blocks":["minecraft:water"]}}}
	ctx.data[ns].predicates["in_water"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:any_of","terms":[{"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"forward":True}}}},{"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"backward":True}}}},{"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"left":True}}}},{"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"right":True}}}}]}
	ctx.data[ns].predicates["input/any"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"backward":True}}}}
	ctx.data[ns].predicates["input/backward"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"forward":True}}}}
	ctx.data[ns].predicates["input/forward"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"left":True}}}}
	ctx.data[ns].predicates["input/left"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"condition":"minecraft:entity_properties","entity":"this","predicate":{"minecraft:type_specific/player":{"input":{"right":True}}}}
	ctx.data[ns].predicates["input/right"] = set_json_encoder(Predicate(json_content), max_level=-1)

	json_content = {"values":["white_concrete","orange_concrete","magenta_concrete","light_blue_concrete","yellow_concrete","lime_concrete","pink_concrete","gray_concrete","light_gray_concrete","cyan_concrete","purple_concrete","blue_concrete","brown_concrete","green_concrete","red_concrete","black_concrete"]}
	ctx.data[ns].block_tags["kart_surfaces/fast"] = set_json_encoder(BlockTag(json_content))

	json_content = {"values":["ice","packed_ice","blue_ice"]}
	ctx.data[ns].block_tags["kart_surfaces/slippery"] = set_json_encoder(BlockTag(json_content))

	json_content = {"values":["dirt","coarse_dirt","rooted_dirt","farmland","grass_block","mycelium","podzol","sand","red_sand","gravel","clay","snow_block","snow","soul_soil","moss_block","suspicious_sand","suspicious_gravel"]}
	ctx.data[ns].block_tags["kart_surfaces/slow"] = set_json_encoder(BlockTag(json_content))

	json_content = {"values":["soul_sand","mud","mud_brick_slab","mud_brick_stairs","mud_brick_wall","honey_block","slime_block"]}
	ctx.data[ns].block_tags["kart_surfaces/very_slow"] = set_json_encoder(BlockTag(json_content))

