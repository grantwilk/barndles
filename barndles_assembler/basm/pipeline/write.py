import struct
from basm.util import constants
from basm.util import strings
from basm.pipeline import disassemble


def write_image(output_image_filepath, instructions):
    """
    Writes assembled instructions to a image file
    :param output_image_filepath: the filepath of the image file
    :param instructions: a list of assembled instructions
    :return: None
    """
    return


def write_binary(output_binary_filepath, instructions):
    """
    Writes assembled instructions to a binary file
    :param output_binary_filepath: the filepath of the binary file
    :param instructions: a list of assembled instructions
    :return: None
    """

    # open output binary file for binary write
    output_binary_file = open(output_binary_filepath, "wb")

    # write zeros for unused sections of memory
    for i in range(constants.get_instruction_section_base()):
        output_binary_file.write(struct.pack(">I", 0x00000000))

    # write each instruction to the binary file
    for instruction in instructions:
        binary_instruction = struct.pack(">I", instruction)
        output_binary_file.write(binary_instruction)

    # write zeros for remaining instruction memory
    instruction_mem_size = constants.get_instruction_section_size()
    for i in range(instruction_mem_size - len(instructions)):
        output_binary_file.write(struct.pack(">I", 0x00000000))

    # close the binary file
    output_binary_file.close()


def write_disasm(output_disassembly_filepath, instructions):
    """
    Disassembles and writes assembled instructions to a source file
    :param output_disassembly_filepath: the filepath of the disassembly file
    :param instructions: a list of assembled instructions
    :return: None
    """

    # open output disassembly file for write
    output_disassembly_file = open(output_disassembly_filepath, "w")

    # disassemble and write each instruction to the text file
    for instruction in instructions:
        disassembled_instr = disassemble.disassemble_instruction(instruction)
        instr_string = strings.instr_to_string(disassembled_instr) + "\n"
        output_disassembly_file.write(instr_string)

    # close output disassembly file
    output_disassembly_file.close()
