# Lockr

Lockr is a toy project started as an experiment with [crossbar](http://crossbar.io/), [python](https://www.python.org/) and [angular](https://angularjs.org/).

It implements the concept of mutex (sort of) for an IRL resource.

Users can lock/unlock the resource through an angular front-end.
A python back-end manages the resource.

## Running it

Install crossbar the way you want (system package, virtualenv...) and run the router:

    crossbar start

### Back-end

You'll need autobahn for python 3:
    
    pip install autobahn

Then run server:
    
    ./server.py

### Front-end

Install required components (from web directory):

    bower install

Open your browser at http://localhost:8080

## Licence

WTFPL
