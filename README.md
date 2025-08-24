#+TITLE: rainbowrooster - Test Markdown Generator

* Overview
Python app that generates test markdown files for products and stores with customizable frontmatter.

* Installation
#+begin_src bash
pip install rainbowrooster
#+end_src

* Usage
#+begin_src bash
# Generate markdown files from default text files
rainbowrooster

# Use custom input files
rainbowrooster --products custom_products.txt --stores custom_stores.txt

# Add test suffix to filenames
rainbowrooster --annotate-test

# Enable verbose logging
rainbowrooster -v

# Show version
rainbowrooster --version
#+end_src
