from basm.util.error import *
from basm.util import classify


def get_sections(lines, path):
    """
    Collects
    :param lines: the lines of an assembly file
    :param path: the path to the assembly file
    :return:
    """

    # initialize line number count
    line_num = 0

    # initialize section dictionary
    sections = {}

    # initialize current section identifier
    section_identifier = None

    # initialize the line number of the section header
    section_header_line_num = 0

    # initialize section lines
    section_lines = []

    # iterate until we hit a section header or the end of the file
    while line_num < len(lines):

        # get the line
        line = lines[line_num]

        # tokenize the line
        tokens = line.split()

        # break if we hit a section header
        if len(tokens) > 0 and tokens[0] == ".SECTION":
            break

        # raise an error if we hit a line that is not empty or a comment
        elif not (len(tokens) == 0 or classify.line_is_comment(line)):
            raise SectionError(
                line_num=line_num + 1,
                line_text=line,
                source_file_path=path,
                msg="Text has no section."
            )

        # increment the line number
        line_num += 1

    # collect each section
    while line_num < len(lines):

        # get the line
        line = lines[line_num]

        # tokenize the line
        tokens = line.split()

        # if we hit a section header
        if len(tokens) > 0 and tokens[0] == ".SECTION":

            # raise an error if there is an invalid number of arguments
            if len(tokens) != 2:
                raise SectionError(
                    line_num=line_num + 1,
                    line_text=line,
                    source_file_path=path,
                    msg="Invalid number of arguments in section header."
                )

            # add lines to the old section in the form
            if section_identifier is not None:
                sections[section_identifier] = {
                    "identifier": section_identifier,
                    "header_line_num": section_header_line_num,
                    "lines": section_lines
                }

            # set the new section identifier
            section_identifier = tokens[1]

            # set the new section header line number
            section_header_line_num = line_num + 1

            # raise an error if the section identifier is invalid
            if not classify.is_section_identifier(section_identifier):
                raise SectionError(
                    line_num=line_num + 1,
                    line_text=line,
                    source_file_path=path,
                    msg="Unknown section identifier \"{0}\"."
                        .format(section_identifier)
                )

            # reset the section lines
            section_lines = []

        # otherwise, append the line to the section lines list
        else:
            section_lines.append(line)

        # increment line number
        line_num += 1

    # add the last section to the sections dictionary
    sections[section_identifier] = {
        "identifier": section_identifier,
        "header_line_num": section_header_line_num,
        "lines": section_lines
    }

    return sections
