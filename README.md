# Mikrowelle OS

Mikrowelle OS is a static page generator for podcast websites and feeds. Tested on Python 2.7.

## What does "static page generator" mean?

You won't need a special webserver to serve the application. You can simply throw in all podcast data into this application and it will generate all necessary files. Those files can be uploaded to any hosting without any need for CGI, PHP or so.

## Is it working?

Yep, where are using it actively in our podcast: [Mikrowelle](http://mikrowelle.me/). Though, there may be some issues. If you need assistance, feel free to contact me ([Twitter](http://twitter.com/thomersch), [ADN](http://alpha.app.net/thomersch/)).


## Dependencies

* Python
	* lxml (for feed generation)
	* jinja2 (templating engine)
	* markdown (easy markdown language)
* JavaScript _(those are already included in the repository)_
	* jQuery
	* Podlove Web Player


## Installation Instructions

* Install Python dependencies.
	* `sudo pip install lxml jinja2 markdown`
* Clone git repository.
	* `git clone https://github.com/thomersch/Mikrowelle-OS.git`
* Customize your podcast settings.
	* Go to `settings.json` and change the values the way you need it.
* For the best expierence, use Auphonic. For instructions see section *"Working with Auphonic"*.
* Run `webgen.py`.
* Publish the `audio` folder and the `pub` folder on the interwebz.


## Working with [Auphonic](http://auphonic.com/)

Auphonic is a fully automatic audio post-production service, that converts all your podcast data into well sounding audio files.

This application is build for best use with Auphonic: All meta tags should be put into the webinterface of Auphonic. Description is automatically converted with markdown as well as the summary. Put into the "track" file the number of the podcast episode.

As output files you should select all of the desired audio data types. Plus you must add the "Production description" as json file.

You may as well add chapter marks, they will be automatically processed in put into the web player.

The output of auphonic has to be put where the settings.json `filefolder` is configured. The generator will automatically pick up the right files and do the rest.

## My website is ugly!

You can customize your templates at any time. Simply go to the template folder and edit the files. Variables should be rather self explainatory.

Adding a stylesheet is nice as well, give it a try.

## Other Questions?

Ask me. If you're nice to me, I will answer you.

## License

BSD License. No bullshit. See `LICENSE` file.