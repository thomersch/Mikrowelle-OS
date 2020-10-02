# Mikrowelle OS [![Build Status](https://secure.travis-ci.org/thomersch/Mikrowelle-OS.png)](http://travis-ci.org/thomersch/Mikrowelle-OS)

Mikrowelle OS is a static page generator for podcast websites and feeds.
You will enjoy by visiting the website.

Tested on Python 2.7, 3.3, 3.4 and PyPy 2.5. Will not work under Python 2.6, please update in this case. If possible, prefer Python 3.

## Feature List

* Generating podcast feeds
	* iTunes compatible
	* Payment tag (Flattr)
	* with TTL-support (reduces traffic by setting a sane default interval for feed-refreshing in podcast clients)
* Full text search in the browser
* Flattr support
	* New item for every episode, no manual generation needed.
* Modern player
	* Podlove Web Player included
	* Chapter mark support
* Auphonic support
* Podlove Simple Chapters
* Suitable for heavy load situations
	* no CGI/PHP/runtime bloat

## What does "static page generator" mean?

You won't need a special webserver to serve the application. You can simply throw in all podcast data into this application and it will generate all necessary files. Those files can be uploaded to any hosting without any need for CGI, PHP or so.

## Is it working?

Yep, we are using it actively in our podcast: [Mikrowelle](http://mikrowelle.me/). Though, there may be some issues. If you need assistance, feel free to contact me ([Twitter](http://twitter.com/thomersch)) or create an issue.

## Dependencies

* Python
	* lxml (for feed generation)
	* jinja2 (templating engine)
	* markdown (easy markdown language)
* JavaScript _(those are already included in the repository)_
	* jQuery
	* Podlove Web Player

## Installation Instructions

* Clone git repository.
	* `git clone https://github.com/thomersch/Mikrowelle-OS.git`
* Install Python dependencies.
	* on Debian based systems: `sudo apt-get install python3-lxml`
	* `pip install -r requirements.txt`
* Customize your podcast settings.
	* Rename `settings.default.json` to `settings.json` and change the values the way you need it.
* For the best expierence, use Auphonic. For instructions see section *"Working with Auphonic"*.
* Run `mikrowelle.py`.
* Publish the `audio` folder and the `pub` folder on the interwebz.


## Working with [Auphonic](http://auphonic.com/)

Auphonic is a fully automatic audio post-production service, that converts all your podcast data into well sounding audio files.

This application is build for best use with Auphonic: All meta tags should be put into the webinterface of Auphonic. Description is automatically converted with markdown as well as the summary. Put into the "track" file the number of the podcast episode.

As output files you should select all of the desired audio data types. Plus you must add the "Production description" as json file.

You may as well add chapter marks, they will be automatically processed and put into the web player.

The output of auphonic has to be put where the settings.json `filefolder` is configured. The generator will automatically pick up the right files and do the rest.

## Working without Auphonic

You can run _Mikrowelle OS_ without Auphonic as well. In order to do that, you will need to create a json file per episode and put it into your `posts` folder.

The file name doesn't really matter, but your episode order will depend on it.

### Example: Post file

	{
		"chapters": [
		    {
		        "image": null,
		        "start": "00:22:46.190",
		        "title": "Chapter 1",
		        "url": "http://example.com/1/"
		    },
		    {
		        "image": null,
		        "start": "01:21:33.010",
		        "title": "Chapter 2",
		        "url": "http://example.com/2/"
		    },
		    {
		        "image": null,
		        "start": "01:17:00.130",
		        "title": "Chapter 3",
		        "url": "http://example.com/3/"
		    }
		],
		"content": "<p>Summary</p>",
		"date": "2013-06-09T22:55:48.500Z",
		"duration": "01:35:29.914",
		"episode": "001",
		"filename": "001",
		"humandate": "09.06.2013",
		"subtitle": "<p>It is just the beginning.</p>",
		"title": "001 Title"
	}

## Templating
### Changing the looks of your podcast page.

If you want to start a new style, I recommend to duplicate the `templates/base-template` folder and start editing in the duplicate. Remember to change the `tplfolder` path in `settings.json`.

Adding a stylesheet is nice as well, give it a try. The directory `res` in the template path will be linked in the pub-path, so you can place all your assets in `$templatename/res` and those will be available at `res` on your main publishing path, e.g. `podcast.example.com/res`.

## Feature requests

Give 'em to me. Create a GitHub issue or contact me.

## Other Questions?

Ask me.

## License

BSD License. No bullshit. See `LICENSE` file.

## Contributors

* Thomas Skowron
* Thomas Sänger (HorayNarea)
* Andreas Hubel (saerdnaer)
