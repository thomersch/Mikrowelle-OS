<!DOCTYPE html>
<html>
<head>
	<link href="/res/pwp/css/pwp-dark-green.css" rel="stylesheet" media="screen" type="text/css" />
</head>
<body>
	<audio>
		<source src="{{settings.audio_base_url}}{{post.filename}}.mp3" type="audio/mpeg"></source>
	</audio>

	<script src="/res/pwp/js/vendor/jquery.min.js"></script>
	<script src="/res/pwp/js/podlove-web-player.js"></script>
	<script type="text/javascript">
		$('audio').podlovewebplayer({
			title: '{{post.title|e}}',
			subtitle: '{{post.subtitle|e}}',
			poster: '{{settings.artwork_url}}',
			chapters: [ {% for chapter in post.chapters %} {"start":"{{chapter.start}}", "title": "{{chapter.title}}"}, {% endfor %} ]
		});
	</script>
</body>
</html>