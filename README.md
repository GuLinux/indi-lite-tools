# INDI Lite Tools

This project is a collection of simple tools for INDI astrophotography.

Currently it consists of two main projects:

 - [indi-sequence-shell](indi-sequence-shell/): a bash only sequence generator
 - [indi-ccd-preview](indi-ccd-preview/): a web application to preview images, meant to be useed as GUI complementary for indi-sequence-shell.

The typical workflow of this set of applications would be:

 - **start a screen session, or even better, tmux, for each shell**, if you work remotely, to avoid killing the programs when you close your shell. It is recommended to start 3 sessions:
  1. indi server
  2. indi-ccd-preview
  3. indi-sequence-shell
 - start the *indi-ccd-preview* server
 - connect to indi-ccd-preview using your browser, to get an initial focus, choose the right field of view, and to get an initial preview of the correct exposures to use.
 - create the sequence using indi-sequence-shell
 - configure the sequence as described in [indi-sequence-shell README](indi-sequence-shell/README.md)
 - start the sequence
 - for each filter in the sequence, connect to indi-ccd-preview using your browser to refocus, then in the *Misc* tab you can automatically make the sequence continue.

