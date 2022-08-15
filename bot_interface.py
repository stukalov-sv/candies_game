from bot_comands import *
def start_button():
    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    cl_start_handler = CommandHandler('close', cl_start)

    conv_handler_login = ConversationHandler(
        entry_points=[CommandHandler('p_vs_p', p_vs_p)],
        states={
            FIRST_P: [MessageHandler(Filters.text & ~Filters.command, first_p)],
            SECOND_P: [MessageHandler(Filters.text & ~Filters.command, second_p)],
            AMOUNT: [MessageHandler(Filters.text & ~Filters.command, amount)],
            CAND_TURN: [MessageHandler(Filters.text & ~Filters.command, cand_turn)],
            EVEN_TURN: [MessageHandler(Filters.text & ~Filters.command, even_turn)],
            ODD_TURN: [MessageHandler(Filters.text & ~Filters.command, odd_turn)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # message_handler = MessageHandler(Filters.text, message)
    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(cl_start_handler)

    dispatcher.add_handler(conv_handler_login)


    # dispatcher.add_handler(message_handler)
    dispatcher.add_handler(unknown_handler)


    print('server started')
    updater.start_polling()
    updater.idle()
