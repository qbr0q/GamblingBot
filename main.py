from service import init_app, create_bot


def main():
    init_app(bot)
    bot.infinity_polling()


if __name__ == "__main__":
    bot = create_bot()
    main()
