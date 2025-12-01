from ivy.std_api import *

FCU_ON = False
def on_push(agent, *larg):
	global FCU_ON
	if FCU_ON == False:
		FCU_ON = True
		IvySendMsg("FCUAP1 on")
	else:
		FCU_ON = False
		IvySendMsg("FCUAP1 off")

null_callback = lambda *a: None

IvyInit(
    "Hello Simulator",
    "Ready",
    0,
    null_callback,
    null_callback
)

IvyStart("127.255.255.255:2010")
IvyBindMsg(on_push, r'^FCUAP1 (\S+)')
IvyMainLoop()
