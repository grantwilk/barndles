def disassemble_instruction(binary_instr):
    """
    Disassembles a binary instruction
    :param binary_instr: the binary
    :return: the disassembled instruction as a dictionary
    """

    # initialize dictionary with universal fields
    instr_dict = {
        "opcode": binary_instr >> 19,
        "imm_flag": binary_instr >> 18 & 0x1,
        "cpsr_flag": binary_instr >> 17 & 0x1,
        "negate_flag": binary_instr >> 16 & 0x1,
    }

    # if immediate instruction
    if instr_dict["imm_flag"] == 1:
        instr_dict["imm"] = binary_instr >> 4 & 0xFFF
        instr_dict["rd"] = binary_instr & 0xF

    # if non-immediate instruction
    else:
        instr_dict["rm"] = binary_instr >> 8 & 0xF
        instr_dict["rn"] = binary_instr >> 4 & 0xF
        instr_dict["rd"] = binary_instr & 0xF

    return instr_dict
