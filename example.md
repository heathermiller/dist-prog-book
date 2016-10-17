---
layout: page
title:  "Remote Procedure Call"
by: "Joe Schmoe and Mary Jane"
---
You’ll find this post in your `_posts` directory. Go ahead and edit it and re-build the site to see your changes. You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

To add new posts, simply add a file in the `_posts` directory that follows the convention `YYYY-MM-DD-name-of-post.ext` and includes the necessary front matter. Take a look at the source for this post to get an idea about how it works.

Jekyll also offers powerful support for code snippets:

```ruby
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
```

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

## Header

Here's some text<label for="sn-proprietary-monotype-bembo" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-proprietary-monotype-bembo" class="margin-toggle"/><span class="sidenote">See Tufte’s comment in the <a href="http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0000Vt">Tufte book fonts</a> thread.</span> which has a little foot/side note thingy.

This is another example of a thing.<label for="mn-blue-links" class="margin-toggle">&#8853;</label><input type="checkbox" id="mn-blue-links" class="margin-toggle"/><span class="marginnote">Blue text, while also a widely recognizable clickable-text indicator, is crass and distracting. Luckily, it is also rendered unnecessary by the use of underlining.</span> This thing is different becuase it doesn't have a number I guess?

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.

One can also have blockquotes

<blockquote>
  <p>The English language . . . becomes ugly and inaccurate because our thoughts are foolish, but the slovenliness of our language makes it easier for us to have foolish thoughts.</p>
  <footer>George Orwell, “Politics and the English Language”</footer>
</blockquote>

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

> This is also a blockquote, but I guess it doesn't have who it's attributed to.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. {% cite Uniqueness %}

<figure class="fullwidth">
  <img src="{{ site.baseurl }}/img/napoleons-march.png" alt="Figurative map of the successive losses of the French Army in the Russian campaign, 1812-1813" />
</figure>

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. {% cite Elsman2005 Kennedy2004 %}

This is a bulleted list:

- one
- two
- three

This is a numbered list:

1. one
2. two
3. three

You can also have inline math, like this $$x^2+x=4$$ as well as equation blocks:

\\[x^2 + 3 = y\\]

## References

{% bibliography --file example %}

