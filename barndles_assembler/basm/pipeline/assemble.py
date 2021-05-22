def assemble_imm_instruction(instruction):
    """
    Converts an immediate instruction dictionary to binary
    :param instruction: the dictionary containing the instruction
    :return: the hexadecimal assembly of the instruction
    """

    # zero out none operands
    for operand in ["rd", "imm"]:
        if instruction[operand] is None:
            instruction[operand] = 0

    # convert immediate to twos-complement if negative
    if instruction["imm"] < 1:
        instruction["imm"] %= (1 << 12)

    # assemble the rest of the instruction
    op_code = instruction["opcode"] << 19
    i_flag = instruction["imm_flag"] << 18
    s_flag = instruction["cpsr_flag"] << 17
    n_flag = instruction["negate_flag"] << 16
    imm = instruction["imm"] << 4
    rd = instruction["rd"] << 0

    return op_code | i_flag | s_flag | n_flag | imm | rd


def assemble_nonimm_instruction(instruction):
    """
    Converts a non-immediate instruction dictionary to binary
    :param instruction: the dictionary containing the instruction
    :return: the hexadecimal assembly of the instruction
    """

    # zero out none operands
    for operand in ["rd", "rm", "rn"]:
        if instruction[operand] is None:
            instruction[operand] = 0

    # assemble the instruction
    op_code = instruction["opcode"] << 19
    i_flag = instruction["imm_flag"] << 18
    s_flag = instruction["cpsr_flag"] << 17
    n_flag = instruction["negate_flag"] << 16
    rm = instruction["rm"] << 8
    rn = instruction["rn"] << 4
    rd = instruction["rd"] << 0

    return op_code | i_flag | s_flag | n_flag | rm | rn | rd
