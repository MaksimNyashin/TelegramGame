__author__ = 'Maks_El_Diablo'
# This Python file uses the following encoding: utf-8
import telegram

import database
import misc


def rate_update(game):
    score1 = sum(list_id for list_id in game.success[::2])
    score2 = sum(list_id for list_id in game.success[1::2])
    pl1_rate = database.get_rate(game.pl1)
    pl2_rate = database.get_rate(game.pl2)
    n_rate_pl1, n_rate_pl2 = pl1_rate, pl2_rate
    if abs(pl2_rate - pl1_rate) < misc.small_delta:
        if score1 == score2:
            n_rate_pl1 += misc.equal_draw
            n_rate_pl2 += misc.equal_draw
        elif score1 > score2:
            n_rate_pl1 += misc.equal_win
            n_rate_pl2 += misc.equal_lose
        else:
            n_rate_pl1 += misc.equal_lose
            n_rate_pl2 += misc.equal_win
    elif pl1_rate > pl2_rate:
        if score1 == score2:
            n_rate_pl1 += misc.bigger_draw
            n_rate_pl2 += misc.smaller_draw
        elif score1 > score2:
            n_rate_pl1 += misc.bigger_win
            n_rate_pl2 += misc.smaller_lose
        else:
            n_rate_pl1 += misc.bigger_lose
            n_rate_pl2 += misc.smaller_win
    else:
        if score1 == score2:
            n_rate_pl1 += misc.smaller_draw
            n_rate_pl2 += misc.bigger_draw
        elif score1 > score2:
            n_rate_pl1 += misc.smaller_win
            n_rate_pl2 += misc.bigger_lose
        else:
            n_rate_pl1 += misc.smaller_lose
            n_rate_pl2 += misc.bigger_win
    if score1 == misc.questions_in_game:
        n_rate_pl1 += 1
    if score2 == misc.questions_in_game:
        n_rate_pl2 += 1
    database.set_rate(game.pl1, n_rate_pl1)
    database.set_rate(game.pl2, n_rate_pl2)


def get_out_text(user_id, s, name):
    database.add_player(user_id, name)
    game_id = database.get_last_game(user_id)
    if game_id == -1:
        # staring new game
        if s == "/new_game":
            res = database.create_game(user_id)
            if not res:
                return misc.too_many_games
            d = [misc.game_created, misc.tgmm]
            return d
        elif s.startswith("/new_game "):
            opp_name = " ".join(i for i in s.split(" ")[1:])
            opp_id = database.get_id(opp_name)
            if opp_id == -1:
                opp_id = database.get_id(opp_name + '\t')
            if opp_id == -1:
                return [misc.no_such_player, misc.tgmm]
            res = database.create_game(user_id, opp_id)
            if not res:
                return misc.too_many_games
            import bot
            bot.send_message(opp_id, misc.you_were_chosen(database.get_name(user_id)))
            d = [misc.game_created, misc.tgmm]
            return d
        # get list of games that are possible to play
        elif s == "/game":
            lst = database.get_games_list(user_id)
            js = [["/game_{} Игра с {}  {}".format(str(i[0]), database.get_name(i[1]), database.Games.get_score(i[0], user_id))] for i in lst[0]]
            z = ["Игра с {}  {}".format(database.get_name(i[1]), database.Games.get_score(i[0], user_id)) for i in lst[1]]
            print("logic.get_out_text.js:", js)
            d = [misc.choose_game(z), telegram.ReplyKeyboardMarkup(js, resize_keyboard=True)]
            return d
        # changing name
        elif s.startswith("/change_name "):
            b = database.change_name(user_id, s[13:])
            if b:
                return misc.success_changed_name + s[13:]
            else:
                return misc.failed_changed_name
        elif s == "/stats":
            d = [database.get_stats(user_id), misc.tgmm]
            return d
    else:
        # choosing theme
        if s.startswith("/theme_"):
            theme_id = s[7:].split(" ")[0]
            try:
                theme_id = int(theme_id)
            except ValueError:
                return ""
            game_id = database.get_last_game(user_id)
            game = database.Games.Game(d=database.Games.get_game(game_id))
            if len(game.questions) // 3 < len(game.themes):
                return misc.early_theme
            sht_id = misc.themes_to_choose * len(game.themes)
            if theme_id not in game.shuffled_themes[sht_id: sht_id + misc.themes_to_choose]:
                return misc.wrong_theme
            game.themes.append(theme_id)
            database.Games.write_game(game_id, d=game.get_dict())
            b = database.get_question(user_id, game_id)
            if b is None:
                return misc.none(database.get_last_game(user_id) == -1)
            js = [[{"text": "А) " + b[3]}, {"text": "Б) " + b[4]}], [{"text": "В) " + b[5]}, {"text": "Г) " + b[6]}]]
            d = [b[2], telegram.ReplyKeyboardMarkup(js)]
            return d
        # selecting answer
        elif s.startswith("А) ") or s.startswith("Б) ") or s.startswith("В) ") or s.startswith("Г) "):
            cut_s = s[3:]
            js = [[misc.next_question]]
            game = database.Games.Game(d=database.Games.get_game(database.get_last_game(user_id)))
            print("logic.starts_with.game.turn:", game.turn)
            q = database.get_question_by_number(game.questions[game.turn // 2])
            ok = q[1]

            print("logic.starts_with.ok&cut_s&turn:", ok, cut_s, game.turn)
            if ok == cut_s:
                d = [misc.right_answer, js]
                game.success[game.turn] = 1
            else:
                d = [misc.wrong_answer(ok), js]
            d[1] = telegram.ReplyKeyboardMarkup(d[1], resize_keyboard=True)
            # it was here
            database.Games.write_game(game.id, game.get_dict())
            return d
    # get question
    if s.startswith("/game_") or s == misc.next_question or s == "й":
        if s.startswith("/game_"):
            try:
                game_id = int(s[6:].split(" ")[0])
            except ValueError:
                return misc.wrong_game_syntax
            if not database.Games.get_possibility(game_id, user_id):
                return misc.wrong_game
        else:
            game_id = database.get_last_game(user_id)
        if game_id == -1:
            return misc.none(game_id == -1)
        game = database.Games.Game(d=database.Games.get_game(game_id))
        # check if game is finished
        if database.get_finished(game_id) == 1:
            d = [""] * 2
            an_pl_id = game.pl1 if game.turn % 2 == 1 else game.pl2
            d[1] = misc.tgmm
            d[0] = misc.game_finished_send(database.get_name(an_pl_id), database.Games.get_score(game_id, user_id))
            return d
        # check if it is time to select theme
        if game.get_next_turn() % (4 * misc.questions_in_block) in [0, 2 * misc.questions_in_block + 1] and game.turn + 2 < misc.questions_in_game * 2:
            tour = game.get_next_turn() // 2 // misc.questions_in_block
            database.update_last_game(user_id, game_id)
            js = [["/theme_{}{} {}".format((game.shuffled_themes[i]) // 10, (game.shuffled_themes[i]) % 10, misc.categories[game.shuffled_themes[i] - 1])] for i in range(tour * misc.themes_to_choose, (tour + 1) * misc.themes_to_choose)]
            d = [misc.choose_theme, telegram.ReplyKeyboardMarkup(js, resize_keyboard=True)]
            database.Games.write_game(game_id, d=game.get_dict())
            return d
        # check if it is time to finish the turn or the game
        if (game.get_next_turn() < game.turn or game.get_next_turn() == misc.questions_in_game * 2) and database.get_last_game(user_id) == game_id:
            d = [""] * 2
            database.update_last_game(user_id, -1)
            # finishing the game
            if game.get_next_turn() == misc.questions_in_game * 2:
                rate_update(game)
                an_pl_id = game.pl1 if game.turn % 2 == 1 else game.pl2
                d[1] = misc.tgmm
                d[0] = misc.game_finished_send(database.get_name(an_pl_id), database.Games.get_score(game_id, user_id))
                database.set_finished(game.id)
                pl_id = game.pl1 if game.turn % 2 == 0 else game.pl2
                import bot
                bot.send_message(chat_id=an_pl_id, text=misc.game_finished_send(database.get_name(pl_id), database.get_score(game.id, an_pl_id)))
            # finishing the turn
            else:

                an_pl_id = game.pl1 if game.turn % 2 == 1 else game.pl2
                pl_id = game.pl1 if game.turn % 2 == 0 else game.pl2
                print("logic.next_question.an_pl_id&pl_id", an_pl_id, pl_id)
                if an_pl_id != -1 and an_pl_id is not None:
                    import bot
                    bot.send_message(chat_id=an_pl_id, text=misc.turn_finished(database.get_name(pl_id)))
                d[0] = misc.turn_finished_yours
                d[1] = misc.tgmm
            return d
        # getting theme
        if game.get_next_turn() % (4 * misc.questions_in_block) in (1, 2 * misc.questions_in_block):
            import bot
            bot.send_message(chat_id=user_id, text=misc.your_theme_is(misc.categories[game.themes[-1] - 1]))

        b = database.get_question(user_id, game_id)
        if b is None:
            return misc.none(database.get_last_game(user_id) == -1)
        js = [[{"text": "А) " + b[3]}, {"text": "Б) " + b[4]}], [{"text": "В) " + b[5]}, {"text": "Г) " + b[6]}]]
        d = [b[2], telegram.ReplyKeyboardMarkup(js)]
        return d
    print("logic.s:", s)
    return misc.none(database.get_last_game(user_id) == -1)


if __name__ == "__main__":
    # get_out_text("/start")
    pass
