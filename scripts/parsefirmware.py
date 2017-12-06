import sys
import struct 

def upload(ilm_size, dlm_size):

    USB_END_PADDING = 4
    UPLOAD_FW_UNIT = 14592
    HDR_LEN = 32


    cur_len = 0
    sent_len = 0

    cur_len = 0x40      # 64

    while True:
        sent_len_max = UPLOAD_FW_UNIT - HDR_LEN - USB_END_PADDING
   
        if ilm_len - cur_len > sent_len_max:
            sent_len = sent_len_max
        else:
            sent_len = ilm_len - cur_len

        print("cur_len:                      {}".format(cur_len))
        print("sent_len:                     {}".format(cur_len))

        if sent_len > 0:

            low = (cur_len & 0xFFFF)
            high = (cur_len & 0xFFFF0000) >> 16

            print("USB SEND 0x42 cur_len low:    {} 0x230".format(low))
            print("USB SEND 0x42 cur_len high:   {} 0x232".format(high))

            cur_len += sent_len

            low = ((sent_len << 16) & 0xFFFF)
            high = ((sent_len << 16) & 0xFFFF0000) >> 16

            print("USB SEND 0x42 sent_len low:   {} 0x234".format(low))
            print("USB SEND 0x42 sent_len high:  {} 0x236".format(high))


        else:
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} firmware.bin".format(sys.argv[0]))
        exit()

    files = sys.argv[1:]

    for filename in files:
        data = None
        with open(filename, "rb") as f:
            data = f.read()

        image_size = len(data)

    #    ilm_len 4 bytes
    #    dlm_len 4 bytes
    #    fw_ver 2 bytes
    #    build_ver 2 bytes
    #
    #    4 bytes of something? 
    #
    #    build_time 16 byte str starting from byte 16 (base+16) """
        hdr = data[:32]
        ilm_len, dlm_len, fw_ver, build_ver, something, build_time = struct.unpack("<IIHH4s16s", hdr)

        if ilm_len + dlm_len + 32 != image_size:
            print("searching for header at end of file")

            hdr = data[image_size-32:]
            ilm_len, dlm_len, fw_ver, build_ver, something, build_time = struct.unpack("<IIHH4s16s", hdr)

            if ilm_len + dlm_len + 32 != image_size:
                print("section lengths don't match for {}".format(filename))
                continue

        print("image name: {}".format(filename))
        print("image size: {}".format(image_size))
        print("ilm_len:    {}".format(ilm_len))
        print("dlm_len:    {}".format(dlm_len))
        print("fw_ver:     {}".format(fw_ver))
        print("build_ver:  {:2x}".format(build_ver))
        print("something:  {}".format(something))
        print("build_time: {}".format(build_time))


        print("fw version:{}.{}.{}"
            .format(
                (fw_ver & 0xf000) >> 8, 
                (fw_ver & 0x0f00) >> 8, 
                fw_ver & 0x00ff))
        print("")

        upload(ilm_len, dlm_len)

