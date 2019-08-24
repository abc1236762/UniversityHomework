using System.Collections;

namespace JumpingArrayPuzzle
{
	internal interface ISearch
	{
		void Trace();
		(int createdNodeCount, int skippedNodeCount, IList path) Result();
	}
}
