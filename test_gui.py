from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
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

class EnigmaSettings(Widget):
    left_roter_setting = ObjectProperty(None)
    center_roter_setting = ObjectProperty(None)
    right_roter_setting = ObjectProperty(None)
    left_roter_start = ObjectProperty(None)
    center_roter_start = ObjectProperty(None)
    right_roter_start = ObjectProperty(None)
    left_roter_position = ObjectProperty(None)
    center_roter_position = ObjectProperty(None)
    right_roter_position = ObjectProperty(None)
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

    e = Enimga(rightstart='b')
    keysound = SoundLoader.load('data/keyboard.mp3')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_roter_dispaly()

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

    def settings(self):
        self.box = EnigmaSettings()

        right, center, left = self.e.get_roter_settings()

        # Setting up valid values
        self.box.right_roter_setting.values = self.e.get_valid_roters()
        self.box.center_roter_setting.values = self.e.get_valid_roters()
        self.box.left_roter_setting.values = self.e.get_valid_roters()

        self.box.right_roter_start.values = self.e.ALPHA
        self.box.right_roter_position.values = self.e.ALPHA

        self.box.center_roter_start.values = self.e.ALPHA
        self.box.center_roter_position.values = self.e.ALPHA

        self.box.left_roter_start.values = self.e.ALPHA
        self.box.left_roter_position.values = self.e.ALPHA

        # Set Current Values
        self.box.right_roter_setting.text = right[0]
        self.box.right_roter_start.text = right[1]
        self.box.right_roter_position.text = right[2]

        self.box.center_roter_setting.text = center[0]
        self.box.center_roter_start.text = center[1]
        self.box.center_roter_position.text = center[2]

        self.box.left_roter_setting.text = left[0]
        self.box.left_roter_start.text = left[1]
        self.box.left_roter_position.text = left[2]

        but = (Button(text="close", size_hint=(None, None),
                      width=200, height=50, pos_hint={'x': 0, 'y': 0}))
        self.box.add_widget(but)
        self.main_popup = Popup(content=self.box, auto_dismiss=False)
        but.bind(on_press=self.pop_close)
        self.main_popup.open()

    def pop_close(self, btn):
        right, center, left = self.e.get_roter_settings()
        right_change = not (self.box.right_roter_setting.text, self.box.right_roter_start.text,
                            self.box.right_roter_position.text) == right
        center_change = not (self.box.center_roter_setting.text, self.box.center_roter_start.text,
                             self.box.center_roter_position.text) == center
        left_change = not (self.box.right_roter_setting.text, self.box.left_roter_start.text,
                           self.box.left_roter_position.text) == left
        if right_change or center_change or left_change:
            self.output = ""
            self.e = Enimga(left=self.box.left_roter_setting.text, leftstart=self.box.left_roter_start.text,
                            leftringsetting=self.box.left_roter_position.text,
                            center=self.box.center_roter_setting.text, centerstart=self.box.center_roter_start.text,
                            centerringsetting=self.box.center_roter_position.text,
                            right=self.box.right_roter_setting.text, rightstart=self.box.right_roter_start.text,
                            rightringsetting=self.box.right_roter_position.text)
            self.update_roter_dispaly()
        self.main_popup.dismiss()

class EnigmaApp(App):

    KEYS_COLOR = (1, 0, 0, 1)

    OUTPUT_COLORS = (0, 0, 0, 0)

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
