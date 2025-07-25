"""Contains a metaclass and helper functions used to create
protocol message classes from Descriptor objects at runtime.

Recall that a metaclass is the "type" of a class.
(A class is to a metaclass what an instance is to a class.)

In this case, we use the GeneratedProtocolMessageType metaclass
to inject all the useful functionality into the classes
output by the protocol compiler at compile-time.

The upshot of all this is that the real implementation
details for ALL pure-Python protocol buffers are *here in
this file*.
"""

class GeneratedProtocolMessageType(type):
    """Metaclass for protocol message classes created at runtime from Descriptors.

    The protocol compiler currently uses this metaclass to create protocol
    message classes at runtime.  Clients can also manually create their own
    classes at runtime, as in this example:

    mydescriptor = Descriptor(.....)
    factory = symbol_database.Default()
    factory.pool.AddDescriptor(mydescriptor)
    MyProtoClass = message_factory.GetMessageClass(mydescriptor)
    myproto_instance = MyProtoClass()
    myproto.foo_field = 23
    ...

    The above example will not work for nested types. If you wish to include them,
    use reflection.MakeClass() instead of manually instantiating the class in
    order to create the appropriate class structure.
    """

    def __new__(cls, name, bases, dictionary): ...
