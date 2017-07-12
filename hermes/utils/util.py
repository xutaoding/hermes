# -*- encoding: utf-8 -*-

import re
import six
import os.path
import hashlib
import random
import socket
import struct
from random import sample
from string import letters, digits


def md5(text):
    m = hashlib.md5()
    m.update(to_bytes(text))
    return m.hexdigest()


def recognize_chz_letter(string):
    chz_chars = []
    chz_regex = re.compile(u'[\u4e00-\u9fbf]', re.U)
    letters_regex = re.compile(u'[0-9A-Za-z]', re.U)

    for char in string:
        if chz_regex.search(char) or letters_regex.search(char):
            chz_chars.append(char)
    return ''.join(chz_chars)


def is_exists(file_or_dir_path):
    if os.path.basename(file_or_dir_path):
        file_path = os.path.dirname(file_or_dir_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    else:
        if not os.path.exists(file_or_dir_path):
            os.makedirs(file_or_dir_path)


def write(dir_path, filename, lines, uri=None, repl=u'\n'):
    is_exists(dir_path)
    base_path = [dir_path, filename, '_']

    if uri is not None:
        suffix = [md5(uri)]
    else:
        suffix = sample(letters, 8) + sample(digits, 6)

    abs_filename = ''.join(base_path + suffix + ['.txt'])

    with open(abs_filename, 'w') as fp:
        try:
            if isinstance(lines, (tuple, list)):
                lines_seq = repl.join(lines).encode('u8')
            else:
                lines_seq = lines
            fp.writelines(lines_seq)
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass


def combinations(good_name, brand, keyword, category_list, sku_attr_list):
    """ Search Key sort and priority """
    data = list()
    base_search_word = ' '.join([brand, keyword])
    min_word_prio = (base_search_word, 0)

    cat_list = [c.strip() for c in category_list if c.strip()]
    sku_list = [s.split('-', 1)[-1].strip() for s in sku_attr_list if s.split('-', 1)[-1].strip()]
    search_words = sku_list + cat_list

    data.append((good_name, len(search_words) + 1))
    left_words, right_words = search_words[::], search_words[::]

    while left_words or right_words:
        r_prio, l_prio = len(right_words), len(left_words)
        right_word_prio = (' '.join([base_search_word] + right_words), r_prio)
        left_word_prio = (' '.join([base_search_word] + left_words), l_prio)

        right_word_prio not in data and data.append(right_word_prio)
        left_word_prio not in data and data.append(left_word_prio)

        right_words and right_words.pop()
        left_words and left_words.pop(0)

    if keyword and min_word_prio not in search_words:
        data.append(min_word_prio)

    return data[::-1]


def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of `text`. If `text`
        is already a bytes object, return it as-is."""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)


def fake_proxy():
    random_ip_pool = ['10.253.110.30/0']
    str_ip = random_ip_pool[random.randint(0, len(random_ip_pool) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I'.encode('u8'), socket.inet_aton(str_ip_addr))[0]
    mask = 0x0

    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | (1 << i)

    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)

    return socket.inet_ntoa(struct.pack('>I'.encode('u8'), random.randint(ip_addr_min, ip_addr_max)))


if __name__ == '__main__':
    m5 = md5('12345')
    print m5
    print len(m5)


