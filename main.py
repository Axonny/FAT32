from boot_sector import Boot


if __name__ == "__main__":
    with open("mbr.vhd", "rb") as f:
        f.read(65536)
        boot = Boot(f)

    print(boot.size_sector)
