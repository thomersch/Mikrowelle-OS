{% for feed in feeds %}<link rel="alternate" type="application/rss+xml" title="{{ feed }} Podcast Feed" href="/{{ feed }}.xml" />
{% endfor %}
<link href="/res/static/podlove-web-player.css" rel="stylesheet" media="screen" type="text/css" />
<script src="/res/libs/html5shiv.js"></script>
<script src="/res/libs/jquery-1.10.1.min.js"></script>
<script src="/res/static/podlove-web-player.js"></script>