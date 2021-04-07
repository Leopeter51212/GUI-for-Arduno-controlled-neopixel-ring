// Author: Yiheng Chang     Date: 2021 Mar 1st

#include <Adafruit_NeoPixel.h>

#define LED_PIN     6

#define LED_COUNT   60
#define BRIGHTNESS  50
#define DELAY_TIME  50

#define SHORT_DELAY_TIME 50
#define MEDIUM_DELAY_TIME 100
#define LONG_DELAY_TIME 200

// Build an object of Adafruit_NeoPixel class and named strip
// NEO_RGBW Pixels are wired for RGBW bitstream
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB+NEO_KHZ800);

void setup() {
  Serial.begin(4800);
  Serial.flush();
  strip.begin();                  // Initialize NeoPixel strip object
  strip.show();                   // Initialize all pixels to 'off'
  strip.setBrightness(BRIGHTNESS);// Set the LED BRIGHTNESS to about 1/5 (max = 255)
}

char var;

void loop() {
  // if the port is connected
  while(Serial.available()>0)
  {
    // read the serial port
    var = Serial.read();
    if(var == '0'){
      colorWipe(strip.Color(  255, 255, 255), DELAY_TIME);   // RGB white      
    }
    if(var== '1'){
      colorWipe(strip.Color(  255, 0,   0), DELAY_TIME);         // Red
    }
    if(var=='2'){
      colorWipe(strip.Color(  0,   255,   0), DELAY_TIME);       // Green
    }
    if(var=='3'){
      colorWipe(strip.Color(  0,   0, 255), DELAY_TIME);         // Blue
    }
    if(var=='4'){
      on_off(strip.Color(  255,   255,  255), strip.numPixels() - 1, DELAY_TIME);           // turn all LED on
    }
    if(var=='5'){
      on_off(strip.Color(  0,  0,  0), strip.numPixels() - 1, DELAY_TIME);             // turn all LED off
    }
    if(var=='6'){
      half_on(strip.Color(  255,  255,  255), 0, 8, DELAY_TIME);             // turn left hand side LED on
    }
    if(var=='7'){
      half_on(strip.Color(  255,  255,  255), 8, 15, DELAY_TIME);             // turn right hand side LED on
    }
    if(var=='8'){
      odd_Blink(DELAY_TIME);                   // odd index blink
    }
    if(var=='9'){
      even_Blink(DELAY_TIME);                  // even index blink
    }
    if(var=='a'){
      individual_Blink(strip.Color(  255,   255,   255), LONG_DELAY_TIME);             // individual LED blink
    }
    if(var=='b'){
      individual_On(strip.Color( 255, 255, 255),0);
      Serial.flush();
    }
    if(var=='c'){
      individual_On(strip.Color( 255, 255, 255),1);
      Serial.flush();
    }
    if(var=='d'){
      individual_On(strip.Color( 255, 255, 255),2);
      Serial.flush();
    }
    if(var=='e'){
      individual_On(strip.Color( 255, 255, 255),3);
      Serial.flush();
    }
    if(var=='f'){
      individual_On(strip.Color( 255, 255, 255),4);
      Serial.flush();
    }
    if(var=='g'){
      individual_On(strip.Color( 255, 255, 255),5);
      Serial.flush();
    }
    if(var=='h'){
      individual_On(strip.Color( 255, 255, 255),6);
      Serial.flush();
    }
    if(var=='i'){
      individual_On(strip.Color( 255, 255, 255),7);
      Serial.flush();
    }
    if(var=='j'){
      individual_On(strip.Color( 255, 255, 255),8);
      Serial.flush();
    }
    if(var=='k'){
      individual_On(strip.Color( 255, 255, 255),9);
    }
    if(var=='l'){
      individual_On(strip.Color( 255, 255, 255),10);
    }
    if(var=='m'){
      individual_On(strip.Color( 255, 255, 255),11);
    }
    if(var=='n'){
      individual_On(strip.Color( 255, 255, 255),12);
    }
    if(var=='o'){
      individual_On(strip.Color( 255, 255, 255),13);
    }
    if(var=='p'){
      individual_On(strip.Color( 255, 255, 255),14);
    }
    if(var=='q'){
      individual_On(strip.Color( 255, 255, 255),15);
    }
    if(var=='r'){
      short_loop();
    } 
    if(var=='s'){
      medium_loop();
    }
    if(var=='t'){
      long_loop();
    }
  }
}

// Turn on all the LED in the same color in the index order
void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }  
}

// Turn on or off of all LED
void on_off(uint32_t color,int number, int wait) {
  strip.fill(color, 0, number); //  fill the strip with black or true white
  strip.show();                 //  Update strip to match
  delay(wait);
}

// Turn on half of the LED
void half_on(uint32_t color, int start_index, int end_index, int wait) {
    strip.fill(color, start_index, end_index);
    strip.show();
    delay(wait);
}

// Turn on all the LED with even index in order (in color white)
void odd_Blink(uint8_t wait) {
  for(int i=0; i<strip.numPixels(); i+=2){
    strip.setPixelColor(i,strip.Color(255, 255, 255));
    strip.show();
    delay(DELAY_TIME);
  }
}

// Turn on all the LED with odd index in order (in color white)
void even_Blink(uint8_t wait) {
  for(int i=1; i<strip.numPixels(); i+=2){
    strip.setPixelColor(i,strip.Color(255, 255, 255));
    strip.show();
    delay(DELAY_TIME);
  }
}

// Only one LED blink at one time
void individual_Blink(uint32_t color, uint8_t wait) {
    for(int i=0; i<strip.numPixels(); i++) {
      strip.fill(strip.Color(0, 0, 0, 0));      // Turn all LED on the ring off
      strip.setPixelColor(i, color);            // Set pixel's color(in RAM)
      strip.show();                             // Update strip to match
      delay(wait);                              // Pause for a moment
  }
}

// Only one LED blink at one time
void individual_On(uint32_t color, int index) {
  strip.setPixelColor(index, color);            // Set pixel's color(in RAM)
  strip.show();                             // Update strip to match
}

void short_loop(){
  for(int i=0; i<10; i++){
    half_on(strip.Color(  255, 255, 255), 0, 8, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 8, 15, DELAY_TIME);
    delay(SHORT_DELAY_TIME);
    half_on(strip.Color(  255, 255, 255), 8, 15, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 0, 8, DELAY_TIME); 
  }
}

void medium_loop(){
  for(int i=0; i<10; i++){
    half_on(strip.Color(  255, 255, 255), 0, 8, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 8, 15, DELAY_TIME);
    delay(MEDIUM_DELAY_TIME);
    half_on(strip.Color(  255, 255, 255), 8, 15, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 0, 8, DELAY_TIME); 
  }
}

void long_loop(){
  for(int i=0; i<10; i++){
    half_on(strip.Color(  255, 255, 255), 0, 8, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 8, 15, DELAY_TIME);
    delay(LONG_DELAY_TIME);
    half_on(strip.Color(  255, 255, 255), 8, 15, DELAY_TIME);
    half_on(strip.Color(  0,  0,  0), 0, 8, DELAY_TIME); 
  }
}
