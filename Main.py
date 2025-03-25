import traceback
from datetime import datetime
import time

import asyncio

from auth import auth_utilities
from f1 import nextGP, raceResults
from music import postRecommendation
from weather import postForecast
from utilities import Printer,TelegramService

def main():
    """
    Función principal del programa que en función del día y la hora ejecuta el resto de scripts.
    """
    Printer.print_title_message(f"BOT INITIALISED AT {datetime.now()}")

    client = auth_utilities.authenticate_to_twitter()

    try:
        while True:
            now = datetime.now()

            if now.hour == 7 and now.minute == 0:
                postForecast.main(client)

            elif now.hour == 9 and now.minute == 30:
                nextGP.main(client)

            elif now.hour == 14 and now.minute == 0:
                postRecommendation.main(client)

            elif now.weekday() == 6 and now.hour == 18 and now.minute == 0:
                raceResults.main(client)

            time.sleep(30)

    except Exception as ex:
        Printer.print_message("ERROR", str(ex), "red")
        asyncio.run(TelegramService.send_error_message(f"ERROR {str(ex)}"))
        traceback.print_exc()


if __name__ == '__main__':
    main()
