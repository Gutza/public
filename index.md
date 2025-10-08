---
layout: default
title: "Bogdan's public essays"
description: "The front page of Bogdan's public essays blog (post index)"
---

# Bogdan's public essays

Various public essays and ad hoc text snippets originally posted on [my blog](https://gutza.github.io/public):
{% for post in site.posts %}- [{{ post.title }}]({{ post.url | relative_url }}) ({{ post.date | date: "%B %-d, %Y" }})
{% endfor %}
