# -*- coding: utf_8 -*-
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile


class MyStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        # 处理逻辑
        if 'image' in content.content_type:
            # 如果是图片，则加水印
            image = self.watermark_with_text(content, 'cq', 'red')
            content = self.convert_image_file(image, name)
        return super(MyStorage, self).save(name, content, max_length)

    @staticmethod
    def watermark_with_text(file_obj, text, color, fontfamily='/home/cq/Downloads/Mada-Regular.otf'):
        image = Image.open(file_obj).convert('RGBA')

        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        font = ImageFont.truetype(fontfamily, int(height/20))
        text_width, text_height = draw.textsize(text, font)
        x = (width - text_width - margin) / 2
        y = height - text_height - margin

        draw.text((x, y), text, color, font)

        return image

    @staticmethod
    def convert_image_file(image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)


