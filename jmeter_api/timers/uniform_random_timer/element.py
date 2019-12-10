from xml.etree import ElementTree
from jmeter_api.basics.timer.elements import BasicTimer
from jmeter_api.basics.utils import Renderable
import xmltodict
import dicttoxml


class UniformRandTimer(BasicTimer):
    """
    Uniform random timer class.
    (Capslock means arguments)

    Let you create uniform timer instance with name, constant offset delay and random delay in milliseconds.
    UniformRandTimer(name: str, rand_delay: str, offset_delay: str) creates instance with name NAME,
    OFFSET_DELAY and RAND_DELAY in milliseconds
    set_delays(offset_delay: str, rand_delay: str) sets time delays in milliseconds. Default value is 300 ms
    """

    def __init__(self,
                 name: str = 'Uniform Random Timer',
                 comments: str = '',
                 offset_delay: int = 0,
                 rand_delay: float = 100,
                 is_enabled: bool = True
                 ):
        super().__init__(name=name, comments=comments, is_enabled=is_enabled)
        self.rand_delay = rand_delay
        self.offset_delay = offset_delay

    @property
    def offset_delay(self):
        return self._offset_delay

    @offset_delay.setter
    def offset_delay(self, value):
        if not isinstance(value, int) or value < 0:
            raise TypeError(f'Failed to create uniform random timer due to wrong type '
                            f'of OFFSET_DELAY argument. {type(value).__name__} was given, Should be positive'
                            f'str.')
        self._offset_delay = str(value)

    @property
    def rand_delay(self):
        return self._rand_delay

    @rand_delay.setter
    def rand_delay(self, value):
        if not isinstance(value, float) and not isinstance(value, int) or value < 0:
            raise TypeError(f'Failed to create uniform random timer due to wrong type '
                            f'of RAND_DELAY argument. {type(value).__name__} was given, Should be positive'
                            f'float or int.')
        self._rand_delay = str(value)

    def __repr__(self):
        return f'Uniform constant timer: {self.name}, offset: {self.offset_delay}, ' \
            f'random delay: {self.rand_delay}'


class UniformRandTimerXML(UniformRandTimer, Renderable):
    def render_element(self) -> str:
        """
        Set all parameters in xml and convert it to the string.
        :return: xml in string format
        """
        xml_tree: ElementTree = super().render_element()
        root = xml_tree.getroot()
        for element in root.iter('UniformRandomTimer'):
            element.set('testname', self.name)
            element.set('enabled', self.is_enable)

        temp = [self.offset_delay, self.rand_delay, self.comments]
        for element, t in zip(root.iter('stringProp'), temp):
            element.text = t
        xml_data = ''

        for element in list(root):
            xml_data += ElementTree.tostring(element).decode('utf8')
        return xml_data

t = UniformRandTimerXML()
print(t.render_element())