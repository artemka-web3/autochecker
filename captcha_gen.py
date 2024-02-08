from captcha.image import ImageCaptcha
from random import choice

def gen_captcha(username):
    numbers = [str(i) for i in range(1, 10)]
    letters = [chr(ord('A') + i) for i in range(26)]
    result_list = numbers + letters

    pattern = []

    for i in range(10):
        pattern.append(choice(result_list))

    image_captcha = ImageCaptcha(width=300, height=200)
    image_captcha.write(pattern, f'{username}_captcha.png')
    return "".join(str(item) for item in pattern)