import mathutils
import sio

sio.TITLE_CENTER = 15
sio.PROMPT_LENGTH = 25

sio.print_title('Simple IO Examples')
sio.print_newline()

sio.print_title('make_float_readable Examples')
sio.print_text(mathutils.make_float_readable(1))
sio.print_text(mathutils.make_float_readable(12))
sio.print_text(mathutils.make_float_readable('123.4'))
sio.print_text(mathutils.make_float_readable(1234.5))
sio.print_text(mathutils.make_float_readable(12345))
sio.print_text(mathutils.make_float_readable(123456))
sio.print_text(mathutils.make_float_readable(1234567))
sio.print_newline(3)

sio.print_title('make_int_readable Examples')
sio.print_text(mathutils.make_int_readable(1))
sio.print_text(mathutils.make_int_readable(12))
sio.print_text(mathutils.make_int_readable('123'))
sio.print_text(mathutils.make_int_readable(1234.0))
sio.print_text(mathutils.make_int_readable(12345))
sio.print_text(mathutils.make_int_readable(123456))
sio.print_text(mathutils.make_int_readable(1234567))
sio.print_newline(3)

sio.print_title('print_choice Example')
sio.print_choice('1', 'Perform action #1')
sio.print_choice('2', 'Perform action #2')
sio.print_choice('3', 'Perform action #3')
sio.print_choice('4', 'Perform action #4')
sio.print_choice('5', 'Perform action #5')
sio.print_choice('6', 'Perform action #6')
s = sio.read_line('Select action to perform')
a = mathutils.to_int(s, 0)
sio.print_text('Selected action %i' % a)
sio.print_newline(3)

sio.print_title('print_labeled_text Example')
sio.print_labeled_text('Perform action #1', '1')
sio.print_labeled_text('Perform action #2', '2')
sio.print_labeled_text('Perform action #3', '3')
sio.print_labeled_text('Perform action #4', '4')
sio.print_labeled_text('Perform action #5', '5')
sio.print_labeled_text('Perform action #6', '6')
s = sio.read_line('Select action to perform')
a = mathutils.to_int(s, 0)
sio.print_text('Selected action %s' % a)
sio.print_newline(3)

sio.print_title('print_prompt Example')
sio.print_prompt('Do you want to continue? (Yes|No)')
sio.print_newline()
sio.print_prompt('Do you want to continue? (Yes|No)', defaultValue='Yes')
sio.print_newline()
#def print_prompt(prompt, indent=None, defaultFormat=None, defaultValue=None, printLeader=False):

sio.print_newline(3)
sio.print_text('DONE')