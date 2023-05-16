import ast
import logging
import numpy as np
import pandas as pd
import typing
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

"""
Design Notes:

I provide 2 solutions
- class NaiveMovieSolver contains literal interpretations of some requirements
Literal interpretations are correct in theory but usually wrong in practical terms,
because they contain multiple outliers
Ideally unclear requirements should be discussed with product owner, but we are not in this case
- ExperimentalMovieSolver contains more liberal interpretations
I expect those to be better, but they rely on my heuristics and business assumptions, so may be wrong

For simple tasks, the use of OOP here is overkill, but the task asks us to demonstrate OOP so
OOP here is for demonstration
In the real world, a lot of these ideas should be implemented with simpler flags and params

use sphinx markup for docstrings, it is considered the de facto standard
"""


class Tables(Enum):
    MOVIES = 1
    RATINGS = 2


class AbcMovieSolver(ABC):
    """
    Interface for the whole hierarchy and container for docs
    """

    @abstractmethod
    def __init__(self, file_path: Path):
        """
        Load a dataset

        :param Path file_path: absolute path to dataset
        """
        pass

    @abstractmethod
    def movie_count(self):
        """
        :return: count of all movies
        :rtype: int
        """
        pass

    @abstractmethod
    def average_rating_of_all(self):
        """
        :return: average rating of all movies
        :rtype: float
        """
        pass

    @abstractmethod
    def best_rated(self, count: int):
        """
        :param int count: maximum number of movies returned
        :return: the highest rated movies
        :rtype: list
        """
        pass

    @abstractmethod
    def releases_by_year(self):
        """
        :return: count of released movies, broken by year
        :rtype: dict
        """
        pass

    @abstractmethod
    def count_by_genre(self):
        """
        :return: count of movies, broken by genre
        :rtype: dict
        """
        pass

    @abstractmethod
    def export_to_json(self, file_path: Path):
        """
        Export data to json

        :param Path file_path: absolute path to destination
        """
        pass


class NaiveMovieSolver(AbcMovieSolver):

    def __init__(self, file_path: Path):
        """
        Load a dataset

        :param Path file_path: absolute path to dataset
        """
        logging.debug("loading movies data ...")

        # Performance optimization
        # always assign dtypes
        # if not, pandas will try to guess and that is memory intensive
        mov_types = {
            "adult": bool,
            "belongs_to_collection": object,
            "budget": object,
            "genres": object,
            "homepage": object,
            "id": object,
            "imdb_id": object,
            "original_language": object,
            "original_title": object,
            "overview": object,
            "popularity": np.float64,
            "poster_path": object,
            "production_companies": object,
            "production_countries": object,
            "release_date": object,
            "revenue": np.int64,
            "runtime": np.float64,
            "spoken_languages": object,
            "status": object,
            "tagline": object,
            "title": object,
            "video": bool,
            "vote_average": np.float64,
            "vote_count": np.int64,
        }

        logging.debug("preparing data for use ...")

        self.mov_df = pd.read_csv(file_path, index_col="id", dtype=mov_types)
        self.mov_df["release_date"] = pd.to_datetime(self.mov_df["release_date"])

        # load genres from string into data
        self.mov_df["genres"] = self.mov_df["genres"].apply(lambda genres_str: ast.literal_eval(genres_str))

    def movie_count(self):
        logging.debug("movie count ...")
        return len(self.mov_df)

    def average_rating_of_all(self):
        logging.debug("average rating of all ...")
        return self.mov_df["vote_average"].mean()

    def best_rated(self, count: int):
        logging.debug("best rated ...")
        return self.mov_df.sort_values(
            by=["vote_average", "vote_count"],
            ascending=False
        ).head(count)['title'].values.tolist()

    def releases_by_year(self):
        logging.debug("releases by year ...")
        result = self.mov_df.groupby(self.mov_df["release_date"].dt.year, as_index=False).size()
        # format - remove trailing zero-s from float years
        result["release_date"] = result["release_date"].apply(lambda x: int(x))
        return result.set_index("release_date")["size"].to_dict()

    def count_by_genre(self):
        logging.debug("count by genre ...")
        genre_data = self.mov_df["genres"].apply(lambda genres: [genre["name"] for genre in genres])
        res = dict()
        for m, genre_cell in genre_data.items():
            for g in genre_cell:
                if g in res:
                    res[g] += 1
                else:
                    res[g] = 1
        return res

    def export_to_json(self, file_path: Path):
        """
        Export strategy is subject to requirements discussion
        """
        logging.debug("export to json ...")
        self.mov_df.to_json(file_path, orient="split")


class ExperimentalMovieSolver(NaiveMovieSolver):

    def __init__(self, file_paths: typing.Dict[Tables, Path]):
        """
        :param Dict[Tables, Path] file_paths: dict with paths to datasets
        """
        super().__init__(file_paths[Tables.MOVIES])



        # Assumption
        # We assume we are interested only in existing movies
        # Subject to requirements discussion
        logging.debug("cutting non-existing movies ...")
        self.mov_df = self.mov_df[
            (self.mov_df["status"] == "Released") & (self.mov_df["release_date"].notnull())
        ]

        logging.debug("loading ratings data ...")

        rat_types = {
            "userId": np.int64,
            "movieId": np.int64,
            "rating": np.float64,
            "timestamp": np.int64,
        }

        self.rat_df = pd.read_csv(file_paths[Tables.RATINGS], dtype=rat_types)

    def average_rating_of_all(self):
        logging.debug("average rating of all ...")
        return self.rat_df["rating"].mean()

    def best_rated(self, count: int):
        logging.debug("best rated ...")
        df = self.mov_df
        df["heuristic_rating"] = ((df["vote_average"] - 5) * df["vote_count"])
        return df.sort_values(
            by=["heuristic_rating"],
            ascending=False
        ).head(count)['title'].values.tolist()

    def export_to_json(self, file_paths: typing.Dict[Tables, Path]):
        """
        :param Dict[Tables, Path] file_paths: absolute paths to destinations
        """
        logging.debug("export movies ...")
        self.mov_df.to_json(file_paths[Tables.MOVIES], orient="split")
        logging.debug("export ratings ...")
        self.rat_df.to_json(file_paths[Tables.RATINGS], orient="split")
