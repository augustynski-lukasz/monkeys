import os
import sys
import time
import random
import threading

keyboard_letters='abcdefghijklmnopqrstuvwxyz 1234567890'

monkey_timeout_max=0.5
monkeys_number = 500

aimed_text='abc'

done_event = threading.Event()

random.seed()

class TypingMonkey:
    monkey_name=0

    def __init__(self):
        TypingMonkey.monkey_name += 1
        self.monkey_name = TypingMonkey.monkey_name

    def get_name(self):
        return self.monkey_name

    def get_next_value(self):
        time.sleep(random.uniform(0,monkey_timeout_max))
        return random.choice(keyboard_letters)


class TypingMonkeyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.monkey = TypingMonkey()
        self.name = self.monkey.get_name()
        self.exit_flag = False
        self.hit_position = 0

    def hit(self):
        #print("Monkey %s hit at position %d!" % (self.name, self.hit_position))
        self.hit_position +=1
        if self.hit_position == len(aimed_text):
            print("Monkey %s typed whole text!" % (self.name))
            self.exit_flag = True
            done_event.set()
    
    def no_hit(self, val):
        self.hit_position = 0
        if check(val):
            self.hit()
                    
    def check(self, val):
        return aimed_text[self.hit_position] == val
        
    def run(self):
        #print("Starting monkey %s" % self.name)
        while True:
            if self.exit_flag:
                break
            val = self.monkey.get_next_value()

            if check(val):
                self.hit()
            else:
                self.no_hit(val)
                
            #print("Monkey %s typed %s " % (self.name, val))

        #print("Exiting monkey %s" % self.name)

def main():
    print("Starting %d monkeys " % monkeys_number)
    start_time = time.time()

    monkey_threads = []
    for i in range(0,monkeys_number):
        monkey_thread = TypingMonkeyThread()
        monkey_thread.start()
        monkey_threads.append(monkey_thread)

    monkey_typed_aimed_text = done_event.wait()
    print('One monkey has typed desired text: ', aimed_text)
    end_time = time.time()

    print("Time elapsed %s" % (end_time - start_time ))
    print("Stoping %d monkeys " % monkeys_number)

    for t in monkey_threads:
        t.exit_flag = True

    # Wait for all threads to complete
    for t in monkey_threads:
        t.join()


    print("Exiting Main Thread")

if __name__ == "__main__":
    main()
