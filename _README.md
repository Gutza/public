---
published: false
---

For all commands below to work, save the current directory to a variable:
```ps1
$pwd = (Get-Location).Path
```

Install dependencies:
```ps1
docker run --rm -it -v "${PWD}:/srv/jekyll" -v "${PWD}\vendor\bundle:/usr/local/bundle" jekyll/jekyll:4 bundle install
```

Start the Jekyll container and serve the site:
```ps1
docker run --rm -it -p 4000:4000 -p 35729:35729 -v "${PWD}:/srv/jekyll" -v "${PWD}\vendor\bundle:/usr/local/bundle" jekyll/jekyll:4 sh -lc "git config --global --add safe.directory /srv/jekyll; jekyll serve --host 0.0.0.0 --livereload --force_polling"
```

Then visit http://localhost:4000/public/ to view the site.