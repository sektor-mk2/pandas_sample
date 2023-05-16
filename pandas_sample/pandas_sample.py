import logging
from pathlib import Path
from MovieSolver import ExperimentalMovieSolver, NaiveMovieSolver, Tables
from config import *


def demo_naive():
    """
    Demonstrates the solution using naive approach
    """
    logging.basicConfig(level=LOG_LEVEL)
    project_folder = Path(__file__).parent.resolve()
    in_file = Path.joinpath(project_folder, DATA_FOLDER, MOVIES_DATA_FILE)
    out_file = Path.joinpath(project_folder, EXPORT_FOLDER, MOVIES_EXPORT_FILE)

    logging.info("###################")
    logging.info("Solution 1 - Naive")
    logging.info("###################")
    m = NaiveMovieSolver(in_file)
    logging.info("Movie Count:")
    logging.info(m.movie_count())
    logging.info("Average Rating:")
    logging.info(m.average_rating_of_all())
    logging.info("Best Rated:")
    logging.info(m.best_rated(5))
    logging.info("Releases by Year:")
    logging.info(m.releases_by_year())
    logging.info("Movies by Genre:")
    logging.info(m.count_by_genre())
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
    logging.info("###################")
    logging.info("Solution 2 - Experimental")
    logging.info("###################")
    m = ExperimentalMovieSolver(in_files)
    logging.info("Movie Count:")
    logging.info(m.movie_count())
    logging.info("Average Rating:")
    logging.info(m.average_rating_of_all())
    logging.info("Best Rated:")
    logging.info(m.best_rated(5))
    logging.info("Releases by Year:")
    logging.info(m.releases_by_year())
    logging.info("Movies by Genre:")
    logging.info(m.count_by_genre())

    m.export_to_json(out_files)


if __name__ == "__main__":
    demo_naive()
    demo_experimental()
