"""
*****
LaTeX
*****

Export NetworkX graphs in LaTeX format using the TikZ library within TeX/LaTeX.
Usually, you will want the drawing to appear in a figure environment so
you use ``to_latex(G, caption="A caption")``. If you want the raw
drawing commands without a figure environment use :func:`to_latex_raw`.
And if you want to write to a file instead of just returning the latex
code as a string, use ``write_latex(G, "filename.tex", caption="A caption")``.

To construct a figure with subfigures for each graph to be shown, provide
``to_latex`` or ``write_latex`` a list of graphs, a list of subcaptions,
and a number of rows of subfigures inside the figure.

To be able to refer to the figures or subfigures in latex using ``\\\\ref``,
the keyword ``latex_label`` is available for figures and `sub_labels` for
a list of labels, one for each subfigure.

We intend to eventually provide an interface to the TikZ Graph
features which include e.g. layout algorithms.

Let us know via github what you'd like to see available, or better yet
give us some code to do it, or even better make a github pull request
to add the feature.

The TikZ approach
=================
Drawing options can be stored on the graph as node/edge attributes, or
can be provided as dicts keyed by node/edge to a string of the options
for that node/edge. Similarly a label can be shown for each node/edge
by specifying the labels as graph node/edge attributes or by providing
a dict keyed by node/edge to the text to be written for that node/edge.

Options for the tikzpicture environment (e.g. "[scale=2]") can be provided
via a keyword argument. Similarly default node and edge options can be
provided through keywords arguments. The default node options are applied
to the single TikZ "path" that draws all nodes (and no edges). The default edge
options are applied to a TikZ "scope" which contains a path for each edge.

Examples
========
>>> G = nx.path_graph(3)
>>> nx.write_latex(G, "just_my_figure.tex", as_document=True)
>>> nx.write_latex(G, "my_figure.tex", caption="A path graph", latex_label="fig1")
>>> latex_code = nx.to_latex(G)  # a string rather than a file

You can change many features of the nodes and edges.

>>> G = nx.path_graph(4, create_using=nx.DiGraph)
>>> pos = {n: (n, n) for n in G}  # nodes set on a line

>>> G.nodes[0]["style"] = "blue"
>>> G.nodes[2]["style"] = "line width=3,draw"
>>> G.nodes[3]["label"] = "Stop"
>>> G.edges[(0, 1)]["label"] = "1st Step"
>>> G.edges[(0, 1)]["label_opts"] = "near start"
>>> G.edges[(1, 2)]["style"] = "line width=3"
>>> G.edges[(1, 2)]["label"] = "2nd Step"
>>> G.edges[(2, 3)]["style"] = "green"
>>> G.edges[(2, 3)]["label"] = "3rd Step"
>>> G.edges[(2, 3)]["label_opts"] = "near end"

>>> nx.write_latex(G, "latex_graph.tex", pos=pos, as_document=True)

Then compile the LaTeX using something like ``pdflatex latex_graph.tex``
and view the pdf file created: ``latex_graph.pdf``.

If you want **subfigures** each containing one graph, you can input a list of graphs.

>>> H1 = nx.path_graph(4)
>>> H2 = nx.complete_graph(4)
>>> H3 = nx.path_graph(8)
>>> H4 = nx.complete_graph(8)
>>> graphs = [H1, H2, H3, H4]
>>> caps = ["Path 4", "Complete graph 4", "Path 8", "Complete graph 8"]
>>> lbls = ["fig2a", "fig2b", "fig2c", "fig2d"]
>>> nx.write_latex(graphs, "subfigs.tex", n_rows=2, sub_captions=caps, sub_labels=lbls)
>>> latex_code = nx.to_latex(graphs, n_rows=2, sub_captions=caps, sub_labels=lbls)

>>> node_color = {0: "red", 1: "orange", 2: "blue", 3: "gray!90"}
>>> edge_width = {e: "line width=1.5" for e in H3.edges}
>>> pos = nx.circular_layout(H3)
>>> latex_code = nx.to_latex(H3, pos, node_options=node_color, edge_options=edge_width)
>>> print(latex_code)
\\documentclass{report}
\\usepackage{tikz}
\\usepackage{subcaption}
<BLANKLINE>
\\begin{document}
\\begin{figure}
  \\begin{tikzpicture}
      \\draw
        (1.0, 0.0) node[red] (0){0}
        (0.707, 0.707) node[orange] (1){1}
        (-0.0, 1.0) node[blue] (2){2}
        (-0.707, 0.707) node[gray!90] (3){3}
        (-1.0, -0.0) node (4){4}
        (-0.707, -0.707) node (5){5}
        (0.0, -1.0) node (6){6}
        (0.707, -0.707) node (7){7};
      \\begin{scope}[-]
        \\draw[line width=1.5] (0) to (1);
        \\draw[line width=1.5] (1) to (2);
        \\draw[line width=1.5] (2) to (3);
        \\draw[line width=1.5] (3) to (4);
        \\draw[line width=1.5] (4) to (5);
        \\draw[line width=1.5] (5) to (6);
        \\draw[line width=1.5] (6) to (7);
      \\end{scope}
    \\end{tikzpicture}
\\end{figure}
\\end{document}

Notes
-----
If you want to change the preamble/postamble of the figure/document/subfigure
environment, use the keyword arguments: `figure_wrapper`, `document_wrapper`,
`subfigure_wrapper`. The default values are stored in private variables
e.g. ``nx.nx_layout._DOCUMENT_WRAPPER``

References
----------
TikZ:          https://tikz.dev/

TikZ options details:   https://tikz.dev/tikz-actions
"""

__all__ = ["to_latex_raw", "to_latex", "write_latex"]

def to_latex_raw(
    G,
    pos: str = "pos",
    tikz_options: str = "",
    default_node_options: str = "",
    node_options: str = "node_options",
    node_label: str = "label",
    default_edge_options: str = "",
    edge_options: str = "edge_options",
    edge_label: str = "label",
    edge_label_options: str = "edge_label_options",
):
    """Return a string of the LaTeX/TikZ code to draw `G`

    This function produces just the code for the tikzpicture
    without any enclosing environment.

    Parameters
    ==========
    G : NetworkX graph
        The NetworkX graph to be drawn
    pos : string or dict (default "pos")
        The name of the node attribute on `G` that holds the position of each node.
        Positions can be sequences of length 2 with numbers for (x,y) coordinates.
        They can also be strings to denote positions in TikZ style, such as (x, y)
        or (angle:radius).
        If a dict, it should be keyed by node to a position.
        If an empty dict, a circular layout is computed by TikZ.
    tikz_options : string
        The tikzpicture options description defining the options for the picture.
        Often large scale options like `[scale=2]`.
    default_node_options : string
        The draw options for a path of nodes. Individual node options override these.
    node_options : string or dict
        The name of the node attribute on `G` that holds the options for each node.
        Or a dict keyed by node to a string holding the options for that node.
    node_label : string or dict
        The name of the node attribute on `G` that holds the node label (text)
        displayed for each node. If the attribute is "" or not present, the node
        itself is drawn as a string. LaTeX processing such as ``"$A_1$"`` is allowed.
        Or a dict keyed by node to a string holding the label for that node.
    default_edge_options : string
        The options for the scope drawing all edges. The default is "[-]" for
        undirected graphs and "[->]" for directed graphs.
    edge_options : string or dict
        The name of the edge attribute on `G` that holds the options for each edge.
        If the edge is a self-loop and ``"loop" not in edge_options`` the option
        "loop," is added to the options for the self-loop edge. Hence you can
        use "[loop above]" explicitly, but the default is "[loop]".
        Or a dict keyed by edge to a string holding the options for that edge.
    edge_label : string or dict
        The name of the edge attribute on `G` that holds the edge label (text)
        displayed for each edge. If the attribute is "" or not present, no edge
        label is drawn.
        Or a dict keyed by edge to a string holding the label for that edge.
    edge_label_options : string or dict
        The name of the edge attribute on `G` that holds the label options for
        each edge. For example, "[sloped,above,blue]". The default is no options.
        Or a dict keyed by edge to a string holding the label options for that edge.

    Returns
    =======
    latex_code : string
       The text string which draws the desired graph(s) when compiled by LaTeX.

    See Also
    ========
    to_latex
    write_latex
    """

def to_latex(
    Gbunch,
    pos: str = "pos",
    tikz_options: str = "",
    default_node_options: str = "",
    node_options: str = "node_options",
    node_label: str = "node_label",
    default_edge_options: str = "",
    edge_options: str = "edge_options",
    edge_label: str = "edge_label",
    edge_label_options: str = "edge_label_options",
    caption: str = "",
    latex_label: str = "",
    sub_captions=None,
    sub_labels=None,
    n_rows: int = 1,
    as_document: bool = True,
    document_wrapper: str = ...,
    figure_wrapper: str = ...,
    subfigure_wrapper: str = ...,
):
    """Return latex code to draw the graph(s) in `Gbunch`

    The TikZ drawing utility in LaTeX is used to draw the graph(s).
    If `Gbunch` is a graph, it is drawn in a figure environment.
    If `Gbunch` is an iterable of graphs, each is drawn in a subfigure environment
    within a single figure environment.

    If `as_document` is True, the figure is wrapped inside a document environment
    so that the resulting string is ready to be compiled by LaTeX. Otherwise,
    the string is ready for inclusion in a larger tex document using ``\\include``
    or ``\\input`` statements.

    Parameters
    ==========
    Gbunch : NetworkX graph or iterable of NetworkX graphs
        The NetworkX graph to be drawn or an iterable of graphs
        to be drawn inside subfigures of a single figure.
    pos : string or list of strings
        The name of the node attribute on `G` that holds the position of each node.
        Positions can be sequences of length 2 with numbers for (x,y) coordinates.
        They can also be strings to denote positions in TikZ style, such as (x, y)
        or (angle:radius).
        If a dict, it should be keyed by node to a position.
        If an empty dict, a circular layout is computed by TikZ.
        If you are drawing many graphs in subfigures, use a list of position dicts.
    tikz_options : string
        The tikzpicture options description defining the options for the picture.
        Often large scale options like `[scale=2]`.
    default_node_options : string
        The draw options for a path of nodes. Individual node options override these.
    node_options : string or dict
        The name of the node attribute on `G` that holds the options for each node.
        Or a dict keyed by node to a string holding the options for that node.
    node_label : string or dict
        The name of the node attribute on `G` that holds the node label (text)
        displayed for each node. If the attribute is "" or not present, the node
        itself is drawn as a string. LaTeX processing such as ``"$A_1$"`` is allowed.
        Or a dict keyed by node to a string holding the label for that node.
    default_edge_options : string
        The options for the scope drawing all edges. The default is "[-]" for
        undirected graphs and "[->]" for directed graphs.
    edge_options : string or dict
        The name of the edge attribute on `G` that holds the options for each edge.
        If the edge is a self-loop and ``"loop" not in edge_options`` the option
        "loop," is added to the options for the self-loop edge. Hence you can
        use "[loop above]" explicitly, but the default is "[loop]".
        Or a dict keyed by edge to a string holding the options for that edge.
    edge_label : string or dict
        The name of the edge attribute on `G` that holds the edge label (text)
        displayed for each edge. If the attribute is "" or not present, no edge
        label is drawn.
        Or a dict keyed by edge to a string holding the label for that edge.
    edge_label_options : string or dict
        The name of the edge attribute on `G` that holds the label options for
        each edge. For example, "[sloped,above,blue]". The default is no options.
        Or a dict keyed by edge to a string holding the label options for that edge.
    caption : string
        The caption string for the figure environment
    latex_label : string
        The latex label used for the figure for easy referral from the main text
    sub_captions : list of strings
        The sub_caption string for each subfigure in the figure
    sub_latex_labels : list of strings
        The latex label for each subfigure in the figure
    n_rows : int
        The number of rows of subfigures to arrange for multiple graphs
    as_document : bool
        Whether to wrap the latex code in a document environment for compiling
    document_wrapper : formatted text string with variable ``content``.
        This text is called to evaluate the content embedded in a document
        environment with a preamble setting up TikZ.
    figure_wrapper : formatted text string
        This text is evaluated with variables ``content``, ``caption`` and ``label``.
        It wraps the content and if a caption is provided, adds the latex code for
        that caption, and if a label is provided, adds the latex code for a label.
    subfigure_wrapper : formatted text string
        This text evaluate variables ``size``, ``content``, ``caption`` and ``label``.
        It wraps the content and if a caption is provided, adds the latex code for
        that caption, and if a label is provided, adds the latex code for a label.
        The size is the vertical size of each row of subfigures as a fraction.

    Returns
    =======
    latex_code : string
        The text string which draws the desired graph(s) when compiled by LaTeX.

    See Also
    ========
    write_latex
    to_latex_raw
    """

def write_latex(Gbunch, path, **options) -> None:
    """Write the latex code to draw the graph(s) onto `path`.

    This convenience function creates the latex drawing code as a string
    and writes that to a file ready to be compiled when `as_document` is True
    or ready to be ``import`` ed or ``include`` ed into your main LaTeX document.

    The `path` argument can be a string filename or a file handle to write to.

    Parameters
    ----------
    Gbunch : NetworkX graph or iterable of NetworkX graphs
        If Gbunch is a graph, it is drawn in a figure environment.
        If Gbunch is an iterable of graphs, each is drawn in a subfigure
        environment within a single figure environment.
    path : string or file
        Filename or file handle to write to.
        Filenames ending in .gz or .bz2 will be compressed.
    options : dict
        By default, TikZ is used with options: (others are ignored)::

            pos : string or dict or list
                The name of the node attribute on `G` that holds the position of each node.
                Positions can be sequences of length 2 with numbers for (x,y) coordinates.
                They can also be strings to denote positions in TikZ style, such as (x, y)
                or (angle:radius).
                If a dict, it should be keyed by node to a position.
                If an empty dict, a circular layout is computed by TikZ.
                If you are drawing many graphs in subfigures, use a list of position dicts.
            tikz_options : string
                The tikzpicture options description defining the options for the picture.
                Often large scale options like `[scale=2]`.
            default_node_options : string
                The draw options for a path of nodes. Individual node options override these.
            node_options : string or dict
                The name of the node attribute on `G` that holds the options for each node.
                Or a dict keyed by node to a string holding the options for that node.
            node_label : string or dict
                The name of the node attribute on `G` that holds the node label (text)
                displayed for each node. If the attribute is "" or not present, the node
                itself is drawn as a string. LaTeX processing such as ``"$A_1$"`` is allowed.
                Or a dict keyed by node to a string holding the label for that node.
            default_edge_options : string
                The options for the scope drawing all edges. The default is "[-]" for
                undirected graphs and "[->]" for directed graphs.
            edge_options : string or dict
                The name of the edge attribute on `G` that holds the options for each edge.
                If the edge is a self-loop and ``"loop" not in edge_options`` the option
                "loop," is added to the options for the self-loop edge. Hence you can
                use "[loop above]" explicitly, but the default is "[loop]".
                Or a dict keyed by edge to a string holding the options for that edge.
            edge_label : string or dict
                The name of the edge attribute on `G` that holds the edge label (text)
                displayed for each edge. If the attribute is "" or not present, no edge
                label is drawn.
                Or a dict keyed by edge to a string holding the label for that edge.
            edge_label_options : string or dict
                The name of the edge attribute on `G` that holds the label options for
                each edge. For example, "[sloped,above,blue]". The default is no options.
                Or a dict keyed by edge to a string holding the label options for that edge.
            caption : string
                The caption string for the figure environment
            latex_label : string
                The latex label used for the figure for easy referral from the main text
            sub_captions : list of strings
                The sub_caption string for each subfigure in the figure
            sub_latex_labels : list of strings
                The latex label for each subfigure in the figure
            n_rows : int
                The number of rows of subfigures to arrange for multiple graphs
            as_document : bool
                Whether to wrap the latex code in a document environment for compiling
            document_wrapper : formatted text string with variable ``content``.
                This text is called to evaluate the content embedded in a document
                environment with a preamble setting up the TikZ syntax.
            figure_wrapper : formatted text string
                This text is evaluated with variables ``content``, ``caption`` and ``label``.
                It wraps the content and if a caption is provided, adds the latex code for
                that caption, and if a label is provided, adds the latex code for a label.
            subfigure_wrapper : formatted text string
                This text evaluate variables ``size``, ``content``, ``caption`` and ``label``.
                It wraps the content and if a caption is provided, adds the latex code for
                that caption, and if a label is provided, adds the latex code for a label.
                The size is the vertical size of each row of subfigures as a fraction.

    See Also
    ========
    to_latex
    """
