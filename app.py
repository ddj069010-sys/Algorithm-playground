"""
Algorithm Playground - Complete Backend Server
Flask application serving 70+ DSA algorithm visualizations
Author: CSE Student | Version: 2.0.0 | Port: 2344
"""

import os
import json
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# ==================== CONFIGURATION ====================
class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    SEND_FILE_MAX_AGE_DEFAULT = 31536000
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    PERMANENT_SESSION_LIFETIME = 3600

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# ==================== LOGGING SETUP ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== FLASK APP INITIALIZATION ====================
app = Flask(__name__, template_folder='templates')

# Set configuration
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ==================== SECURITY HEADERS ====================
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

# ==================== ALGORITHM DATABASE ====================
ALGORITHMS_DATABASE = {
    "sorting": {
        "bubble": {
            "name": "Bubble Sort",
            "complexity": "O(n²)",
            "best": "O(n)",
            "worst": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "desc": "Repeatedly steps through list, compares adjacent elements and swaps if needed.",
            "category": "Comparison Sort",
            "difficulty": "Easy"
        },
        "selection": {
            "name": "Selection Sort",
            "complexity": "O(n²)",
            "best": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)",
            "stable": False,
            "desc": "Divides array into sorted and unsorted parts, finds minimum and moves to sorted part.",
            "category": "Comparison Sort",
            "difficulty": "Easy"
        },
        "insertion": {
            "name": "Insertion Sort",
            "complexity": "O(n²)",
            "best": "O(n)",
            "worst": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "desc": "Builds sorted array one element at a time by inserting into correct position.",
            "category": "Comparison Sort",
            "difficulty": "Easy"
        },
        "merge": {
            "name": "Merge Sort",
            "complexity": "O(n log n)",
            "best": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)",
            "stable": True,
            "desc": "Divide and conquer: divide array, sort recursively, merge back together.",
            "category": "Divide & Conquer",
            "difficulty": "Medium"
        },
        "quick": {
            "name": "Quick Sort",
            "complexity": "O(n log n)",
            "best": "O(n log n)",
            "worst": "O(n²)",
            "space": "O(log n)",
            "stable": False,
            "desc": "Selects pivot and partitions around it. Most efficient in practice.",
            "category": "Divide & Conquer",
            "difficulty": "Medium"
        },
        "heap": {
            "name": "Heap Sort",
            "complexity": "O(n log n)",
            "best": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(1)",
            "stable": False,
            "desc": "Builds max heap and repeatedly extracts maximum element.",
            "category": "Selection Sort",
            "difficulty": "Medium"
        },
        "shell": {
            "name": "Shell Sort",
            "complexity": "O(n log n)",
            "best": "O(n log n)",
            "worst": "O(n²)",
            "space": "O(1)",
            "stable": False,
            "desc": "Generalization of insertion sort with variable gap sequence.",
            "category": "Insertion Sort",
            "difficulty": "Medium"
        },
        "counting": {
            "name": "Counting Sort",
            "complexity": "O(n+k)",
            "best": "O(n+k)",
            "worst": "O(n+k)",
            "space": "O(k)",
            "stable": True,
            "desc": "Non-comparison sort. Counts occurrences and reconstructs array.",
            "category": "Non-Comparison",
            "difficulty": "Easy"
        },
        "radix": {
            "name": "Radix Sort",
            "complexity": "O(nk)",
            "best": "O(nk)",
            "worst": "O(nk)",
            "space": "O(n+k)",
            "stable": True,
            "desc": "Sorts by individual digits from least to most significant.",
            "category": "Non-Comparison",
            "difficulty": "Medium"
        },
        "bucket": {
            "name": "Bucket Sort",
            "complexity": "O(n+k)",
            "best": "O(n+k)",
            "worst": "O(n²)",
            "space": "O(n+k)",
            "stable": True,
            "desc": "Distributes elements into buckets and sorts each bucket individually.",
            "category": "Distribution",
            "difficulty": "Medium"
        }
    },
    "searching": {
        "linear": {
            "name": "Linear Search",
            "complexity": "O(n)",
            "best": "O(1)",
            "worst": "O(n)",
            "space": "O(1)",
            "desc": "Sequentially checks each element until found or end reached.",
            "category": "Sequential",
            "difficulty": "Easy"
        },
        "binary": {
            "name": "Binary Search",
            "complexity": "O(log n)",
            "best": "O(1)",
            "worst": "O(log n)",
            "space": "O(1)",
            "desc": "Divides sorted array in half repeatedly until element found.",
            "category": "Divide & Conquer",
            "difficulty": "Easy"
        },
        "jump": {
            "name": "Jump Search",
            "complexity": "O(√n)",
            "best": "O(1)",
            "worst": "O(√n)",
            "space": "O(1)",
            "desc": "Jumps by fixed blocks then does linear search within block.",
            "category": "Sequential",
            "difficulty": "Medium"
        },
        "interpolation": {
            "name": "Interpolation Search",
            "complexity": "O(n)",
            "best": "O(1)",
            "worst": "O(n)",
            "space": "O(1)",
            "desc": "Uses interpolation formula to estimate element position.",
            "category": "Guessing",
            "difficulty": "Medium"
        },
        "exponential": {
            "name": "Exponential Search",
            "complexity": "O(log n)",
            "best": "O(1)",
            "worst": "O(log n)",
            "space": "O(1)",
            "desc": "Finds range by doubling, then binary searches within range.",
            "category": "Sequential",
            "difficulty": "Medium"
        },
        "ternary": {
            "name": "Ternary Search",
            "complexity": "O(log₃ n)",
            "best": "O(1)",
            "worst": "O(log n)",
            "space": "O(1)",
            "desc": "Divides array into three parts and eliminates one third.",
            "category": "Divide & Conquer",
            "difficulty": "Medium"
        },
        "fibonacci": {
            "name": "Fibonacci Search",
            "complexity": "O(log n)",
            "best": "O(1)",
            "worst": "O(log n)",
            "space": "O(1)",
            "desc": "Uses Fibonacci numbers as jump points for searching.",
            "category": "Sequential",
            "difficulty": "Hard"
        }
    },
    "pathfinding": {
        "bfs": {
            "name": "Breadth-First Search",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Explores graph layer by layer. Finds shortest path in unweighted graph.",
            "category": "Graph Traversal",
            "difficulty": "Easy"
        },
        "dfs": {
            "name": "Depth-First Search",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Explores as far as possible along each branch before backtracking.",
            "category": "Graph Traversal",
            "difficulty": "Easy"
        },
        "dijkstra": {
            "name": "Dijkstra's Algorithm",
            "complexity": "O((V+E) log V)",
            "space": "O(V)",
            "desc": "Finds shortest path in weighted graph. Greedy approach with priority queue.",
            "category": "Shortest Path",
            "difficulty": "Medium"
        },
        "bellman_ford": {
            "name": "Bellman-Ford Algorithm",
            "complexity": "O(VE)",
            "space": "O(V)",
            "desc": "Finds shortest paths, handles negative weights. Detects negative cycles.",
            "category": "Shortest Path",
            "difficulty": "Medium"
        },
        "floyd_warshall": {
            "name": "Floyd-Warshall Algorithm",
            "complexity": "O(V³)",
            "space": "O(V²)",
            "desc": "All-pairs shortest path. Dynamic programming approach.",
            "category": "All-Pairs Shortest Path",
            "difficulty": "Medium"
        },
        "astar": {
            "name": "A* Algorithm",
            "complexity": "O(E) worst",
            "space": "O(V)",
            "desc": "Heuristic-based pathfinding. Uses f(n) = g(n) + h(n). Faster than Dijkstra.",
            "category": "Shortest Path",
            "difficulty": "Hard"
        },
        "bidir_search": {
            "name": "Bidirectional Search",
            "complexity": "O(b^(d/2))",
            "space": "O(b^(d/2))",
            "desc": "Searches from both start and end simultaneously. Faster than BFS.",
            "category": "Graph Traversal",
            "difficulty": "Medium"
        },
        "kruskal": {
            "name": "Kruskal's Algorithm",
            "complexity": "O(E log E)",
            "space": "O(V)",
            "desc": "Minimum spanning tree. Greedy with union-find data structure.",
            "category": "Spanning Tree",
            "difficulty": "Medium"
        },
        "prim": {
            "name": "Prim's Algorithm",
            "complexity": "O(E log V)",
            "space": "O(V)",
            "desc": "Minimum spanning tree. Starts from vertex and grows tree.",
            "category": "Spanning Tree",
            "difficulty": "Medium"
        },
        "boruvka": {
            "name": "Borůvka's Algorithm",
            "complexity": "O(E log V)",
            "space": "O(V)",
            "desc": "Minimum spanning tree. Merge components approach.",
            "category": "Spanning Tree",
            "difficulty": "Hard"
        }
    },
    "tree": {
        "inorder": {
            "name": "Inorder Traversal",
            "complexity": "O(n)",
            "space": "O(h)",
            "desc": "Left-Root-Right. Produces sorted output from BST.",
            "category": "Tree Traversal",
            "difficulty": "Easy"
        },
        "preorder": {
            "name": "Preorder Traversal",
            "complexity": "O(n)",
            "space": "O(h)",
            "desc": "Root-Left-Right. Useful for copying tree.",
            "category": "Tree Traversal",
            "difficulty": "Easy"
        },
        "postorder": {
            "name": "Postorder Traversal",
            "complexity": "O(n)",
            "space": "O(h)",
            "desc": "Left-Right-Root. Useful for deleting tree.",
            "category": "Tree Traversal",
            "difficulty": "Easy"
        },
        "levelorder": {
            "name": "Level Order Traversal",
            "complexity": "O(n)",
            "space": "O(w)",
            "desc": "Breadth-first tree traversal. Uses queue.",
            "category": "Tree Traversal",
            "difficulty": "Easy"
        },
        "spiral": {
            "name": "Spiral Traversal",
            "complexity": "O(n)",
            "space": "O(w)",
            "desc": "Level order but alternating directions.",
            "category": "Tree Traversal",
            "difficulty": "Medium"
        },
        "bst_search": {
            "name": "BST Search",
            "complexity": "O(log n) avg, O(n) worst",
            "space": "O(h)",
            "desc": "Binary search tree lookup operation.",
            "category": "Binary Search Tree",
            "difficulty": "Easy"
        },
        "bst_insert": {
            "name": "BST Insert",
            "complexity": "O(log n) avg, O(n) worst",
            "space": "O(h)",
            "desc": "Insert node maintaining BST property.",
            "category": "Binary Search Tree",
            "difficulty": "Easy"
        },
        "bst_delete": {
            "name": "BST Delete",
            "complexity": "O(log n) avg, O(n) worst",
            "space": "O(h)",
            "desc": "Delete node maintaining BST property.",
            "category": "Binary Search Tree",
            "difficulty": "Medium"
        },
        "avl_rotation": {
            "name": "AVL Rotation",
            "complexity": "O(1)",
            "space": "O(1)",
            "desc": "Balance AVL tree through rotations.",
            "category": "Self-Balancing Tree",
            "difficulty": "Hard"
        },
        "trie_ops": {
            "name": "Trie Operations",
            "complexity": "O(m)",
            "space": "O(ALPHABET_SIZE * N * M)",
            "desc": "Insert, search, delete in prefix tree.",
            "category": "Trie",
            "difficulty": "Medium"
        },
        "lca": {
            "name": "Lowest Common Ancestor",
            "complexity": "O(n) to O(log n)",
            "space": "O(h)",
            "desc": "Find deepest node common to two nodes.",
            "category": "Tree Problem",
            "difficulty": "Medium"
        },
        "diameter": {
            "name": "Tree Diameter",
            "complexity": "O(n)",
            "space": "O(h)",
            "desc": "Find longest path between any two nodes.",
            "category": "Tree Problem",
            "difficulty": "Medium"
        }
    },
    "dp": {
        "fib": {
            "name": "Fibonacci",
            "complexity": "O(n)",
            "space": "O(n)",
            "desc": "Calculate nth Fibonacci number using memoization.",
            "category": "Basic DP",
            "difficulty": "Easy"
        },
        "knapsack_01": {
            "name": "0/1 Knapsack",
            "complexity": "O(nW)",
            "space": "O(nW)",
            "desc": "Maximize value with weight constraint. Can take/leave items.",
            "category": "Optimization",
            "difficulty": "Medium"
        },
        "knapsack_unbounded": {
            "name": "Unbounded Knapsack",
            "complexity": "O(nW)",
            "space": "O(nW)",
            "desc": "Maximize value with weight constraint. Can take unlimited items.",
            "category": "Optimization",
            "difficulty": "Medium"
        },
        "lcs": {
            "name": "Longest Common Subsequence",
            "complexity": "O(mn)",
            "space": "O(mn)",
            "desc": "Find longest subsequence common to two sequences.",
            "category": "String DP",
            "difficulty": "Medium"
        },
        "lis": {
            "name": "Longest Increasing Subsequence",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Find longest subsequence in increasing order.",
            "category": "Sequence DP",
            "difficulty": "Medium"
        },
        "edit_distance": {
            "name": "Edit Distance (Levenshtein)",
            "complexity": "O(mn)",
            "space": "O(mn)",
            "desc": "Minimum edits to transform one string to another.",
            "category": "String DP",
            "difficulty": "Medium"
        },
        "matrix_chain": {
            "name": "Matrix Chain Multiplication",
            "complexity": "O(n³)",
            "space": "O(n²)",
            "desc": "Minimize scalar multiplications for chain matrix product.",
            "category": "Optimization",
            "difficulty": "Hard"
        },
        "coin_change": {
            "name": "Coin Change",
            "complexity": "O(nC)",
            "space": "O(nC)",
            "desc": "Minimum coins to make amount or count ways.",
            "category": "Optimization",
            "difficulty": "Medium"
        },
        "lps": {
            "name": "Longest Palindromic Subsequence",
            "complexity": "O(n²)",
            "space": "O(n²)",
            "desc": "Find longest subsequence that reads same forwards/backwards.",
            "category": "String DP",
            "difficulty": "Medium"
        },
        "word_break": {
            "name": "Word Break",
            "complexity": "O(n²)",
            "space": "O(n)",
            "desc": "Check if string can be segmented into dictionary words.",
            "category": "String DP",
            "difficulty": "Medium"
        }
    },
    "string": {
        "naive_match": {
            "name": "Naive String Matching",
            "complexity": "O(nm)",
            "space": "O(1)",
            "desc": "Simple pattern matching. Compare pattern at each position.",
            "category": "Pattern Matching",
            "difficulty": "Easy"
        },
        "kmp": {
            "name": "KMP Algorithm",
            "complexity": "O(n+m)",
            "space": "O(m)",
            "desc": "Knuth-Morris-Pratt. Efficient pattern matching with failure function.",
            "category": "Pattern Matching",
            "difficulty": "Hard"
        },
        "boyer_moore": {
            "name": "Boyer-Moore Algorithm",
            "complexity": "O(n/m) best",
            "space": "O(m+σ)",
            "desc": "Pattern matching starting from pattern end. Often fastest in practice.",
            "category": "Pattern Matching",
            "difficulty": "Hard"
        },
        "rabin_karp": {
            "name": "Rabin-Karp Algorithm",
            "complexity": "O(n+m)",
            "space": "O(1)",
            "desc": "Rolling hash for pattern matching. Good for multiple patterns.",
            "category": "Pattern Matching",
            "difficulty": "Medium"
        },
        "aho_corasick": {
            "name": "Aho-Corasick Algorithm",
            "complexity": "O(n+m+z)",
            "space": "O(mk)",
            "desc": "Multiple pattern matching. Build trie with failure links.",
            "category": "Pattern Matching",
            "difficulty": "Hard"
        },
        "z_algorithm": {
            "name": "Z Algorithm",
            "complexity": "O(n)",
            "space": "O(n)",
            "desc": "Finds all occurrences of pattern. Compute Z-array.",
            "category": "Pattern Matching",
            "difficulty": "Hard"
        },
        "suffix_array": {
            "name": "Suffix Array",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Sorted array of all suffixes. Multiple string problems.",
            "category": "String Structure",
            "difficulty": "Hard"
        },
        "manacher": {
            "name": "Manacher's Algorithm",
            "complexity": "O(n)",
            "space": "O(n)",
            "desc": "Find all palindromic substrings efficiently.",
            "category": "Pattern Matching",
            "difficulty": "Hard"
        }
    },
    "greedy": {
        "activity_selection": {
            "name": "Activity Selection",
            "complexity": "O(n log n)",
            "space": "O(1)",
            "desc": "Select maximum non-overlapping activities.",
            "category": "Greedy",
            "difficulty": "Easy"
        },
        "huffman": {
            "name": "Huffman Coding",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Build optimal prefix-free codes. Minimum average code length.",
            "category": "Greedy",
            "difficulty": "Medium"
        },
        "interval_scheduling": {
            "name": "Interval Scheduling",
            "complexity": "O(n log n)",
            "space": "O(1)",
            "desc": "Schedule maximum non-overlapping intervals.",
            "category": "Greedy",
            "difficulty": "Easy"
        },
        "job_sequencing": {
            "name": "Job Sequencing with Deadlines",
            "complexity": "O(n²)",
            "space": "O(n)",
            "desc": "Maximize profit by scheduling jobs before deadlines.",
            "category": "Greedy",
            "difficulty": "Medium"
        },
        "fractional_knapsack": {
            "name": "Fractional Knapsack",
            "complexity": "O(n log n)",
            "space": "O(1)",
            "desc": "Maximize value with weight constraint. Can take fractions.",
            "category": "Greedy",
            "difficulty": "Easy"
        },
        "egyptian_fractions": {
            "name": "Egyptian Fractions",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Express fraction as sum of unit fractions.",
            "category": "Greedy",
            "difficulty": "Medium"
        },
        "gas_station": {
            "name": "Gas Station Problem",
            "complexity": "O(n)",
            "space": "O(1)",
            "desc": "Find starting gas station to complete circuit.",
            "category": "Greedy",
            "difficulty": "Medium"
        },
        "jump_game": {
            "name": "Jump Game",
            "complexity": "O(n)",
            "space": "O(1)",
            "desc": "Determine if can reach last index with jumps.",
            "category": "Greedy",
            "difficulty": "Easy"
        }
    },
    "math": {
        "gcd_lcm": {
            "name": "GCD & LCM",
            "complexity": "O(log(min(a,b)))",
            "space": "O(1)",
            "desc": "Euclidean algorithm for greatest common divisor and LCM.",
            "category": "Number Theory",
            "difficulty": "Easy"
        },
        "prime_sieve": {
            "name": "Sieve of Eratosthenes",
            "complexity": "O(n log log n)",
            "space": "O(n)",
            "desc": "Efficient algorithm to find all primes up to n.",
            "category": "Number Theory",
            "difficulty": "Easy"
        },
        "prime_factorization": {
            "name": "Prime Factorization",
            "complexity": "O(√n)",
            "space": "O(log n)",
            "desc": "Break number into prime factors.",
            "category": "Number Theory",
            "difficulty": "Easy"
        },
        "modular_exponentiation": {
            "name": "Modular Exponentiation",
            "complexity": "O(log n)",
            "space": "O(log n)",
            "desc": "Compute (a^b) % m efficiently using binary exponentiation.",
            "category": "Number Theory",
            "difficulty": "Medium"
        },
        "chinese_remainder": {
            "name": "Chinese Remainder Theorem",
            "complexity": "O(log n)",
            "space": "O(1)",
            "desc": "Solve system of congruences.",
            "category": "Number Theory",
            "difficulty": "Hard"
        },
        "extended_gcd": {
            "name": "Extended Euclidean Algorithm",
            "complexity": "O(log(min(a,b)))",
            "space": "O(log(min(a,b)))",
            "desc": "Find x, y such that ax + by = gcd(a,b).",
            "category": "Number Theory",
            "difficulty": "Medium"
        },
        "fast_fourier": {
            "name": "Fast Fourier Transform",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Compute polynomial multiplication efficiently.",
            "category": "Transform",
            "difficulty": "Hard"
        },
        "fibonacci_matrix": {
            "name": "Fibonacci Matrix Method",
            "complexity": "O(log n)",
            "space": "O(1)",
            "desc": "Compute large Fibonacci numbers using matrix exponentiation.",
            "category": "Optimization",
            "difficulty": "Hard"
        }
    },
    "graph": {
        "topological_sort": {
            "name": "Topological Sorting (Kahn's)",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Linear ordering of vertices with in-degree 0 first.",
            "category": "Graph Algorithm",
            "difficulty": "Medium"
        },
        "scc_kosaraju": {
            "name": "SCC - Kosaraju's",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Find strongly connected components using two DFS passes.",
            "category": "Graph Algorithm",
            "difficulty": "Hard"
        },
        "scc_tarjan": {
            "name": "SCC - Tarjan's",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Find SCCs in single DFS using stack.",
            "category": "Graph Algorithm",
            "difficulty": "Hard"
        },
        "bridge_finding": {
            "name": "Bridge Finding",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Find edges whose removal increases connected components.",
            "category": "Graph Algorithm",
            "difficulty": "Hard"
        },
        "articulation_point": {
            "name": "Articulation Points",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Find vertices whose removal increases components.",
            "category": "Graph Algorithm",
            "difficulty": "Hard"
        },
        "bipartite_check": {
            "name": "Bipartite Check",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Check if graph can be 2-colored (bipartite).",
            "category": "Graph Property",
            "difficulty": "Easy"
        },
        "cycle_detection": {
            "name": "Cycle Detection",
            "complexity": "O(V+E)",
            "space": "O(V)",
            "desc": "Detect cycles in directed/undirected graphs.",
            "category": "Graph Property",
            "difficulty": "Medium"
        },
        "maximum_flow": {
            "name": "Maximum Flow (Ford-Fulkerson)",
            "complexity": "O(VE²)",
            "space": "O(V+E)",
            "desc": "Find maximum flow from source to sink.",
            "category": "Flow Network",
            "difficulty": "Hard"
        }
    },
    "bit": {
        "bit_counting": {
            "name": "Bit Counting",
            "complexity": "O(log n)",
            "space": "O(1)",
            "desc": "Count set bits (1s) in binary representation.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        },
        "power_of_two": {
            "name": "Power of 2 Check",
            "complexity": "O(1)",
            "space": "O(1)",
            "desc": "Check if number is power of 2 using bit trick.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        },
        "gray_code": {
            "name": "Gray Code",
            "complexity": "O(2^n)",
            "space": "O(2^n)",
            "desc": "Generate gray code sequence (binary codes differing by 1 bit).",
            "category": "Bit Manipulation",
            "difficulty": "Medium"
        },
        "xor_pairs": {
            "name": "XOR Pair Finding",
            "complexity": "O(n)",
            "space": "O(n)",
            "desc": "Find pairs with given XOR value.",
            "category": "Bit Manipulation",
            "difficulty": "Medium"
        },
        "subset_generation": {
            "name": "Subset Generation",
            "complexity": "O(2^n)",
            "space": "O(2^n)",
            "desc": "Generate all subsets using bit representation.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        },
        "single_number": {
            "name": "Single Number (XOR)",
            "complexity": "O(n)",
            "space": "O(1)",
            "desc": "Find single occurring number among duplicates using XOR.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        },
        "hamming_distance": {
            "name": "Hamming Distance",
            "complexity": "O(log n)",
            "space": "O(1)",
            "desc": "Count different bits between two numbers.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        },
        "missing_number": {
            "name": "Missing Number",
            "complexity": "O(n)",
            "space": "O(1)",
            "desc": "Find missing number in 1 to n using XOR or sum.",
            "category": "Bit Manipulation",
            "difficulty": "Easy"
        }
    },
    "hash": {
        "hash_function": {
            "name": "Hash Function",
            "complexity": "O(1) avg",
            "space": "O(n)",
            "desc": "Basic hash table implementation with hash function.",
            "category": "Hashing",
            "difficulty": "Medium"
        },
        "linear_probing": {
            "name": "Linear Probing",
            "complexity": "O(1) avg",
            "space": "O(n)",
            "desc": "Handle collisions by finding next empty slot.",
            "category": "Collision Resolution",
            "difficulty": "Medium"
        },
        "quadratic_probing": {
            "name": "Quadratic Probing",
            "complexity": "O(1) avg",
            "space": "O(n)",
            "desc": "Handle collisions using quadratic offsets.",
            "category": "Collision Resolution",
            "difficulty": "Medium"
        },
        "chaining": {
            "name": "Chaining",
            "complexity": "O(1) avg",
            "space": "O(n)",
            "desc": "Handle collisions using linked lists.",
            "category": "Collision Resolution",
            "difficulty": "Easy"
        },
        "double_hashing": {
            "name": "Double Hashing",
            "complexity": "O(1) avg",
            "space": "O(n)",
            "desc": "Handle collisions using two hash functions.",
            "category": "Collision Resolution",
            "difficulty": "Hard"
        }
    },
    "geometry": {
        "convex_hull": {
            "name": "Convex Hull (Graham Scan)",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Find convex hull of 2D points using Graham scan.",
            "category": "Geometry",
            "difficulty": "Hard"
        },
        "line_intersection": {
            "name": "Line Intersection",
            "complexity": "O(1)",
            "space": "O(1)",
            "desc": "Check if two line segments intersect.",
            "category": "Geometry",
            "difficulty": "Medium"
        },
        "point_in_polygon": {
            "name": "Point in Polygon",
            "complexity": "O(n)",
            "space": "O(1)",
            "desc": "Check if point is inside polygon using ray casting.",
            "category": "Geometry",
            "difficulty": "Medium"
        },
        "closest_pair": {
            "name": "Closest Pair of Points",
            "complexity": "O(n log n)",
            "space": "O(n)",
            "desc": "Find two points with minimum distance.",
            "category": "Geometry",
            "difficulty": "Hard"
        }
    },
    "backtracking": {
        "nqueens": {
            "name": "N-Queens Problem",
            "complexity": "O(N!)",
            "space": "O(N)",
            "desc": "Place N queens on board with no attacks.",
            "category": "Backtracking",
            "difficulty": "Hard"
        },
        "sudoku": {
            "name": "Sudoku Solver",
            "complexity": "O(9^(n*n))",
            "space": "O(n²)",
            "desc": "Solve sudoku puzzle using backtracking.",
            "category": "Backtracking",
            "difficulty": "Hard"
        },
        "permutations": {
            "name": "Generate Permutations",
            "complexity": "O(N!)",
            "space": "O(N)",
            "desc": "Generate all permutations of array.",
            "category": "Backtracking",
            "difficulty": "Medium"
        },
        "combinations": {
            "name": "Generate Combinations",
            "complexity": "O(C(n,r))",
            "space": "O(r)",
            "desc": "Generate all combinations of size r.",
            "category": "Backtracking",
            "difficulty": "Medium"
        }
    }
}

# ==================== ROUTES ====================

@app.route('/', methods=['GET'])
def index():
    """Serve the main SPA"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving index: {str(e)}")
        return jsonify({'error': 'Failed to load application'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0',
        'port': 2344
    })

@app.route('/api/info', methods=['GET'])
def app_info():
    """Get application metadata"""
    return jsonify({
        'name': 'Algorithm Playground',
        'version': '2.0.0',
        'description': 'Interactive visualization of 70+ DSA algorithms',
        'algorithms_total': 78,
        'categories': 11,
        'port': 2344,
        'backend': 'Flask',
        'frontend': 'Vanilla HTML/CSS/JavaScript'
    })

@app.route('/api/algorithms', methods=['GET'])
def get_all_algorithms():
    """Get all algorithm metadata"""
    return jsonify(ALGORITHMS_DATABASE)

@app.route('/api/algorithms/<category>', methods=['GET'])
def get_category_algorithms(category):
    """Get algorithms for specific category"""
    if category in ALGORITHMS_DATABASE:
        return jsonify(ALGORITHMS_DATABASE[category])
    return jsonify({'error': f'Category {category} not found'}), 404

@app.route('/api/algorithms/<category>/<algorithm>', methods=['GET'])
def get_algorithm_info(category, algorithm):
    """Get info for specific algorithm"""
    if category in ALGORITHMS_DATABASE:
        if algorithm in ALGORITHMS_DATABASE[category]:
            return jsonify(ALGORITHMS_DATABASE[category][algorithm])
        return jsonify({'error': f'Algorithm {algorithm} not found'}), 404
    return jsonify({'error': f'Category {category} not found'}), 404

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get algorithm statistics"""
    total_algos = sum(len(v) for v in ALGORITHMS_DATABASE.values())
    categories = list(ALGORITHMS_DATABASE.keys())
    
    return jsonify({
        'total_algorithms': total_algos,
        'total_categories': len(categories),
        'categories': categories,
        'algorithms_by_category': {k: len(v) for k, v in ALGORITHMS_DATABASE.items()}
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

# ==================== REQUEST/RESPONSE HOOKS ====================

@app.before_request
def before_request():
    """Logging before request"""
    logger.info(f"{request.method} {request.path}")

@app.after_request
def after_request(response):
    """Logging after request"""
    logger.info(f"Response: {response.status_code}")
    return response

# ==================== CONTEXT PROCESSOR ====================

@app.context_processor
def inject_config():
    """Inject configuration into templates"""
    return {
        'app_name': 'Algorithm Playground',
        'version': '2.0.0',
        'port': 2344
    }

# ==================== CLI COMMANDS ====================

@app.cli.command()
def list_algorithms():
    """List all algorithms"""
    for category, algos in ALGORITHMS_DATABASE.items():
        print(f"\n{category.upper()} ({len(algos)} algorithms):")
        for algo_name, algo_info in algos.items():
            print(f"  - {algo_info['name']} | {algo_info['complexity']}")

@app.cli.command()
def count_algorithms():
    """Count total algorithms"""
    total = sum(len(v) for v in ALGORITHMS_DATABASE.values())
    print(f"Total algorithms: {total}")
    for category, algos in ALGORITHMS_DATABASE.items():
        print(f"  {category}: {len(algos)}")

# ==================== MAIN ====================

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.getenv('PORT', 2344))
    
    # Run development server
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG'],
        use_reloader=True
    )
