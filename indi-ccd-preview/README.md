# INDI CCD Preview - Simple preview webapp for INDI

## Dependencies

indi-ccd-preview is written in python (server side), and javascript.
It requires a modern html5 browser supporting Server Side Events. Internet Explorer/Microsoft Edge are not supported.
It is based on bootstrap and jquery, so it's also mobile ready.

The Server application requires the following python modules:

 - flask
 - scipy
 - numpy
 - astropy

In ubuntu/debian, you can install them with the following command:

    sudo apt-get install python3-flask python3-scipy python3-numpy python3-astropy

You can also use pip:

    pip3 install flask scipy numpy astropy

You can remove the '3' from python3 and pip3 to use python2 (not recommended).

## Usage

Just run the indi-ccd-preview.py script directly from this directory:

    ./indi-ccd-preview.py

If you wish to change the python version executable, just prepend it to the python main module:

    python2 ./indi-ccd-preview.py

## Options

Run `./indi-ccd-preview.py --help` to see a list of supported options.

A few interesting examples:

 - `--host <HOSTNAME>`: binds the application to the specified ip address (use 0.0.0.0 to accept connection from every network).
 - `--port <PORT>`: binds the application to the specified port (default: 5000).
 - `--debug`: runs the application in debug mode.

