import re
from basm.util.error import *
from basm.util import constants
from basm.pipeline import parse


def is_mnemonic(mnemonic):
    """
    Determines whether a mnemonic is a valid BARNDLES mnemonic
    :param mnemonic: the mnemonic to test
    :return: True if the mnemonic is valid, False otherwise
    """
    return mnemonic in constants.get_mnemonics()


def is_op_code(op_code):
    """
    Determines whether an op code is a valid BARNDLES op code
    :param op_code: the op code to test
    :return: True if the op code is valid, False otherwise
    """
    return op_code in constants.get_op_codes()


def is_flag(flag):
    """
    Determines whether a flag is a valid BARNDLES optional suffix flag
    :param flag: the flag to test
    :return: True if the flag is valid, False otherwise
    """
    return flag in constants.get_flags()


def is_register_by_alias(alias):
    """
    Determines whether a register exists by its alias
    :param alias: the alias to test
    :return: True if the register exists, False otherwise
    """
    return constants.get_register_index(alias) is not None


def is_register_by_index(index):
    """
    Determines whether a register exists by its index
    :param index: the index to test
    :return: True if the register exists, False otherwise
    """
    return index in constants.registers.keys()


def is_section_identifier(identifier):
    """
    Determines whether a section identifier is a valid BARNDLES
    section identifier
    :param identifier: the section identifier to test
    :return: True if the section identifier is valid, false otherwise
    """
    return identifier in constants.get_section_identifiers()


def is_immediate_instruction(instr_tokens):
    """
    Determines whether or not a set of instruction tokens signify an immediate
    instruction
    :param instr_tokens: the instruction tokens
    :return: True if the instruction tokens signify an immediate instruction,
    False otherwise
    """
    last_operand = instr_tokens[len(instr_tokens) - 1]
    numerical_imm = is_numerical_immediate(last_operand)
    label_imm = is_label_immediate(last_operand)
    mnemonic = is_mnemonic(last_operand)
    return (numerical_imm or label_imm) and not mnemonic


def is_immediate_operand(operand):
    """
    Determines whether an operand is a valid immediate operand
    :param operand: the operand to test
    :return: True if the operand is a valid immediate operand, False otherwise
    """
    is_label_imm = is_label_immediate(operand)
    is_numerical_imm = is_numerical_immediate(operand)
    is_not_register = not is_register_operand(operand)
    return is_label_imm or is_numerical_imm and is_not_register


def line_is_comment(line):
    """
    Determines whether a line of assembly is a comment
    :param line: the line to test
    :return: True if the line is a comment, False otherwise
    """
    return re.fullmatch(r'^(#|//).*', line) is not None


def line_is_empty(line):
    """
    Determines whether a string is empty
    :param line: the line to test
    :return: True if the line is empty, False otherwise
    """
    return not line


def line_is_label(line):
    """
    Determines whether a line of assembly is a label
    :param line: the line to test
    :return: True if the line is a label, False otherwise
    """
    return re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9-_]*[:]', line) is not None


def is_label_immediate(operand):
    """
    Determines whether a operand is a label immediate
    :param operand: the operand to test
    :return: True if the operand is a label immediate, False otherwise
    """
    is_register = is_register_operand(operand)
    is_label_imm = re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9-_]*', operand) is not None
    return is_label_imm and not is_register


def is_numerical_immediate(operand):
    """
    Determines whether an operand is a numerical immediate operand
    :param operand: the operand to test
    :return: True if the operand is a numerical immediate operand,
    False otherwise
    """

    # check to see if the operand starts with a #
    is_immediate = operand[0] == "#"

    # check to see if the following value fits a number profile
    binary = is_binary(operand[1:])
    octal = is_octal(operand[1:])
    base_ten = is_base_ten(operand[1:])
    hexadecimal = is_hexadecimal(operand[1:])

    return is_immediate and (binary or octal or base_ten or hexadecimal)


def is_base_ten(number):
    """
    Determines whether a number is base ten
    :param number: the number to test
    :return: true if the number is base ten, false otherwise
    """
    return re.fullmatch(r'^[#]?[-]?[0-9]+', number) is not None


def is_binary(number):
    """
    Determines whether an number is binary
    :param number: the number to test
    :return: true if the number is binary, false otherwise
    """
    return re.fullmatch(r'^[#]?(0b|0B)[0-1]+', number) is not None


def is_hexadecimal(number):
    """
    Determines whether an number is hexadecimal
    :param number: the number to test
    :return: true if the number is hexadecimal, false otherwise
    """
    return re.fullmatch(r'^[#]?(0x|0X)[0-9a-fA-F]+', number) is not None


def is_octal(number):
    """
        Determines whether an number is octal
        :param number: the number to test
        :return: true if the number is octal, false otherwise
        """
    return re.fullmatch(r'^[#]?(0c|0C)[0-8]+', number) is not None


def is_register_operand(operand):
    """
    Determines whether an operand is a register operand
    :param operand: the operand to test
    :return: True if the operand is a register operand, False otherwise
    """
    return re.fullmatch("^([R][0-9]+|SP|LR|PC|CPSR)[,]?", operand) is not None


def is_operator(operator):
    """
    Determines whether an operator is has a valid mnemonic and valid flags
    :param operator: the operator string
    :return: True if the operator is valid, False otherwise
    """

    # check if mnemonic is valid
    mnemonic = parse.get_mnemonic_from_operator(operator)
    valid_mnemonic = is_mnemonic(mnemonic)

    # check if flags are valid
    flags = parse.get_flags(operator)
    invalid_flags = []
    for flag in flags:
        invalid_flags.append(flag) if not is_flag(flag) else None

    # check for duplicate flags
    duplicate_flags = []
    for flag in flags:
        duplicate_flags.append(flag) if flags.count(flag) > 1 else None

    # raise mnemonic error if mnemonic invalid
    if not valid_mnemonic:
        raise MnemonicError(
            "Unknown mnemonic \"{0}\"."
            .format(mnemonic)
        )

    # raise flag error if flags invalid
    for flag in invalid_flags:
        raise FlagError(
            "Unknown flag \"{0}\" for mnemonic \"{1}\"."
            .format(flag, mnemonic)
        )

    # raise flag error if duplicate flags are found
    for flag in duplicate_flags:
        raise FlagError(
            "Duplicate flag \"{0}\" in operator \"{1}\"."
            .format(flag, operator)
        )

    return valid_mnemonic and not invalid_flags
