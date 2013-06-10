<article>
	<h3>{{ post.title }}</h3>

	<audio id="audio_{{post.episode}}">
		<source src="{{settings.audio_base_url}}{{post.filename}}.mp3" type="audio/mpeg"></source>
		<source src="{{settings.audio_base_url}}{{post.filename}}.m4a" type="audio/mp4"></source>
		<source src="{{settings.audio_base_url}}{{post.filename}}.opus" type="audio/ogg; codecs=opus"></source>
	</audio>

	{{ post.content }}

	<div class="actions">Veröffentlicht am: {{ post.humandate }}, <a href="{{ post.episode }}.html">Direktlink zur Episode</a>, Download: <a href="{{ settings.audio_base_url }}{{ post.filename }}.mp3">mp3</a>, <a href="{{ settings.audio_base_url }}{{ post.filename }}.opus">opus</a>, <a href="{{ settings.audio_base_url }}{{ post.filename }}.m4a">mp4</a></div>

	<script>
		$('#audio_{{post.episode}}').podlovewebplayer({
			title: '{{post.title}}',
			subtitle: '{{post.subtitle}}',
			poster: '{{settings.artwork_url}}',
			chapters: [ {% for chapter in post.chapters %} {"start":"{{chapter.start}}", "title": "{{chapter.title}}"}, {% endfor %} ],
			chaptersVisible: true
		});
	</script>
</article>