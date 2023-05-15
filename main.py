from pathlib import Path
from config import MOVIES_DATA_FILE, MOVIES_EXPORT_FILE
from MovieSolver import ExperimentalMovieSolver

# TODO errors in original dataset


def main():
    project_folder = Path(__file__).parent.resolve()
    in_file = Path.joinpath(project_folder, MOVIES_DATA_FILE)
    out_file = Path.joinpath(project_folder, MOVIES_EXPORT_FILE)
    m = ExperimentalMovieSolver(in_file)

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


if __name__ == "__main__":
    main()
