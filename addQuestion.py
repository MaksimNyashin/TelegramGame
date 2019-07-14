__author__ = 'Maks_El_Diablo'
# This Python file uses the following encoding: utf-8
import database
import misc

change = misc.change


def chfl(s):
    s0 = "йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjklzxcvbnm"
    s1 = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFGHJKLZXCVBNM"
    if s[0] in s0:
        z = s0.index(s[0])
        return s1[z] + s[1:]
    return s


def read_all():
    import codecs
    fi = codecs.open("questions.txt", "r", "utf-8")
    z = fi.read().split("\n\n")
    fi.close()
    return z


def update():
    z = read_all()
    for i in range(len(z)):
        q = z[i].split("\n")
        for j in range(1, len(q)):
            w = q[j].split("/")
            for l in range(len(w)):
                w[l] = change(w[l])
            q[j] = "/".join(i for i in w)
        z[i] = "\n".join(i for i in q)
    import codecs
    fo = codecs.open('questions.txt', "w", "utf-8")
    fo.write("\n\n".join(i for i in z))
    fo.close()


def main():
    z = read_all()

    while True:
        theme = input("Theme: ")
        if theme[0] == '-':
            if theme == "-п":
                print_sizes()
            elif theme == "-а":
                play_alex()
            elif theme == "-exit" or theme == "-конец":
                break
            else:
                print_sizes(int(theme[2:]))
            continue

        theme = int(theme)
        question = chfl(input("Quest: "))
        if not question.endswith("?"):
            question += "?"
        ok = chfl(input("OK: "))
        wa1 = chfl(input("WA1: "))
        wa2 = chfl(input("WA2: "))
        wa3 = chfl(input("WA3: "))
        z[theme - 1] += '\n' + "/".join(change(i) for i in [question, ok, wa1, wa2, wa3])

        import codecs
        fo = codecs.open('questions.txt', "w", "utf-8")
        fo.write("\n\n".join(i for i in z))
        fo.close()


def print_sizes(x=0):
    z = read_all()

    lst = []
    for i in range(len(z)):
        if x == 0 or x == i + 1:
            q = z[i].split('\n')
            lst.append([q[0], len(q) - 1])
    lst.sort(key=lambda y: -y[1])
    ans = 0
    for i in lst:
        print(i[0], i[1])
        ans += i[1]
    if x == 0:
        print("total =", ans)


def add_questions():
    z = read_all()

    for i in range(len(z)):
        z[i] = z[i].split("\n")[1:]
        cnt = database.get_constant("theme_" + str(i + 1))
        # for j in range(cnt, len(z[i])):
        for j in range(cnt, 20):
            quest, ok, wa1, wa2, wa3 = z[i][j].split("/")
            database.add_question(i + 1, quest, ok, wa1, wa2, wa3)
        # print("addQuestion.add_questions.newCnt", database.get_constant("theme_" + str(i + 1)))
    database.print_table("questions")
    pass


def play_alex():
    z = read_all()
    n = len(misc.categories)
    for i in range(n):
        z[i] = z[i].split("\n")[1:]
    import random
    while True:
        a = random.randint(1, n)
        b = random.randint(1, len(z[a - 1]))
        c = [misc.re_change(i) for i in z[a - 1][b - 1].split("/")]
        print(misc.categories[a - 1])
        print(c[0])
        print(c[1], c[2], c[3], c[4], sep="     ")
        ex = input()
        if ex != "":
            break


if __name__ == '__main__':
    # add_questions()
    # update()
    # print(change("/?.,.+-*"))
    main()
    # print_sizes()
    # play_alex()
    pass
