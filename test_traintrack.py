import unittest
from traintrack import TrainTrack
import json


class TestTrainTrack(unittest.TestCase):
    def setUp(self):
        # Example JSON string for testing purposes
        self.json_string = '{"station_graph":[{"start":"Station West","end":"Entry Signal West"},{"start":"Entry Signal West","end":"Point 1"},{"start":"Point 1","end":"Exit Signal West 1"},{"start":"Point 1","end":"Exit Signal West 2"},{"start":"Exit Signal West 1","end":"Exit Signal East 1"},{"start":"Exit Signal West 2","end":"Exit Signal East 2"},{"start":"Exit Signal East 1","end":"Point 2"},{"start":"Exit Signal East 2","end":"Point 2"},{"start":"Point 2","end":"Entry Signal East"},{"start":"Entry Signal East","end":"Station East"}],"routes":[{"start":"Entry Signal West","end":"Exit Signal East 1","occupied":false},{"start":"Entry Signal West","end":"Exit Signal East 2","occupied":false},{"start":"Exit Signal East 1","end":"Station East","occupied":false},{"start":"Exit Signal East 2","end":"Station East","occupied":false},{"start":"Entry Signal East","end":"Exit Signal West 1","occupied":false},{"start":"Entry Signal East","end":"Exit Signal West 2","occupied":false},{"start":"Point 1","end":"Exit Signal East 1","occupied":true},{"start":"Exit Signal West 2","end":"Station West","occupied":false}],"check_route":{"start":"Exit Signal East 1","end":"Point 2"}}'
        self.train_track = TrainTrack(json.loads(self.json_string))

    def test_get_edges(self):
        edges = self.train_track.get_edges()
        self.assertEqual(len(edges), 10)

    def test_get_occupied_edges(self):
        occupied_edges = self.train_track.get_occupied_edges()
        self.assertEqual(len(occupied_edges), 2)

    def test_get_unoccupied_edges(self):
        unoccupied_edges = self.train_track.get_unoccupied_edges()
        self.assertEqual(len(unoccupied_edges), 8)

    def test_get_interested_edges(self):
        interested_edges = self.train_track.get_interested_edges()
        self.assertEqual(len(interested_edges), 1)

    def test_check_graph_connectedness(self):
        connected = self.train_track.check_graph_connectedness()
        self.assertTrue(connected)

    def test_is_it_possible_to_travle(self):
        possible = self.train_track.is_it_possible_to_travle()
        self.assertTrue(possible)


if __name__ == "__main__":
    unittest.main()
