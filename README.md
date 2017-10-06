Programming Models for Distributed Computation
==============================================

Source repo for the book that I and my students in my course at Northeastern University, [CS7680 Special Topics in Computing Systems: Programming Models for Distributed Computing](http://heather.miller.am/teaching/cs7680/), are writing on the topic of programming models for distributed systems.

This is a book about the programming constructs we use to build distributed
systems. These range from the small, RPC, futures, actors, to the large; systems
built up of these components like MapReduce and Spark. We explore issues and
concerns central to distributed systems like consistency, availability, and
fault tolerance, from the lens of the programming models and frameworks that
the programmer uses to build these systems.

_**Please note that this is a work in progress, the book contents are in this repo, but we have not yet polished everything and published the final book online. Expected release: end of December**_

_Note: the chapters can be viewed by manually going to `http://dist-prog-book.com/chapter/x/article-name.html`, e.g., http://dist-prog-book.com/chapter/2/futures.html. One we finish off the chapters that need the most work, we will "release" the book by putting a proper index page in place._

## Chapters

1. RPC
2. Futures & Promises
3. Message-passing
4. Distributed Programming Languages
5. Languages Extended for Distribution
6. CAP, Consistency, & CRDTs
7. Programming Languages & Consistency
8. Large-scale Parallel Batch Processing
9. Large-scale Streaming

## Editing this book

### Workflow

1. Fork/clone
2. Edit on your local branch
3. **Make a pull request to the `master` branch with your changes. Do not commit directly to the repository**
4. After merge, visit the live site `http://dist-prog-book.com/chapter/x/your-article.html`

Note: We have CI that builds the book for each commit. Pull requests that don't
build will not be merged.

Note: when PRs are merged, the site is built and redeployed automatically.

### Structure

Chapters are located in the `chapter` folder of the root directory.

## Dependencies

This site uses a Jekyll, a Ruby framework. You'll need Ruby and Bundler
installed.

If you have Ruby already installed, to install Bundler, just do `sudo gem install bundler`

## Building & Viewing

**Please build and view your site locally before submitting a PR!**

cd into the directory where you cloned this repository, then install the
required gems with `bundle install`. This will automatically put the gems into
`./vendor/bundle`.

Start the server in the context of the bundle:

    bundle exec jekyll serve

The generated site is available at `http://localhost:4000`

Note, this will bring you to the index page. If you'd like to see your chapter,
make sure to navigate there explicitly, e.g.,
`http://localhost:4000/chapter/1/rpc.html`.

## Adding/editing pages

Articles are in Markdown with straightforward YAML frontmatter.

You can include code, math (LaTeX syntax), figures, blockquotes, side notes,
etc. You can also use regular BibTeX to make a bibliography. To see everything
you can do, I've prepared an example article.

- [Live example article](http://dist-prog-book.com/example.html)
- [Corresponding example page markdown](https://raw.githubusercontent.com/heathermiller/dist-prog-book/master/example.md)

If you would like to add BibTeX entries to the bibliography for your chapter,
check the `_bibliography` directory for a `.bib` file named after your chapter.
