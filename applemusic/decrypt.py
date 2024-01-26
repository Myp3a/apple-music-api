# https://github.com/truedread/pymp4decrypt/blob/master/src/decrypt.py
from collections import deque
from io import BufferedReader, BytesIO

from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter
from pymp4.parser import Box
from pymp4.util import BoxUtil


def fix_headers(box):
    """
    fix_headers()

    @param box: pymp4 Box object
    """
    original_format = b"mp4a"
    for stsd_box in BoxUtil.find(box, b"stsd"):
        for entry in stsd_box.entries:
            if b"enc" in entry.format:
                entry.format = original_format
    return


def decrypt(key, inp, out):
    """
    decrypt()

    @param key: AES-128 CENC key in bytes
    @param inp: Open input file
    @param out: Open output file
    """

    with BufferedReader(inp) as reader:
        senc_boxes = deque()
        trun_boxes = deque()
        boxes = []
        while reader.peek(1):
            box = Box.parse_stream(reader)
            fix_headers(box)

            for stsd_box in BoxUtil.find(box, b"stsz"):
                sample_size = stsd_box.sample_size

            for stsd_box in BoxUtil.find(box, b"stsd"):
                newbox = stsd_box.entries[0]
                for b in newbox.children:
                    if b.type == b"sinf":
                        newbox.children.remove(b)

            if box.type == b"moof":
                senc_boxes.extend(BoxUtil.find(box, b"senc"))
                trun_boxes.extend(BoxUtil.find(box, b"trun"))
            elif box.type == b"mdat":
                senc_box = senc_boxes.popleft()
                trun_box = trun_boxes.popleft()

                clear_box = b""

                with BytesIO(box.data) as box_bytes:
                    for sample, sample_info in zip(
                        senc_box.sample_encryption_info, trun_box.sample_info
                    ):
                        counter = Counter.new(
                            64, prefix=sample.iv, initial_value=0
                        )

                        cipher = AES.new(key, AES.MODE_CTR, counter=counter)

                        if sample_size:
                            cipher_bytes = box_bytes.read(sample_size)
                            clear_box += cipher.decrypt(cipher_bytes)
                        elif not sample.subsample_encryption_info:
                            cipher_bytes = box_bytes.read(
                                sample_info.sample_size
                            )
                            clear_box += cipher.decrypt(cipher_bytes)
                        else:
                            for subsample in sample.subsample_encryption_info:
                                clear_box += box_bytes.read(
                                    subsample.clear_bytes
                                )
                                cipher_bytes = box_bytes.read(
                                    subsample.cipher_bytes
                                )
                                clear_box += cipher.decrypt(cipher_bytes)
                box.data = clear_box
            boxes.append(box)
    for b in boxes:
        out.write(Box.build(b))
    return
