using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JumpingArrayPuzzle
{
	internal class PuzzleDepthFirstSearch : ISearch
	{
		private PuzzlePathGraph graph;

		public Puzzle StartPuzzle { get; }
		public Puzzle EndPuzzle { get; }

		public PuzzleDepthFirstSearch(Puzzle startPuzzle, Puzzle endPuzzle) =>
			(this.StartPuzzle, this.EndPuzzle) = (startPuzzle, endPuzzle);

		public void Trace() {
			this.graph = new PuzzlePathGraph(this.StartPuzzle);
			PuzzlePathGraph.Node node = this.graph.Root;
			while (node.Puzzle != this.EndPuzzle) {
				PuzzlePathGraph.Node nextNode = node.NextMovableNode();
				if (!(nextNode is null)) node = nextNode;
				else if (!(node.Present is null)) node = node.Present;
				else throw new ApplicationException();
			}
		}

		public (int createdNodeCount, int skippedNodeCount, IList path) Result() {
			List<PuzzlePathGraph.Node> path = new List<PuzzlePathGraph.Node>();
			PuzzlePathGraph.Node node = this.graph.Root;
			while (!(node is null)) {
				path.Add(node);
				if (node.NextNode is null) break;
				node = node.NextNode;
			}
			return (this.graph.CreatedNodeCount,
				this.graph.SkippedNodeCount, path);
		}
	}
}
