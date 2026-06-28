from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
import threading
import os
from enhancer import RealESRGANEnhancer

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class EnhancerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.enhancer = RealESRGANEnhancer()
        self.selected_file = None

        self.add_widget(Label(
            text='Real-ESRGAN Video Enhancer',
            font_size='22sp', bold=True, size_hint_y=0.1
        ))

        self.file_chooser = FileChooserListView(
            filters=['*.mp4', '*.mkv', '*.avi'],
            size_hint_y=0.5
        )
        self.file_chooser.bind(selection=self.on_file_select)
        self.add_widget(self.file_chooser)

        self.status = Label(
            text='একটি ভিডিও সিলেক্ট করুন',
            size_hint_y=0.1, font_size='16sp'
        )
        self.add_widget(self.status)

        self.progress = ProgressBar(max=100, value=0, size_hint_y=0.05)
        self.add_widget(self.progress)

        self.btn = Button(
            text='Enhance করুন',
            size_hint_y=0.15,
            background_color=(0.2, 0.6, 1, 1),
            font_size='18sp'
        )
        self.btn.bind(on_press=self.start_enhance)
        self.add_widget(self.btn)

    def on_file_select(self, chooser, selection):
        if selection:
            self.selected_file = selection[0]
            name = os.path.basename(self.selected_file)
            self.status.text = f'সিলেক্ট: {name}'

    def start_enhance(self, *args):
        if not self.selected_file:
            self.status.text = 'আগে ভিডিও সিলেক্ট করুন!'
            return
        self.btn.disabled = True
        self.status.text = 'Model লোড হচ্ছে...'
        threading.Thread(target=self.run_enhance).start()

    def run_enhance(self):
        self.enhancer.load_model()
        input_path = self.selected_file
        output_path = input_path.replace('.mp4', '_enhanced.mp4') \
                                .replace('.mkv', '_enhanced.mp4') \
                                .replace('.avi', '_enhanced.mp4')
        self.update_status('Enhance শুরু হচ্ছে...')

        self.enhancer.enhance_video(
            input_path, output_path,
            progress_callback=self.update_progress
        )
        self.update_status(f'সম্পন্ন! সেভ হয়েছে: {os.path.basename(output_path)}')
        self.enable_btn()

    @mainthread
    def update_progress(self, val):
        self.progress.value = val
        self.status.text = f'প্রসেসিং... {val}%'

    @mainthread
    def update_status(self, msg):
        self.status.text = msg

    @mainthread
    def enable_btn(self):
        self.btn.disabled = False


class EnhancerApp(App):
    def build(self):
        return EnhancerUI()

if __name__ == '__main__':
    EnhancerApp().run()
