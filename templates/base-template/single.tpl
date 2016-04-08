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
		<div id="backlink"><a href="/">zurück zur Übersicht</a></div>

		{% include 'post.tpl' %}

		{% include 'meta_block.tpl' %}
	</section>

</body>

</html>