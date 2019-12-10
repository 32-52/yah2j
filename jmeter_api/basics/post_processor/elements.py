from jmeter_api.basics.element.elements import BasicElement
import logging


class BasicPostProcessor(BasicElement):

    def __init__(self,
                 name: str = 'BasicElement',
                 comments: str = '',
                 is_enabled: bool = True
                 ):
        super().__init__(name, comments, is_enabled)
