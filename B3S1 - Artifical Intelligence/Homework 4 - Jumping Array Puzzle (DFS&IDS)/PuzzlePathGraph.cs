using System;
using System.Collections.Generic;
using System.Linq;

namespace JumpingArrayPuzzle
{
	internal class PuzzlePathGraph
	{
		private readonly Dictionary<Puzzle, int> passedPuzzles =
			new Dictionary<Puzzle, int>();

		public static bool ShowTraceMessage { get; set; } = false;
		public int DepthLimit { get; private set; } = 0;
		public int CreatedNodeCount { get; private set; } = 0;
		public int SkippedNodeCount { get; private set; } = 0;
		public Node Root { get; }

		public enum Actions
		{
			GoPrevious = -1,
			Finished,
			MoveLeft,
			MoveRight,
			JumpLeft,
			JumpRight,
		}

		static public string ActionToString(Actions action) =>
			string.Join("", action.ToString().PadRight(
				Enum.GetNames(typeof(Actions)).Select(x => x.Length).Max())
				.Select(x => x.ToString()).Select(x =>
				x != x.ToLower() ? " " + x.ToLower() : x)).TrimStart(' ');

		public class Node
		{
			private readonly PuzzlePathGraph ownGraph;

			public Puzzle Puzzle { get; }
			public Actions NextAction { get; private set; } = Actions.Finished;
			public int Depth { get; }
			public Node Present { get; }
			public Node NextNode { get; private set; }

			public Node(Puzzle puzzle,
				Node present, int depth, PuzzlePathGraph ownGraph) {
				this.Puzzle = puzzle;
				this.Present = present;
				this.Depth = depth;
				this.ownGraph = ownGraph;
			}

			private Puzzle NextPuzzle(Puzzle puzzle, Actions action) {
				Puzzle nextPuzzle(Func<int, bool> checkIndex, int swapIndex) {
					Puzzle newPuzzle = puzzle.Clone() as Puzzle;
					if (checkIndex(puzzle.IndexOfZero)) {
						newPuzzle.Swap(puzzle.IndexOfZero, swapIndex);
						return newPuzzle;
					}
					return null;
				}

				switch (action) {
					case Actions.MoveLeft:
						return nextPuzzle(x => x > 0, puzzle.IndexOfZero - 1);
					case Actions.MoveRight:
						return nextPuzzle(x => x < puzzle.Length - 1,
							puzzle.IndexOfZero + 1);
					case Actions.JumpLeft:
						return nextPuzzle(x => x > 1, puzzle.IndexOfZero - 2);
					case Actions.JumpRight:
						return nextPuzzle(x => x < puzzle.Length - 2,
							puzzle.IndexOfZero + 2);
				}
				return null;
			}

			public Node NextMovableNode() {
				if (this.Depth < this.ownGraph.DepthLimit ||
					this.ownGraph.DepthLimit == 0) {
					foreach (string nextActionString in
						Enum.GetNames(typeof(Actions))) {
						Actions nextAction = (Actions)Enum.Parse(
							typeof(Actions), nextActionString);
						if (this.NextAction >= nextAction ||
							nextAction == Actions.Finished ||
							nextAction == Actions.GoPrevious) continue;

						Puzzle nextPuzzle =
							this.NextPuzzle(this.Puzzle, nextAction);
						if (nextPuzzle is null) {
							this.TraceMessage(false, false, nextAction);
							this.ownGraph.SkippedNodeCount += 1;
							continue;
						} else if (this.ownGraph.passedPuzzles
							.ContainsKey(nextPuzzle) && this.ownGraph
							.passedPuzzles[nextPuzzle] <= this.Depth) {
							this.TraceMessage(false, true, nextAction, nextPuzzle,
								this.ownGraph.passedPuzzles[nextPuzzle]);
							this.ownGraph.SkippedNodeCount += 1;
							continue;
						}

						this.NextAction = nextAction;
						this.NextNode = new Node(nextPuzzle,
							this, this.Depth + 1, this.ownGraph);
						this.ownGraph.CreatedNodeCount += 1;
						this.ownGraph.passedPuzzles[nextPuzzle] = this.Depth + 1;
						this.TraceMessage(true, true, nextAction, nextPuzzle);
						return this.NextNode;
					}
				}

				if (!(this.Present is null))
					this.TraceMessage(true, false,
						Actions.GoPrevious, this.Present.Puzzle);
				else if (ShowTraceMessage)
					Console.WriteLine("Trace: terminated, " +
						"no remaining actions to move");
				return null;
			}

			private void TraceMessage(bool isMove, bool isNextMoveOrPassed,
				Actions action = Actions.GoPrevious,
				Puzzle nextPuzzle = null, int passedDepth = 0) {
				if (!ShowTraceMessage) return;

				string depthToString(int depth) =>
					depth.ToString().PadLeft(this.ownGraph
						.DepthLimit.ToString().Length);

				string depthString = depthToString(this.Depth);
				string nextDepthString = depthToString(isNextMoveOrPassed ||
					!isMove ? this.Depth + 1 : this.Depth - 1);
				string message = $"Trace: (depth {depthString}) {this.Puzzle} ";

				if (isMove) {
					message += $"-[{ActionToString(action)}]->" +
						$" (depth {nextDepthString}) {nextPuzzle} / " +
						(isNextMoveOrPassed ? "create node" :
						"no remaining " + (this.Depth == this.ownGraph
						.DepthLimit ? "depth" : "actions"));
				} else {
					string puzzleString = isNextMoveOrPassed ? nextPuzzle
						.ToString() : string.Join("", this.Puzzle
						.ToString().Select(x => char.IsDigit(x) ? ' ' : x));
					string passedDepthString = depthToString(passedDepth);
					message += $"-[{ActionToString(action)}]-×" +
						$" (depth {nextDepthString}) {puzzleString} / skip, " +
						(!isNextMoveOrPassed ? $"try others" :
						$"passed in (depth {passedDepthString}) already");
				}

				Console.WriteLine(message);
			}
		}

		public PuzzlePathGraph(Puzzle puzzle, int depthLimit = 0) {
			if (depthLimit < 0) throw new OverflowException();

			this.passedPuzzles.Clear();
			this.DepthLimit = depthLimit;
			this.Root = new Node(puzzle, null, 0, this);
			this.passedPuzzles.Add(puzzle, 0);
			this.CreatedNodeCount = 1;

			if (ShowTraceMessage && depthLimit > 0)
				Console.WriteLine($"Trace: start with depth limit {depthLimit}");
		}
	}
}
