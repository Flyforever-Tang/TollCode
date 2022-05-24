import PySimpleGUI as sg
import os
from PIL import Image
import numpy as np


class ImageCounter(object):
    def __init__(self,
                 root_path: str,
                 fixed_height: int = 800,
                 temp_path: str = None,
                 image_format: tuple = ('.png', '.jpg', '.jpeg', '.JPG', '.PNG')):
        self.fixed_height = fixed_height

        if temp_path is None:
            self.temp_path = '/'.join(root_path.split('/')[:-1]) + '/temp'
        else:
            self.temp_path = temp_path
        if not os.path.exists(self.temp_path):
            os.makedirs(self.temp_path)

        self.images = []
        self.image_names = []
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if os.path.splitext(file)[-1] in image_format:
                    image_path = root + '/' + file
                    self.images.append(image_path)
                    self.image_names.append(file)
        self.sum = len(self.images)
        self.count = 0
        self.index = 0
        self.names_and_labels = np.array([[self.image_names[i], False] for i in range(self.sum)])
        self.labels = [False for _ in range(self.sum)]
        self.finish = False

    def back(self):
        if self.index > 0:
            self.index -= 1
            return True
        return False

    def next(self):
        if self.index < self.sum - 1:
            self.index += 1
            return True
        return False

    def set_label(self,
                  label: bool):
        if self.index < self.sum - 1:
            self.labels[self.index] = label
            self.names_and_labels[self.index, 1] = label
            self.count = self.labels.count(True)
            self.index += 1
            return True
        elif self.index == self.sum - 1 and not self.finish:
            self.labels[self.index] = label
            self.names_and_labels[self.index, 1] = label
            self.count = self.labels.count(True)
            self.finish = True
            return True
        return False

    def get(self):
        image_path = self.images[self.index]
        image_name = self.image_names[self.index]
        name_split = image_name.split('.')
        new_path = self.temp_path + '/' + '.'.join(name_split[:-1]) + '.png'
        if not os.path.exists(new_path):
            image = Image.open(image_path)
            image = image.resize((image.width * self.fixed_height // image.height, self.fixed_height))
            image.save(new_path)
        self.images[self.index] = new_path
        return self.images[self.index]


def main():
    counter = None
    fixed_height = 512
    row_height = 20

    layout = [
        [sg.Text('Number: '), sg.InputText('0', key='current', size=(4, 1)), sg.Text('/'), sg.Text('0', key='sum'),
         sg.Button('Go', key='go', focus=True, bind_return_key=True), sg.Text('    '),
         sg.Text('Correct:'), sg.Text('0', key='correct'), sg.Text('    ')],
        [sg.Table([[' ' * 30]], ['name', 'label'], row_height=row_height, num_rows=fixed_height // row_height,
                  justification='left', enable_click_events=True, font=('Times New Roman', 10), key='image_table'),
         sg.Image(size=(0, fixed_height), key='image', expand_x=True, background_color='white')],
        [sg.Button('Select Folder', key='select')]
    ]
    window = sg.Window('Imitator', layout, font=('Times New Roman', 20), return_keyboard_events=True)

    while True:
        ui_event, values = window.read()
        print(ui_event)
        print(values)
        if ui_event is None:
            break
        elif ui_event == 'select':
            folder_path = sg.popup_get_folder('Select Image Folder')
            counter = ImageCounter(folder_path, fixed_height)
            window['image'].Update(filename=counter.get())
            window['image'].set_size((None, fixed_height))
            window['current'].Update(1)
            window['sum'].Update(counter.sum)
            window['correct'].Update(0)
            window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
        if counter is not None:
            if ui_event == 'Left:37':
                if counter.back():
                    window['image'].Update(filename=counter.get())
                    window['image'].set_size((None, fixed_height))
                    window['current'].Update(counter.index + 1)
                    window['sum'].Update(counter.sum)
                    window['correct'].Update(counter.count)
                    window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
            if ui_event == 'Right:39':
                if counter.next():
                    window['image'].Update(filename=counter.get())
                    window['image'].set_size((None, fixed_height))
                    window['current'].Update(counter.index + 1)
                    window['sum'].Update(counter.sum)
                    window['correct'].Update(counter.count)
                    window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
            elif ui_event == 'Up:38':
                if counter.set_label(True):
                    window['image'].Update(filename=counter.get())
                    window['image'].set_size((None, fixed_height))
                    window['current'].Update(counter.index + 1)
                    window['sum'].Update(counter.sum)
                    window['correct'].Update(counter.count)
                    window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
            elif ui_event == 'Down:40':
                if counter.set_label(False):
                    window['image'].Update(filename=counter.get())
                    window['image'].set_size((None, fixed_height))
                    window['current'].Update(counter.index + 1)
                    window['sum'].Update(counter.sum)
                    window['correct'].Update(counter.count)
                    window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
            elif ui_event == 'go':
                counter.index = int(values['current']) - 1
                window['image'].Update(filename=counter.get())
                window['image'].set_size((None, fixed_height))
                window['current'].Update(counter.index + 1)
                window['sum'].Update(counter.sum)
                window['correct'].Update(counter.count)
                window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])
            elif 'image_table' in ui_event:
                row = ui_event[-1][0]
                counter.index = row
                window['current'].Update(row)
                window['image'].Update(filename=counter.get())
                window['image'].set_size((None, fixed_height))
                window['current'].Update(counter.index + 1)
                window['sum'].Update(counter.sum)
                window['correct'].Update(counter.count)
                window['image_table'].Update(values=counter.names_and_labels, select_rows=[counter.index])

    window.close()


if __name__ == '__main__':
    main()
