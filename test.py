from ivy.std_api import *

FCU_ON = False
def on_push(agent, *larg):
	global FCU_ON
	if FCU_ON:
		IvySendMsg("FCUAP1 off")
	else:
		IvySendMsg("FCUAP1 on")
	FCU_ON = not FCU_ON

null_callback = lambda *a: None

IvyInit(
    "HelloSimulator",
    "Ready",
    0,
    null_callback,
    null_callback
)

IvyStart("127.255.255.255:2010")
IvyBindMsg(on_push, r'^FCUAP1 (\S+)')
IvyMainLoop()
