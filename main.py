from boot_sector import Boot


if __name__ == "__main__":
    with open("VirtualHardDrive.VHD", "rb") as f:
        boot = Boot(f)

    print(boot.count_sectors)


