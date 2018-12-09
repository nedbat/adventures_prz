# Helpers for cogging slides.

import os
import textwrap

import cog
import cagedprompt

def quote_html(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def clip_long_boring_line(s, l):
    """
    If s is a line with only one character in it, shorten it to length l.
    """
    if len(s) > l and len(set(s)) == 1:
        s = s[:l]
    return s


def include_file(
        fname,
        start=None, end=None,
        start_has=None, end_has=None,
        start_from=None, end_at=None,
        line_count=None,
        highlight=None,
        section=None,
        px=False,
        classes=""
    ):
    """Include a text file.

    `fname` is read as text, and included in a <pre> tag.

    `highlight` is a list of lines to highlight.

    `start` and `end` are the first and last line numbers to show, if provided.
    `start_has` is text that must appear in the start line, to check that the
    file hasn't changed. Similarly for `end_has`.

    `start_from` and `end_at` are substrings of the first and last lines to
    show.

    `section` is a named section.  If provided, a marked section in the file is extracted
    for display.  Markers for section foobar are "(((foobar))" and "(((end)))".

    If `px` is true, the result is meant for text rather than slides.

    `classes` are extra css classes to add to the <pre> tag.

    """
    with open(fname) as f:
        text = f.read()

    lines = text.splitlines()
    if section:
        assert start_from is None
        assert end_at is None
        assert line_count is None
        start_from = "(((" + section + ")))"
        end_at = "(((end)))"
    if start_from:
        assert start is None
        assert end is None
        start = next(i for i, l in enumerate(lines, 1) if start_from in l)
        if end_at:
            end = next(i for i, l in enumerate(lines[start:], start+1) if end_at in l)
        elif line_count is not None:
            end = start + line_count - 1
        if section:
            start += 1
            end -= 1
    else:
        if start is None:
            start = 1
        if end is None:
            end = len(lines)

    if start_has:
        start_line = lines[start-1]
        if start_has not in start_line:
            raise Exception("Didn't find {!r} in the start line: {}:{} {!r}".format(start_has, fname, start, start_line))
    if end_has:
        end_line = lines[end-1]
        if end_has not in end_line:
            raise Exception("Didn't find {!r} in the end line: {}:{} {!r}".format(end_has, fname, end, end_line))

    # Take only the lines we want, and shorten lines that are too long and
    # easily shortened.
    lines = [clip_long_boring_line(l, 60) for l in lines[start-1:end]]

    text = "\n".join(lines)

    lang = "python" if fname.endswith(".py") else "text"
    include_code(text, lang=lang, firstline=start, number=True, highlight=highlight, px=px, classes=classes)


def include_code(text, lang=None, number=False, firstline=1, show_text=False, highlight=None, px=False, classes=""):
    text = textwrap.dedent(text)

    if px:
        cog.outl("<code lang='{}'>".format(lang))
        cog.outl(text.replace("&", "&amp;").replace("<", "&lt;"))
        cog.outl("</code>")
        return

    # Put the code in a comment, so we can see it in the HTML while editing.
    if show_text:
        cog.outl("<!--")
        cog.outl(text.replace("-", u"\N{EN DASH}".encode("utf8"))) # Prevent breaking the HTML comment.
        cog.outl("-->")

    if os.environ.get("NOPYG"):
        cog.outl("<!-- *** NOPYG: {} lines of text will be here. *** -->".format(len(text.splitlines())))
        return

    result = []
    if classes:
        classes += " "
    classes += lang
    result.append("<pre class='{}'>".format(classes))
    result.append(quote_html(text))
    result.append("</pre>")
    cog.outl("\n".join(result))


def prompt_session(input, command=False, prelude=""):
    output = ""
    if command:
        output += "$ python\n"
    output += cagedprompt.prompt_session(input, banner=command, prelude=prelude)
    include_code(output, lang="pycon", number=False)
