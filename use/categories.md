---
title: List of categories
layout: page
---

<div id="sitemap" markdown="1">

{% assign site_categories = site.pages | map: "category" | compact | sort | uniq %}

{% for category in site_categories %}{% if category == "YOUR-CATEGORY" %}{% continue %}{% endif %}
- {{ category }}{% for page in site.pages %}{% if page.category == category %}
    - <a href="{{ site.baseurl }}{{ page.url }}">{{ page.title }}</a> {% endif %}{% endfor %}
{% endfor %}

</div>