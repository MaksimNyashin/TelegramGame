__author__ = 'Maks_El_Diablo'
# This Python file uses the following encoding: utf-8
import misc


class Tables:
    @staticmethod
    def drop_table(table_name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE " + table_name)
        conn.commit()

    @staticmethod
    def remake_table(table_name, f):
        drop_table(table_name)
        f()

    @staticmethod
    def print_table(table_name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        if table_name == "questions":
            cursor.execute("SELECT * FROM " + table_name + " ORDER BY theme, id")
            lst = cursor.fetchall()
            for list_id in range(len(lst)):
                print("database.print_name.{}.{}:".format(table_name, str(list_id)), lst[list_id])
        else:
            cursor.execute("SELECT * FROM " + table_name)
            lst = cursor.fetchall()
            print("database.print_name.{}:".format(table_name), lst)

    @staticmethod
    def drop_theme(theme_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE theme=?", (theme_id,))
        conn.commit()
        update_constant("theme_" + str(theme_id), 0)


drop_table = Tables.drop_table
drop_theme = Tables.drop_theme
print_table = Tables.print_table
remake_table = Tables.remake_table


class Consts:
    @staticmethod
    def create_constants_table():
        cursor = misc.get_conn().cursor()
        cursor.execute("""CREATE TABLE consts(name text, value integer)""")

    @staticmethod
    def add_constant(name, value):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO consts VALUES(?, ?)""", (name, value))
        conn.commit()

    @staticmethod
    def get_constant(name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT value FROM consts WHERE name=?""", (name,))
        lst = cursor.fetchall()
        print("database.get_constant.{}:".format(name), lst)
        return lst[0][0]

    @staticmethod
    def update_constant(name, new_value):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""UPDATE consts SET value=? WHERE name=?""", (new_value, name))
        conn.commit()


add_constant = Consts.add_constant
create_constants_table = Consts.create_constants_table
get_constant = Consts.get_constant
update_constant = Consts.update_constant


class Players:
    @staticmethod
    def create_player_table():
        cursor = misc.get_conn().cursor()
        cursor.execute("""CREATE TABLE players(name text, id integer, last_game integer, rate integer)""")

    @staticmethod
    def add_player(player_id, name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM players WHERE id=?""", (player_id,))
        lst = cursor.fetchall()
        if len(lst) != 0:
            print("database.add_player.lst:", lst)
            if lst[0][0] != name:
                if name[-1] != "\t" or name[:-7] != lst[0][0][:-7]:
                    cursor.execute("""UPDATE players SET name=? WHERE id=?""", (name, player_id))
                    conn.commit()
            return
        cursor.execute("""INSERT INTO players VALUES(?, ?, ?, ?)""", (name, player_id, -1, misc.base_rate))
        conn.commit()

    @staticmethod
    def change_name(player_id, new_name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM players WHERE name=?""", (new_name,))
        if len(cursor.fetchall()) != 0:
            return False
        print("database.change_name.new_name&player_id:", new_name, player_id)
        cursor.execute("""UPDATE players SET name=? WHERE id=?""", (new_name, player_id))
        conn.commit()
        return True

    @staticmethod
    def get_name(player_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT name FROM players WHERE id=?""", (player_id,))
        lst = cursor.fetchall()
        return lst[0][0]

    @staticmethod
    def get_last_game(player_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT last_game FROM players WHERE id=?""", (player_id,))
        lst = cursor.fetchall()
        return lst[0][0]

    @staticmethod
    def update_last_game(player_id, new_last_game):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""UPDATE players SET last_game=? WHERE id=?""", (new_last_game, player_id))
        conn.commit()

    @staticmethod
    def get_rate(player_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT rate FROM players WHERE id=?""", (player_id,))
        lst = cursor.fetchone()
        return lst[0]

    @staticmethod
    def set_rate(player_id, new_rate):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""UPDATE players SET rate=? WHERE id=?""", (new_rate, player_id))
        conn.commit()

    @staticmethod
    def get_id(player_name):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id FROM players WHERE name=?""", (player_name,))
        lst = cursor.fetchone()
        if len(lst) == 0:
            return -1
        return lst[0]


add_player = Players.add_player
change_name = Players.change_name
create_player_table = Players.create_player_table
get_id = Players.get_id
get_last_game = Players.get_last_game
get_name = Players.get_name
get_rate = Players.get_rate
set_rate = Players.set_rate
update_last_game = Players.update_last_game


class Questions:
    @staticmethod
    def create_questions_table():
        cursor = misc.get_conn().cursor()
        cursor.execute(
            """CREATE TABLE questions(theme integer, id integer, question text, answer text, wa1 text, wa2 text, wa3 text, rate integer)""")

    @staticmethod
    def add_question(theme, question, answer, wa1, wa2, wa3):
        conn = misc.get_conn()
        cursor = conn.cursor()
        quest_id = get_constant("theme_" + str(theme))
        cursor.execute("""INSERT INTO questions VALUES(?, ?, ?, ?, ?, ?, ?, ?)""",
                       (theme, quest_id, question, answer, wa1, wa2, wa3, 1000))
        conn.commit()
        update_constant("theme_" + str(theme), quest_id + 1)

    @staticmethod
    def get_question_by_theme(theme):
        conn = misc.get_conn()
        cursor = conn.cursor()
        import random
        if theme == 18:
            theme = random.randint(1, misc.len_cat - 1)

        cursor.execute("""SELECT * FROM questions WHERE theme=?""", (theme,))
        lst = cursor.fetchall()
        # print("database.Players.get_question_by_theme.{}:".format(theme), lst)
        ret = list(lst[random.randint(0, len(lst) - 1)])
        for cnt in range(misc.shuffle_const):
            a, b = random.randint(3, 6), random.randint(3, 6)
            ret[a], ret[b] = ret[b], ret[a]
        for list_id in range(2, 7):
            ret[list_id] = misc.re_change(ret[list_id])
        return ret

    @staticmethod
    def get_question_by_number(quest_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM questions WHERE id=? AND theme=?""", (quest_id // 100, quest_id % 100))
        lst = cursor.fetchall()
        import random
        ret = list(lst[random.randint(0, len(lst) - 1)])
        for list_id in range(2, 7):
            ret[list_id] = misc.re_change(ret[list_id])
        ok = ret[3]
        for cnt in range(misc.shuffle_const):
            a, b = random.randint(3, 6), random.randint(3, 6)
            ret[a], ret[b] = ret[b], ret[a]
        print("database.get_question_by_number", ret)
        return ret, ok

    @staticmethod
    def get_question(user_id, game_number_str):
        def get_q(quests, q_id):
            if len(quests) > q_id:
                return quests[q_id]
            return -1

        try:
            game_number = int(game_number_str)
        except ValueError:
            return None
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM games WHERE (pl1=? OR pl2=?) AND id=?""", (user_id, user_id, game_number))
        lst = cursor.fetchall()
        if len(lst) == 0:
            return None
        game = Games.Game(d=Games.get_game(game_number))
        game.next_turn()
        update_last_game(user_id, game_number)
        if len(game.questions) > game.turn // 2:
            import time
            game.time = int(time.time())
            Games.write_game(game_number, d=game.get_dict())
            return get_question_by_number(game.questions[game.turn // 2])[0]
        # if len(game.questions) % 3 == 0 and len(game.questions) % 2 == game.turn % 2 :
        #    import random
        #    theme = random.randint(1, len(misc.categories))
        #    game.themes.append(theme)
        # else:
        theme = game.themes[-1]
        used_lst = [get_q(game.questions, game.turn // 2 // misc.questions_in_block * misc.questions_in_block + list_id)
                    for list_id in range(misc.questions_in_block)]
        print("database.Questions.get_question.used_lst:", used_lst)
        while True:
            quest = get_question_by_theme(theme)
            if quest[1] * 100 + quest[0] not in used_lst:
                break
        game.questions.append(quest[1] * 100 + quest[0])
        import time
        game.time = int(time.time())
        Games.write_game(game_number, d=game.get_dict())
        return quest


add_question = Questions.add_question
create_questions_table = Questions.create_questions_table
get_question = Questions.get_question
get_question_by_number = Questions.get_question_by_number
get_question_by_theme = Questions.get_question_by_theme


class Games:
    @staticmethod
    def create_game_table():
        cursor = misc.get_conn().cursor()
        cursor.execute("""CREATE TABLE games(id integer, pl1 integer, pl2 integer, finished integer)""")

    class Game:
        def __init__(self, d=None, game_id=None, pl1=None, pl2=None, themes=None, questions=None,
                     success=[0] * misc.questions_in_game * 2, shuffled_themes=None,
                     turn=-1, time=None):
            if themes is None:
                themes = list()
            if questions is None:
                questions = list()
            if shuffled_themes is None:
                shuffled_themes = [ii + 1 for ii in range(misc.len_cat)]
            if d is None:
                self.id = game_id
                self.pl1 = pl1
                self.pl2 = pl2
                self.themes = themes
                self.questions = questions
                self.success = success
                self.shuffled_themes = shuffled_themes
                self.turn = turn
                self.time = time
            else:
                self.id = d["id"]
                if "pl1" in d:
                    self.pl1 = d["pl1"]
                if "pl2" in d:
                    self.pl2 = d["pl2"]
                if "themes" in d:
                    self.themes = d["themes"]
                if "questions" in d:
                    self.questions = d["questions"]
                if "success" in d:
                    self.success = d["success"]
                if "shuffled_themes" in d:
                    self.shuffled_themes = d["shuffled_themes"]
                if "turn" in d:
                    self.turn = d["turn"]
                if "time" in d:
                    self.time = d["time"]
            pass

        def get_dict(self):
            d = {"id": self.id, "pl1": self.pl1, "pl2": self.pl2, "themes": self.themes, "questions": self.questions,
                 "success": self.success, "shuffled_themes": self.shuffled_themes, "turn": self.turn, "time": self.time}
            return d

        def next_turn(self):
            self.turn = self.get_next_turn()
            pass

        def get_next_turn(self):
            ret = self.turn
            if self.turn >= misc.questions_in_game * 2:
                return misc.questions_in_game * 2
            # if self.turn + 2 == misc.questions_in_game * 2:
            # ret = self.turn + 2
            elif self.turn == -1:
                ret = 0
            elif (self.turn + 1) % (4 * misc.questions_in_block) == 0:
                ret -= (2 * misc.questions_in_block - 1)
            elif (self.turn + 2) % (4 * misc.questions_in_block) == 2 * misc.questions_in_block:
                ret -= (2 * misc.questions_in_block - 3)
            else:
                ret += 2
            return ret

    @staticmethod
    def get_possibility(game_id, pl_id, _game=None):
        if _game is None:
            _game = Games.get_game(game_id)
        z = Games.Game(d=_game)
        pl1 = z.pl1
        pl2 = z.pl2
        if pl1 != pl_id and pl2 != pl_id:
            return False
        q = z.get_next_turn()
        # print("\t", pl1, pl2, pl_id, q)
        if pl1 == pl_id and q % 2 == 0:
            return True
        if pl2 == pl_id and q % 2 == 1:
            return True
        return False

    @staticmethod
    def get_game(game_id):
        import json
        fi = open("Games/{}.json".format(str(game_id)), "r")
        z = json.load(fi)
        fi.close()
        return z

    @staticmethod
    def write_game(game_id, d):
        import json
        fo = open("Games/{}.json".format(str(game_id)), "w")
        json.dump(d, fo)
        fo.close()

    @staticmethod
    def get_score(game_id, player_id):
        game = Games.Game(d=Games.get_game(game_id))
        gg = game.get_next_turn() // 2 * 2
        sc1 = sum(list_id for list_id in game.success[:gg:2])
        sc2 = sum(list_id for list_id in game.success[1:gg:2])
        if game.pl2 == player_id:
            sc1, sc2 = sc2, sc1
        return "{}:{}".format(sc1, sc2)

    @staticmethod
    def create_game(player_id, opp_id=None):
        conn = misc.get_conn()
        cursor = conn.cursor()

        def check_games(pl_id):
            cursor.execute("""SELECT * FROM games WHERE (pl1=? OR pl2=?) AND finished=0""", (pl_id, pl_id))
            lst0 = cursor.fetchall()
            if len(lst0) >= misc.max_games_number:
                return False
            return True

        if not check_games(player_id):
            return False
        if opp_id is not None and not check_games(opp_id):
            return False
        # cursor.execute("""SELECT * FROM games WHERE pl2=0 AND pl1<>? AND finished=0""", (player_id,))
        cursor.execute("""SELECT * FROM games WHERE pl2=0""")
        lst = cursor.fetchall()
        print("database.create_game.lst:", lst)
        if len(lst) == 0 or opp_id is not None:
            game_id = get_constant("game_id")
            print(game_id, player_id, opp_id)
            if opp_id is None:
                cursor.execute("""INSERT INTO games VALUES(?, ?, ?, ?)""", (game_id, player_id, 0, 0))
                conn.commit()
            else:
                cursor.execute("""INSERT INTO games VALUES(?, ?, ?, ?)""", (game_id, player_id, opp_id, 0))
                conn.commit()
            shuffled_themes = [list_id + 1 for list_id in range(misc.len_cat)]
            import random
            random.shuffle(shuffled_themes)
            shuffled_themes += [
                shuffled_themes[random.randint(1, misc.len_cat) - 1]]  # TODO: replace with random question theme
            if opp_id is None:
                Games.write_game(game_id,
                                 Games.Game(game_id=game_id, pl1=player_id, shuffled_themes=shuffled_themes).get_dict())
            else:
                Games.write_game(game_id, Games.Game(game_id=game_id, pl1=player_id, pl2=opp_id,
                                                     shuffled_themes=shuffled_themes).get_dict())
            update_constant("game_id", game_id + 1)
        else:
            game_id = lst[-1][0]
            game = Games.Game(d=Games.get_game(game_id))
            game.pl2 = player_id
            Games.write_game(game_id, game.get_dict())
            cursor.execute("""UPDATE games SET pl2=? WHERE id=?""", (player_id, game_id))
            conn.commit()
        return True

    @staticmethod
    def get_games_list(player_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, pl1, pl2 FROM games WHERE (pl1=? OR pl2=?) AND finished=0""",
                       (player_id, player_id))
        lst = cursor.fetchall()
        # print("database.get_games_list.lst:", lst)
        ret = []
        ret2 = []
        for game in lst:
            if Games.get_possibility(game[0], player_id):
                pl = game[1] if game[2] == player_id else game[2]
                ret.append([game[0], pl])
            else:
                pl = game[1] if game[2] == player_id else game[2]
                ret2.append([game[0], pl])
        # print("database.get_games_list.lst:", lst)
        print("database.get_games_list.ret:", ret)
        print("database.get_games_list.ret2:", ret2)
        return ret, ret2

    @staticmethod
    def set_finished(game_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""UPDATE games SET finished=1 WHERE id=?""", (game_id,))
        conn.commit()

    @staticmethod
    def get_finished(game_id):
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT finished FROM games WHERE id=?""", (game_id,))
        lst = cursor.fetchall()
        return lst[0][0]

    @staticmethod
    def get_stats(player_id):  # TODO: Finish get stats
        conn = misc.get_conn()
        cursor = conn.cursor()
        cursor.execute("""SELECT id FROM games WHERE (pl1=? OR pl2=?) AND finished=1""", (player_id, player_id))
        lst0 = cursor.fetchall()
        lst = [lst_id[0] for lst_id in lst0]
        a = ["Игры", "Победы", "Ничьи", "Поражения", "Игры без ошибок", "Срединй счёт"]
        for cat_id in misc.categories[:-1]:
            a.append(cat_id)
        d1, d2 = {}, {}
        for a_id in a:
            d1[a_id] = 0
            d2[a_id] = 0
        for a_id in range(5):
            d2[a[a_id]] = 1
        for game_id in lst:
            game = Games.Game(d=Games.get_game(game_id))
            d1[a[0]] += 1
            sc = list(int(sc_id) for sc_id in get_score(game_id, player_id).split(":"))
            d1[a[5]] += sc[0]
            if sc[0] > sc[1]:
                d1[a[1]] += 100
            elif sc[0] == sc[1]:
                d1[a[2]] += 100
            else:
                d1[a[3]] += 100
            if sc[0] == misc.questions_in_game:
                d1[a[4]] += 1

            z = 0
            if game.pl2 == player_id:
                z = 1
            for que_id in range(z, misc.questions_in_game * 2, 2):
                theme = game.questions[que_id // 2] % 100
                d2[misc.categories[theme - 1]] += 1
                if game.success[que_id] == 1:
                    d1[misc.categories[theme - 1]] += 100
        d2[a[1]], d2[a[2]], d2[a[3]], d2[a[5]] = d1[a[0]], d1[a[0]], d1[a[0]], d1[a[0]]
        f = lambda x, y: 0 if y == 0 else (x // y if x % y == 0 else int(x / y))

        def strip(a_, b_, l):
            sp = " " * l
            l = 20
            sp = " " * (l - len(a_))
            return a_ + sp + b_
            # return a_ + " " * (l) + b_

        ret = misc.your_stats + strip("Рейтинг", str(get_rate(player_id)), misc.strip_size) + "\n" + "\n".join(
            strip(a_id, str(f(d1[a_id], d2[a_id])) + ("%" if a_id not in [a[0], a[4], a[5]] else ""), misc.strip_size) for a_id in a)
        print(d1)
        print(d2)
        return ret


create_game = Games.create_game
create_game_table = Games.create_game_table
get_finished = Games.get_finished
get_games_list = Games.get_games_list
get_score = Games.get_score
get_stats = Games.get_stats
set_finished = Games.set_finished

if __name__ == "__main__":
    if False:  # update players
        remake_table("players", create_player_table)
        add_player(0, "Неизвестный игрок")
    if False:  # update games
        remake_table("games", create_game_table)
        update_constant("game_id", 0)
    if False:  # update questions
        remake_table("questions", create_questions_table)
        for i in range(1, misc.len_cat):
            update_constant("theme_" + str(i), 0)
    if False:  # update consts
        remake_table("consts", create_constants_table)
        add_constant("game_id", 0)
        add_constant("last_update_id", 0)
        for i in range(1, 17):
            add_constant("theme_" + str(i), 0)

    # drop_theme(14)
    '''game = Games.Game(d = Games.get_game(2))
    for i in range(misc.questions_in_game * 2 + 1):
        print(game.turn, Games.get_possibility(game.id, game.pl1))
        game.next_turn()
        Games.write_game(game.id, game.get_dict())
    print(game.turn)'''
    print_table("consts")
    print_table("players")
    # print_table("questions")
    print_table("games")
