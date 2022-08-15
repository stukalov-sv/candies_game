import random
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler, Filters
from config import TOKEN



def first_turn_tossup() -> bool:
    toss = False
    if (random.randint(1, 9) % 2 == 0):
        toss = True
    return toss


def basic_bot_player() -> int:
    bot_turn = random.randint(1, 28)
    return bot_turn


def mind_bot_player(player_turn: int) -> int:
    bot_turn = 29 - player_turn
    return bot_turn


def p_vs_basic_bot(candies_amount: int, tossup: bool) -> bool:
    winner = False

    while candies_amount > 0:
        while tossup:
            player_turn = player_turn(first_name)
            winner = False
            if player_turn < 29:
                tossup = False
                print(f'{first_name} take: {player_turn}')
                candies_amount -= player_turn
                print(f'Candies left: {candies_amount}')
            else:
                print('Incorrect data')

        if (candies_amount > 0 and not tossup):
            if (candies_amount < 2):
                winner = True
                candies_amount -= candies_amount
            else:
                bot_player = basic_bot_player()
                tossup = True
                print(f'Computer take: {bot_player}')
                candies_amount -= bot_player
                print(f'Candies left: {candies_amount}')
    return winner


def p_vs_mind_bot(candies_amount: int, tossup: bool, first_bot_turn: bool) -> bool:
    winner = False

    while candies_amount > 0:
        while tossup:
            winner = False
            player_turn = player_turn(first_name)
            if player_turn < 29:
                tossup = False
                print(f'{first_name} take: {player_turn}')
                candies_amount -= player_turn
                print(f'Candies left: {candies_amount}')
            else:
                print('Incorrect data')

        if (candies_amount > 0 and not tossup):
            if (first_bot_turn):
                bot_player = 19
                tossup = True
                print(f'Computer take: {bot_player}')
                candies_amount -= bot_player
                print(f'Candies left: {candies_amount}')
                first_bot_turn = False
            elif (candies_amount < 2):
                winner = True
                candies_amount -= candies_amount
            else:
                bot_player = mind_bot_player(player_turn)
                tossup = True
                print(f'Computer take: {bot_player}')
                candies_amount -= bot_player
                print(f'Candies left: {candies_amount}')
    return winner


def help(update, context):
    context.bot.send_message(update.effective_chat.id, '/help - помощь\n'
                                                       '/start - начало игры\n')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'Incorrect command. Try /help')


def start(update, context):
    reply_keyboard = [['Choose game type'], ['/p_vs_p', '/p_vs_easy_bot', '/p_vs_mind_bot'],
                        ['Shut down'], ['/close']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Choose your game", reply_markup=markup_key)


def cl_start(update, _):
    update.message.reply_text('See you later', reply_markup=ReplyKeyboardRemove())


def p_vs_p(update, _):
    update.message.reply_text(
        "Hello! It's Candies game.\nPlayer 1, what's your name?\nOr /cancel to exit game", 
        reply_markup=ReplyKeyboardRemove())
    return FIRST_P


def first_p(update, _):
    global first_name
    first_name = update.message.text
    update.message.reply_text(
        f"OK, {update.message.text}.\nAnd player 2, your name is?\nOr /cancel to exit game")
    return SECOND_P


def second_p(update, _):
    global second_name
    second_name = update.message.text
    update.message.reply_text(
        f"OK, {update.message.text}.\nHow many candies put on the table for your game?\nOr /cancel to exit game")
    return AMOUNT


def amount(update, _):    
    global candies_amount
    candies_amount = None
    if type(int(update.message.text)) == int:
        candies_amount = int(update.message.text)
        update.message.reply_text(
            f"Good. You have {update.message.text} candies on table.\nHow many candies you want to take for one turn?\nOr /cancel to exit game")
        return CAND_TURN
    else:
        update.message.reply_text(
            f"Incorrect data {update.message.text} - not number. Try again /start")
        return ConversationHandler.END


def cand_turn(update, _):
    global candies_turn, first_name, second_name
    candies_turn = None
    if type(int(update.message.text)) == int:
        candies_turn = int(update.message.text)
        turn = first_turn_tossup()
        if turn:
            update.message.reply_text(
                f"Let's go, players. You must take some candies up to {update.message.text} for your turn.\nWho take last candy - lose the game.\nRandom say: '{first_name} turn first'.\nOr /cancel to exit game")
            return EVEN_TURN
        else:
            update.message.reply_text(
                f"Let's go, players. You must take some candies up to {update.message.text} for your turn.\nWho take last candy - lose the game.\nRandom say: '{second_name} turn first'.\nOr /cancel to exit game")
            return ODD_TURN
    else:
        update.message.reply_text(
            f"Incorrect data {update.message.text} - not number. Try again /start")
        return ConversationHandler.END


def even_turn(update, _):
    global candies_amount, candies_turn, first_name, second_name
    if type(int(update.message.text)) == int:
        player_turn = int(update.message.text)
        if player_turn < candies_turn + 1:
            candies_amount -= player_turn
            if candies_amount < 1:
                update.message.reply_text(
                f"{second_name} wins the game. Congratulation! Try again /start")
                return ConversationHandler.END
            else:
                update.message.reply_text(
                f"{first_name} take: {player_turn}. Candies left: {candies_amount}\n{second_name} your turn")
                return ODD_TURN
        else:
            update.message.reply_text(
                f"Incorrect data. Try again /start")
            return ConversationHandler.END
    else:
        update.message.reply_text(
            f"Incorrect data {update.message.text} - not number. Try again /start")
        return ConversationHandler.END


def odd_turn(update, _):
    global candies_amount, candies_turn, second_name
    if type(int(update.message.text)) == int:
        player_turn = int(update.message.text)
        if player_turn < int(candies_turn) + 1:
            candies_amount -= player_turn
            if candies_amount < 1:
                update.message.reply_text(
                f"{first_name} wins the game. Congratulation! Try again /start")
                return ConversationHandler.END
            else:
                update.message.reply_text(
                    f"{second_name} take: {player_turn}. Candies left: {candies_amount}\n{first_name} your turn")
                return EVEN_TURN
        else:
            update.message.reply_text(
                f"Incorrect data. Try again /start")
            return ConversationHandler.END
    else:
        update.message.reply_text(
            f"Incorrect data {update.message.text} - not number. Try again /start")
        return ConversationHandler.END


def cancel(update, _):
    update.message.reply_text('Good luck')
    return ConversationHandler.END


global first_name, second_name, candies_amount, candies_turn

FIRST_P, SECOND_P, AMOUNT, CAND_TURN, EVEN_TURN, ODD_TURN = range(6)
