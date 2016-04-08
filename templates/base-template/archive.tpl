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
			Duration: {{ post.humanduration }} h
			<div class="actions">
				Published on: {{ post.humandate }},
				<a href="{{ post.episode }}.html">Direct Episode Link</a>
				Download:
					{% for extension, mime in formats.iteritems() %}
						<a href="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}">{{ mime }}</a>
					{% endfor %}
			</div>
		</article>
		{% endfor %}
	</section>
</body>

</html>
