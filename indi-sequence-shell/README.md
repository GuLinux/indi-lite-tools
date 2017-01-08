# INDI Sequence Generator

This directory contains a powerful shell sequence generator for INDI.

It's written entirely in bash, with only a few pretty standard system commands as dependecies (plus, of course, INDI itself).

## Installation

Simply clone this repository in any directory.

The best way to have it ready as a command is to add this line in your `$HOME/.bashrc`:

    alias indi-create-sequence="<PATH_WHERE_YOU_CLONED_REPOSITORY>/indi-sequence-shell/indi_helper create-script"

This will add the command alias `indi-create-sequence` available for usage.

## Usage

First you must make sure that you have already started indiserver with the correct drivers. Please refer to INDI documentation for this.

Just type `indi-create-sequence SESSION_NAME` to create a new sequence session.

`SESSION_NAME` can be anything describing the shooting session (a date, the object you are shooting), but please make sure it doesn't contain any space or unusual characted. In doubt, replace them with an underscore.

To start the sequence, just enter the `SESSION_NAME` directory, and run the `./start_sequence` script. Before doing this, anyway, make sure you have a look at the configuration to choose the number of shots and exposures.

## Configuration

Simply open the `settings` file with any text editor.
This is an example settings file:

    DEFAULT_DEVICE="CCD Simulator"
    SESSION_NAME="M42"
    FILTERS="L R G B"
    DARK=AFTER_ALL
    DARK_SEQUENCE=10
    EXPOSURES[L]="1:10 3:10 5:10"
    EXPOSURES[R]="5:5 10:5 15:5"
    EXPOSURES[G]="${EXPOSURES[R]}"
    EXPOSURES[B]="${EXPOSURES[R]}"


 - `DEFAULT_DEVICE`: this the main shooting device that will be used, as reported by `indi_getprop`
 - `SESSION_NAME`: the name of the session (will also be used for file names).
 - `FILTERS`: you can use this to create multiple sequences, useful when you have a filter wheel and you need to take different exposures and number of shots for each one of them. Detailed explanation in the next section. If don't have or don't want to use filters (or if you have a colour camera), put a single value in this configuration entry (for instance, "L").
 - `DARK`: if the value is `AFTER_ALL`, after all sequences are completed all the dark exposures will be taken, with a number of `DARK_SEQUENCE` shots for each different exposure.
 - `EXPOSURES[FILTER_NAME]`: see next section.

The default behaviour of the sequence is to wait for user confirmation after each filter is completed.
If you want a different behaviour, copy the `customizations.sample` file to `customizations`, edit it, and change or implement the desired functions according to the documentation.
For instance, if you have an autofocuser and an automatic filter wheel, you can add manually the commands to operate them, instead of waiting for user input.

As a final option, you can also modify the `start_sequence` shell script itself if you need a greater flexibility.

### Filters and Exposures

As mentioned before, you can create sequences of sequences with different filters.

To obtain this, populate the `FILTERS` variable with a space separated list of filters enclosed in quotes (example: `"L R G B"`).

Now you need to configure the exposures for each filter.
As shown in the example, you do this by assigning values to the `EXPOSURES[FILTER_NAME]` variable.
The value is a space separated list of exposure entries.

Each entry has this format: `exposure_in_seconds:number_of_shots`.

In the above example, for the filter "L" we have 10 exposures of 1 second, 10 exposures of 3 seconds, and 10 of 5 seconds, while for the R, G, and B filters we have 5 exposures of 5 seconds, 5 of 10 seconds, and 5 of 15 seconds.


