# Important

This library is not finished, still working on support for other operands and bin -> hex instructions for hex PROM & icache.

This library is also quite buggy, bugreports are appreciated!

*NOTE*  This library requres the libraries `mcschematic` and `pygame` install them via:

```bash
pip install pygame
pip install mcschematic
```

# Documentation

## To import the library, use:

```py
from minecraftCPUlib import Schematic, Compile, CPU
```

## Compile

You can compile programs into bin or hex using a custom compiler I built

```py
isa = {
    "instructions": ['noop', 'ldi', 'rst', 'rld', 'add', 'sub', 'or', 'nor', 'and', 'nand', 'xor', 'xnor', 'imp', 'nimp', 'inc_a', 'dec', 'pst', 'pld', 'hlt', 'jmp', 'brc', 'rast', 'rald', 'acw', 'inc'] # All of your instructions from your ISA, sorted from 0-max
    "flags": ['none', 'zero', 'cout'] # Same with your flags
}

compiled = Compile(cpu.get_code(), ISA=isa) # Init your compiled program.
```

### Binary

You can convert your instructions into binary code, which can use your ISA.

```py
c = compiled.to_binary()
```

### Hex

Currently, hex is being worked on... It will probably be available in the future, but it's still quite buggy and WIP.

## Schematic

You can convert your compiled code into a minecraft schematic.

```py
s = Schematic(c)
s.binary("my_program") # without the .schem
```

The distance arguement is how far apart the blocks should be. Max X is how many barrels should be in a row.

## CPU

### Examples

#### Start

```py
from minecraftCPUlib import CPU, Compile, Schematic

cpu = CPU.OP_1(bits=8, register_count=4, ram_cells=0, port_count=3, output_ports=True, simulation_speed=10)
```

### Execute

#### Description

Execute your CPU. When defining it you can select if there should be an output file and if it should print the ports. You can use `CPU().execute()`

### Load Immediate

#### Description

To load an immediate, you can use the function `CPU().load_immediate(value)` , where `value` is the immediate value. The immediate will be stored in the ACC.

#### Examples

```py
cpu.load_immediate(128) # Will load an immmediate of value 128 and store it into the ACC
```

### Register Read

#### Description

To read from a register, you can use the function `CPU().register_read(address)`, where `address`  is the register you are reading from. The output will be stored into the ACC. *NOTE* you will probably get an index error if define the address as a greater number then the amount of registers your CPU contains.

#### Examples

```py
cpu.register_read(3) # NOTE: the first registers address is 0, so register 2's address would be 1.
```

### Register Write

#### Description

To write to a register, you can use the function `CPU().register_write(address)`, where `address` is the register you are writing to. The value stored in the ACC will move to the register.

#### Examples

```py
cpu.load_immediate(128)
cpu.register_store(1) # Will store the ACC's value (128) into register address 1.
```

### RAM write, read

#### Description

writing and reading from the RAM is basically the same as writing and reading from a register. Caching will be introduced to this library soon. You can use the functions `CPU().ram_write(address)` `CPU().ram_read(address)`

### Jump, Branch

To jump, you can use the functin `CPU().jump(address)` where `address` is which instruction you're jumping to. *NOTE* instrsuction 0 is the first instruction, instead of instruction 1. Branching is quite similair but, you also have a flag arguement. flag 0 is zero flag and flag 1 is COUT. `CPU().branch(address, flag)`

#### Description

```py
# Fibonacci example

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

cpu.branch(13, 1) # Branch outside of the jump loop if cout flag
cpu.jump(2) # Jump to the start of the program
```

### Port Write

#### Description

To write to the ports, you can use the function `CPU.port_write(address)`, where `address` is the port you are writing to. Basically the same as Register Write, but to different memory.

#### Examples

````py
cpu.increment()
cpu.increment()
cpu.port_write(0) # Will write the value 2 into port 0
```
````

### Port Read

#### Description

To read from the ports you can use the function `CPU().port_read(address)`, where `address` is the port you are reading from. It is basically like Register Read. You can also write values to the ports from outside the CPU program with `CPU().write_to_port(address, value)`

#### Examples

```py
from threading import Thread

cpu.port_read(0)
cpu.port_write(1)
cpu.jump(0) # Jump to instruction 0

CPU_thread = Thread(target=cpu.execute)
CPU_thread.daemon = True
CPU_thread.start()

while True:
    cpu.write_to_port(int(input(""))
```

### Increment

#### Description

To increment the ACC (acc = acc + 1), you can use the function `CPU().increment()`. This instruction does not have any operands.

#### Examples

```py
cpu.load_immediate(53)
cpu.increment() # The ACC will now contain the value 54, instead of 53.
```

### Decrement

#### Description

To decrement the ACC (acc = acc - 1), you can use the function `CPU().decrement()`. This instruction does not have any operands.

#### Examples

```py
cpu.load_immediate(129)
cpu.decrement() # The ACC will now contain the value 128, instead of 129.
```

### Add

#### Description

To add two values together, you can use the function `CPU.add(address)`, where address is the register you are doing addition with. This instruction will perform `ACC = ACC + register[address]`, in other words, it will add the ACC with a register and the otuput will be stored into the ACC.

#### Examples

```py
cpu.load_immediate(2)
cpu.register_store(0)
cpu.load_immediate(4)
cpu.add(0) # Will add ACC with register 0.
```

### Sub

#### Description

To subtract from the ACC, using a register address, you can use the function `CPU.sub(address)`, where address is the register you are subtracting from the ACC.

#### Examples

```py
cpu.load_immediate(10)
cpu.register_store(1)
cpu.load_immediate(8)
cpu.sub(1) # ACC - reg1 = ACC
```

### Other arithmetic

Here, will be other arithmetic you can perform with this library. All these commands are exactly like Sub and Add, in the sense of addresses and storing stuff into the ACC. If you wanted to perform addition and then store it into a register

```py
cpu.load_immediate(2)
cpu.register_store(0)
cpu.load_immediate(4)
cpu.add(0)

cpu.register_store(3) # Store into register 3.
```

#### XOR, XNOR

You can use the function `cpu.XOR(address)` and the same for XNOR, just change XOR: `cpu.XNOR(address)`

#### AND, NAND, OR, NOR

The same as XOR and XNOR.
