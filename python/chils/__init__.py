import ctypes
import os
import platform

_lib_name = "libCHILS.so"
if platform.system() == "Windows":
    _lib_name = "libCHILS.dll"

_lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), _lib_name))

_lib.chils_initialize.restype = ctypes.c_void_p
_lib.chils_release.argtypes = [ctypes.c_void_p]
_lib.chils_add_vertex.argtypes = [ctypes.c_void_p, ctypes.c_longlong]
_lib.chils_add_vertex.restype = ctypes.c_int
_lib.chils_add_edge.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
_lib.chils_run_full.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int, ctypes.c_uint]
_lib.chils_run_local_search_only.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_uint]
_lib.chils_solution_get_size.argtypes = [ctypes.c_void_p]
_lib.chils_solution_get_size.restype = ctypes.c_int
_lib.chils_solution_get_weight.argtypes = [ctypes.c_void_p]
_lib.chils_solution_get_weight.restype = ctypes.c_longlong
_lib.chils_solution_get_time.argtypes = [ctypes.c_void_p]
_lib.chils_solution_get_time.restype = ctypes.c_double
_lib.chils_solution_get_vertex_configuration.argtypes = [ctypes.c_void_p, ctypes.c_int]
_lib.chils_solution_get_vertex_configuration.restype = ctypes.c_int

class CHILS:
    """
    A Python interface for the CHILS solver.

    This class provides a way to interact with the CHILS C library.
    It allows you to build a graph, run the solver, and retrieve the
    results.
    """
    def __init__(self):
        """Initializes the CHILS solver."""
        self.solver = _lib.chils_initialize()

    def __del__(self):
        """Releases the memory allocated by the solver."""
        _lib.chils_release(self.solver)

    def add_vertex(self, weight):
        """
        Adds a new vertex to the graph.

        Args:
            weight (int): The weight of the new vertex.

        Returns:
            int: The ID of the newly added vertex.
        """
        return _lib.chils_add_vertex(self.solver, weight)

    def add_edge(self, u, v):
        """
        Adds a new undirected edge to the graph.

        Args:
            u (int): The first endpoint of the edge.
            v (int): The second endpoint of the edge.
        """
        _lib.chils_add_edge(self.solver, u, v)

    def run_full(self, time_limit, n_solutions, seed):
        """
        Runs the full CHILS algorithm.

        Args:
            time_limit (float): The time limit in seconds.
            n_solutions (int): The number of solutions to use for CHILS.
            seed (int): The seed for the random number generator.
        """
        try:
            _lib.chils_run_full(self.solver, time_limit, n_solutions, seed)
        except KeyboardInterrupt:
            print("\nInterrupt detected, shutting down gracefully...")
            _lib.chils_request_stop()
            raise

    def run_local_search_only(self, time_limit, seed):
        """
        Runs only the local search part of the algorithm.

        Args:
            time_limit (float): The time limit in seconds.
            seed (int): The seed for the random number generator.
        """
        try:
            _lib.chils_run_local_search_only(self.solver, time_limit, seed)
        except KeyboardInterrupt:
            print("\nInterrupt detected, shutting down gracefully...")
            _lib.chils_request_stop()
            raise

    def get_solution_size(self):
        """
        Gets the size of the best independent set found.

        Returns:
            int: The number of vertices in the best solution.
        """
        return _lib.chils_solution_get_size(self.solver)

    def get_solution_weight(self):
        """
        Gets the weight of the best independent set found.

        Returns:
            int: The weight of the best solution.
        """
        return _lib.chils_solution_get_weight(self.solver)

    def get_solution_time(self):
        """
        Gets the time when the best solution was found.

        Returns:
            float: The time in seconds to find the best solution.
        """
        return _lib.chils_solution_get_time(self.solver)

    def get_solution_vertex_configuration(self, u):
        """
        Gets the configuration of a vertex in the best solution.

        Args:
            u (int): The ID of the vertex.

        Returns:
            int: 1 if the vertex is in the independent set, 0 otherwise.
        """
        return _lib.chils_solution_get_vertex_configuration(self.solver, u)
