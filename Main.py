import asyncio
import traceback
from datetime import datetime

from auth import auth_utilities
from f1 import nextGP, raceResults
from music import postRecommendation
from weather import postForecast
from utilities import Printer,TelegramService

async def main():
    """
    Función principal del programa que en función del día y la hora ejecuta el resto de scripts.
    """
    Printer.print_title_message(f"BOT INITIALISED AT {datetime.now()}")

    client = auth_utilities.authenticate_to_twitter()

    try:
        while True:
            now = datetime.now()

            if now.hour == 18 and now.minute == 46:
                await postForecast.main()

            elif now.hour == 9 and now.minute == 30:
                await nextGP.main(client)

            elif now.hour == 14 and now.minute == 0:
                await postRecommendation.main(client)

            elif now.weekday() == 6 and now.hour == 18 and now.minute == 0:
                await raceResults.main(client)

            #mentions.main(client)

            await asyncio.sleep(60)

    except Exception as ex:
        Printer.print_message("ERROR", str(ex), "red")
        await TelegramService.send_error_message(f"ERROR {str(ex)}")
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
