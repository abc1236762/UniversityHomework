using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace JumpingArrayPuzzle
{
	internal class Puzzle : IEnumerable<uint>, ICloneable
	{
		private readonly uint[] data;

		public uint[] Data => this.CloneData();
		public int Length => this.data.Length;
		public int IndexOfZero => Array.IndexOf(this.data, 0U);

		public Puzzle(uint[] data) => this.data = data;

		public static bool operator ==(Puzzle a, Puzzle b) =>
			!(a is null) && !(b is null) && Enumerable.SequenceEqual(a, b);

		public static bool operator !=(Puzzle a, Puzzle b) =>
			a is null || b is null || !Enumerable.SequenceEqual(a, b);

		public void Swap(int indexA, int indexB) =>
			(this.data[indexA], this.data[indexB]) =
			(this.data[indexB], this.data[indexA]);

		public IEnumerator<uint> GetEnumerator() {
			foreach (uint value in this.data) yield return value;
		}

		IEnumerator IEnumerable.GetEnumerator() => this.GetEnumerator();

		private uint[] CloneData() {
			uint[] newData = Array.CreateInstance(
				typeof(uint), this.data.Length) as uint[];
			this.data.CopyTo(newData, 0);
			return newData;
		}

		public object Clone() => new Puzzle(this.CloneData());

		public override bool Equals(object obj) =>
			obj is Puzzle puzzle ? puzzle == this : false;

		public override int GetHashCode() =>
			(this.data as IStructuralEquatable)
			.GetHashCode(EqualityComparer<uint>.Default);

		public override string ToString() {
			IEnumerable<string> dataString = this.data.Select(x => x.ToString());
			int maxDigits = dataString.Select(x => x.Length).Max();
			dataString = dataString.Select(x => x = x.PadLeft(maxDigits));
			return $"[{string.Join(", ", dataString)}]";
		}
	}
}
