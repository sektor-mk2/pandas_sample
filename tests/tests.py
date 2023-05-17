import pytest
import timeit
from pathlib import Path
from MovieSolver import NaiveMovieSolver


def helper_functional(in_file: Path):
    """
    Execute code under test
    Used for functional testing
    """
    m = NaiveMovieSolver(in_file)
    result = {
        "movie_count": m.movie_count(),
        "average_rating_of_all": round(m.average_rating_of_all(), 1),
        "best_rated": m.best_rated(5),
        "releases_by_year": m.releases_by_year(),
        "count_by_genre": m.count_by_genre()
    }
    return result


def helper_performance(in_file: Path):
    """
    Execute code under test
    Used for performance testing
    """
    m = NaiveMovieSolver(in_file)
    m.movie_count()
    m.average_rating_of_all()
    m.best_rated(5)
    m.releases_by_year()
    m.count_by_genre()


test_params = [
    (
        # Basic happy path scenario
        # All fields have valid values
        # Wherever possible, strings have multiple words without quotes
        "happy_path.csv",
        {
            "movie_count": 1,
            "average_rating_of_all": 7.7,
            "best_rated": ["Movie Title 1"],
            "releases_by_year": {
                1995: 1
            },
            "count_by_genre": {
                "Genre 1": 1,
                "Genre 2": 1,
                "Genre 3": 1
            }
        }
    ),
    (
        # Almost basic happy path scenario
        # Check all fields can have missing values IF we expect they can
        # This may not be the actual expected behavior, needs to sync with product owner
        # My judgement is based on - can that be nan in original big dataset
        # This test also works as a valid test for counting all movies
        "missing_values.csv",
        {
            "movie_count": 16,
            "average_rating_of_all": 7.7,
            "best_rated": ["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"],
            "releases_by_year": {
                1995: 15
            },
            "count_by_genre": {
                "Genre 1": 15,
                "Genre 2": 15,
                "Genre 3": 15
            }
        }
    ),
    (
        # Test sorting the 5 best rated movies
        # Check things specific to our naive algorithm:
        # - non-existing movies are also checked
        # - vote count does not affect movies with different rating
        # - if 2 movies have the same rating, they are ordered by vote count
        "best_rated.csv",
        {
            "movie_count": 7,
            "average_rating_of_all": 9.4,
            "best_rated": ["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"],
            "releases_by_year": {
                1995: 6
            },
            "count_by_genre": {
                "Genre 1": 7,
                "Genre 2": 7,
                "Genre 3": 7
            }
        }
    ),
    (
        # Remaining tests are called after the method they test
        "average_rating.csv",
        {
            "movie_count": 7,
            "average_rating_of_all": 7.1,
            "best_rated": ["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"],
            "releases_by_year": {
                1995: 6,
            },
            "count_by_genre": {
                "Genre 1": 7,
                "Genre 2": 7,
                "Genre 3": 7
            }
        }
    ),
    (
        "releases_by_year.csv",
        {
            "movie_count": 9,
            "average_rating_of_all": 7.7,
            "best_rated": ["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"],
            "releases_by_year": {
                1995: 3,
                1996: 1,
                1997: 1,
                1998: 3,
            },
            "count_by_genre": {
                "Genre 1": 9,
                "Genre 2": 9,
                "Genre 3": 9,
            }
        }
    ),
    (
        "count_by_genre.csv",
        {
            "movie_count": 9,
            "average_rating_of_all": 7.7,
            "best_rated": ["Movie Title 1", "Movie Title 2", "Movie Title 3", "Movie Title 4", "Movie Title 5"],
            "releases_by_year": {
                1995: 3,
                1997: 1,
                1998: 4,
            },
            "count_by_genre": {
                "Genre 1": 3,
                "Genre 2": 3,
                "Genre 3": 3,
                "Genre 4": 1,
                "Genre 5": 1,
                "Genre 6": 2,
                "Genre 7": 3,
            }
        }
    ),
]


@pytest.mark.parametrize("data_file_name,expected", test_params)
def test_functional(data_file_name, expected):
    """
    This docstring explains our testing strategy for functional testing

    The main QA activity that consumes majority of our time is not writing tests
    The main activity is troubleshooting test failures
    This means we need to optimize our strategy for ease of troubleshooting
    The primary rule for good tests is tests must be independent
    Sharing the same dataset across tests is considered very evil practice
    For this purpose I provide separate data sets (csv files) for each individual test

    But what about the case with real db ?
    In the real world it will be prohibitively expensive to have hundreds of db tables for each individual tests
    The solution would be the following:
    - this applies for small unit tests like the current project
    - each individual test inserts its own data in db, as setup
    - each test marks its data (ex - a label) and looks only for its own data
    - this data insertion is code, so we can add clarifying comments to it
    - each test cleans up after itself with teardown

    We do all that for the purpose of making tests independent and easy to troubleshoot
    We can do more to assist this goal:
    - we can add comments to clarify what each data record is testing for (not applicable to csv)
    - we can use data that is easy to navigate.
    For example here I use values that match the column and have an index - like Movie Title 1, 2 etc,
    This makes it easy to find which line and which column in the csv causes failures

    Avoid code duplication:
    In most companies tests look like hundreds of walls of copy-pasted code
    This is evil practice
    A simple way to avoid that is to have a single test body with parametrized data

    Exception Handling:
    In this project we do not catch exceptions
    The good practice is that we do not catch an exception if there is nothing meaningful we can do with it
    For exception cases I found the error handling of libs I used in the project to be correct and readable
    Hence I do not think it is necessary to add tests that catch expected exceptions

    Further Reading:
    I held multiple dev.bg lections , for more of the topic of how we write tests, you can read my materials here:
    https://docs.google.com/presentation/d/1d5rPGHaCheRY5bN5aPElYQt16Aj1NnvDvWjb3oSE79o
    """
    tests_folder = Path(__file__).parent.resolve()
    file_with_test_data = Path.joinpath(tests_folder, data_file_name)
    actual = helper_functional(file_with_test_data)
    assert(actual == expected)


perf_folder = Path(__file__).parent.resolve()
perf_data = Path.joinpath(perf_folder, "chunky_data.csv")


def test_performance():
    """
    Performance Testing

    This is not the best way to do performance testing, but it's not wrong
    and it's so simple, that it's almost free.
    Free performance test is better than no performance test

    Please provide a chunky_data.csv in the tests folder
    This project does not do this for you as it does not contain large files

    Be careful with the numbers parameter
    """
    perf_result = timeit.timeit('helper_performance(perf_data)', globals=globals(), number=3)
    assert(perf_result < 4.3)

