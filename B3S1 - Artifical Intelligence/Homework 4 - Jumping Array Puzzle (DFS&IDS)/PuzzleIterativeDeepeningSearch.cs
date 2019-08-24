using System.Collections;
using System.Collections.Generic;

namespace JumpingArrayPuzzle
{
	internal class PuzzleIterativeDeepeningSearch : ISearch
	{
		private PuzzlePathGraph graph;

		public Puzzle StartPuzzle { get; }
		public Puzzle EndPuzzle { get; }

		public PuzzleIterativeDeepeningSearch(
			Puzzle startPuzzle, Puzzle endPuzzle) =>
			(this.StartPuzzle, this.EndPuzzle) = (startPuzzle, endPuzzle);

		public void Trace() {
			int depthLimit = 0;
			while (true) {
				depthLimit += 1;
				this.graph = new PuzzlePathGraph(this.StartPuzzle, depthLimit);
				PuzzlePathGraph.Node node = this.graph.Root;
				while (node.Puzzle != this.EndPuzzle) {
					PuzzlePathGraph.Node nextNode = node.NextMovableNode();
					if (!(nextNode is null)) node = nextNode;
					else if (!(node.Present is null)) node = node.Present;
					else break;
				}
				if (node.Puzzle == this.EndPuzzle) return;
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
