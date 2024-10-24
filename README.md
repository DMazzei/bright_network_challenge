# Bright Network Hiring Challenge - Job Recommendations Algorithm

> In one of our suggested programming languages, please implement a **very simple** recommendations algorithm to match members to their perfect job.

<details>
<summary>Click to toggle the challenge description</summary>
<br>
Please fetch the required data from the following APIs:

https://bn-hiring-challenge.fly.dev/members.json

https://bn-hiring-challenge.fly.dev/jobs.json

For each member, please print their name and their recommended job(s).

We'd like you to spend less than 2 hours on the problem, so your solution will not be perfect (and that's absolutely fine). The purpose is to let us see some of your code, and to give us something to discuss in the technical interview.

Please work in a git repository, and share this with us via either a link or zip file. Please also include a brief README which explains the choices you made and the limitations of your approach.

### Suggested Languages

* Python
* JavaScript
* TypeScript

</details>


## Local Setup

### Prerequisites

- Assuming you already cloned this repository and are inside the right folder...

- The **python-version** used for the solution is `3.11.10`, and I'm using [pyenv](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://github.com/pyenv/pyenv&ved=2ahUKEwiP057ItKeJAxUXZ0EAHRs5HNMQFnoECAgQAQ&usg=AOvVaw0RqKEeNd2EnMGr0ZKFd1fA) and [pyenv-virtualenv](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://github.com/pyenv/pyenv-virtualenv&ved=2ahUKEwjX4-zXtKeJAxXYQUEAHdrbO2cQFnoECAgQAQ&usg=AOvVaw1PBZqgiCFJPYGzsbzm_RaV) to manage the python version and environment, but feel free to use whatever you prefer.
    - In case you also go with the above, you can create an environment exclusively for this excercise using:
        ```bash
        pyenv virtualenv 3.11 bn-challenge-3.11
        pyenv activate bn-challenge-3.11
        ```

- This project uses [poetry](https://python-poetry.org/) as the dependency management software.
    - Easiest way to install IMO is via [pipx](https://github.com/pypa/pipx)
        ```bash
        pipx install poetry
        ```

### Getting Started

- Install dependencies:
    ```bash
    make install
    ```

    This will also install the required pre-trained language models.
<br><br>
    You can see all available commands using:
    ```bash
    make help
    ```


### Running the tests

This will run all existing unit-tests in `verbose` mode:

```bash
make test
```

or you can invoke it directly using poetry:

```bash
poetry run pytest
```


### Running the algorithm

Simple way is using the `make` instruction which will give the simplest output:

```bash
make run
```

Or you can use explore the additional arguments the algorithm accepts using:

```bash
poetry run python main.py --help
```

I find that this combinations gives the best recommendation visibility:

```bash
poetry run python main.py -vl
```

<br><br><br>

# Thoughts on the proposed solution

## Choices

1. Simple CLI to run the algorithm via terminal, as the boilerplate of creating a web UI, for example, would be too time-consuming for its benefits.

2. To fetch the required data, I decided to use a very simple `http_client`, implementing only the `get` method, as the test app doesn't require any authentication.

3. To parse the text data within the candidate's bio, I decided to use `spaCy` [spacy.io](https://spacy.io/) for basic NLP implementation, given how quick and flexible it is to start using it. Mainly to take advantage of GPE POS tags to identify "locations" easily. And it also allowed me to use pre-defined patterns used in custom matchers, for a simpler solution.

4. I used `pydantic` models to have the core model classes well-defined and allow for the take advantage of validations in the future. It also made parsing the API's raw data much easier and faster.

5. The "job title" matching is done using `fuzzywuzzy`, for its quick implementation and decent results when combined with `python-levenshtein`.

6. Matching algorithm: I implemented a simple score system, fine-tuned using matching ratios and weights. The "Job Title" has preference over location, so to an exact match, 1 point is added to the score. Otherwise the fuzzy matching score is used (if it's above the stipulated threshold - `60`). The "Job Location" weight is configurable, but the default value used is `0.5`.

7. To generate the recommendation list, all jobs are scored as a match for the candidate, this list is then sorted and filtered.

<br><br>

## Limitations

1. The data processed by the algorith is limited to what's offered bt the API, and would be interesting to implement optional data sources.

2. The implementation of NLP used in the "bio" parser is rudimentary and simplistic. Trained models or more complex patterns would significantly improve the data extraction and matching. Also a more well-thought parsing of negation, context and duplications would give more accurate results.

3. Given the time constraints and the recommendation for a "simple solution", I did not focus on performance, memory- or cpu-usage.

4. I tried to use type-hints as much as I could and enforce it properly, but I didn't have time to add linters to ensure nothing escaped my attention.

5. In real life, the data would be pre-processed and normalized.


<br><br>

## If I had a bit more time...

* Add additional data source options
* Add more tests for exceptions and edge cases
* Add asyncio, to avoid time waste with sequential API response waiting
* ~~Add pre-hooks (`pre-commit`) to run linters before commiting and pushing the code~~
