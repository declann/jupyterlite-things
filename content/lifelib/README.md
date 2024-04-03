
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

This is the self-contained model, independent of `modelx`.

I was interested to compare interactive performance using/without `modelx`, but got an error trying to read that model.
