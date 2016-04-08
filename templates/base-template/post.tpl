<article>
	<h3>{{ post.title }}</h3>

	<audio controls="controls" data-podlove-web-player-source="player_{{post.episode}}.html">
		{% for extension, mime in formats.iteritems() %}
			<source src="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}" type="{{ mime }}"</source>
		{% endfor %}
	</audio>

	{{ post.content }}

	<div class="actions">
		Published on: {{ post.humandate }},
		<a href="{{ post.episode }}.html">Direct Episode Link</a>
		Download:
		{% for extension, mime in formats.iteritems() %}
			<a href="{{ settings.audio_base_url }}{{ post.filename }}.{{ extension }}">{{ mime }}</a>
		{% endfor %}
	</div>
</article>