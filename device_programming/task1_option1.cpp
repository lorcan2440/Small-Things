#include "mbed.h"

Serial pc(SERIAL_TX, SERIAL_RX);

DigitalOut led1(LED1);  // green
DigitalOut led2(LED2);  // blue
DigitalOut led3(LED3);  // red

Timeout button_debounce_timeout;
float debounce_time_interval = 0.3;

InterruptIn button(USER_BUTTON);

Ticker cycle_ticker;
int pressed;
float cycle_time_interval = 1.0;

const int num_inputs = 5;
int entered = 0;
int playback = 0;
int inputs[num_inputs];
char *input_colours[num_inputs];

void onButtonStopDebouncing(void);

char *getColourFromLed(int ledNum)
{
    switch (ledNum) {
        case 1: return "green";
        case 2: return "blue";
        case 3: return "red";
        default: return "";
    }
}

void onButtonPress(void)
{

    if (led1) {pressed = 1;}
    else if (led2) {pressed = 2;}
    else if (led3) {pressed = 3;}
        
    inputs[entered] = pressed;
    entered++;
        
    button.rise(NULL);
    button_debounce_timeout.attach(onButtonStopDebouncing, debounce_time_interval);
}

void lightUpLed(int ledNum)
{
    switch (ledNum) {
        case 1: led1 = true; led2 = false; led3 = false; break;
        case 2: led1 = false; led2 = true; led3 = false; break;
        case 3: led1 = false; led2 = false; led3 = true; break;
    }
}

void onPlayback(void)
{
    lightUpLed(inputs[playback]);
    playback++;
}

void onButtonStopDebouncing(void)
{
    button.rise(onButtonPress);
}

void onCycleTicker(void) 
{
    if (led1) {led1 = false; led2 = true; led3 = false; return;}
    else if (led2) {led1 = false; led2 = false; led3 = true; return;}
    else if (led3) {led1 = true; led2 = false; led3 = false; return;}
    else {led1 = true; led2 = false; led3 = false; return;}
}

int main()
{
    pc.baud(9600);

    led1 = false;
    led2 = false;
    led3 = false;
        
    // when the button is pressed, call onButtonPress (inverts led1, disconnects function to prevent
    // triggering during bouncing and waits)
    button.rise(onButtonPress);

    // every 1 second, call onCycleTicker (move to next LED)
    cycle_ticker.attach(onCycleTicker, cycle_time_interval);

    pc.printf("Started, press %d buttons...\n", num_inputs);

    while (true) {
        if (entered == num_inputs)
        {
            pc.printf("Inputs finished. Playing back sequence: ");
            for (int i = 0; i < num_inputs; i++) {
                input_colours[i] = getColourFromLed(inputs[i]);
                if (i == num_inputs - 1) {
                    pc.printf(input_colours[i]); pc.printf(".\n");
                } else {
                    pc.printf(input_colours[i]); pc.printf(" -> ");
                }
            }
            entered = 0;
            playback = 0;
            cycle_ticker.attach(onPlayback, cycle_time_interval);
            button.rise(NULL);
        }
        
        if (playback == num_inputs)
        {
            pc.printf("Playback finished. Awaiting inputs...\n");
            entered = 0;
            playback = 0;
            cycle_ticker.attach(onCycleTicker, cycle_time_interval);
            button.rise(onButtonPress);
        }

        wait(cycle_time_interval);
    }
}