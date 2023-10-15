import pylab as plt
import networkx as nx
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure


class TrainTrack:
    """
    A class representing a train track.

    Attributes:
    -----------
    data : dict
        A dictionary containing the train track data in JSON format.
    G : networkx.Graph
        A graph representing the train track.
    """

    def __init__(self, json_string):
        """
        Initializes a TrainTrack object.

        Parameters:
        -----------
        json_string : str
            A string containing the train track data in JSON format.
        """
        self.data = json_string
        self.G = nx.Graph()
        self._add_station_graph_edges()
        self._mark_occupied_routes()
        self._mark_interested_routes()

    def _add_station_graph_edges(self):
        """
        Adds edges to the train track graph based on the station graph data.
        """
        for edge in self.data["station_graph"]:
            self.G.add_edge(edge["start"], edge["end"])

    def _mark_occupied_routes(self):
        """
        Marks the routes that are currently occupied in the train track graph.
        """
        for route in self.data["routes"]:
            if route["occupied"]:
                start_node = route["start"]
                end_node = route["end"]
                nodes_to_mark_occupied = nx.shortest_path(
                    self.G, source=start_node, target=end_node
                )
                for i in range(len(nodes_to_mark_occupied) - 1):
                    start_node = nodes_to_mark_occupied[i]
                    end_node = nodes_to_mark_occupied[i + 1]

                    if self.G.has_edge(start_node, end_node):
                        self.G.edges[start_node, end_node]["occupied"] = True
            else:
                start_node = route["start"]
                end_node = route["end"]
                nodes_to_mark_unoccupied = nx.shortest_path(
                    self.G, source=start_node, target=end_node
                )
                for i in range(len(nodes_to_mark_unoccupied) - 1):
                    start_node = nodes_to_mark_unoccupied[i]
                    end_node = nodes_to_mark_unoccupied[i + 1]

                    if self.G.has_edge(start_node, end_node):
                        self.G.edges[start_node, end_node]["occupied"] = False

    def _mark_interested_routes(self):
        """
        Marks the routes that are of interest in the train track graph.
        """

        nodes_to_be_traversed = nx.shortest_path(
            self.G,
            source=self.data["check_route"]["start"],
            target=self.data["check_route"]["end"],
        )

        all_paths = list(
            nx.all_simple_paths(
                self.G,
                source=self.data["check_route"]["start"],
                target=self.data["check_route"]["end"],
            )
        )
        all_paths.sort(key=len)

        for path in all_paths:
            is_occupied = False
            for i in range(len(path) - 1):
                start_node = path[i]
                end_node = path[i + 1]
                if self.G[start_node][end_node]["occupied"]:
                    is_occupied = True
                    break
            if not is_occupied:
                # print(path)
                nodes_to_be_traversed = path
                break

        for i in range(len(nodes_to_be_traversed) - 1):
            start_node = nodes_to_be_traversed[i]
            end_node = nodes_to_be_traversed[i + 1]

            if self.G.has_edge(start_node, end_node):
                self.G.edges[start_node, end_node]["want"] = True

    def get_edges(self):
        """
        Returns all the edges in the train track graph.

        Returns:
        --------
        edges : list
            A list of tuples representing the edges in the train track graph.
        """
        return self.G.edges(data=True)

    def get_occupied_edges(self):
        """
        Returns the edges in the train track graph that are currently occupied.

        Returns:
        --------
        edges : list
            A list of tuples representing the occupied edges in the train track graph.
        """
        return [
            (edge[0], edge[1])
            for edge in self.G.edges(data=True)
            if edge[2]["occupied"]
        ]

    def get_unoccupied_edges(self):
        """
        Returns the edges in the train track graph that are currently unoccupied.

        Returns:
        --------
        edges : list
            A list of tuples representing the unoccupied edges in the train track graph.
        """
        return [
            (edge[0], edge[1])
            for edge in self.G.edges(data=True)
            if not edge[2]["occupied"]
        ]

    def get_interested_edges(self):
        """
        Returns the edges in the train track graph that are both occupied and of interest.

        Returns:
        --------
        edges : list
            A list of tuples representing the interested edges in the train track graph.
        """
        return [
            (edge[0], edge[1]) for edge in self.G.edges(data=True) if "want" in edge[2]
        ]

    def check_graph_connectedness(self):
        """
        Checks if the train track graph is connected.

        Returns:
        --------
        connected : bool
            True if the train track graph is connected, False otherwise.
        """
        return nx.is_connected(self.G)

    def is_it_possible_to_travle(self):
        """
        Checks if the train track graph has no intersecting routs.

        Returns:
        --------
        possible : bool
            True if the train track can be traversed along the check_route given.
        """
        possible = [
            edge
            for edge in self.get_interested_edges()
            if edge in self.get_occupied_edges()
        ]
        if len(possible) == 0:
            return True
        else:
            return False

    def plot_graph(self):
        """
        Plots the train track graph.
        """
        pos = nx.spring_layout(self.G)
        plt.figure(figsize=(12, 8))

        # Draw the nodes
        nx.draw_networkx_nodes(self.G, pos)

        # Draw unoccupied (normal) edges
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=self.get_unoccupied_edges(),
            edge_color="black",
            width=2,
            style="dashed",
        )

        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=self.get_interested_edges(),
            edge_color="green",
            width=2,
        )

        nx.draw_networkx_edges(
            self.G, pos, edgelist=self.get_occupied_edges(), edge_color="red", width=2
        )

        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=[
                edge
                for edge in self.get_interested_edges()
                if edge in self.get_occupied_edges()
            ],
            edge_color="orange",
            width=2,
        )

        # Draw the labels
        labels = {node: node for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, pos, labels)

        plt.axis("off")
        plt.show()

    def plot_web_graph(self):
        """
        Plots the train track graph.
        """

        pos = nx.spring_layout(self.G)
        fig = Figure(figsize=(12, 8))
        ax = fig.subplots()

        # Draw the nodes
        nx.draw_networkx_nodes(self.G, pos, ax=ax)

        # Draw edges based on your criteria (unoccupied, interested, occupied, etc.)
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=self.get_unoccupied_edges(),
            edge_color="black",
            width=2,
            style="dashed",
            ax=ax,
        )
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=self.get_interested_edges(),
            edge_color="green",
            width=2,
            ax=ax,
        )
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=self.get_occupied_edges(),
            edge_color="orange",
            width=2,
            ax=ax,
        )
        nx.draw_networkx_edges(
            self.G,
            pos,
            edgelist=[
                edge
                for edge in self.get_interested_edges()
                if edge in self.get_occupied_edges()
            ],
            edge_color="red",
            width=2,
            ax=ax,
        )

        # Draw the labels
        labels = {node: node for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, pos, labels, ax=ax)

        # Save the figure to a temporary buffer and convert it to base64
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        # Generate HTML to embed the image
        html = f"data:image/png;base64,{data}"
        # return f"<img src='data:image/png;base64,{data}'/>"

        return html
