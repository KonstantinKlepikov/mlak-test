"""
Напишите программу, которая создает два потока
и выводит сообщения из них параллельно.
"""
import threading


def message(text: str) -> None:
    print(text)


def make_message_wrom_threas() -> None:
    """Make two treads and get messages from both
    """
    threads = [
        threading.Thread(target=message, args=['In thread one!', ]),
        threading.Thread(target=message, args=['In thread two!', ]),
            ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':

    make_message_wrom_threas()
