

if __name__ == "__main__":
    with open("VirtualHardDrive.VHD", "rb") as f:
        for b in f.read():
            if b != 0:
                print(b)
        #  print(f.read())

