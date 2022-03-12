# What about

Imagine a pdf file that contains some essential information and some auxiliary
notes. It would be great to be able to stare at the essential information
without having to scroll through endless notes. Being able to fold and unfold
said notes would be great, but pdf doesn't handle that! (Does it?) HTML and CSS
could be used to achieve the intended result.

I don't want to manually convert the tex file that outputs my pdf into an HTML
file. I would like a script to do it. And here is my attempt at writing one.

# Issues

* There are cases where I need to "look ahead." For example, something like
  "\textbf" could have its argument on the same line ("\textbf{argument}") or on
  some subsequent line ("\textbf{%\n argument\n }") or, some "\item" could have
  all of its content on the same line, or some of it on subsequent lines. What
  is the best way of handling the multi line cases? I'm trying for "If this line
  begins with \item, and as long as the next line does not begin with \item,
  do something." But then I hit list length hell.
