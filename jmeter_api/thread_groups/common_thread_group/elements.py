from xml.etree.ElementTree import Element

from jmeter_api.basics.thread_group.elements import BasicStandartThreadGroup, ThreadGroupAction
from jmeter_api.basics.utils import Renderable, IncludesElements, tree_to_str


class CommonThreadGroup(BasicStandartThreadGroup, Renderable):

    root_element_name = 'ThreadGroup'

    def __init__(self, *,
                 num_threads: int = 1,
                 ramp_time: int = 0,
                 continue_forever: bool = False,
                 loops: int = None,
                 delayed_start: bool = False,
                 is_sheduler_enable: bool = False,
                 sheduler_duration: int = None,
                 sheduler_delay: int = None,
                 on_sample_error: ThreadGroupAction = ThreadGroupAction.CONTINUE,
                 name: str = 'Thread Group',
                 comments: str = '',
                 is_enabled: bool = True,):
        self.delayed_start = delayed_start
        BasicStandartThreadGroup.__init__(self, name=name,
                                          comments=comments,
                                          is_enabled=is_enabled,
                                          num_threads=num_threads,
                                          ramp_time=ramp_time,
                                          continue_forever=continue_forever,
                                          loops=loops,
                                          is_sheduler_enable=is_sheduler_enable,
                                          sheduler_duration=sheduler_duration,
                                          sheduler_delay=sheduler_delay,
                                          on_sample_error=on_sample_error)

    @property
    def delayed_start(self) -> bool:
        return self._delayed_start

    @delayed_start.setter
    def delayed_start(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(
                f'delayed_start must be bool. continue_forever {type(value)} = {value}')
        else:
            self._delayed_start = value

    def to_xml(self) -> str:
        element_root, xml_tree = super()._add_basics()

        for element in list(element_root):
            try:
                if element.attrib['name'] == 'ThreadGroup.on_sample_error':
                    element.text = self.on_sample_error.value
                elif element.attrib['name'] == 'ThreadGroup.num_threads':
                    element.text = str(self.num_threads)
                elif element.attrib['name'] == 'ThreadGroup.ramp_time':
                    element.text = str(self.ramp_time)
                elif element.attrib['name'] == 'ThreadGroup.scheduler':
                    element.text = str(self.is_sheduler_enable).lower()
                elif element.attrib['name'] == 'ThreadGroup.duration' and self.is_sheduler_enable:
                    element.text = self.sheduler_duration
                elif element.attrib['name'] == 'ThreadGroup.delay' and self.is_sheduler_enable:
                    element.text = self.sheduler_delay
                elif element.attrib['name'] == 'ThreadGroup.main_controller':
                    for main_controller_element in list(element):
                        if main_controller_element.attrib['name'] == 'LoopController.continue_forever':
                            main_controller_element.text = str(self.continue_forever).lower()
                        elif main_controller_element.attrib['name'] == 'LoopController.loops':
                            main_controller_element.text = str(self.loops)
            except KeyError:
                continue
        if self.delayed_start:
            el = Element("boolProp", attrib={"name": "ThreadGroup.delayedStart"})
            el.text = str(self.delayed_start).lower()
            element_root.append(el)
        content_root = xml_tree.find('hashTree')
        content_root.text = self._render_inner_elements()
        return tree_to_str(xml_tree)
