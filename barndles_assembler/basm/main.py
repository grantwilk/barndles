import os
import time
import argparse
import subprocess

from basm.pipeline.section import instruction
from basm.pipeline.section import read_only
from basm.util.error import *
from basm.pipeline import sections
from basm.pipeline import write
from basm.util import strings
from basm.util import constants


# class for holding text effects
class TxtFX:
    """
    Container class for holding pretty text effects
    """
    black = "\033[1;30;48m"
    white = "\033[1;37;48m"
    red = "\033[1;31;48m"
    yellow = "\033[1;33;48m"
    green = "\033[1;32;48m"
    cyan = "\033[1;36;48m"
    blue = "\033[1;34;48m"
    purple = "\033[1;35;48m"


# workaround for missing colored text
subprocess.call('', shell=True)

# initialize commandline parser and add arguments
parser = argparse.ArgumentParser(
    prog="main.py",
    description="An assembler for the BARNDLES ASM language.",
    epilog="Made by Grant Wilk (April 10 2020).",
    usage="main.py SOURCE_FILEPATH [-img IMAGE_FILEPATH] [-bin BINARY_FILEPATH]"
          " [-dsm DISASM_FILEPATH]"
)

parser.add_argument(
    "SOURCE_FILEPATH",
    help="filepath to the source file"
)

parser.add_argument(
    "-img",
    dest="image_filepath",
    help="(optional) filepath to the output image file"
)

parser.add_argument(
    "-bin",
    dest="binary_filepath",
    help="filepath to the output binary file"
)

parser.add_argument(
    "-dsm",
    metavar="DISASM_FILEPATH",
    dest="disassembly_filepath",
    help="filepath to the output disassembly file"
)

parser.add_argument(
    "-dump",
    dest="print_dump",
    action="store_true",
    help="dump instructions to console after assembly"
)

# parse arguments
args = parser.parse_args()

# assign arguments
source_filepath = args.SOURCE_FILEPATH
output_image_filepath = args.image_filepath
output_binary_filepath = args.binary_filepath
output_disassembly_filepath = args.disassembly_filepath
print_dump = args.print_dump

# confirm that source filepath is an actual file
if not os.path.isfile(source_filepath):
    print(TxtFX.red + "Error: No such file: {}".format(source_filepath))
    print(TxtFX.white + "Assembler terminated.")
    quit()

print(
"""
{0}-=============================================================-{1}

 ____     ____   ____    ____    ___     _         ___    _____
|    \   /    | |    \  |    \  |   \   | |       /  _]  / ___/
|  o  ) |  o  | |  D  ) |  _  | |    \  | |      /  [_  (   \_
|     | |     | |    /  |  |  | |  D  | | |___  |    _]  \__  |
|  O  | |  _  | |    \  |  |  | |     | |     | |   [_   /  \ |
|     | |  |  | |  .  \ |  |  | |     | |     | |     |  \    |
|_____| |__|__| |__|\_| |__|__| |_____| |_____| |_____|   \___|

                     - A S S E M B L E R -

                MADE (WITH LOVE) BY GRANT WILK
                 VERSION 1.0 | APRIL 10, 2020

{0}-=============================================================-{1}
""".format(TxtFX.cyan, TxtFX.white)
)

# print command line args
print("Source File: {}".format(source_filepath))

if output_image_filepath:
    print("Output Image: {}".format(output_image_filepath))

if output_binary_filepath:
    print("Output Binary: {}".format(output_binary_filepath))

if output_disassembly_filepath:
    print("Output Disassembly: {}".format(output_disassembly_filepath))

# print start message
print("{0}\nSTARTING ASSEMBLY PROCESS\n{1}".format(TxtFX.yellow, TxtFX.white))

# start assembly timer
start_time = time.time()

# initialize our list of labels
labels = {}

try:

    # load and prepare the source file
    print("Preparing source...")
    with open(source_filepath) as f:
        lines = f.readlines()
        lines = [line.strip().upper() for line in lines]
        f.close()
    print(
        "{0}Source prepared.{1}\n"
        .format(TxtFX.yellow, TxtFX.white)
    )

    # get the sections from the source lines
    print("Sectioning source...")
    sections = sections.get_sections(lines, source_filepath)
    identifiers = sections.keys()
    print(
        "{0}Source sectioned.{1}\n"
        .format(TxtFX.yellow, TxtFX.white)
    )

    # if there is a read-only memory section
    if constants.read_only_section_identifier in identifiers:

        print("Assembling read-only memory...")

        allocations = {}
        read_only_section = sections[constants.read_only_section_identifier]

        read_only.parse_allocations(
            lines=read_only_section["lines"],
            labels=labels,
            allocations=allocations,
            line_num=read_only_section["header_line_num"],
            path=source_filepath
        )

        print(
            "{0}Assembled read-only memory.{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

    # if there is a read-write memory section
    if constants.read_only_section_identifier in identifiers:
        print("Assembling read-write memory...")
        print(
            "{0}Assembled read-write memory.{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

    # if there is a instruction memory section
    if constants.instruction_section_identifier in identifiers:

        print("Assembling instruction memory...")

        instructions = {}
        instruction_section = sections[constants.instruction_section_identifier]

        # parse the instructions from the lines
        instruction.parse_instructions(
            lines=instruction_section["lines"],
            labels=labels,
            instructions=instructions,
            line_num=instruction_section["header_line_num"],
            path=source_filepath
        )

        # link the instructions
        instruction.link_instructions(
            labels,
            instructions
        )

        # assemble the instructions
        assembled_instructions = instruction.assemble_instructions(
            instructions
        )

        print(
            "{0}Assembled instruction memory.{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

        # print binary dump
        if print_dump:
            print("Dumping Assembled Instructions:")
            print(
                TxtFX.yellow +
                strings.binary_dump(assembled_instructions) +
                TxtFX.white
            )

    # write image
    if output_image_filepath:
        print("Writing to image...")
        print(
            "{0}Image write complete!{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

    # write binary
    if output_binary_filepath:
        print("Writing to binary...")
        write.write_binary(output_binary_filepath, assembled_instructions)
        print(
            "{0}Binary write complete!{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

    # write disassembly
    if output_disassembly_filepath:
        print("Writing to disassembly...")
        write.write_disasm(output_disassembly_filepath, assembled_instructions)
        print(
            "{0}Disassembly write complete!{1}\n"
            .format(TxtFX.yellow, TxtFX.white)
        )

    # print time elapsed in milliseconds
    time_elapsed = (time.time() - start_time) * 1000
    print(TxtFX.green + "ASSEMBLY PROCESS COMPLETE!" + TxtFX.white)
    print("[Finished in {:.2f}ms]".format(time_elapsed))

except (SectionError, ParsingError) as e:
    print(
        "{0}\nASSEMBLY PROCESS FAILED!\n{1}"
        .format(TxtFX.yellow, TxtFX.white) +
        "{0}\nError on line {1} of {2}:  {3}\n"
        .format(TxtFX.red, e.line_num, e.source_filepath, e.line_text) +
        "{0}{1}".format(e.msg, TxtFX.white)
    )

except LinkingError as e:
    print(
        "{0}\nASSEMBLY PROCESS FAILED!\n{1}"
        .format(TxtFX.yellow, TxtFX.white) +
        "{0}\nError while linking label: {1}\n"
        .format(TxtFX.red, e.label) +
        "{0}{1}".format(e.msg, TxtFX.white)
    )
