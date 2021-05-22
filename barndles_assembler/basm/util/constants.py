"""
A nested dictionary of all BARNDLES mnemonics, their op codes, their supported
optional suffix flags, and the number of operands they support.

Dictionary formatted as {
    "MNEMONIC": {
        "mnemonic": MNEMONIC
        "opcode":   OP_CODE,
        "flags":    ["FLAG_1", "FLAG_2"],
        "operands": (NUM_IMM_OPERANDS, NUM_NONIMM_OPERANDS),
    }
}
"""
mnemonics = {
    "DON": {
        "mnemonic": "DON",
        "opcode":   0x00,
        "flags":    [],
        "operands": (0, 0)
    },
    "MOV": {
        "mnemonic": "MOV",
        "opcode":   0x01,
        "flags":    ["N", "S"],
        "operands": (2, 2)
    },
    "ADD": {
        "mnemonic": "ADD",
        "opcode": 0x02,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "SUB": {
        "mnemonic": "SUB",
        "opcode": 0x03,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "MUL": {
        "mnemonic": "MUL",
        "opcode": 0x04,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "DIV": {
        "mnemonic": "DIV",
        "opcode": 0x05,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "AND": {
        "mnemonic": "AND",
        "opcode": 0x06,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "ORR": {
        "mnemonic": "ORR",
        "opcode": 0x07,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "XOR": {
        "mnemonic": "XOR",
        "opcode": 0x08,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "LGA": {
        "mnemonic": "LGA",
        "opcode": 0x09,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "LGO": {
        "mnemonic": "LGO",
        "opcode": 0x0A,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "LGX": {
        "mnemonic": "LGX",
        "opcode": 0x0B,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "LSL": {
        "mnemonic": "LSL",
        "opcode": 0x0C,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "LSR": {
        "mnemonic": "LSR",
        "opcode": 0x0D,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "ASR": {
        "mnemonic": "ASR",
        "opcode": 0x0E,
        "flags": ["N", "S"],
        "operands": (3, 2)
    },
    "CPA": {
        "mnemonic": "CPA",
        "opcode": 0x0F,
        "flags": [],
        "operands": (2, 2)
    },
    "CPS": {
        "mnemonic": "CPS",
        "opcode": 0x10,
        "flags": [],
        "operands": (2, 2)
    },
    "BCH": {
        "mnemonic": "BCH",
        "opcode": 0x11,
        "flags": [],
        "operands": (1, 1)
    },
    "BAL": {
        "mnemonic": "BAL",
        "opcode": 0x12,
        "flags": [],
        "operands": (1, 1)
    },
    "BEQ": {
        "mnemonic": "BEQ",
        "opcode": 0x13,
        "flags": [],
        "operands": (1, 1)
    },
    "BNE": {
        "mnemonic": "BNE",
        "opcode": 0x14,
        "flags": [],
        "operands": (1, 1)
    },
    "BGT": {
        "mnemonic": "BGT",
        "opcode": 0x15,
        "flags": [],
        "operands": (1, 1)
    },
    "BLT": {
        "mnemonic": "BLT",
        "opcode": 0x16,
        "flags": [],
        "operands": (1, 1)
    },
    "BGE": {
        "mnemonic": "BGE",
        "opcode": 0x17,
        "flags": [],
        "operands": (1, 1)
    },
    "BLE": {
        "mnemonic": "BLE",
        "opcode": 0x18,
        "flags": [],
        "operands": (1, 1)
    },
    "LDR": {
        "mnemonic": "LDR",
        "opcode": 0x19,
        "flags": [],
        "operands": (2, 2)
    },
    "STR": {
        "mnemonic": "STR",
        "opcode": 0x1A,
        "flags": [],
        "operands": (2, 2)
    },
    "PSH": {
        "mnemonic": "PSH",
        "opcode": 0x1B,
        "flags": [],
        "operands": (1, 1)
    },
    "POP": {
        "mnemonic": "POP",
        "opcode": 0x1C,
        "flags": [],
        "operands": (1, 1)
    },
}

"""
A nested dictionary of all BARNDLES registers and their aliases.

Dictionary formatted as {
    REGISTER_INDEX: {
        "index":   REGISTER_INDEX
        "aliases": ["ALIAS_1", "ALIAS_2"],
    }
}
"""
registers = {
    0x00: {"index": 0x00, "name": "R0",   "aliases": ["R0", "R00"]},
    0x01: {"index": 0x01, "name": "R1",   "aliases": ["R1", "R01"]},
    0x02: {"index": 0x02, "name": "R2",   "aliases": ["R2", "R02"]},
    0x03: {"index": 0x03, "name": "R3",   "aliases": ["R3", "R03"]},
    0x04: {"index": 0x04, "name": "R4",   "aliases": ["R4", "R04"]},
    0x05: {"index": 0x05, "name": "R5",   "aliases": ["R5", "R05"]},
    0x06: {"index": 0x06, "name": "R6",   "aliases": ["R6", "R06"]},
    0x07: {"index": 0x07, "name": "R7",   "aliases": ["R7", "R07"]},
    0x08: {"index": 0x08, "name": "R8",   "aliases": ["R8", "R08"]},
    0x09: {"index": 0x09, "name": "R9",   "aliases": ["R9", "R09"]},
    0x0A: {"index": 0x0A, "name": "R10",  "aliases": ["R10"]},
    0x0B: {"index": 0x0B, "name": "R11",  "aliases": ["R11"]},
    0x0C: {"index": 0x0C, "name": "SP",   "aliases": ["R12", "SP"]},
    0x0D: {"index": 0x0D, "name": "LR",   "aliases": ["R13", "LR"]},
    0x0E: {"index": 0x0E, "name": "PC",   "aliases": ["R14", "PC"]},
    0x0F: {"index": 0x0F, "name": "CPSR", "aliases": ["R15", "CPSR"]},
}

"""
The section identifier for the read-only memory section
"""
read_only_section_identifier = "READ-ONLY"

"""
The section identifier for the read-write memory section
"""
read_write_section_identifier = "READ-WRITE"

"""
The section identifier for the instruction memory section
"""
instruction_section_identifier = "INSTRUCTION"

"""
A list of valid section names
"""
section_identifiers = [
    read_only_section_identifier,
    read_write_section_identifier,
    instruction_section_identifier
]

"""
The maximum value for an unsigned 12-bit number
"""
unsigned_immediate_max = 4095

"""
The minimum value for an unsigned 12-bit number
"""
unsigned_immediate_min = 0

"""
The maximum value for a signed 12-bit number
"""
signed_immediate_max = 2047

"""
The minimum value for a signed 12-bit number
"""
signed_immediate_min = -2048

"""
The base address of BARNDLES instruction memory
"""
instruction_memory_base = 0x600

"""
The size of BARNDLES instruction memory
"""
instruction_memory_size = 0x9FF

"""
The base address of BARNDLES read-only data memory
"""
read_only_data_memory_base = 0x400

"""
The size of BARNDLES read-only data memory 
"""
read_only_data_memory_size = 0x1FF

"""
The base address of BARNDLES read-write data memory
"""
read_write_data_memory_base = 0x200

"""
The size of BARNDLES read-write data memory 
"""
read_write_data_memory_size = 0x1FF

"""
The base address of BARNDLES stack memory
"""
stack_memory_base = 0x010

"""
The size of BARNDLES stack memory
"""
stack_memory_size = 0x1EF

"""
The base address of the BARNDLES register file
"""
register_file_memory_base = 0x000


"""
The size of the BARNDLES register file
"""
register_file_memory_size = 0x00F


def get_mnemonic(op_code):
    """
    Gets a mnemonic by its op code
    :param op_code: the op code of the mnemonic
    :return: the mnemonic
    """
    for mnemonic in mnemonics.values():
        if mnemonic.get("opcode") == op_code:
            return mnemonic.get("mnemonic")


def get_op_code(mnemonic):
    """
    Gets an op code by its mnemonic
    :param mnemonic: the mnemonic of the op code
    :return: the op code
    """
    return mnemonics.get(mnemonic).get("opcode")


def get_supported_flags(mnemonic):
    """
    Gets the supported flags by mnemonic
    :param mnemonic: the mnemonic
    :return: a list of supported flags
    """
    return mnemonics.get(mnemonic).get("flags")


def get_supported_operands(mnemonic):
    """
    Gets the number of supported operands by mnemonic
    :param mnemonic: the mnemonic
    :return: the number of supported operands in a tuple formatted like
    (# of non-immediate operands, # of immediate operands)
    """
    return mnemonics.get(mnemonic).get("operands")


def get_mnemonics():
    """
    Gets the full list of valid BARNDLES mnemonics
    :return: a full list of valid BARNDLES mnemonics
    """
    return mnemonics.keys()


def get_op_codes():
    """
    Gets the full list of valid BARNDLES op codes
    :return: a full list of valid BARNDLES op codes
    """
    op_codes = []
    for mnemonic in mnemonics.values():
        op_codes.append(mnemonic.get("opcode"))
    return op_codes


def get_flags():
    """
    Gets the full list of valid BARNDLES optional suffix flags
    :return: a full list of valid BARNDLES optional suffix flags
    """
    flags = []
    for mnemonic in mnemonics.values():
        mnemonic_flags = mnemonic.get("flags")
        for flag in mnemonic_flags:
            if flag not in flags:
                flags.append(flag)
    return flags


def get_unsigned_immediate_max():
    """
    Gets the maximum value for an unsigned 12-bit immediate
    :return: the maximum value for an unsigned 12-bit immediate
    """
    return unsigned_immediate_max


def get_unsigned_immediate_min():
    """
    Gets the minimum value for an unsigned 12-bit immediate
    :return: the minimum value for an unsigned 12-bit immediate
    """
    return unsigned_immediate_min


def get_signed_immediate_max():
    """
    Gets the maximum value for a signed 12-bit immediate
    :return: the maximum value for a signed 12-bit immediate
    """
    return signed_immediate_max


def get_signed_immediate_min():
    """
    Gets the minimum value for a signed 12-bit immediate
    :return: the minimum value for a signed 12-bit immediate
    """
    return signed_immediate_min


def get_register_index(alias):
    """
    Gets the index of a register from its alias
    :param alias: an alias of the register
    :return: the index of the register
    """
    for register in registers.values():
        if alias in register.get("aliases"):
            return register.get("index")


def get_register_aliases_by_alias(alias):
    """
    Gets the aliases of a register from one of its aliases
    :param alias: an alias of the register
    :return: a list of aliases for that register
    """
    index = get_register_index(alias)
    return registers.get(index).get("aliases")


def get_register_aliases_by_index(index):
    """
    Gets the aliases of a register from its index
    :param index: the index of the register
    :return: a list of aliases for that register
    """
    return registers.get(index).get("aliases")


def get_register_name_by_alias(alias):
    """
    Gets the formal name of a register from its alias
    :param alias: an alias of the register
    :return: the formal name of the register
    """
    index = get_register_index(alias)
    return registers.get(index).get("name")


def get_register_name_by_index(index):
    """
    Gets the formal name of a register from its index
    :param index: the index of the register
    :return: the formal name of the register
    """
    return registers.get(index).get("name")


def get_instruction_section_base():
    """
    Gets the base address of the instruction memory section
    :return: the base address of the instruction memory section
    """
    return instruction_memory_base


def get_instruction_section_size():
    """
    Gets the size of the instruction memory section in words
    :return: the size of the instruction memory section
    """
    return instruction_memory_size


def get_read_only_section_base():
    """
    Gets the base address of the read-only data memory section
    :return: the base address of the read-only data memory section
    """
    return read_only_data_memory_base


def get_read_only_section_size():
    """
    Gets the size of the read-only data memory section in words
    :return: the size of the read-only data memory section
    """
    return read_only_data_memory_size


def get_read_write_data_memory_base():
    """
    Gets the base address of the read-write data memory section
    :return: the base address of the read-write data memory section
    """
    return read_write_data_memory_base


def get_read_write_data_memory_size():
    """
    Gets the size of the read-write data memory section in words
    :return: the size of the read-write data memory section
    """
    return read_write_data_memory_size


def get_stack_memory_base():
    """
    Gets the base address of the stack memory section
    :return: the base address of the stack memory section
    """
    return stack_memory_base


def get_stack_memory_size():
    """
    Gets the size of the stack memory section in words
    :return: the size of the stack memory section
    """
    return stack_memory_size


def get_register_file_base():
    """
    Gets the base address of the register file memory section
    :return: the base address of the register file memory section
    """
    return register_file_memory_base


def get_register_file_memory_size():
    """
    Gets the size of the register file memory section in words
    :return: the size of the register file memory section
    """
    return register_file_memory_size


def get_section_identifiers():
    """
    Gets a list of section identifiers
    :return: a list of section identifiers
    """
    return section_identifiers