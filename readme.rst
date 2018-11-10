Overview
========
This software consists of a number of python modules that can be used to analyse historic football results and betting history and predict key futures matches to bet on.

Usage
=====
...

Requirements
------------
Python 3.7+
shimbase 1.0.6+

Database - database directory
=============================
...

The Sweeper application interacts with the 'shimbase' abstraced db via 'shimbase' generated database objects. The underlying db is currently a SQLite3 db.

Config Files - config directory
===============================
The following config file is a template for the sweeper.ini file that is required by sweeper to email results to interested parties and provide algo configuration. It contains mail addresses and algo config parameters.


::

    example.sweeper.ini


Modify the mail parameters to specify an appropriate mail sever and distribution list and save the result as 'sweeper.ini' under the config directory. Modify the algo parameters to specify which leagues you wish to run the algos over and what marks to use for prediction, also allows for configuration of the number of seasons to be included in analysis.

Source Modules - src directory
==============================
...
