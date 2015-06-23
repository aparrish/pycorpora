pycorpora
=========

.. image:: https://travis-ci.org/aparrish/pycorpora.svg?branch=master
    :target: https://travis-ci.org/aparrish/pycorpora

A simple Python interface for Darius Kazemi's `Corpora Project
<https://github.com/dariusk/corpora>`_, "a collection of static corpora
(plural of 'corpus') that are potentially useful in the creation of weird
internet stuff." The ``pycorpora`` interface makes it easy to use data from the
Corpora Project in your program. Here's an example of how it works::

    import pycorpora
    import random

    # print a random flower name
    print random.choice(pycorpora.plants.flowers['flowers'])

    # print a random word coined by Shakespeare
    print random.choice(pycorpora.words.literature.shakespeare_words['words'])

`Allison Parrish <http://www.decontextualize.com/>`_ created the ``pycorpora`` 
interface. Python 3 is not yet supported. The source code for the package is `on GitHub
<https://github.com/aparrish/pycorpora>`_. Contributions are welcome!

Installation
------------

Installation by hand::

    python setup.py install

Installation with pip::

    pip install pycorpora

The package does not include data from the Corpora Project; instead, the data
is downloaded when the package is installed (using either of the methods
above). By default, the "master" branch of the `Corpora Project GitHub
repository <https://github.com/dariusk/corpora>`_ is used as the source for the
data. You can specify an alternative URL to download the data from using the
argument ``--corpora-zip-url`` on the command line with either of the two
methods above::

    python setup.py install --corpora-zip-url=http://example.com/corpora.zip

... or, with ``pip``::

    pip install pycorpora --install-option="--corpora-zip-url=http://example.com/corpora.zip"

(The intention of ``--corpora-zip-url`` is to let you install Corpora Project
data from a particular branch, commit or fork, so that changes to the bleeding
edge of the project don't break your code.)

Update
------

Update Corpora Project data by reinstalling with pip:

    pip install --upgrade --force-reinstall pycorpora

Usage
-----

Getting the data from a particular Corpora Project file is easy. Here's an
example::

    import pycorpora
    crayola_data = pycorpora.colors.crayola
    print crayola_data["colors"][0]["color"] # prints "Almond"

The expression ``pycorpora.colors.crayola`` returns data deserialized from the
JSON file located at ``data/colors/crayola.json`` in the Corpora Project (i.e.,
`this file
<https://github.com/dariusk/corpora/blob/master/data/colors/crayola.json>`_).
You can use this syntax even with more deeply nested subdirectories::

    import pycorpora
    mr_men_little_miss_data = pycorpora.words.literature.mr_men_little_miss
    print mr_men_little_miss_data["little_miss"][-1] # prints "Wise"

You can use ``from pycorpora import ...`` to import a particular Corpora Project
category::

    from pycorpora import governments
    print governments.nsa_projects["codenames"][0] # prints "ARTIFICE"

    from pycorpora import humans
    print humans.occupations["occupations"][0] # prints "accountant"

You can also use square bracket indexing instead of attributes for accessing
subcategories and individual corpora (just in case the Corpora Project ever adds
files with names that aren't valid Python identifiers)::

    import pycorpora
    import random
    fruits = pycorpora.foods["fruits"]
    print random.choice(fruits["fruits"]) # prints "pomelo" maybe

Additionally, ``pycorpora`` supports an API similar to that provided by the `Corpora Project node package <https://www.npmjs.com/package/corpora-project>`_::

    import pycorpora

    # get a list of all categories
    pycorpora.get_categories() # ["animals", "archetypes"...]

    # get a list of subcategories for a particular category
    pycorpora.get_categories("words") # ["literature", "word_clues"...]

    # get a list of all files in a particular category
    pycorpora.get_files("animals") # ["birds_antarctica", "birds_uk", ...]

    # get data deserialized from the JSON data in a particular file
    pycorpora.get_file("animals", "birds_antarctica") # returns dict w/data

    # get file in a subcategory
    pycorpora.get_file("words/literature", "shakespeare_words")

As an extension of this interface, you can also use the ``get_categories``,
``get_files`` and ``get_file`` methods on individual categories::

    import pycorpora

    # get a list of files in the "archetypes" category
    pycorpora.archetypes.get_files() # ['artifact', 'character', 'event', ...]

    # get an individual file from the "archetypes" category
    pycorpora.archetypes.get_file("character") # returns dictionary w/data

    # get subcategories of a category
    pycorpora.words.get_categories() # ['literature', 'word_clues']

Examples
--------

Here are a few quick examples of using data from the Corpora Project to do
weird and fun stuff.

Create a list of whimsically colored flowers::

    from pycorpora import plants, colors
    import random

    random_flowers = random.sample(plants.flowers["flowers"], 10)
    random_colors = random.sample(
        [item['color'] for item in colors.crayola["colors"]], 10)
    for pair in zip(random_colors, random_flowers):
        print " ".join(pair).title()

    # outputs (e.g.):
    #   Maroon Bergamot
    #   Blue Bell Zinnia
    #   Pink Flamingo Camellias
    #   Tickle Me Pink Begonia
    #   Burnt Orange Clover
    #   Fuzzy Wuzzy Hibiscus
    #   Outer Space Forget Me Not
    #   Almond Petunia
    #   Pine Green Ladys Slipper
    #   Shadow Jasmine

Create random biographies::

    from pycorpora import humans, geography
    import random
    
    def a_biography():
        return "{0} is a(n) {1} who lives in {2}.".format(
            random.choice(humans.firstNames["firstNames"]),
            random.choice(humans.occupations["occupations"]),
            random.choice(geography.us_cities["cities"])["city"])
    
    for i in range(5):
        print a_biography()

    # outputs (e.g.):
    #   Jessica is a(n) ceiling tile installer who lives in Grand Forks.
    #   Kayla is a(n) substance abuse social worker who lives in Torrance.
    #   Luis is a(n) hydrologist who lives in Saginaw.
    #   Leah is a(n) heating installer who lives in Danville.
    #   Grant is a(n) building inspector who lives in Vineland.

Automated pizza topping-related boasts about your inebriation::

    from pycorpora import words, foods
    import random

    # "I'm so smashed I could eat a pizza with spinach, cheese, *and* hot sauce."
    print "I'm so {0} I could eat a pizza with {1}, {2}, *and* {3}.".format(
        random.choice(words.states_of_drunkenness["states_of_drunkenness"]),
        *random.sample(foods.pizzaToppings["pizzaToppings"], 3))

The possibilities... are endless.

History
-------

* 0.1.2: Python 3 compatibility (contributed by Sam Raker); vastly improved
  build process (contributed by Hugo van Kemenade).

License
-------

The ``pycorpora`` package is MIT licensed (see LICENSE.txt). The data in the
Corpora Project is itself in the public domain (CC0).

Acknowledgements
----------------

Thanks to Darius Kazemi and all of the Corpora Project contributors!

This package was developed as part of my Spring 2015 research fellowship at
`ITP <http://itp.nyu.edu/>`_. Thank you to the program and its students for
their interest and support!

