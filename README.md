# radar

This is a web app written in python and flask, intended to implement check-ins as described by the RADAR framework created by the [Multiamory](https://www.multiamory.com/radar) podcast.

## RADAR check-in format

A radar check-in consists of 5 parts:
* Review
* Agree to Agenda
* Discuss
* Action Points
* Reconnect

The app flow ideally *should* gently guide you through this process.

The primary advantage of having this in app form are that:

1. You can look at old check-ins to see what was discussed
2. You can pre-populate the things from the last check-in that need review in step one
3. You can keep track of action points more easily
4. It's easy to keep track of items that are usually on your agenda
