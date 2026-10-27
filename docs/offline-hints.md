# Offline investigation hints

Python 3.11+ is the only required tool. Run setup.py and one example before reading
all modules. Use `python3 -B -m unittest discover -s tests -v` for public checks.
A JSON response with ok:false may be expected for a denied action. Inspect fields.

The standard library can load a small request with json.load and save a modified
copy with json.dump. Keep original fixtures intact when making a reproduction.
copy.deepcopy is useful when proving an input was not modified. unittest supports
assertEqual, assertNotIn and assertRaises; no testing package is needed.

Trace a decision from examples through service.dispatch to one module, then compare
it with the corresponding current policy section. A positive example and a nearby
negative example usually reveal more than a large random test. Write down the
input, observed response and why that response supports the finding. Separate a
model result from claims about a device or service that was never supplied.

XML can be read with xml.etree.ElementTree. Find the mode section before evaluating
its include and exclude rows. For nested JSON, compare values and types separately;
Python booleans are also integers for isinstance, so exact JSON type matters.

If AI or internet is unavailable, the same source reading, local experiment and
verification can be recorded in CHOICES.md. No subscription or browser is required.
