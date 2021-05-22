from basm.util.error import *
from basm.pipeline import assemble, validate, parse
from basm.util import constants, classify


def parse_instructions(lines, labels, instructions, line_num, path):
    """
    Parses instructions and labels from the lines of the instruction
    memory section
    :param lines: the lines of the instruction memory section
    :param labels: the running dictionary of labels
    :param instructions: the dictionary to place the parsed instructions in
    :param line_num: the line number of the instruction memory section
    header for error reporting
    :param path: path to the source file for error reporting
    """

    # initialize instruction num
    instruction_num = 0

    # initialize line variable
    line = ""

    try:

        # for each line in the file
        for line in lines:

            # increase the source line number
            line_num += 1

            # classify the characteristics of the line
            is_label = classify.line_is_label(line)
            is_comment = classify.line_is_comment(line)
            is_empty = classify.line_is_empty(line)

            # if the line is a label
            if is_label:

                # parse the labels value
                label = parse.get_label(line)

                # raise an error if the label has been previously defined
                if label in labels.keys():
                    raise LabelError(
                        "Label \"{}\" defined in multiple locations."
                        .format(label)
                    )

                # otherwise
                else:

                    # get the instruction section base address
                    instruction_base = constants.get_instruction_section_base()

                    # determine label address
                    label_address = instruction_base + instruction_num

                    # add the label to our label dictionary
                    labels[label] = label_address

            # if the line is an instruction
            elif not (is_comment or is_empty):

                # tokenize the line
                tokens = line.split()

                # parse and validate immediate instruction
                if classify.is_immediate_instruction(tokens):
                    instruction = parse.parse_imm_instruction(tokens)
                    validate.validate_immediate_instruction(instruction)

                # parse and validate non-immediate instruction
                else:
                    instruction = parse.parse_nonimm_instruction(tokens)
                    validate.validate_nonimmediate_instruction(instruction)

                # raise an error if instruction memory is overfilled
                if instruction_num > constants.get_instruction_section_size():
                    raise ParsingError(
                        line_num=line_num,
                        line_text=line,
                        source_file_path=path,
                        msg="Insufficient instruction memory."
                    )

                # append packet to our parsed instructions dictionary
                instructions[instruction_num] = instruction

                # increase instruction index
                instruction_num += 1

    except SectionError as e:
        raise e from e

    except basm_errors as e:
        raise ParsingError(
            line_num=line_num,
            line_text=line,
            source_file_path=path,
            msg=e.msg
        )


def link_instructions(labels, instructions):
    """
    Links label addresses to parsed instructions with label immediates
    :param labels: the dictionary of labels
    :param instructions: the dictionary of parsed instructions
    :return: a list of linked instructions
    """

    # for each instruction
    for instruction in instructions.values():

        # if the instruction is an immediate instruction
        if instruction["imm_flag"]:

            # get the instruction's immediate
            immediate = instruction["imm"]

            # if the instructions immediate is a label immediate
            if classify.is_label_immediate(str(immediate)):

                # if the immediate points to an existing label
                if immediate in labels.keys():

                    # assign the value of the immediate to the instruction
                    instruction["imm"] = labels[immediate]

                # otherwise, raise an error
                else:
                    raise LinkingError(
                        label=immediate,
                        msg="Label was never declared."
                    )


def assemble_instructions(instructions):
    """
    Assembles a list of linked instruction dictionaries
    :param instructions: the list of linked instruction dictionaries to
    assemble
    :return: a list of assembled instructions
    """

    # list of assembled instructions
    assembled_instructions = []

    # assemble each instruction
    for instruction in instructions.values():

        # immediate instructions
        if instruction["imm_flag"]:
            assembled_instr = assemble.assemble_imm_instruction(instruction)

        # non-immediate instructions
        else:
            assembled_instr = assemble.assemble_nonimm_instruction(instruction)

        # append the assembled instruction to our list
        assembled_instructions.append(assembled_instr)

    return assembled_instructions
