"""
Aggregation for calculating pairwise distances in a large database
"""
__author__ = "Jimmy-Xuan Shen"
__email__ = "jmmshn@gmail.com"


from typing import Iterable

from maggma.builders import MapBuilder
from pymatgen import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher


class DistanceBuilder(MapBuilder):
    """
    Take all (i, j) pairs with i< j and compute the distance between them.
    """

    def __int__(self, **kwargs):
        super().__init__(**kwargs)
        q = self.query or {}
        q.update({"migration_graph": {"$ne": None}})
        self.query = q

    def get_items(self) -> Iterable:
        def modify_item(item):
            """
            Look for all j_indices that are greater than i
            """
            gt_query = {self.source.key: {"$gt": item[self.source.key]}, "migration_graph": {"$ne": None}}
            self.logger.debug(f"QUERY {gt_query}")
            with self.source as store:
                j_docs = list(store.query(criteria=gt_query, properties=[self.source.key, "migration_graph"]))
            self.logger.debug(f"Found {len(j_docs)} documents with greater index value.")
            return {self.source.key: item[self.source.key], "i_doc": item, "j_docs": j_docs}

        yield from map(modify_item, super().get_items())

    def unary_function(self, item):
        sm = StructureMatcher(ltol=0.2, stol=0.3, angle_tol=5, primitive_cell=True, scale=True, attempt_supercell=False)
        i_doc = item["i_doc"]
        struct_i = Structure.from_dict(i_doc["migration_graph"]["structure"])
        comparisons = {}
        for j_doc in item["j_docs"]:
            # Calculate the distance
            assert "migration_graph" in j_doc
            struct_j = Structure.from_dict(j_doc["migration_graph"]["structure"])
            comparisons[j_doc[self.target.key]] = {"structure_matched": sm.fit(struct_i, struct_j), "distance": 0}

        return {self.source.key: i_doc[self.source.key], "comparisons": comparisons}
