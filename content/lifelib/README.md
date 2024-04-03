
`BasicTerm_S_nomx` comes from command:

~~~python
import modelx as mx
mx.read_model("BasicTerm_S").export("BasicTerm_S_nomx")
~~~

after doing:

~~~python
import lifelib
lifelib.create('basicterm', 'basicterm')
~~~

using:

modelx 0.25.0
lifelib 0.9.5

## comments

This is the self-contained Python model, independent of `modelx`. (see [Export Feature Intro](https://modelx.io/blog/2023/07/29/export-feature-intro/) blog post on modelx.io)

I was interested to compare interactive performance using/without `modelx`, but got an error trying to read that model (in local Jupyter however, I reproduce numbers [here](https://modelx.io/blog/2023/08/19/enhanced-speed-for-exported-lifelib-models/)).
