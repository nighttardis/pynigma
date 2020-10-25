from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from time import sleep
from enimga import Enimga
from kivy.properties import Property
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
    pass


class SteckerbrettSettings(Widget):
    setup = True
    first = True

    def __init__(self, steckerbrett: dict, **kwargs):
        super().__init__(**kwargs)
        self.alpha_dict = steckerbrett

    def update(self, value, instance):

        # Control automated recursion and initial setup since I'm lazy and didn't populate the text values in the kv file
        if not self.first or self.setup: return

        # Set that another process has entered this function
        self.first = False

        for wid, widget in self.ids.items():
            if widget.__self__ == instance:
                break
        wid_letter = wid.split('_')[-1]

        # Fixes if the current letter was changed and need to reset the other pair
        if self.alpha_dict[wid_letter] != wid_letter:
            old_letter = self.alpha_dict[wid_letter]
            getattr(self, f"steckerbrett_{old_letter}").text = old_letter
            self.alpha_dict[old_letter] = old_letter

        # Fixes if the pair letter was set to another letter and resets its pair
        if getattr(self, f"steckerbrett_{value}").text != value:
            old_letter = getattr(self, f"steckerbrett_{value}").text
            getattr(self, f"steckerbrett_{old_letter}").text = old_letter
            self.alpha_dict[old_letter] = old_letter

        self.alpha_dict[wid_letter] = value
        self.alpha_dict[value] = wid_letter
        getattr(self, f"steckerbrett_{value}").text = wid_letter

        # Reset value for the next run of the function
        self.first = True

    def setup_values(self, alpha):
        for id, widget in self.ids.items():
            if id.endswith("label"): continue
            widget.values = alpha
            widget.text = self.alpha_dict[id.split('_')[-1]]
        self.setup = False


class EnigmaUI(Widget):

    e = Enimga()
    keysound = SoundLoader.load('data/keyboard.mp3')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__key_bind()
        self.update_roter_dispaly()

    def __key_bind(self):
        Window.bind(on_key_down=self.key_action)
        Window.bind(on_key_up=self.key_up)

    def __key_unbind(self):
        Window.unbind(on_key_down=self.key_action)
        Window.unbind(on_key_up=self.key_up)

    def key_action(self, *args):
        k = list(args)[-2].upper()
        if k.lower() not in self.e.ALPHA: return
        self.output_letter = self.e.encrypt(k.lower()).strip()
        self.input_letter = k
        self.output.text += self.output_letter.upper()
        if self.keysound:
            self.keysound.seek(0)
            self.keysound.play()
        try:
            getattr(self, f"output_{self.input_letter.lower()}").background_color = (1, 0, 0, 1)
            getattr(self, f"output_{self.output_letter.lower()}").background_color = (1, 1, 1, 1)
            getattr(self, f"output_{self.output_letter.lower()}").color = (0, 0, 0)
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
        sleep(0.5)
        try:
            getattr(self, f"output_{self.input_letter.lower()}").background_color = (0, 0, 0, 1)
            getattr(self, f"output_{self.output_letter.lower()}").background_color = (0, 0, 0, 1)
            getattr(self, f"output_{self.output_letter.lower()}").color = (1, 1, 1)
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
        self.__key_unbind()
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

        # but = (Button(text="close", size_hint=(None, None),
        #               width=200, height=50, pos_hint={'x': 0, 'y': 0}))
        # self.box.add_widget(but)
        self.main_popup = Popup(content=self.box, auto_dismiss=False)
        # but.bind(on_press=self.pop_close)
        self.main_popup.open()

    def settings_close(self):
        right, center, left = self.e.get_roter_settings()
        right_change = not (self.box.right_roter_setting.text, self.box.right_roter_start.text,
                            self.box.right_roter_position.text) == right
        center_change = not (self.box.center_roter_setting.text, self.box.center_roter_start.text,
                             self.box.center_roter_position.text) == center
        left_change = not (self.box.right_roter_setting.text, self.box.left_roter_start.text,
                           self.box.left_roter_position.text) == left
        if right_change or center_change or left_change:
            self.output.text = ""
            self.e.reset_roters(left=self.box.left_roter_setting.text, leftstart=self.box.left_roter_start.text,
                                leftringsetting=self.box.left_roter_position.text,
                                center=self.box.center_roter_setting.text, centerstart=self.box.center_roter_start.text,
                                centerringsetting=self.box.center_roter_position.text,
                                right=self.box.right_roter_setting.text, rightstart=self.box.right_roter_start.text,
                                rightringsetting=self.box.right_roter_position.text)
            self.update_roter_dispaly()
        self.__key_bind()
        self.main_popup.dismiss()

    def steckerbrett(self):
        self.__key_unbind()
        self.steckerbrett_box = SteckerbrettSettings(self.e.get_steckerbrett())
        self.steckerbrett_box.setup_values(self.e.ALPHA)
        self.main_popup = Popup(content=self.steckerbrett_box, auto_dismiss=False)
        self.main_popup.open()

    def steckerbrett_close(self):
        if self.steckerbrett_box.alpha_dict != self.e.get_steckerbrett():
            self.output.text = ""
            self.e.update_steckerbrett(steckerbrett=self.steckerbrett_box.alpha_dict, full_alpha=True)
            self.e.reset_roters()
            self.update_roter_dispaly()
        self.__key_bind()
        self.main_popup.dismiss()


class EnigmaApp(App):

    KEYS_COLOR = (1, 0, 0, 1)

    OUTPUT_COLORS = (0, 0, 0, 0)

    def build(self):
        self.enigamui = EnigmaUI()
        return self.enigamui

    def close_steckerbrett(self):
        self.enigamui.steckerbrett_close()

    def close_enigma_settings(self):
        self.enigamui.settings_close()


EnigmaApp().run()
