from pathlib import Path
from MovieSolver import ExperimentalMovieSolver, NaiveMovieSolver, Tables

# TODO errors in original dataset

"""
Paths used in Demo
"""
DATA_FOLDER = "data"
EXPORT_FOLDER = "export"
MOVIES_DATA_FILE = "movies_metadata.csv"
MOVIES_EXPORT_FILE = "movies.json"
RATINGS_DATA_FILE = "ratings.csv"
RATINGS_EXPORT_FILE = "ratings.json"


def demo_naive():
    """
    Demonstrates the solution using naive approach
    """
    project_folder = Path(__file__).parent.resolve()
    in_file = Path.joinpath(project_folder, DATA_FOLDER, MOVIES_DATA_FILE)
    out_file = Path.joinpath(project_folder, EXPORT_FOLDER, MOVIES_EXPORT_FILE)
    m = NaiveMovieSolver(in_file)

    print("###################")
    print("Solution 1 - Naive")
    print("###################")

    print("Movie Count:")
    print(m.movie_count())
    print("Average Rating:")
    print(m.average_rating_of_all())
    print("Best Rated:")
    print(m.best_rated(5))
    print("Releases by Year:")
    print(m.releases_by_year())
    print("Movies by Genre:")
    print(m.count_by_genre())

    m.export_to_json(out_file)


def demo_experimental():
    """
    Demonstrates the solution using experimental approach
    """

    project_folder = Path(__file__).parent.resolve()
    in_files = {
        Tables.MOVIES: Path.joinpath(project_folder, DATA_FOLDER, MOVIES_DATA_FILE),
        Tables.RATINGS: Path.joinpath(project_folder, DATA_FOLDER, RATINGS_DATA_FILE)
    }
    out_files = {
        Tables.MOVIES: Path.joinpath(project_folder, EXPORT_FOLDER, MOVIES_EXPORT_FILE),
        Tables.RATINGS: Path.joinpath(project_folder, EXPORT_FOLDER, RATINGS_EXPORT_FILE)
    }
    m = ExperimentalMovieSolver(in_files)

    print("###################")
    print("Solution 2 - Experimental")
    print("###################")

    print("Movie Count:")
    print(m.movie_count())
    print("Average Rating:")
    print(m.average_rating_of_all())
    print("Best Rated:")
    print(m.best_rated(5))
    print("Releases by Year:")
    print(m.releases_by_year())
    print("Movies by Genre:")
    print(m.count_by_genre())

    m.export_to_json(out_files)


if __name__ == "__main__":
    # demo_naive()
    demo_experimental()
