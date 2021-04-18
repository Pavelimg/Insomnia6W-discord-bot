from PIL import Image
import os
import imageio


class Ring:
    def __init__(self, name, file_format, arrow):
        self.name = name
        self.FileFormat = file_format
        self.arrow = arrow

    def create_files(self, rotate):
        if not os.path.exists('Images'):
            os.mkdir("Images")
        im = Image.open(f'{self.name}.{self.FileFormat}')

        for i in range(0, 361, rotate):
            if not os.path.exists(f'Images/{self.name}_{i}.{self.FileFormat}'):
                im_rotate = im.rotate(i)
                im_rotate.paste(Image.open(self.arrow), (0, 218), Image.open(self.arrow))
                im_rotate.save(f'Images/{self.name}_{i}.{self.FileFormat}', quality=100)
                print(f"Create {self.name}_{i}.{self.FileFormat}")
            else:
                print(f"Already exists {self.name}_{i}.{self.FileFormat}")
        im.close()
        print("File creator finished work")

    def create_video(self, rotate):
        if os.path.exists('result.gif'):
            os.remove('result.gif')
        try:
            with imageio.get_writer('result.gif', mode='I') as writer:
                for i in range(360 - rotate, -1, -rotate):
                    image = imageio.imread(f'Images/{self.name}_{i}.{self.FileFormat}')
                    writer.append_data(image)
                    print(f"{self.name}_{i}.jpg")
            print('Video successfully created')
        except FileNotFoundError:
            print(f"ERROR: Make sure files exist 'Images/{self.name}_{i}.{self.FileFormat}'")

    def create_pro_video(self, start, fps, rotates):
        if os.path.exists('result.gif'):
            os.remove('result.gif')
        try:
            with imageio.get_writer('result.gif', mode='I', fps=fps) as writer:
                now_rotate = start
                for i in rotates:
                    for j in range(i[0]):
                        image = imageio.imread(f'Images/{self.name}_{now_rotate}.{self.FileFormat}')
                        writer.append_data(image)
                        print(f"Add {self.name}_{now_rotate}.{self.FileFormat} in GIF")
                        if now_rotate <= i[1]:
                            now_rotate += 360
                        now_rotate -= i[1]
            print('Video successfully created')
        except FileNotFoundError:
            print(f"ERROR: Make sure files exist Images/{self.name}_{now_rotate}.{self.FileFormat}'")
        N = 360 - now_rotate
        if N in range(0, 45) or N in range(180, 225):
            return 0
        elif N in range(45, 90) or N in range(225, 270):
            return 1.5
        elif N in range(90, 135) or N in range(270, 305):
            return 2
        elif N in range(135, 180) or N in range(305, 360):
            return 0.5

    def clear_files(self):
        for i in range(0, 360):
            if os.path.exists(f'Images/{self.name}_{i}.{self.FileFormat}'):
                os.remove(f'Images/{self.name}_{i}.{self.FileFormat}')
        print("Cleaning completed")
