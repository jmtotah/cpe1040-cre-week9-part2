menu = [ "hex?", "uint?", "signed int?", "float?", "ascii?"]#Hex was included for a way to view the data



menuIndex = 0
CONVERTING = True



        while( CONVERTING ): #Do all the stuff in this CONVERTING body
            display.clear()
            while( not( button_b.was_pressed())):
                display.scroll(menu[menuIndex])
                if(button_a.was_pressed()):
                    while( not( button_a.was_pressed())):
                        if(0 == menuIndex):
                            #Hex logic
                            value = int("".join(leds),2) #Combine all the bit values and convert to an unsigned integer range:0..(2^32)-1
                            display.scroll("0x{:08x}".format(value),250)

                        elif(1 == menuIndex):
                            #Unsigned int logic
                            value = int("".join(leds),2) #Combine all the bit values and convert to an unsigned integer range:0..(2^32)-1
                            display.scroll(value)

                        elif(2 == menuIndex):
                            #two's complement integer
                            signedLeds = leds.copy()
                            if "1" == leds[31]: #Check to see if the MSB(sign bit) is on
                                for i in range (32): #Walk through the array
                                    #Flip bits
                                    if signedLeds[i] == "0": #Check if the led is a 0
                                        signedLeds[i] = "1" #Make it a 1
                                    else:
                                        signedLeds[i] = "0" #Make it a 0
                                value = -int("".join(signedLeds),2) - 1 #Assign negative range:-1..-(2^31)
                            else:
                                value = int("".join(signedLeds),2) #Assign positive value, range:0..(2^31)

                            display.scroll(value)

                        elif(3 == menuIndex):
                            #Float logic - reference: https://en.wikipedia.org/wiki/Single-precision_floating-point_format
                            sign = (-1)**int(leds[0]) #-1 raised to power of bit 31 e.g. -1**1 = -1 OR -1**0 = 1
                            exponent = int("".join(leds[1:9]),2) #Combining bit values 30 - 23 and converting to an int
                            mantissa = int("".join(leds[9:]),2) #Combining bit values 22 - 0 and converting to an int
                            if (255 == exponent) and (0 != mantissa): #Check for all bits on in exponent AND mantissa not = 0
                                value = "nan"
                            elif (255 == exponent) and (0 == mantissa): #Check for all bits on in exponent AND mantissa = 0
                                value = "+ infinity" if 0 < sign else "- infinity" #For sign > 0, value = - infinity.For sign < 0, value = infinity
                            else:
                                if 0 == exponent: #Check for all bits off in exponent === 0 - special denormalized case
                                    exponent = 2**(int("".join(leds[1:9]),2)-126) #2 raised to the power of the int of (leds 30 through 23) - 126
                                    mantissa = 0.0 #Invisible leading bit in mantissa does not apply
                                else: # not denormalized - "normal" case
                                    exponent = 2**(int("".join(leds[1:9]),2)-127) #2 raised to the power of the int of (leds 30 through 23) - 127
                                    mantissa = 1.0 #Invisible leading bit in mantissa does apply
                                power = -1 #No magic numbers
                                for led in (leds[9:]): #Working with the bits in the mantissa
                                    if "1" == led: #Check which bits in the mantissa are on
                                        mantissa = 2**power + mantissa #Add the on bits
                                    power = power - 1 #Each index in the mantissa has it's own power, going down by 1
                                value = sign*exponent*mantissa #Combine the sign,exponent and mantissa

                            display.scroll(value)


                        elif(4 == menuIndex):
                            #Ascii logic
                            asciiValue = value&0xff
                            asciiValue += ((value>>8)&0xff)
                            asciiValue += ((value>>16)&0xff)
                            asciiValue += ((value>>24)&0xff)
                            display.scroll(asciiValue)

            sleep(LongPress)
            if button_b.is_pressed(): #If true, break out of CONVERTING loop and go to INPUTTING screen
                screen = INPUTTING
                break

            menuIndex = (menuIndex + 1) % len(menu) #Walking through the menu options

