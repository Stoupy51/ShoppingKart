
# ruff: noqa: E501
# Imports
from beet import Context
from stewbeet import write_function


# Setup math functions functions
def setup_math_functions(ctx: Context) -> None:
	ns: str = ctx.project_id

	write_function(f"{ns}:math/sqrt", f"""
# Initialize values
scoreboard players set #output {ns}.data 0
scoreboard players set #increment {ns}.data 32768
# Execute recursive function
function {ns}:math/sqrt_loop

""")

	write_function(f"{ns}:math/sqrt_loop", f"""
# Compute test
scoreboard players operation #test {ns}.data = #output {ns}.data
scoreboard players operation #test {ns}.data += #increment {ns}.data
scoreboard players operation #test {ns}.data *= #test {ns}.data
# Compare values
execute if score #test {ns}.data <= #input {ns}.data run scoreboard players operation #output {ns}.data += #increment {ns}.data
# Execute recursive function
scoreboard players operation #increment {ns}.data /= #2 {ns}.data
execute if score #increment {ns}.data matches 1.. run function {ns}:math/sqrt_loop

""")

