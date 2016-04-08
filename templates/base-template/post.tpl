<article>
	<h3>{{ post.title }}</h3>

	<audio controls="controls" data-podlove-web-player-source="player_{{post.episode}}.html" preload="none">
		{% for extension, mime in formats.items() %}
			<source src="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}" type="{{ mime }}"</source>
		{% endfor %}
	</audio>

	{{ post.content }}

	<div class="actions">
		Published on: {{ post.humandate }},
		<a href="{{ post.episode }}.html">Direct Episode Link</a>
		Download:
		{% for extension, mime in formats.items() %}
			<a href="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}">{{ extension }}</a>
		{% endfor %}
	</div>
</article>