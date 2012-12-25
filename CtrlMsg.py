defs = open("ctrl_msg.h")
constants = dict()
for line in defs:
	name = line.split()[1]
	value = int(line.split()[2])
	constants[name] = value

CtrlMsg = type(
           'CtrlMsg',
           (object,),
		constants
           )
