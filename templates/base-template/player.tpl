<!DOCTYPE html>
<html>
<head>
	<link href="/res/pwp/css/pwp-dark-green.css" rel="stylesheet" media="screen" type="text/css" />
</head>
<body>
	<audio preload="none">
		{% for extension, mime in formats.items() %}
			<source src="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}" type="{{ mime }}"</source>
		{% endfor %}
	</audio>

	<script src="/res/pwp/js/vendor/jquery.min.js"></script>
	<script src="/res/pwp/js/podlove-web-player.min.js"></script>
	<script type="text/javascript">
		$('audio').podlovewebplayer({
			show: {
				title: '{{ settings.web_title|e }}',
				url: '{{ settings.baseurl }}'
			},
			title: '{{ post.title|e }}',
			subtitle: '{{ post.subtitle }}',
			poster: '{{ settings.artwork_url }}',
			permalink: '{{ post.episode }}',
			chapters: [ {% for chapter in post.chapters %} {"start":"{{chapter.start}}", "title": "{{chapter.title}}"}, {% endfor %} ]
		});
	</script>
</body>
</html>