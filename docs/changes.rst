Changes
=======

beta releases
*************

The beta releases mark a turning point and the intention to outgrow **Flask-Jeroboam**'s initial internal use. The 0.1.0 version is primarily based on forking FastAPI and departs from the first naive implementation of alpha releases.


Version 0.1.0.beta2
-------------------

Released March, 9th 2023

* Writing Documentation
* Fixing bugs
* Breaking Change: Fixing the embed mechnism for request bodies

Version 0.1.0.beta
-------------------

Released February, 22nd 2023

* Support for explicit location of inbound arguments with special functions
* Support for validation options on explicit inbound arguments
* Response Serialization mechanism is improved
* OpenAPI Documentation Auto-generation
* You can add Tags to endpoints and blueprints
* Extensive Refactoring of the codebase

alpha releases
**************

The alpha releases share a minimalist implementation of a tiny portion of the targetted features set.
They are a packaged version of helper functions that I used to level up one particular flask project and are largely overfitted to this specific context.

Version 0.0.3.alpha
-------------------

Released January, 16th 2023

* Improved request parsing
* Introducing Model Utils (Parsers and Serializers)
* Improvement of type hinting

Version 0.0.2.alpha
-------------------

Released January, 9th 2023

* Upgrade Dependencies

Version 0.0.1.alpha
-------------------

Released August, 16th 2022

* First public version
* Basic request parsing-validation-injection using type hints of view function arguments
* Basic response serialization using response_model on route decorators
