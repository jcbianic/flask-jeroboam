---
name: Feature request
about: Suggest a new feature for Flask-Jeroboam
---

## Feature Request: <NAME>

### Abstract

<!--
Replace this comment with a A brief summary of the feature request.
Exemple: Response Model as Lists of primitives or BaseModels
-->

### Use Case

<!--
Replace this comment with A clear and concise description of the use case for this feature and how it will be used.
Identify the problem it solves or the opportunity it generates.
Exemple: Response Models can be defined as generic type List of either primitives (int, str, ...) or
subclasses of pydantic BaseModels, especially for read index type of view functions.
-->

#### Motivation

<!--
Replace this comment with why this feature is important, and how it will benefit users or the project as a whole.
Identify the problem it solves or the opportunity it generates.
Exemple: When users want to return a list of objects without any metadata like the total_count, it's the most
straightforward approach to defining a response_model and make the economy of defining a wrapping response_model.
-->

#### Desired user API

<!--
Replace this comment with The desired user API and how it will be used.
Include current user API if relevant.
Exemple:
The Following will be supported:
```python
@app.get("/return_a_list_of_primitives", response_model=List[int])
def get_a_list():
    return [2, 3, 4]


class MyModel(OutboundModel):
    name: str
    count: int

@app.get("/return_a_list_of_base_models", response_model=List[MyModel])
def get_a_list():
    return [MyModel(name="Test1", count=3), MyModel(name="Test2", count=10)]


@app.get("/return_a_list_of_dicts", response_model=List[MyModel])
def get_a_list():
    return [{"name": "Test1", "count": 3}, {"name": "Test2", "count": 10}]
```
-->

#### Desired output/behavior

<!--
Replace this comment with the desired output or behavior of the feature.
Include current output/behavior if relevant.
Exemple:
When hit the aboce-defined endpoints would return:

>> curl return_a_list_of_primitives
[2, 3, 4]
>> curl return_a_list_of_base_models
[{"name": "Test1", "count": 3}, {"name": "Test2", "count": 10}]
>> curl return_a_list_of_dicts
[{"name": "Test1", "count": 3}, {"name": "Test2", "count": 10}]
-->

### Alternatives Considered

<!--
Replace this comment with a clear and concise description of any alternative solutions or features that were considered.
Explain why the proposed solution is the best approach.
-->

### Additional context

<!--
Replace this comment with any other relevant information, that may be helpful in understanding the feature request.
-->
