"""
The "sio" module provides support for basic interaction through command-line prompts and input.
"""

import sys

DOT_LEADER = '.'
HYP_LEADER = '-'
PROMPT_LENGTH = 55
TITLE_CENTER = 30
CHOICE_DELIMITER = ' -> '

STDOUT_STACK = []

def print_choice(choice, description, indent=None, delimiter=CHOICE_DELIMITER):
    """
    Output a choice to stdout.

    :param choice:      the character or string to be entered
    :param description: a description of the choice
    :param indent:      the number of spaces to use in the indent
    :param delimiter:   the delimiter to display between the choice and its description (defaults to CHOICE_DELIMITER)
    """
    print_indent(indent)
    print_text('%s%s%s' % (choice, delimiter, description), True)

def print_indent(indent):
    """
    Output an indent  of the specified length to stdout.

    :param indent:  the number of spaces to use in the indent
    """
    if (indent is not None) and (indent > 0):
        print_text(' ' * indent, False)

def print_labeled_text(label, text, indent=None, newline=True):
    """
    Output labeled text to stdout.
    This causes the label to be printed, if it exists, followed by dot leader, and then the desired text.

    :param label:   the label to be output at the start of the line
    :param text:    the text to output after the leader
    :param indent:  the number of spaces of indent (default is None)
    :param newline: flag indicating whether to print a new line after the text (default is True)
    """
    if text is not None:
        print_indent(indent)
        if label:
            print_text(label, False)
        if indent:
            if label:
                length = PROMPT_LENGTH - indent - len(label)
            else:
                length = PROMPT_LENGTH - indent
        elif label:
            length = PROMPT_LENGTH - len(label)
        else:
            length = PROMPT_LENGTH
        print_leader(length)
        print_text(text, newline)

def print_leader(length, type=DOT_LEADER):
    """
    Output dot leader of the specified length to stdout.

    :param length:  the length of the dot leader to output
    :param type:    the type of leader to print (defaults to DOT_LEADER)
    """
    if length > 0:
        print_text(type * length, False)

def print_newline(n=1):
    """
    Output the specified number of new lines to stdout.

    :param n:   the number of new lines to output (default is 1)
    """
    i = 0
    while i < n:
        print
        i += 1

def print_prompt(prompt, indent=None, defaultFormat=None, defaultValue=None, printLeader=False):
    """
    Output a prompt to stdout.

    :param prompt:  the prompt text to output
    :param indent:  the amount of indent before the prompt text (default is None)
    :param defaultFormat:   text describing the default format of the desired input (default is None)
    :param defaultValue:    default value returned if no input provided (default is None)
    """
    if (prompt is not None) or (defaultFormat is not None) or (defaultValue is not None):
        print_indent(indent)
        p = ""
        if prompt is not None:
            p += prompt
        if defaultValue is not None:
            p += ' [' + defaultValue + ']'
        elif defaultFormat is not None:
            p += ' [' + defaultFormat + ']'
        print_text(p, False)
        if (indent is not None) and (indent > 0):
            length = PROMPT_LENGTH - indent - len(p)
        else:
            length = PROMPT_LENGTH - len(p)
        if printLeader is not None:
            print_leader(length)
        print_text(":", False)

def print_text(text, newline=True):
    """
    Output the provided text to stdout.
    This will iterate collections to provide a more regular output.

    :param text:    the text to print
    :param newline: flag indicating whether to print a new line after the text (default is True)
    """
    if type(text) is list:
        if len(text) == 1:
            if type(text[0]) is str:
                text = text[0].strip()
            else:
                text = text[0]
        elif len(text) > 1:
            print_newline()
            for s in text:
                if type(s) is str:
                    s = s.strip()
                print s
            return
        else:
            return
    print text,
    if newline:
        print

def print_title(title):
    """
    Output a title to stdout.

    :param title:   the title text to output
    """
    title_length = len(title)
    indent = TITLE_CENTER - (title_length / 2)
    print_indent(indent)
    print_text(title)
    print_underscore(title_length, indent)

def print_underscore(length, indent=None, type=HYP_LEADER):
    """
    Output an underscore to stdout.

    :param length:  the length of the underscore following the indent, if any
    :param indent:  the amount of indent (default is None)
    :param type:    type of underscore to use (defaults to HYP_LEADER)
    """
    print_indent(indent)
    print_text(type * length)

def read_delimited_line(delimiter, prompt=None, indent=None, defaultFormat=None, defaultValue=None):
    """
    Read a line of input that may contain delimited values.
    
    :param delimiter:   the delimiter character separating the values
    :param prompt:      the prompt to display for the input (default is None)
    :param indent:      the amount of indent before the prompt text (default is None)
    :param defaultFormat:   text describing the default format of the desired input (default is None)
    :param defaultValue:    default value returned if no input provided (default is None)
    :return:            the split components from the input
    """
    s = read_line(prompt, indent, defaultFormat, defaultValue)
    if s.find(delimiter) != -1:
        parts = s.split(delimiter)
        for i in range(0, len(parts)):
            parts[i] = parts[i].strip()
        return parts
    return s

def read_line(prompt=None, indent=None, defaultFormat=None, defaultValue=None):
    """
    Read a line of input.
    
    :param prompt:  the prompt to display for the input (default is None)
    :param indent:  the amount of indent before the prompt text (default is None)
    :param defaultFormat:   text describing the default format of the desired input (default is None)
    :param defaultValue:    default value returned if no input provided (default is None)
    :return:        the input
    """
    print_prompt(prompt, indent, defaultFormat, defaultValue)
    s = raw_input()
    if len(s):
        return s
    if defaultValue is not None:
        return defaultValue
    return s

def redirect(out=None):
    """
    Push the current value of stdout onto the STDOUT_STACK and redirect it to the specified file.

    :param out: the file or name of the file to redirect stdout to
    """
    STDOUT_STACK.append(sys.stdout)
    if type(out) is str:
        out = open(out, 'w')
    if type(out) is file:
        sys.stdout = out

def restore():
    """
    Restore stdout to a previous value from the STDOUT_STACK.
    """
    if len(STDOUT_STACK) > 0:
        sys.stdout = STDOUT_STACK.pop()
