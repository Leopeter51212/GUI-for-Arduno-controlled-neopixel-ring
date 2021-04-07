# GUI

This is the GUI of the NeoPixel ring controlled by Arduino. This GUI can be used for commercial NeoPixel ring or any self-designed ring compatible with NeoPixel Arduino library. Please upload the Arduino code to the Arduino first, then open main.py file in a python project. The GUI provide various display modes for the LED ring. Once the serial connection between the PC and Arduino is configured, all display functions can be selected.

## GUI structure
### Arduino Configuration
"Auto Scan" 
It will scan the ports used by Arduino. The port rate can be selected in the combo box, and the port rate must be the same as the port rate declared in the Arduino code.

"Open the Port" 
It will open the port according to the selected port number and port rate. 
The port rate for the serial communication is 4800, you can always change that in the Arduino program and python main code. Although if the port rate is set too high, the arbitrary display mode will execute incorrectly.
In Arduino code set up part:
```
Serial.begin(4800);
```

In python main.py line 126:
```
if port_rate != 4800:
```

"Close the Port" 
It will close the port and exit the program.

### Display mode
#### **Default Display Mode**
"Color Wipe" 
Each LED on the ring will light up in the selected color and remain lit.

"All LED on" 
All LED will light up in white.

"All LED Off" 
All LED will turn off.

"Left LED on" 
Left part of the LED ring will light up in white.

"Right LED on" 
Right part of the LED ring will light up in white.

If you have different number of LED on your ring, please change the corresponding index in Arduino code: 
```
half_on(strip.Color(  0,  0,  0,  255), 0, 8, DELAY_TIME);             // turn left hand side LED on
half_on(strip.Color(  0,  0,  0,  255), 8, 15, DELAY_TIME);             // turn right hand side LED on
```
For example, the commerical LED ring used in this project has 16 LEDs. Left is index 0-8, and right is index 8-15.

"Odd index LED blink" 
Odd index of the LED ring will light up in white and remain lit.

"Even index LED blink" 
Even index of the LED ring will light up in white and remain lit.

"Individual Blink" 
Each LED on the ring will light up by the index order.

#### **Loop Display Mode**
"Short loop time" 
The left and right parts of the LED ring will turn on in sequence with a short time interval (50 milliseconds).

"Medium loop time" 
The left and right parts of the LED ring will turn on in sequence with a medium time interval (100 milliseconds).

"Long loop time" 
The left and right parts of the LED ring will turn on in sequence with a long time interval (200 milliseconds).

The loop time can be change in Arduino code global variables declare part:
```
#define SHORT_DELAY_TIME 50
#define MEDIUM_DELAY_TIME 100
#define LONG_DELAY_TIME 200
```

#### **Arbitrary Display Mode**
"Apply" 
The LED with the corresponding check box selected will light up.

"Reset"
All LED will be off and all check boxes will be set to unchecked state.

#### **Change brightness**
If you want to change the brightness of the LED rings, please change it in the Arduino code global variables declare part:
```
#define BRIGHTNESS  50
```

# Author
- ## Yiheng Chang
University of Nottingham, Electronic and Computing Engineering student

**Socials**: [Github](http://www.github.com/Leopeter51212) 

**Contact information**:Email: slyyc7@gmail.com