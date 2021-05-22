# File:     parse.py
# Author:   Grant Wilk
# Created:  April 05, 2020
# Updated:  April 06, 2020
# Desc:     Contains functions for parsing and assembling BARNDLES instructions

from basm.util.error import *
from basm.util import constants, classify


def get_flags(operator):
    """
    Gets a list of all applied flags from an operator
    :param operator: the operator string
    :return: a list of flags that follow the mnemonic of an operator
    """
    flags = []
    for char in operator[3:]:
        flags.append(char)

    return flags


def get_label(line):
    """
    Extracts the label from a line of assembly and returns it
    :param line: the line of assembly to extract the label from
    :return: the extracted label
    """
    return line[:len(line) - 1]


def get_mnemonic_from_operator(operator):
    """
    Gets the mnemonic from an operator
    :param operator: the operator string
    :return: a the mnemonic of the operator
    """
    return operator[:3]


def parse_imm_operand(operand):
    """
    Parses an immediate operand
    :param operand: the operand string to parse
    :return: the numerical value extracted from the immediate operand
    """

    is_label_imm = classify.is_label_immediate(operand)
    is_numerical_imm = classify.is_numerical_immediate(operand)

    # if the immediate is a label immediate
    if is_label_imm:
        imm_value = operand

    # if the immediate is a numerical immediate
    elif is_numerical_imm:

        # parse the immediate value
        try:
            imm_value = parse_number(operand[1:])

        # otherwise, raise an error
        except ValueError:
            raise ImmediateOperandError(
                "Unidentified immediate \"{}\".".format(operand)
            )

        # raise error if immediate is too large
        if imm_value > constants.get_unsigned_immediate_max():
            raise ImmediateOperandError(
                "Immediate \"{0}\" is too large. "
                "Must be less than or equal to {1}."
                .format(imm_value, constants.get_unsigned_immediate_max())
            )

        # raise error if immediate is too small
        if imm_value < constants.get_signed_immediate_min():
            raise ImmediateOperandError(
                "Immediate \"{0}\" is too small. "
                "Must be greater than or equal to {1}."
                .format(imm_value, constants.get_signed_immediate_min())
            )

    # otherwise, raise an error
    else:
        raise ImmediateOperandError(
            "Unidentified immediate \"{}\".".format(operand)
        )

    return imm_value


def parse_reg_operand(operand):
    """
    Parses a register operand and returns the index of the register
    :param operand: the operand to parse
    :return: the index of the register
    """

    # remove the comma at the end of the operand if it has one
    if operand[len(operand) - 1] == ",":
        operand = operand[:len(operand) - 1]

    # if the register is a register operand
    if classify.is_register_operand(operand):

        # if the operand is a valid register alias
        if classify.is_register_by_alias(operand):

            # get the index of the register
            register_index = constants.get_register_index(operand)

        # otherwise, raise an error
        else:
            raise RegisterOperandError(
                "Unknown register alias \"{}\".".format(operand))

    # otherwise, raise an error
    else:
        raise RegisterOperandError("Unknown operand \"{}\".".format(operand))

    return register_index


def parse_imm_instruction(instr_tokens):
    """
    Parses the operands of an immediate instruction
    :param instr_tokens: the instruction tokens
    :return: the parsed instruction as a dictionary
    """

    # split the operator into a mnemonic and flags
    operator = instr_tokens[0]
    mnemonic = get_mnemonic_from_operator(operator)
    flags = get_flags(operator)

    # check validity of mnemonic and flags and raise error if there is an issue
    if not classify.is_mnemonic(mnemonic):
        raise MnemonicError(
            "Unknown mnemonic \"{0}\"."
            .format(mnemonic)
        )

    for flag in flags:
        if not classify.is_flag(flag):
            raise FlagError(
                "Unknown flag \"{0}\" for mnemonic \"{1}\"."
                .format(flag, mnemonic)
            )

    # start our dictionary with op code and flags
    instr_dict = {
        "opcode": constants.get_op_code(mnemonic),
        "imm_flag": 1,
        "cpsr_flag": int("S" in flags),
        "negate_flag": int("N" in flags),
    }

    # 2-operand immediate instruction
    if len(instr_tokens) == 3:
        instr_dict["imm"] = parse_imm_operand(instr_tokens[2])
        instr_dict["rd"] = parse_reg_operand(instr_tokens[1])

    # 1-operand immediate instruction
    elif len(instr_tokens) == 2:
        instr_dict["imm"] = parse_imm_operand(instr_tokens[1])
        instr_dict["rd"] = None

    # 0-operand immediate instruction
    elif len(instr_tokens) == 0:
        instr_dict["imm"] = None
        instr_dict["rd"] = None

    # raise error if there is an invalid number of arguments
    else:
        raise OperandError(
            "Invalid number of operands for mnemonic \"{}\".".format(mnemonic)
        )

    return instr_dict


def parse_nonimm_instruction(instr_tokens):
    """
    Parses the operands of a non-immediate instruction
    :param instr_tokens: the instruction tokens
    :return: the parsed instruction as a dictionary
    """

    # split the operator into a mnemonic and flags
    operator = instr_tokens[0]
    mnemonic = get_mnemonic_from_operator(operator)
    flags = get_flags(operator)

    # check validity of mnemonic and flags and raise error if there is an issue
    if not classify.is_mnemonic(mnemonic):
        raise MnemonicError(
            "Unknown mnemonic \"{0}\"."
            .format(mnemonic)
        )

    for flag in flags:
        if not classify.is_flag(flag):
            raise FlagError(
                "Unknown flag \"{0}\" for mnemonic \"{1}\"."
                .format(flag, mnemonic)
            )

    # start our dictionary with op code and flags
    instr_dict = {
        "opcode": constants.get_op_code(mnemonic),
        "imm_flag": 0,
        "cpsr_flag": int("S" in flags),
        "negate_flag": int("N" in flags),
    }

    # 3-operand non-immediate instruction
    if len(instr_tokens) == 4:
        instr_dict["rm"] = parse_reg_operand(instr_tokens[2])
        instr_dict["rn"] = parse_reg_operand(instr_tokens[3])
        instr_dict["rd"] = parse_reg_operand(instr_tokens[1])

    # 2-operand non-immediate instruction
    elif len(instr_tokens) == 3:
        instr_dict["rm"] = parse_reg_operand(instr_tokens[2])
        instr_dict["rn"] = None
        instr_dict["rd"] = parse_reg_operand(instr_tokens[1])

    # 1-operand non-immediate instruction
    elif len(instr_tokens) == 2:
        instr_dict["rm"] = None
        instr_dict["rn"] = None
        instr_dict["rd"] = parse_reg_operand(instr_tokens[1])

    # 0-operand non-immediate instruction
    elif len(instr_tokens) == 1:
        instr_dict["rm"] = None
        instr_dict["rn"] = None
        instr_dict["rd"] = None

    # raise an error if there is an invalid number of operands
    else:
        raise OperandError(
            "Invalid number of operands for \"{}\".".format(mnemonic)
        )

    return instr_dict


def parse_number(number):
    """
    Parses a number based on its apparent base
    :param number: the number to parse
    :return: the parsed number
    """

    # parse binary
    if classify.is_binary(number):
        value = int(number[2:], 2)

    # parse octal
    elif classify.is_octal(number):
        value = int(number[2:], 8)

    # parse base ten
    elif classify.is_base_ten(number):
        value = int(number, 10)

    # parse hexadecimal
    elif classify.is_hexadecimal(number):
        value = int(number[2:], 16)

    else:
        raise ValueError(None, number)

    return value
