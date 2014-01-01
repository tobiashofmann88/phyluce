.. include:: global.rst

************
Installation
************

phyluce_ uses a number of tools that allow it to assemble data, search for UCE
loci, align results reads, manipulate alignments, prepare alignments for
analysis, etc.  To accomplish these goals, phyluce_ uses wrappers around a
number of programs that do each of these tasks (sometimes phyluce can use
several different programs that accomplish the same task in different ways).
As a result, the
`dependency chain <http://en.wikipedia.org/wiki/Dependency_hell>`_ , or the
programs that phyluce_ requires to run, is reasonably complex.

In previous versions (< 2.x), we required users to install a number of
different software packages, get those into the user's `$PATH`, cross their
fingers, and hope that everything ran smoothly (it usually did not).

In the current versions (> 2.x), we have removed a number of dependencies, **and
we very strongly suggest** that users install phyluce_ using either the
anaconda_ or miniconda_ Python distributions.

.. note:: We do not support installing phyluce through means other than the
   conda_ installer.  This means that we do not test phyluce_ against any
   binaries, other than those we build and distribute through conda_.
   **However**, with this in mind, you can configure phyluce_ to use binaries
   of different provenance using options in the :ref:`Configuration` section.

Why conda?
==========

It may seem odd to impose a particular disitribution on users, and we largely
agree.  However, conda_ makes it very easy for us to distribute both Python_ and
non-Python packages (e.g. velvet, abYss, etc.), setup identical environments
across very heterogenous platforms (unices, osx, etc.), make sure all the
`$PATHs` are correct, and have things run largely as expected. Using conda_ has
several other benefits, including environment separation similar to virtualenv_.
In short, using conda_ gets us as close to a "one-click" install that we will
probably ever get.

Install Process
===============

.. attention:: We build and test phyluce_ using 64-bit, linux and osx computers
   (i.e., x86_64). Most modern computers are of this type.  As such, we **only
   support** phyluce_ **on 64-bit (x86_64) machines**, and the conda_ packges that we
   have built are only available for this architecture.  We can potentially add
   x86 support if it is a major request.

.. attention:: We do not support phyluce_ on Windows.

The installation process is now a 3-step process.  You need to:

#. Install JAVA
#. Install conda_ (either anaconda_ or miniconda_)
#. Install phyluce_

Installing phyluce_ will install all of the required binaries, libraries, and
Python_ dependencies.

Install JAVA
------------

Although we're using conda_, you need to install a JAVA distribution for your
platform.  You should install **JAVA7**, as that will ensure a number of future
tools in phyluce_ will work on your platform.  Installing JAVA is a little
tricky across different platforms (and somewhat beyond the scope of this document),
but we described, below, how we usually do it.

If you do not see your (linux) distribution, check your package manager.

Apple OS X
^^^^^^^^^^

To install JAVA 1.7, download and install the JAVA 1.7 package from Oracle here:
http://www.java.com/en/download/manual.jsp

CentOS/Fedora linux
^^^^^^^^^^^^^^^^^^^

You can install the JRE with the following `yum` command::

    su -c "yum install java-1.7.0-openjdk"

Debian/Ubuntu linux
^^^^^^^^^^^^^^^^^^^

You can install the JRE with the following `apt-get` command::

    sudo apt-get install openjdk-7-jre


Install Anaconda or miniconda
-----------------------------

After you installed JAVA, you need to install anaconda_ or miniconda_.  Which
one you choose is up to you, your needs, how much disk space you have, and if
you are on a fast/slow connection.

.. tip:: Do I want anaconda_ or miniconda_?
   The major difference between the two python distributions is that anaconda_
   comes with many, many packages pre-installed, while miniconda_ comes with
   almost zero packages pre-installed.  As such, the anaconda_ distribution is
   roughly 200-500 MB in size while the miniconda_ distribution is 15-30 MB
   in size.

anaconda
^^^^^^^^

Follow the instructions here for your platform:
http://docs.continuum.io/anaconda/install.html

miniconda
^^^^^^^^^

Find the correct `miniconda-2.x.x` file for your platform from
http://repo.continuum.io/miniconda/ and download that file. When that has
completed, run::

    bash Miniconda-2.2.x-Linux-x86_64.sh  [linux]
    bash Miniconda-2.2.x-MacOSX-x86_64.sh [osx]

Now, you need to edit your `$PATH` to add the Miniconda distribution.  You can
do that manually using a text editor (the best way), or you can quickly quickly
run::

    echo "export PATH=$HOME/anaconda/bin:\${PATH}" >> ~/.bashrc [if you use BASH]
    echo "export PATH=$HOME/anaconda/bin:\${PATH}" >> ~/.zshrc [if you use ZSH]

.. note:: Once you have installed Miniconda, it is called **anaconda**
   forevermore.

Checking your `$PATH`
^^^^^^^^^^^^^^^^^^^^^

Regardless of how you install anaconda_, you need to check that you've installed
the package correctly.  To ensure that the correct location for conda_ or
miniconda_ are added to your $PATH (this occurs automatically on the $BASH
shell), you can try the following, which should show the path to the anaconda
distribution::

    $ echo $PATH | grep anaconda | awk '{split($0,a,":"); print a[1]}'
    /Users/bcf/anaconda/bin


You can also check that you have installed anaconda correctly by running the
`python -V` command::

    $ python -V
    Python 2.7.6 :: Anaconda 1.8.0 (x86_64)

Notice that the output shows we're using the "Anaconda 1.8.0" version of Python_.
If you do not see the expected output, then you likely need to edit your $PATH
variable to add anaconda_ or miniconda_ as the first entry.

Should you need to edit your path, the easiest way to do that is to open
``~/.bashrc`` with a text editor (if you are using ZSH, this will be
``~/.zshrc``) and add, as the last line::

    export PATH=$HOME/path/to/conda/bin:$PATH

where ``$HOME/path/to/conda/bin`` is the location of anaconda/miniconda in your
home directory (usually ``$HOME/anaconda/bin`` or ``$HOME/miniconda/bin``).


Add the faircloth-lab repository to conda
-----------------------------------------

You need to add the location of the packages we need to your conda
distributions.  to do taht, you have to add the
`faircloth-lab conda repository <http://conda.binstar.org/faircloth-lab>`_
to conda.  You can do that with the following command, which automatically edits
your ``~/.condarc`` file)::

    conda config --add channels http://conda.binstar.org/faircloth-lab


Install phyluce
---------------

Now, installing phyluce_ and all of it's dependencies is simply a matter of
running::

    conda install phyluce

This step will also automatically configure phyluce_ to know where all of the
different binaries are located (the subject of the :ref:`Configuration`
section).

Run phyluce
-----------

Once you've installed phyluce_ using conda_, there will be an executable file
named `phyluce` in your $PATH that we will run for all subsequent analyses.
You can find the location of the executable using::

    $ which phyluce
    /Users/bcf/anaconda/bin/phyluce

Because phyluce_ is in our `$PATH`, running `phyluce` should produce the
following output::

    $ phyluce
    usage: phyluce [-h] [-V] command ...

    phyluce is a software package for processing UCEand other phylogenomic data
    for systematics andpopulation genetics.

    positional arguments:
      command
        assemble     Assemble cleaned/trimmed sequencing reads.
        fetch        Fetch (AKA get) UCE contigs from assembled data.
        align        Alignment routines for UCE (and other) FASTA data.
        convert      Convert files to different formats.
        misc         Miscellaneous utilities for files and directories.
        help         Get help info on a phyluce command.

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

What conda installs
===================

When you install phyluce, it specifies a number of dependencies that it needs
to run.  conda_ is great because it will pull specific **versions** of the
required programs from the
`faircloth-lab conda repository <http://conda.binstar.org/faircloth-lab>`_ and
install those on your machine, setup the paths, etc.

Below is a list of what phyluce_ requires for installation.

3rd-party dependencies
----------------------

* trimmomatic 0.32
* velvet 1.2.10
* abyss 1.3.7 (built with boost and google-sparsehash)
* lastz 1.02.00
* mafft 7.13
* muscle 3.8.31
* raxml 8.0.1

Python packages
---------------

* Python 2.7 (sets conda default Python to 2.7)
* numpy 1.7
* BioPython 1.62
* dendropy 3.12.0
* illumiprocessor 2.0.3
* phyluce 2.0.x


Added benefits
==============

An added benefit of using conda_ and installing packages in this way is that
you can also run all of these binaries without worrying about setting the
correct $PATH, etc.

phyluce_ required MUSCLE for installation, and MUSCLE was installed by conda_ as
a dependency of phyluce_. Because ``$HOME/anaconda/bin`` (which we will now call
`$CONDA`) is part of our path now, and because phyluce_ installed MUSCLE, we can
also just run MUSCLE on the command-line, with::

    $ muscle

    MUSCLE v3.8.31 by Robert C. Edgar

    http://www.drive5.com/muscle
    This software is donated to the public domain.
    Please cite: Edgar, R.C. Nucleic Acids Res 32(5), 1792-97.


    Basic usage

        muscle -in <inputfile> -out <outputfile>

    Common options (for a complete list please see the User Guide):

        -in <inputfile>    Input file in FASTA format (default stdin)
        -out <outputfile>  Output alignment in FASTA format (default stdout)
        -diags             Find diagonals (faster for similar sequences)
        -maxiters <n>      Maximum number of iterations (integer, default 16)
        -maxhours <h>      Maximum time to iterate in hours (default no limit)
        -html              Write output in HTML format (default FASTA)
        -msf               Write output in GCG MSF format (default FASTA)
        -clw               Write output in CLUSTALW format (default FASTA)
        -clwstrict         As -clw, with 'CLUSTAL W (1.81)' header
        -log[a] <logfile>  Log to file (append if -loga, overwrite if -log)
        -quiet             Do not write progress messages to stderr
        -version           Display version information and exit

    Without refinement (very fast, avg accuracy similar to T-Coffee): -maxiters 2
    Fastest possible (amino acids): -maxiters 1 -diags -sv -distance1 kbit20_3
    Fastest possible (nucleotides): -maxiters 1 -diags

This is true for other binaries you install from our repository (e.g. velveth,
velvetg, abyss-pe, mafft) or any other conda_ repository - those binaries are
all stored in `$CONDA/bin`.

We have setup conda to install other files in a standard location as well.  So
JAR files are stored in `$CONDA/jar`; libraries that you install from our repo
are stored in `$CONDA/lib`, etc. The locations and versions are standardized
within our conda_ distribution so that we always know where things are
installed, hopefully avoiding lots of the problems with `dependency hell
<http://en.wikipedia.org/wiki/Dependency_hell>`_ and making our lives easier.

The structure of the conda repository that we use looks like the following::

    $CONDA/ (<= can be main CONDA or CONDA env)
        bin/
            Binaries we build.
        docs/
            Pertinent documentation, if any.
        include/
            Header files (Qt, Boost)
        jar/
            Java Archive (JAR) Files
        lib/
            Libraries
        libexec/
            Helpers called by other programs (e.g. mafft)
        share/
            Additional support files
        test/
            Test data required by some programs.

Other useful tools
==================

You will need to be familiar with the command-line/terminal, and it helps to
have a decent text editor for your platform (gedit [linux], Sublime Text
[linux, osx], TextMate [osx]).
