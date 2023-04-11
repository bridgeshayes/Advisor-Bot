import abc


class StateInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'question') and
                callable(subclass.question) and
                hasattr(subclass, 'parse_response') and
                callable(subclass.parse_response))
    