import base64,zlib,os,struct

saves = ["CCGameManager.dat","CCLocalLevels.dat"]
fPath = os.getenv("localappdata") + "\\GeometryDash\\"

def Xor(data,key):
    res = []
    for i in data:
        res.append(i^key)
    return bytearray(res).decode()

def FileOpen(path):
    fr = open(path,"rb")
    data = fr.read()
    fr.close()
    return data

print("1. Encrypt\n2. Decrypt (code download from https://pastebin.com/JakxXUVG by Absolute Gamer)")
while True:
    s = input("\n> ")
    print()
    
    try:
        index = int(s)
    except ValueError as e:
        exit()

    if index == 1:
        for x in range(2):
            try:
                data = FileOpen(saves[x] + ".txt")
            except FileNotFoundError as e:
                print("Can't find", saves[x] + ".txt", "in current directory!")
            except:
                print("Failed to load", saves[x] + ".txt", "!")
            else:
                print("Encrypting", saves[x] + ".txt", "...")
                
                compressedData = zlib.compress(data)
                crc32 = struct.pack('I',zlib.crc32(data))
                dataSize = struct.pack('I',len(data))

                encrypted = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' + compressedData[2:-4] + crc32 + dataSize
                encoded = base64.b64encode(encrypted).decode().replace('+','-').replace('/','_').encode()
                fin = Xor(encoded,11).encode()
                
                try:
                    fw = open(fPath + saves[x],"wb")
                except:
                    print("Failed to write", saves[x], "!")
                else:
                    fw.write(fin)
                    fw.close()
                    print("Done!")
    elif index == 2:
        for x in range(2):
            try:
                data = FileOpen(fPath + saves[x])
            except FileNotFoundError as e:
                print("Can't find", saves[x], "in profile directory!")
            except:
                print("Failed to load", saves[x], "!")
            else:
                print("Decrypting", saves[x], "...")
                
                res = Xor(data,11)
                fin = zlib.decompress(base64.b64decode(res.replace('-','+').replace('_','/').encode())[10:],-zlib.MAX_WBITS)
                
                try:
                    fw = open(saves[x] + ".txt","wb")
                except:
                    print("Failed to write", saves[x] + ".txt", "!")
                else:
                    fw.write(fin)
                    fw.close()
                    print("Done!")
    else:
        exit()