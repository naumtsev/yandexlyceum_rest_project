from PIL import Image


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    resized_image.save(output_image_path)


#resize_image(input_image_path= 'img1.jpg',
#                output_image_path='static/images/23.jpg',
#                size=(300, 456))