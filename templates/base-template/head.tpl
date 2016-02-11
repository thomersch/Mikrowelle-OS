{% for feed in feeds %}<link rel="alternate" type="application/rss+xml" title="{{ feed }} Podcast Feed" href="/{{ feed }}.xml" />
{% endfor %}
<script src="/res/pwp/js/vendor/jquery.min.js"></script>
<script src="/res/pwp/js/podlove-web-moderator.min.js"></script>
<script>
	$(function() {
		$('audio').podlovewebplayer();
	})
</script>
