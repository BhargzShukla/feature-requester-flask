u"""
First step of the process.
"""

list_char = [
    104, 116, 116, 112, 115, 58, 47, 47, 101, 110, 103,
    105, 110, 101, 101, 114, 105, 110, 103, 45, 97, 112,
    112, 108, 105, 99, 97, 116, 105, 111, 110, 46, 98,
    114, 105, 116, 101, 99, 111, 114, 101, 46, 99, 111,
    109, 47, 113, 117, 105, 122, 47, 115, 100, 102, 103,
    119, 114, 52, 52, 104, 114, 102, 104, 102, 104, 45,
    119, 115
    ]


def unicode_magic(character_list):
    u"""
    Convert ASCII codes to characters
    and create a string out of them.
    """
    chr_to_char = []
    for character in character_list:
        chr_to_char.append(chr(character))

    return ''.join(chr_to_char)


u"""
Second step of the application process.
"""

from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
# Some <inspect element> magic is what I'm going  to do!
message = b'gAAAAABcrXqofATLrptW5gsUQke5ymV5WUVXG4_nGReFFBtH9tOX97WlzBvmf-Ue71evmydkncKVffIZV0GNMkYZmqpxbqFiHZqlAxA_adDYPe7tl5zhL-k4ZMelXE8Tc1CmKCJ4nMV2_tPeFzzlUUaUml_epx0eRXAhbw6MvnV_fzLFC-fLyYLogyjvD6XQWt3-Z5cwDYi-'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
    # print(unicode_magic(list_char))
