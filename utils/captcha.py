import random
import string

"""
传入整型参数 a 和 b
生成含有 a 个数字和 b 个字母的随机验证码
验证码全大写
"""


def verification_code(a: int, b: int) -> str:
    digits = [str(random.randint(0, 9)) for _ in range(a)]
    letters = [random.choice(string.ascii_letters) for _ in range(b)]
    code_list = digits + letters
    random.shuffle(code_list)
    code = ''.join(code_list)
    return code.upper()


if __name__ == '__main__':
    print(verification_code(2, 2))
