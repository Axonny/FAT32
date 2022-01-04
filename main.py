from boot_sector import Boot


if __name__ == "__main__":
    with open("mbr.vhd", "rb") as f:
        f.read(65536)
        boot1 = Boot(f)
        f.read(2560)
        boot2 = Boot(f)

    print(boot1.size_sector)
