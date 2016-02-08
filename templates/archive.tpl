<!DOCTYPE html>
<html lang="de">
<head>
	<meta charset="utf-8" />
	<title>{{ settings.web_title }}</title>
	<link rel="stylesheet" href="/style.css" />
	{% include 'head.tpl' %}
</head>

<body>
	<header>
		{{ settings.web_title }}
	</header>

	<section id="maincontent">
		{% include 'meta_block.tpl' %}

		{% for post in posts %}
		<article>
			<h3>{{ post.title }}</h3>
			{{ post.subtitle }}
			Dauer: {{ post.humanduration }} Stunden
			<div class="actions">Veröffentlicht am: {{ post.humandate }}, <a href="{{ post.episode }}.html">Direktlink zur Episode</a>, Download: <a href="{{ settings.audio_base_url }}{{ post.filename }}.mp3">mp3</a>, <a href="{{ settings.audio_base_url }}{{ post.filename }}.opus">opus</a>, <a href="{{ settings.audio_base_url }}{{ post.filename }}.m4a">mp4</a></div>
		</article>
		{% endfor %}
	</section>
</body>

</html>
