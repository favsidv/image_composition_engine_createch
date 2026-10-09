# Filter exchange

Fawzi needs to integrate a filter received from another student and show that
it works with the composition engine. This requirement is still pending.

Before exchanging files, agree on the image format, parameters and imports.
Our filters receive normalized RGB NumPy arrays, use float32 or float64, and
return a new array with the same dimensions. The engine handles alpha.

## What to do

1. Get the original filter file from another student.
2. Copy it into the project without changing its code.
3. Add its import and factory entry in `registry.py`.
4. Use it in a configuration with the provided images and run the engine.
5. Check the output and confirm that the engine's processing logic did not
   need any changes.

The existing registry supports classes with a parameter dictionary or keyword
arguments. Agree on any other dependencies before copying the file.

## What to record

When the exchange is done, add the student's name, the original filter filename,
the registered name, the configuration used and the result of the run here.
Include the received source file and configuration in the repository.

A filter written locally only to test registration does not replace this exchange.
