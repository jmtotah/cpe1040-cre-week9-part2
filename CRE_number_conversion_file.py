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
                            #Float logic
                            display.scroll("float conversion")


                        elif(4 == menuIndex):
                            #Ascii logic
                            value = int("".join(leds),2)
                            asciiValue = value&0xff
                            asciiValue += ((value>>8)&0xff)
                            asciiValue += ((value>>16)&0xff)
                            asciiValue += ((value>>24)&0xff)
                            display.scroll(asciiValue)

            sleep(LongPress)
            if button_b.is_pressed(): #If true, break out of CONVERTING loop and go to INPUTTING screen
                screen = INPUTTING
                break
