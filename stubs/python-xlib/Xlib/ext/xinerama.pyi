"""Xinerama - provide access to the Xinerama extension information.

There are at least there different - and mutually incomparable -
Xinerama extensions available. This uses the one bundled with XFree86
4.6 and/or Xorg 6.9 in the ati/radeon driver. It uses the include
files from that X distribution, so should work with it as well.  I
provide code for the lone Sun 1.0 request that isn't part of 1.1, but
this is untested because I don't have a server that implements it.

The functions loosely follow the libXineram functions. Mostly, they
return an rq.Struct in lieu of passing in pointers that get data from
the rq.Struct crammed into them. The exception is isActive, which
returns the state information - because that's what libXinerama does.
"""

from _typeshed import Unused
from typing import Final

from Xlib.display import Display
from Xlib.protocol import rq
from Xlib.xobject import drawable, resource

extname: Final = "XINERAMA"

class QueryVersion(rq.ReplyRequest): ...

def query_version(self: Display | resource.Resource) -> QueryVersion: ...

class GetState(rq.ReplyRequest): ...

def get_state(self: drawable.Window) -> GetState: ...

class GetScreenCount(rq.ReplyRequest): ...

def get_screen_count(self: drawable.Window) -> GetScreenCount: ...

class GetScreenSize(rq.ReplyRequest): ...

def get_screen_size(self: drawable.Window, screen_no: int) -> GetScreenSize:
    """Returns the size of the given screen number"""

class IsActive(rq.ReplyRequest): ...

def is_active(self: Display | resource.Resource) -> int: ...

class QueryScreens(rq.ReplyRequest): ...

def query_screens(self: Display | resource.Resource) -> QueryScreens: ...

class GetInfo(rq.ReplyRequest): ...

def get_info(self: Display | resource.Resource, visual: int) -> None: ...
def init(disp: Display, info: Unused) -> None: ...
