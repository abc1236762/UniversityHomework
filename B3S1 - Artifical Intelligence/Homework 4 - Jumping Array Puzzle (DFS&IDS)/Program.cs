using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JumpingArrayPuzzle
{
	internal class Program
	{
		private static void Main(string[] args) {
			Console.WriteLine("Format of inputting puzzle:");
			Console.WriteLine("  split by ' ', e.g., `0 1 2`    => [0, 1, 2]");
			Console.WriteLine("  split by ',', e.g., `1,0,2`    => [1, 0, 2]");
			Console.WriteLine("  or by both,   e.g., `2, 1 ,0,` => [2, 1, 0]");
			Console.WriteLine();

			Console.Write("Show tracing message? (Y/[N]): ");
			PuzzlePathGraph.ShowTraceMessage =
				Console.ReadLine().Trim().ToUpper() == "Y";
			Console.WriteLine();

			string searchToString(Searches search) =>
				string.Join("", search.ToString()
					.Select(x => x.ToString()).Select(x =>
					x != x.ToLower() ? " " + x : x)).Trim(' ');

			int times = 0;
			while (true) {
				Console.WriteLine($"#{++times}");
				(Puzzle startPuzzle, Puzzle endPuzzle,
					Searches search) = GetData();
				Console.WriteLine();
				Console.WriteLine($"Tracing {startPuzzle} to " +
					$"{endPuzzle} using {searchToString(search)} ...");

				ISearch searcher;
				switch (search) {
					case Searches.DepthFirstSearch:
						searcher = new PuzzleDepthFirstSearch(
							startPuzzle, endPuzzle);
						break;
					case Searches.IterativeDeepeningSearch:
						searcher = new PuzzleIterativeDeepeningSearch(
							startPuzzle, endPuzzle);
						break;
					default:
						throw new NotImplementedException();
				}

				searcher.Trace();
				Console.WriteLine();
				(int createdNodeCount, int skippedNodeCount,
					IList path) = searcher.Result();
				PrintResult(createdNodeCount, skippedNodeCount,
					path as List<PuzzlePathGraph.Node>);
				Console.WriteLine();
			}
		}

		private static (Puzzle startPuzzle, Puzzle endPuzzle,
			Searches search) GetData() {
			Puzzle startPuzzle = null, endPuzzle = null, searches = null;

			void inputData(string prompt, string example, out Puzzle puzzle,
				Func<Puzzle, Puzzle, Puzzle, bool> compare) {
				while (true) {
					Console.Write(prompt);
					try {
						puzzle = new Puzzle(Console.ReadLine().Split(new char[]
							{ ',', ' ' }, StringSplitOptions.RemoveEmptyEntries)
							.ToList().Select(x => uint.Parse(x)).ToArray());
						if (compare(startPuzzle, endPuzzle, searches)) break;
					} catch { }
					Console.WriteLine($"{new string(' ', prompt.Length)}" +
						$"Try again! e.g., {example}");
				}
			}

			inputData("Input start puzzle: ", "0 1, 2 3,", out startPuzzle, (x,
				y, z) => x.Count() > 1 && x.Where(i => i == 0U).Count() == 1);
			inputData("Input end puzzle:   ", "2, 3, 1 0", out endPuzzle, (x,
				y, z) => x.OrderBy(i => i).SequenceEqual(y.OrderBy(i => i)));
			inputData("Select an algorithm (0 => DFS, 1 => IDS): ", "1",
				out searches, (x, y, z) => z.Count() == 1 && z.First() <=
				(uint)(Searches)Enum.Parse(typeof(Searches),
				Enum.GetNames(typeof(Searches)).Last()));
			return (startPuzzle, endPuzzle, (Searches)searches.First());
		}

		private static void PrintResult(int createdNodeCount,
			int skippedNodeCount, List<PuzzlePathGraph.Node> path) {
			Console.WriteLine($"Result: total depth {path.Count - 1}, created" +
				$" {createdNodeCount} and skipped {skippedNodeCount} nodes");
			for (int i = 0; i < path.Count; i++) {
				string depth = i.ToString().PadLeft(path.Count.ToString().Length);
				Console.WriteLine($"  (depth {depth}) {path[i].Puzzle}, and " +
					$"{PuzzlePathGraph.ActionToString(path[i].NextAction)}");
			}
		}
	}
}
