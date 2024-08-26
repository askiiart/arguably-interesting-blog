#!/usr/bin/env bash

# Makes RSS feed (feed.xml)
# Currently missing description and pubDate
# Based off https://en.wikipedia.org/wiki/RSS, particularly the example
printf "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<rss version=\"2.0\">\n\n<channel>\n  <title>eng.askiiart.net</title>\n  <description>This is the feed for engl.askiiart.net, I guess</description>\n  <link>https://askiiart.net</link>\n  <lastBuildDate>$(TZ='UTC' date --rfc-2822)</lastBuildDate>" >feed.xml
find . -path ./error -prune -o -name '*.html' -print | while read -r item; do
    # Skip template.html, wishlist.html, resume.html, and portfolio.html
    if [[ ${item} == "./index.html" || ${item} == "./template.html" ]]; then
        continue
    fi
    item="${item%.*}"
    item="${item#./}"
    TITLE=$(grep -m 1 -oP '(?<=^# ).*' ${item}.md | cat)
    printf "\n  <item>\n    <title>${TITLE}</title>\n    <link>https://engl.askiiart.net/${item}.html</link>\n  </item>" >>feed.xml
done
printf "\n\n</channel>\n</rss>" >>feed.xml
