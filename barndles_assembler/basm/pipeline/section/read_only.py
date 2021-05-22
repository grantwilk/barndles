from basm.util.error import *
from basm.pipeline import parse
from basm.util import constants, classify


def parse_allocations(lines, labels, allocations, line_num, path):
    """
    Parses allocations and labels from the lines of read-only memory section
    :param lines: the lines of the read-only memory section
    :param labels: the running dictionary of labels
    :param allocations: the dictionary to place parsed allocations in
    :param line_num: the line number of the read-only memory section for
    error reporting
    :param path: path to the source file for error reporting
    """

    # initialize the allocation num
    allocated_words = 0

    # initialize the line variable
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

                # parse the label's value
                label = parse.get_label(line)

                # raise an error if the label has been previously defined
                if label in labels.keys():
                    raise LabelError(
                        "Label \"{}\" defined in multiple locations."
                        .format(label)
                    )

                # otherwise
                else:

                    # get the read only section base address
                    read_only_base = constants.get_read_only_section_base()

                    # determine label address
                    label_address = read_only_base + allocated_words

                    # add the label to our label dictionary
                    labels[label] = label_address

            # if the line is an allocation
            elif not (is_comment or is_empty):

                # tokenize the line
                tokens = line.split()

                # integer allocation
                if tokens[0] == ".INT":

                    # ensure there is an appropriate amount of tokens
                    if len(tokens) != 2:
                        raise AllocationError(
                            msg="Invalid number of arguments for integer "
                                "allocation."
                        )

                    # add the allocation to the allocations list
                    try:

                        # parse the value for the allocation
                        value = parse.parse_number(tokens[1])

                        # raise error if the allocation value is too large
                        if value > constants.get_unsigned_immediate_max():
                            raise AllocationError(
                                "Integer value \"{0}\" is too large. "
                                "Must be less than or equal to {1}."
                                .format(
                                    value,
                                    constants.get_unsigned_immediate_max()
                                )
                            )

                        # raise error if allocation value is too small
                        if value < constants.get_signed_immediate_min():
                            raise AllocationError(
                                "Immediate \"{0}\" is too small. "
                                "Must be greater than or equal to {1}."
                                .format(
                                    value,
                                    constants.get_signed_immediate_min()
                                )
                            )

                        # add the allocation to the dictionary
                        allocations[allocated_words] = {
                            "size": 1,
                            "value": value
                        }

                        # increment the number of allocated words
                        allocated_words += 1

                    # raise an error if there are any invalid types
                    except ValueError:
                        raise AllocationError(
                            msg="Invalid integer value \"{0}\"."
                                .format(tokens[1])
                        )

                # array allocation
                elif tokens[0] == ".ARR":

                    try:

                        # if there is only a size argument
                        if len(tokens) == 2:

                            # get the size of the array
                            size = int(tokens[1])

                            # raise an error if there is an invalid array size
                            if size < 1:
                                raise AllocationError(
                                    "Invalid array size \"{0}\".".format(size)
                                )

                            # add the allocation to the dictionary
                            allocations[allocated_words] = {
                                "size": size,
                                "value": 0
                            }

                            # increment the number of allocated words
                            allocated_words += size

                        # if there is a size and a value argument
                        elif len(tokens) == 3:

                            # get the size of the array
                            size = int(tokens[1])

                            # raise an error if there is an invalid array size
                            if size < 1:
                                raise AllocationError(
                                    "Invalid array size \"{0}\".".format(size)
                                )

                            # parse the value for the allocation
                            value = parse.parse_number(tokens[2])

                            # raise error if the allocation value is too large
                            if value > constants.get_unsigned_immediate_max():
                                raise AllocationError(
                                    "Integer value \"{0}\" is too large. "
                                    "Must be less than or equal to {1}."
                                    .format(
                                        value,
                                        constants.get_unsigned_immediate_max()
                                    )
                                )

                            # raise error if the allocation value is too small
                            if value < constants.get_signed_immediate_min():
                                raise AllocationError(
                                    "Immediate \"{0}\" is too small. "
                                    "Must be greater than or equal to {1}."
                                    .format(
                                        value,
                                        constants.get_signed_immediate_min()
                                    )
                                )

                            # add the allocation to the dictionary
                            allocations[allocated_words] = {
                                "size": size,
                                "value": value
                            }

                            # increment the number of allocated words
                            allocated_words += size

                        # raise an error if there is an invalid number of args
                        else:
                            raise AllocationError(
                                msg="Invalid number of arguments for array "
                                    "allocation."
                            )

                    # raise an error if there are any invalid types
                    except ValueError as e:
                        msg = e.args[0]
                        error_value = msg[(msg.find('\'') + 1):(len(msg) - 1)]
                        print(e.args)
                        raise AllocationError(
                            msg="Invalid integer value \"{0}\"."
                                .format(error_value)
                        )

                # string allocation
                elif tokens[0] == ".STR" and tokens[1]:
                    # TODO
                    pass

                # raise an exception if the first token is unrecognized
                else:
                    raise AllocationError(
                        msg="Invalid allocation type \"{0}\"."
                            .format(tokens[0])
                    )

                # raise an exception if the number of allocated words exceeds
                # the size of the read only section
                if allocated_words > constants.get_read_only_section_size():
                    raise AllocationError(
                        msg="Insufficient read-only data memory."
                    )

    except ASMError as e:
        raise ParsingError(
            line_num=line_num,
            line_text=line,
            source_file_path=path,
            msg=e.msg
        )
