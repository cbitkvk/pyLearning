import threading
import time


def try_bounded(dict, k):
    tr = threading.BoundedSemaphore(value=4)
    tr.acquire()
    print("started {}".format(k))
    time.sleep(20)
    print(dict)
    print("ended dict {}".format(k))
    tr.release()


def main():
    p = range(100)

    for j in p:
        print("{} has started".format(j))
        l = dict()
        l[j] = p
        th = threading.Thread(target=try_bounded, args=(l,j,))
        th.start()
        print("{} has ended".format(j))


if __name__ == "__main__":
    main()