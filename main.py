from app.tasks import add, mul, xsum

def main():
    r1 = add.delay(4, 6)
    r2 = mul.delay(3, 7)
    r3 = xsum.delay([1, 2, 3, 4, 5])

    print("result1:", r1.get())
    print("result2:", r2.get())
    print("result3:", r3.get())

if __name__ == "__main__":
    main()