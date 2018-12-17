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


INCLUDE_FILE_DEFAULTS = dict(
    fname=None,
    show_label=False,
    classes="",
    indir="",
    )

def include_file_default(**kwargs):
    INCLUDE_FILE_DEFAULTS.update(kwargs)

def include_file(
        fname=None,
        start=None, end=None,
        start_has=None, end_has=None,
        start_from=None, end_at=None,
        line_count=None,
        highlight=None,
        section=None,
        show_label=None,
        px=False,
        classes=None,
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
    if fname is None:
        fname = INCLUDE_FILE_DEFAULTS['fname']
    if show_label is None:
        show_label = INCLUDE_FILE_DEFAULTS['show_label']
    if classes is None:
        classes = INCLUDE_FILE_DEFAULTS['classes']
    indir = INCLUDE_FILE_DEFAULTS['indir']

    assert fname is not None, "Need a file name to include!"

    with open(os.path.join(indir, fname)) as f:
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
        start = next((i for i, l in enumerate(lines, 1) if start_from in l), None)
        if start is None:
            raise Exception("Didn't find {!r} as a start line".format(start_from))
        if end_at:
            end = next((i for i, l in enumerate(lines[start:], start+1) if end_at in l), None)
            if end is None:
                raise Exception("Didn't find {!r} as an end line".format(end_at))
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

    if show_label:
        cog.outl("<div>")
        cog.outl("<div class='prelabel'>{}</div>".format(fname))
    include_code(text, lang=lang, firstline=start, number=True, highlight=highlight, px=px, classes=classes)
    if show_label:
        cog.outl("</div>")


def include_code(text, lang=None, number=False, firstline=1, show_text=False, highlight=None, px=False, classes=""):
    text = textwrap.dedent(text)

    text = "\n".join(l.rstrip() for l in text.splitlines())

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
    class_attr = lang
    if classes:
        class_attr += " " + classes
    result.append("<pre class='{}'>".format(class_attr))
    result.append(quote_html(text))
    result.append("</pre>")
    cog.outl("\n".join(result))


def prompt_session(input, command=False, prelude=""):
    output = ""
    if command:
        output += "$ python\n"
    repl_out = cagedprompt.prompt_session(input, banner=command, prelude=prelude)
    # REPL sessions have lone triple-dot lines. Suppress them.
    repl_out = "\n".join('' if l == '... ' else l for l in repl_out.splitlines())
    output += repl_out
    include_code(output, lang="python", number=False, classes="console")
