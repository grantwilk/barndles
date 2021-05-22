from basm.util.error import *
from basm.util import constants


def validate_immediate_instruction(instruction):
    """
    Validates the structure of an immediate instruction
    :param instruction: the instruction to validate
    :return: None
    """

    mnemonic = constants.get_mnemonic(instruction["opcode"])

    # get the number of immediate operands for our mnemonic
    actual_operands = constants.get_supported_operands(mnemonic)[1]

    # initialize operand count
    operand_count = 0

    # count each not none operand
    if instruction["rd"] is not None:
        operand_count += 1

    if instruction["imm"] is not None:
        operand_count += 1

    # raise operand error if there is an invalid number of operands
    if operand_count != actual_operands:
        raise OperandError(
            "Invalid number of operands for mnemonic \"{}\"."
            .format(mnemonic)
        )

    # validate flags
    validate_flags(instruction)


def validate_nonimmediate_instruction(instruction):
    """
    Validates the structure of a non-immediate instruction
    :param instruction: the instruction to validate
    :return: None
    """

    mnemonic = constants.get_mnemonic(instruction["opcode"])

    # get the number of immediate operands for our mnemonic
    actual_operands = constants.get_supported_operands(mnemonic)[0]

    # initialize operand count
    operand_count = 0

    # count each not none operand
    if instruction["rd"] is not None:
        operand_count += 1

    if instruction["rm"] is not None:
        operand_count += 1

    if instruction["rn"] is not None:
        operand_count += 1

    # raise operand error if there is an invalid number of operands
    if operand_count != actual_operands:
        raise OperandError(
            "Invalid number of operands for mnemonic \"{}\"."
            .format(mnemonic)
        )

    # validate flags
    validate_flags(instruction)


def validate_flags(instruction):
    """
    Validates the flags of an instruction
    :param instruction: the instruction to validate
    :return: None
    """

    # get mnemonic
    mnemonic = constants.get_mnemonic(instruction["opcode"])

    # get all active flags in the instruction
    flags = []
    flags.append("S") if instruction["cpsr_flag"] == 1 else None
    flags.append("N") if instruction["negate_flag"] == 1 else None

    # get list of supported flags
    supported_flags = constants.get_supported_flags(mnemonic)

    # if any flag is not supported, raise error
    for flag in flags:
        if flag not in supported_flags:
            raise FlagError(
                "Flag \"{0}\" is not supported for mnemonic \"{1}\"."
                .format(flag, mnemonic)
            )
