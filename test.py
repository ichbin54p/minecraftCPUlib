from minecraftCPUlib import CPU, Compile, Schematic

cpu = CPU.OP_1(register_count=4, ram_cells=0, port_count=1, output_ports=True, simulation_speed=10)

# Basic Fibb Program

# SETUP

cpu.increment()
cpu.register_write(0)

# LOOP

cpu.register_read(1)
cpu.port_write(0)
cpu.add(0)
cpu.register_write(1)

cpu.register_read(0)
cpu.port_write(0)
cpu.add(1)
cpu.register_write(0)

cpu.branch(12, 1)
cpu.jump(2)

isa = {
    "instructions": ['noop', 'ldi', 'rst', 'rld', 'add', 'sub', 'or', 'nor', 'and', 'nand', 'xor', 'xnor', 'imp', 'nimp', 'inc_a', 'dec', 'pst', 'pld', 'hlt', 'jmp', 'brc', 'rast', 'rald', 'acw', 'inc'],
    "flags": ['none', 'zero', 'cout']
}

program = Compile(cpu.get_program(), isa)
schem = Schematic(program.to_hex(), max_x=16)
schem.hex("fibb")

cpu.execute()