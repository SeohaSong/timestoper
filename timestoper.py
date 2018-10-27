import sys
import time
import asyncio
import datetime


async def main(loop):

    def show_time():
        nonlocal is_input, process_alive
        start_time = latest_time = datetime.datetime.now()
        print(' '.join(['(start time)', str(start_time)]))
        while process_alive:
            time.sleep(0.1)
            curr_time = datetime.datetime.now()
            elapsed_time = curr_time-start_time
            if is_input:
                str_ls = ['\r',  ' '*24,
                          '(time interval)', str(curr_time-latest_time)]
                sys.stdout.write(' '.join(str_ls))
                is_input = False
                latest_time = curr_time
            else:
                str_ls = ['\r(elapsed time)', str(elapsed_time)[:9]]
                sys.stdout.write(' '.join(str_ls))                
        print()
    
    def print_time(signal_interval=0.2):
        nonlocal is_input, process_alive
        old_time = -signal_interval
        while process_alive:
            input()
            new_time = time.time()
            if new_time-old_time <= signal_interval:
                process_alive = False
            else:
                is_input = True
                old_time = new_time

    is_input = False
    process_alive = True
    print(' '.join(['(notification)', 'press \'Enter\' to print time']))
    print(' '.join(['(notification)',
                    'press \'Enter\' twice quickly to kill this process']))

    futures = [
        loop.run_in_executor(None, print_time),
        loop.run_in_executor(None, show_time)
    ]
    await asyncio.wait(futures)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()