from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ListProperty
from time import sleep
from enimga import Enimga
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, Property
)
from kivy.core.audio import SoundLoader

#https://stackoverflow.com/questions/57118705/kivy-define-background-color-of-label

# kv = '''
# <ColoredLabel>:
#     canvas.before:
#         Color:
#             rgba: self.background_color
#         Rectangle:
#             pos: self.pos
#             size: self.size
#     '''
#
# Builder.load_string(kv)


class ColoredLabel(Label):
    background_color = ListProperty((0, 0, 0, 1))
    width = Property(50.0)
    height = Property(50.0)
    size = (50, 50)


class ColoredBox(Label):
    background_color = ListProperty((0, 0, 0, 1))
    pass


class EnigmaUI(Widget):
    output = ObjectProperty(None)
    output_a = ObjectProperty(None)
    output_b = ObjectProperty(None)
    output_c = ObjectProperty(None)
    output_d = ObjectProperty(None)
    output_e = ObjectProperty(None)
    output_f = ObjectProperty(None)
    output_g = ObjectProperty(None)
    output_h = ObjectProperty(None)
    output_i = ObjectProperty(None)
    output_j = ObjectProperty(None)
    output_k = ObjectProperty(None)
    output_l = ObjectProperty(None)
    output_m = ObjectProperty(None)
    output_n = ObjectProperty(None)
    output_o = ObjectProperty(None)
    output_p = ObjectProperty(None)
    output_q = ObjectProperty(None)
    output_r = ObjectProperty(None)
    output_s = ObjectProperty(None)
    output_t = ObjectProperty(None)
    output_u = ObjectProperty(None)
    output_v = ObjectProperty(None)
    output_w = ObjectProperty(None)
    output_x = ObjectProperty(None)
    output_y = ObjectProperty(None)
    output_z = ObjectProperty(None)
    left_roter = ObjectProperty(None)
    center_roter = ObjectProperty(None)
    right_roter = ObjectProperty(None)
    e = Enimga()
    keysound = SoundLoader.load('data/keyboard.mp3')

    def key_action(self, *args):
        # print(f"got a key event: {list(args)}")
        k = list(args)[-2].upper()
        if k.lower() not in self.e.ALPHA: return
        self.output_letter = self.e.encrypt(k.lower()).strip()
        self.output.text += self.output_letter.upper()
        if self.keysound:
            self.keysound.seek(0)
            self.keysound.play()
        try:
            getattr(self, f"output_{self.output_letter.lower()}").background_color = (1, 1, 1, 1)
            getattr(self, f"output_{self.output_letter.lower()}").color = (0, 0, 0)
            # print(getattr(self, f"output_{k.lower()}").size)
        except AttributeError:
            pass
        self.update_roter_dispaly()

    def update_roter_dispaly(self):
        data = self.e.get_roter_status()
        if data[0].upper() != self.right_roter.text:
            self.right_roter.text = data[0].upper()
        if data[1].upper() != self.center_roter.text:
            self.center_roter.text = data[1].upper()
        if data[0].upper() != self.left_roter.text:
            self.left_roter.text = data[2].upper()

    def key_up(self, *args):
        # prin/(f"got a key event: {self.keycode_to_string(value=list(args)[1])}")
        sleep(0.5)
        # k = self.keycode_to_string(value=list(args)[1]).upper()
        try:
            getattr(self, f"output_{self.output_letter.lower()}").background_color = (0, 0, 0, 1)
            getattr(self, f"output_{self.output_letter.lower()}").color = (1, 1, 1)
            # print(getattr(self, f"output_{k.lower()}").size)
        except AttributeError:
            pass

    def keycode_to_string(self, value):
        '''Convert a keycode number to a string according to the
        :attr:`Keyboard.keycodes`. If the value is not found in the
        keycodes, it will return ''.
        '''
        keycodes = list(Keyboard.keycodes.values())
        if value in keycodes:
            return list(Keyboard.keycodes.keys())[keycodes.index(value)]
        return ''

class EnigmaApp(App):

    KEYS_COLOR = (1, 0, 0, 1)

    # KEYS = {
    #     "A": ColoredLabel(text="A", background_color=KEYS_COLOR),
    #     "B": ColoredLabel(text="B", background_color=KEYS_COLOR),
    #     "C": ColoredLabel(text="C", background_color=KEYS_COLOR),
    #     "D": ColoredLabel(text="D", background_color=KEYS_COLOR),
    #     "E": ColoredLabel(text="E", background_color=KEYS_COLOR),
    #     "F": ColoredLabel(text="F", background_color=KEYS_COLOR),
    #     "G": ColoredLabel(text="G", background_color=KEYS_COLOR),
    #     "H": ColoredLabel(text="H", background_color=KEYS_COLOR),
    #     "I": ColoredLabel(text="I", background_color=KEYS_COLOR),
    #     "J": ColoredLabel(text="J", background_color=KEYS_COLOR),
    #     "K": ColoredLabel(text="K", background_color=KEYS_COLOR),
    #     "L": ColoredLabel(text="L", background_color=KEYS_COLOR),
    #     "M": ColoredLabel(text="M", background_color=KEYS_COLOR),
    #     "N": ColoredLabel(text="N", background_color=KEYS_COLOR),
    #     "O": ColoredLabel(text="O", background_color=KEYS_COLOR),
    #     "P": ColoredLabel(text="P", background_color=KEYS_COLOR),
    #     "Q": ColoredLabel(text="Q", background_color=KEYS_COLOR),
    #     "R": ColoredLabel(text="R", background_color=KEYS_COLOR),
    #     "S": ColoredLabel(text="S", background_color=KEYS_COLOR),
    #     "T": ColoredLabel(text="T", background_color=KEYS_COLOR),
    #     "U": ColoredLabel(text="U", background_color=KEYS_COLOR),
    #     "V": ColoredLabel(text="V", background_color=KEYS_COLOR),
    #     "W": ColoredLabel(text="W", background_color=KEYS_COLOR),
    #     "X": ColoredLabel(text="X", background_color=KEYS_COLOR),
    #     "Y": ColoredLabel(text="Y", background_color=KEYS_COLOR),
    #     "Z": ColoredLabel(text="Z", background_color=KEYS_COLOR)
    # }

    OUTPUT_COLORS = (0, 0, 0, 0)

    # OUTPUT = {
    #     "A": ColoredLabel(text="A", background_color=OUTPUT_COLORS),
    #     "B": ColoredLabel(text="B", background_color=OUTPUT_COLORS),
    #     "C": ColoredLabel(text="C", background_color=OUTPUT_COLORS),
    #     "D": ColoredLabel(text="D", background_color=OUTPUT_COLORS),
    #     "E": ColoredLabel(text="E", background_color=OUTPUT_COLORS),
    #     "F": ColoredLabel(text="F", background_color=OUTPUT_COLORS),
    #     "G": ColoredLabel(text="G", background_color=OUTPUT_COLORS),
    #     "H": ColoredLabel(text="H", background_color=OUTPUT_COLORS),
    #     "I": ColoredLabel(text="I", background_color=OUTPUT_COLORS),
    #     "J": ColoredLabel(text="J", background_color=OUTPUT_COLORS),
    #     "K": ColoredLabel(text="K", background_color=OUTPUT_COLORS),
    #     "L": ColoredLabel(text="L", background_color=OUTPUT_COLORS),
    #     "M": ColoredLabel(text="M", background_color=OUTPUT_COLORS),
    #     "N": ColoredLabel(text="N", background_color=OUTPUT_COLORS),
    #     "O": ColoredLabel(text="O", background_color=OUTPUT_COLORS),
    #     "P": ColoredLabel(text="P", background_color=OUTPUT_COLORS),
    #     "Q": ColoredLabel(text="Q", background_color=OUTPUT_COLORS),
    #     "R": ColoredLabel(text="R", background_color=OUTPUT_COLORS),
    #     "S": ColoredLabel(text="S", background_color=OUTPUT_COLORS),
    #     "T": ColoredLabel(text="T", background_color=OUTPUT_COLORS),
    #     "U": ColoredLabel(text="U", background_color=OUTPUT_COLORS),
    #     "V": ColoredLabel(text="V", background_color=OUTPUT_COLORS),
    #     "W": ColoredLabel(text="W", background_color=OUTPUT_COLORS),
    #     "X": ColoredLabel(text="X", background_color=OUTPUT_COLORS),
    #     "Y": ColoredLabel(text="Y", background_color=OUTPUT_COLORS),
    #     "Z": ColoredLabel(text="Z", background_color=OUTPUT_COLORS)
    # }

    e = Enimga()

    def build(self):
        lkasjdf = EnigmaUI()
        Window.bind(on_key_down=lkasjdf.key_action)
        Window.bind(on_key_up=lkasjdf.key_up)
        return lkasjdf
        # Window.bind(on_key_down=self.key_action)
        # Window.bind(on_key_up=self.key_up)
        # root = BoxLayout(orientation='vertical')
        #
        # self.output = TextInput(readonly=True)
        #
        # root.add_widget(self.output)
        #
        # row_1o = BoxLayout(orientation='horizontal')
        # for letter in ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]:
        #     row_1o.add_widget(self.OUTPUT[letter])
        #
        # root.add_widget(row_1o)
        #
        # row_2o = BoxLayout(orientation="horizontal")
        # for letter in ["A", "S", "D", "F", "G", "H", "J", "K", "L"]:
        #     row_2o.add_widget(self.OUTPUT[letter])
        #
        # root.add_widget(row_2o)
        #
        # row_3o = BoxLayout(orientation="horizontal")
        # for letter in ["Z", "X", "C", "V", "B", "N", 'M']:
        #     row_3o.add_widget(self.OUTPUT[letter])
        #
        # root.add_widget(row_3o)
        #
        # row_1 = BoxLayout(orientation='horizontal')
        # for letter in ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]:
        #     row_1.add_widget(self.KEYS[letter])
        #
        # root.add_widget(row_1)
        #
        # row_2 = BoxLayout(orientation="horizontal")
        # for letter in ["A", "S", "D", "F", "G", "H", "J", "K", "L"]:
        #     row_2.add_widget(self.KEYS[letter])
        #
        # root.add_widget(row_2)
        #
        # row_3 = BoxLayout(orientation="horizontal")
        # for letter in ["Z", "X", "C", "V", "B", "N", 'M']:
        #     row_3.add_widget(self.KEYS[letter])
        #
        # root.add_widget(row_3)

        # return root

    def key_action(self, *args):
        # print(f"got a key event: {list(args)}")
        k = list(args)[-2].upper()
        if k in self.KEYS:
            self.KEYS[k].background_color = (1, 0, 1, 0.25)
            # print(len(self.output.text.replace(" ", "")) % 5)
            self.ko = self.e.encrypt(k).strip()
            self.OUTPUT[self.ko.upper()].background_color = (1, 1, 1, 1)
            self.OUTPUT[self.ko.upper()].color = (0, 0, 0)
            if len(self.output.text.replace(" ", "")) % 5 == 0:
                self.output.text += f" {self.ko}"
            else:
                self.output.text += f"{self.ko}"

    def key_up(self, *args):
        # prin/(f"got a key event: {self.keycode_to_string(value=list(args)[1])}")
        sleep(0.5)
        k = self.keycode_to_string(value=list(args)[1]).upper()
        if k in self.KEYS:
            self.KEYS[k].background_color = self.KEYS_COLOR
            self.OUTPUT[self.ko.upper()].background_color = self.OUTPUT_COLORS
            self.OUTPUT[self.ko.upper()].color = (1, 1, 1)

    def keycode_to_string(self, value):
        '''Convert a keycode number to a string according to the
        :attr:`Keyboard.keycodes`. If the value is not found in the
        keycodes, it will return ''.
        '''
        keycodes = list(Keyboard.keycodes.values())
        if value in keycodes:
            return list(Keyboard.keycodes.keys())[keycodes.index(value)]
        return ''

EnigmaApp().run()
