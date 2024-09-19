#!/usr/bin/env bash

# Based on this: https://www.lostsaloon.com/technology/how-to-create-an-xml-sitemap-using-wget-and-shell-script/
# (https://web.archive.org/web/20231202193251/https://www.lostsaloon.com/technology/how-to-create-an-xml-sitemap-using-wget-and-shell-script/) (https://archive.ph/qtdMP)
sitedomain=https://engl.askiiart.net
dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
header='<?xml version="1.0" encoding="UTF-8"?><urlset
      xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
            http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
echo $header >sitemap.xml

find . -name "*.md" | while read -r item; do
    item="${item:2}"
    item="${item%.*}"
    echo '<url><loc>'${sitedomain}/${item}.html'</loc></url>' >>sitemap.xml
done

echo "</urlset>" >> sitemap.xml