import os
import sys
import cv2
from PIL import Image
from multiprocessing import Process, cpu_count
import time


class run:
    def __init__(self):
        file_name = input("file name:")
        self.size = 7
        self.starttop = 0
        self.count = 0
        rc = 0
        self.c = [" ", ".", ".", "-", "+", "o", "U", "Ş", "@", "@", "@", "@", "@", "@"]
        vidcap = cv2.VideoCapture(file_name)
        success, image1 = vidcap.read()
        self.fps = 1
        print("Reading frames")
        while success:
            cv2.imwrite("frame%d.jpg" % self.count, image1)  # save frame as JPEG file
            success, image1 = vidcap.read()
            self.count += 1
            for i in range(self.fps):vidcap.read()
            rc += self.fps
        print("done!")

        self.allims = [i for i in range(0,rc,self.fps)]
        self.allims.pop()
        print(len(self.allims))
    def read_image(self,i, z):
        l = []
        for image in range(i * int(len(self.allims) / cpu_count()), (i + 1) * int(len(self.allims) / cpu_count()), self.fps):
            img = Image.open(f"frame{image}.jpg")
            last = ""
            for y in range(self.starttop, int(img.size[1] / self.size)):
                for x in range(int(img.size[0] / self.size)):
                    s = 0
                    for yy in range(self.size - 1):
                        for xx in range(self.size - 1):
                            s += sum(img.getpixel((x * self.size + xx, y * self.size + yy)))

                    last += self.c[int(s / int((765 * (self.size) ** 2) / len(self.c)))]
                last += "\n"
            img.close()
            os.system("")
            l.append(last)
        file1 = open(f"core-{i}.txt", "w+")
        file1.write("".join(l))
        file1.close()
    def main(self):
        threads = []
        for i in range(cpu_count()):
            b = Process(target=self.read_image,args=(i,None))
            threads.append(b)
        for i in threads:
            i.start()
        for i in threads:
            i.join()



        os.system("cls")
        zzz = open("core-0.txt","r")
        img = Image.open("frame0.jpg")
        height = int(img.size[1] / self.size)
        img.close()
        print(height)
        zzz.close()
        print("a")
        while True:
            for i in range(cpu_count()):
                file = open(f"core-{i}.txt","r+")
                z = file.read().replace("\n","i").split("i")
                t = []
                for i in range(0,len(z)-height,height):
                    t.append("\n".join(z[i:i+height]))
                for i,e in enumerate(t):
                   sys.stdout.write('\r')
                   sys.stdout.write("%s" % e)
                   sys.stdout.flush()
                   time.sleep(0.07)

                file.close()
            z = input("Again Y | N ?\n").lower()
            if z != "y":
                break

        for i in range(cpu_count()):
            os.remove(f"core-{i}.txt")
        for i in range(self.count):
            os.remove(f"frame{i}.jpg")



if __name__ == "__main__":
    run().main()
