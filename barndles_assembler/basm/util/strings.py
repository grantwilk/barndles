"""
File:       strings.py
Author:     Grant Wilk
Created:    April 05, 2020
Updated:    April 06, 2020
Desc:       Contains functions for converting special values to strings
"""

from basm.util import constants
from basm.pipeline import disassemble


def hex_to_string(num, width):
    """
    Formats a hexadecimal number and returns it as a string
    :param num: the hexadecimal number to convert
    :param width: the width of the hexidecimal number
    :return: the hexadecimal number formatted as a a string
    """
    return str("0x{0:0{1}X}".format(num, width))


def binary_to_string(num, width):
    """
    Formats a binary number and returns it as a string
    :param num: the binary number to convert
    :param width: the width of the binary number
    :return: the binary number formatted as a string
    """
    return str("0b{0:0{1}b}".format(num, width))


def instr_to_string(instruction):
    """
    Formats an instruction dictionary as a string
    :param instruction: the instruction dictionary
    :return: the instruction dictionary formatted as a string
    """

    # get universal fields
    mnemonic = constants.get_mnemonic(instruction["opcode"])
    imm_flag = instruction["imm_flag"]
    cpsr_flag = instruction["cpsr_flag"]
    negate_flag = instruction["negate_flag"]

    # construct operator
    instr_string = mnemonic

    if negate_flag:
        instr_string += "N"

    if cpsr_flag:
        instr_string += "S"

    # add space between operator and operands
    instr_string += " "

    # if the instruction is immediate
    if imm_flag:

        # get supported operands
        operands = constants.get_supported_operands(mnemonic)[1]

        # get operand values
        rd = instruction["rd"]
        imm = instruction["imm"]

        # construct operands
        if rd is not None and operands > 1:
            instr_string += constants.get_register_name_by_index(rd)

        if rd is not None and imm is not None and operands > 1:
            instr_string += ", "

        if imm is not None:
            instr_string += "#0x{0:X}".format(imm)

    # if the instruction is not immediate
    else:

        # get supported operands
        operands = constants.get_supported_operands(mnemonic)[0]

        # get operand values
        rd = instruction["rd"]
        rm = instruction["rm"]
        rn = instruction["rn"]

        # construct operands
        if rd is not None:
            instr_string += constants.get_register_name_by_index(rd)

        if rd is not None and rm is not None and operands > 1:
            instr_string += ", "

        if rm is not None and operands > 1:
            instr_string += constants.get_register_name_by_index(rm)

        if rm is not None and rn is not None and operands > 2:
            instr_string += ", "

        if rn is not None and operands > 2:
            instr_string += constants.get_register_name_by_index(rn)

    return instr_string


def binary_dump(assembled_instructions):

    # initialize string
    binary_dump_string = ""

    # add header
    binary_dump_string += "ADDR:\tINSTR:\t\tDIS-ASM:\n"

    # initialize address counter
    address = constants.get_instruction_section_base()

    # for each instruction in the binary
    for instruction in assembled_instructions:

        # get disassembly as string
        disasm_instr = disassemble.disassemble_instruction(instruction)
        disasm_string = instr_to_string(disasm_instr)

        # add line
        binary_dump_string += \
            "0x{0:03X}:\t0x{1:06X}   ->\t{2}\n"\
            .format(address, instruction, disasm_string)

        # increment address
        address += 1

    return binary_dump_string
