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
		{% include 'post.tpl' %}
		{% endfor %}

		{% if prev == 0 %}
		<div id="new_episodes">
			<a href="/index.html">newer episodes</a>
		</div>
		{% elif prev and prev > 0 %}
		<div id="new_episodes">
			<a href="/index.{{ prev }}.html">newer episodes</a>
		</div>
		{% endif %}
		{% if next %}
		<div id="prev_episodes">
			<a href="/index.{{ next }}.html">older episodes</a>
		</div>
		{% endif %}
	</section>
</body>

</html>
