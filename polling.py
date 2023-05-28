from bot import main_dispatcher, bot, cfg
import sentry_sdk

if __name__ == "__main__":
    sentry_sdk.init(
        dsn=cfg.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )
    main_dispatcher.run_polling(bot)
