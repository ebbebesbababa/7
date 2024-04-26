import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

dac    = [8, 11, 7,  1,  0,  5, 12, 6]
leds   = [2,  3, 4, 17, 27, 22, 10, 9]
troyka = 13
comp   = 14


GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = True)

def adc():
    result = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        result[i] = 1
        GPIO.output(dac, result)
        time.sleep(0.01)
        if (GPIO.input(comp)):
            result[i] = 0
    
    num_result = 0 
    for i in range(8):
        num_result += result[i] * 2**(7-i)
    return num_result

def DecToBin(dec_num):
    bin_num = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(8):
        bin_num[7-i] = dec_num % 2
        dec_num = dec_num // 2
    return bin_num

def TroykaVolt():
    return adc()
            
try:
    begin = time.time()
    counter = 0
    with open('data.txt', 'w') as f:
        volt = 0
        while(volt < 210):
            volt = TroykaVolt()
            f.write(str(volt) + '\n')
            counter += 1            
        GPIO.output(troyka, False)
        while(volt > 178):
            volt = TroykaVolt()
            f.write(str(volt) + '\n')
            counter += 1

        
except KeyboardInterrupt:
    print("The program was stopped")
finally:
    duration = time.time()-begin
    print(duration)
    print(duration/counter)
    print(counter/duration)
    print(3.3/256)
    
    with open('settings.txt', 'w') as f:
        f.write(str(counter/duration) + '\n')
        f.write(str(3.3/256))
    GPIO.output(leds, False)
    GPIO.cleanup()
    
    

