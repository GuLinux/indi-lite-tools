# Customizations file template for Raspberry Pi

This example will manipulate the leds to notify user of current status.

In particular, it will:

 - Continuously blink the yellow led if waiting for user confirmation to continue the sequence.
 - Turn off the yellow led while shooting, and blink the red led
 - Turn on again the red led when shooting is finished

## Installation

Install the udev rules to allow members of the `users` group full control of leds

    cp 98-leds.rules /etc/udev/rules.d/

Add yourself to the `users` group

    sudo gpasswd -a $USER users

Reboot.
When creating a new sequence, now simply copy the `customizations` file in the sequence directory. This will be automatically imported.

