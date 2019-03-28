
with open('/Users/a1/Desktop/point.csv', 'r') as file:
    lines = file.readlines()
    for s in filter(lambda x: x.startswith("* 쿠폰번호"), lines):
        print(s.split()[3])


