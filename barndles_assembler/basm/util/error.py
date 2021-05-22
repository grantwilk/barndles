class ASMError(Exception):
    """
    Raised when an error is caused by the BARNDLES assembler
    """
    def __init__(self, msg):
        self.msg = msg


class SectionError(ASMError):
    """
    Raised when an error is caused by sectioning
    """
    def __init__(self, line_num, line_text, source_file_path, msg):
        self.line_num = line_num
        self.line_text = line_text
        self.source_filepath = source_file_path
        self.msg = msg


class ParsingError(ASMError):
    """
    Raised when an error occurs during the parsing process
    """
    def __init__(self, line_num, line_text, source_file_path, msg):
        self.line_num = line_num
        self.line_text = line_text
        self.source_filepath = source_file_path
        self.msg = msg


class LinkingError(ASMError):
    """
    Raised when an error occurs during the parsing process
    """
    def __init__(self, label, msg):
        self.label = label
        self.msg = msg


class AllocationError(ASMError):
    """
    Raised when an error is caused by an allocation
    """


class LabelError(ASMError):
    """
    Raised when an error is caused by a label
    """


class OperatorError(ASMError):
    """
    Raised when an error is caused by an operator
    """
    pass


class MnemonicError(ASMError):
    """
    Raised when an error is caused by a mnemonic
    """
    pass


class FlagError(ASMError):
    """
    Raised when an error is caused by a flag
    """
    pass


class OperandError(ASMError):
    """
    Raised when an error is caused by an operand
    """
    pass


class ImmediateOperandError(OperandError):
    """
    Raised when an error is caused by an immediate operand
    """
    pass


class RegisterOperandError(OperandError):
    """
    Raised when an error is caused by a register operand
    """
    pass


"""
List of errors that can be raised by the assembler
"""
basm_errors = (
    ASMError,
    ParsingError,
    OperatorError,
    MnemonicError,
    FlagError,
    OperandError,
    ImmediateOperandError,
    RegisterOperandError
)
